
{% for branch in branches %}
**{{ branch.name|capitalize }}**:  `consistent - {{ branch.consistent }}{%- if branch.consistent != "N/A" -%}d
{%- endif %}`{:color='{%- if branch.consistent == "N/A" or branch.consistent > 5 -%}red
{%- elif branch.consistent < 6 and branch.consistent > 3 -%}yellow
{%- else -%}green
{%- endif -%}'}  `tripleo-ci - {{ branch.tripleoci }}{%- if branch.tripleoci != "N/A" -%}d
{%- endif %}`{:color='{%- if branch.tripleoci == "N/A" or branch.tripleoci > 5 -%}red
{%- elif branch.tripleoci < 6 and branch.tripleoci > 3 -%}yellow
{%- else -%}green
{%- endif -%}'}  `phase1 - {{ branch.phase1 }}{%- if branch.phase1 != "N/A" -%}d
{%- endif %}`{:color='{%- if branch.phase1 == "N/A" or branch.phase1 > 5 -%}red
{%- elif branch.phase1 < 6 and branch.phase1 > 3 -%}yellow
{%- else -%}green
{%- endif -%}'}  `phase2 - {{ branch.phase2 }}{%- if branch.phase2 != "N/A" -%}d
{%- endif %}`{:color='{%- if branch.phase2 == "N/A" or branch.phase2 > 5 -%}red
{%- elif branch.phase2 < 6 and branch.phase2 > 3 -%}yellow
{%- else -%}green
{%- endif -%}'}
{% endfor %}
