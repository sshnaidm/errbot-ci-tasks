import requests

ZUUL_UP = {
    "url": "http://zuul.openstack.org/status",
    "pipelines": ["check", "gate", "experimental"]
}


def get_patch_status(patch):
    web = requests.get(ZUUL_UP['url'])
    if web is not None and web.ok:
        try:
            d = web.json()
        except Exception as e:
            return
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
        return "Patch %s is not in CI." % patch
    if not data['jobs']:
        return "Patch %s is in CI, but no jobs are enqueued for it."
    msg = 'Patch is in CI pipeline "%s". ' % data['used_pipeline']
    if data['jobs']:
        if set([i['start_time'] for i in data['jobs']]) == {None}:
            msg += "It is enqueued and no jobs are in progress yet. "
        elif None not in [i['result'] for i in data['jobs']]:
            msg += "Jobs are finished - "
            # fails = [i['result'] for i in data['jobs']
            #          if i['result'] != "SUCCESS"]
            check_fails = [i['result'] for i in data['jobs']
                     if i['result'] != "SUCCESS" and i.get('voting', True)]
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
                     if i['result'] != "SUCCESS" and i['result'] is not None]
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
