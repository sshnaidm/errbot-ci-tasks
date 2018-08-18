Patch **{{ args.patch }}** is not in CI. Last result in Gerrit: {% if args is undefined or not args %}unknown{% endif -%}
{% if args and 'zuul' in args %} `Zuul: {{ "%+d"|format(args.zuul) }}`{:color='{% if args.zuul >0 %}green{% else %}red{% endif %}'} {% endif -%}
{% if args and 'rdo' in args %} `RDO 3party: {{ "%+d"|format(args.rdo) }}`{:color='{% if args.rdo >0 %}green{% else %}red{% endif %}'}{% endif %}
