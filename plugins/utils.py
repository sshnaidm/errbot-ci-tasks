import datetime
import json
import re
import requests
from errbot.templating import tenv


BRANCHES = [
    'master',
    # 'stein',
    'rocky',
    'queens',
    'pike',
    # 'ocata',
]


date_re = re.compile(r'(20\d\d-\d\d-\d\d \d\d:\d\d)')

ZUUL_UP = {
    "url": "http://zuul.openstack.org/status",
    "pipelines": ["check", "gate", "experimental"],
    "gerrit": "https://review.openstack.org/changes/{}/detail"
}

REPO_URL = {
    "https://trunk.rdoproject.org/centos7-{}/consistent/": 'consistent',
    "https://trunk.rdoproject.org/centos7-{}/current-tripleo/": 'tripleoci',
    "https://trunk.rdoproject.org/centos7-{}/current-tripleo-rdo/": 'phase1',
    ("https://trunk.rdoproject.org/centos7-{}/"
     "current-tripleo-rdo-internal/"): 'phase2',
}


def validate_patch(patch_number):
    if "http" not in patch_number and not patch_number.isdigit():
        return False, "Patch should be either gerrit link or number"
    elif "http" in patch_number:
        patch = patch_number.strip("/").split("/")[-1]
        if not patch.isdigit():
            return False, "Patch number contains non-digits"
    else:
        patch = patch_number
    if len(patch) > 10:
        return False, "Patch length should be less than 20"
    return True, patch


def get_patch_status(patch):
    web = requests.get(ZUUL_UP['url'])
    if web is not None and web.ok:
        try:
            d = web.json()
        except Exception:
            return "Failed to query Zuul"
    else:
        return "Failed to query Zuul"
    data = None
    for i in d['pipelines']:
        if i['name'] in ZUUL_UP['pipelines']:
            for j in i['change_queues']:
                if j['heads']:
                    patches = [k['id'].split(",")[0] for k in j['heads'][0]]
                    if patch in patches:
                        data = j['heads'][0][patches.index(patch)]
                        data['used_pipeline'] = i['name']
    if not data:
        return gerrit_status(patch)
    if not data['jobs']:
        return "Patch %s is in CI, but no jobs are enqueued for it." % patch
    msg = 'Patch is in CI pipeline "%s". ' % data['used_pipeline']
    if data['jobs']:
        if set([i['start_time'] for i in data['jobs']]) == {None}:
            msg += "It is enqueued and no jobs are in progress yet. "
        elif None not in [i['result'] for i in data['jobs']]:
            msg += "Jobs are finished - "
            # fails = [i['result'] for i in data['jobs']
            #          if i['result'] != "SUCCESS"]
            check_fails = [i['result'] for i in data['jobs']
                           if i['result'] != "SUCCESS" and
                           i.get('voting', True)]
            if check_fails:
                msg += "{} job(s) failed from {} :(.".format(
                    len(check_fails), len(data['jobs'])
                )
            else:
                msg += "all {} jobs passed :).".format(len(data['jobs']))
        else:
            msg += "Jobs are in progress"
            fails = [i['result'] for i in data['jobs']
                     if i['result'] != "SUCCESS" and i['result'] is not None
                     and i.get('voting', True)]
            if not fails:
                msg += " and passing so far :). "
            else:
                msg += ", but {} failed :(. ".format(len(fails))
            job_runs = [i['start_time'] for i in data['jobs']
                        if i['result'] is None]
            passed = [i['result'] for i in data['jobs']
                      if i['result'] == 'SUCCESS']
            all_failed = [i['result'] for i in data['jobs']
                          if i['result'] != "SUCCESS" and
                          i['result'] is not None]
            percents = [100 * i['elapsed_time'] / (
                    i['elapsed_time'] + i['remaining_time']
            ) for i in data['jobs'] if i['start_time'] is not None and
                        i['elapsed_time'] is not None and
                        i['remaining_time'] is not None]
            avg = int(sum(percents) / float(len(percents)))
            msg += ("Overall progress: {} jobs are running ({}%)".format(
                len(job_runs) - job_runs.count(None),
                avg))
            if passed:
                msg += ", {} passed".format(len(passed))
            if all_failed:
                msg += ", {} failed ({} voting)".format(
                    len(all_failed), len(fails))
            msg += " and {} jobs are in queue.".format(
                job_runs.count(None)) if job_runs.count(None) else '.'
    return msg


def gerrit_status(patch):

    def get_zuul_status(data):
        if 'labels' in data and 'Verified' in data['labels']:
            zuul_msgs = [
                i for i in data['labels']['Verified'].get('all', [])
                if i['username'] == 'zuul']
            if zuul_msgs:
                value = zuul_msgs[0].get('value')
                if value:
                    return value
        return

    def get_rdo_status(data):
        if 'labels' in data and 'Verified' in data['labels']:
            zuul_msgs = [
                i for i in data['labels']['Verified'].get('all', [])
                if i['username'] == 'rdothirdparty']
            if zuul_msgs:
                value = zuul_msgs[0].get('value')
                if value:
                    return value
        return

    def generate_response(res):
        return tenv().get_template('gerrit_result.md').render(args=res)

    res = {'patch': patch}
    web = requests.get(ZUUL_UP['gerrit'].format(patch))
    if web is not None and web.ok:
        try:
            d = json.loads(web.content[4:])
        except Exception:
            return generate_response(res)
    else:
        return generate_response(res)
    zuul = get_zuul_status(d)
    rdo = get_rdo_status(d)
    if zuul:
        res.update({'zuul': zuul})
    if rdo:
        res.update({'rdo': rdo})
    return generate_response(res)


def get_promotion_status(branch):

    def get_date(text):
        repo_lines = [i for i in text.splitlines() if 'delorean.repo' in i]
        if repo_lines:
            line = repo_lines[0]
            if date_re.search(line):
                date_txt = date_re.search(line).group(1)
                return datetime.datetime.strptime(date_txt, '%Y-%m-%d %H:%M')
        return

    def calculate_diff(t):
        return (datetime.datetime.utcnow() - t).days

    if branch == 'all':
        branches = BRANCHES
    else:
        branches = [branch]
    br_list = []
    for b in branches:
        res = {
            'name': b,
            'consistent': 'N/A',
            'tripleoci': 'N/A',
            'phase1': 'N/A',
            'phase2': 'N/A'
        }
        for repo_url in REPO_URL:
            url = repo_url.format(b)
            web = requests.get(url)
            if web is None or not web.ok:
                continue
            date = get_date(web.text)
            if not date:
                continue
            days = calculate_diff(date)
            if not days:
                continue
            key = REPO_URL[repo_url]
            res[key] = days
        br_list.append(res)
    return tenv().get_template('promotion_status.md').render(branches=br_list)
