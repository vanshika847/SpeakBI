from jinja2 import Template
SQL_TEMPLATE = Template("""
SELECT
  {% for metric in metrics -%}
    {{ metric }}{% if not loop.last %}, {% endif %}
  {% endfor %}
FROM sales
WHERE timestamp BETWEEN '{{ start_date }}' AND '{{ end_date }}'
{% if extra_filters %}
  {% for clause in extra_filters -%}
    AND {{ clause }}
  {% endfor %}
{% endif %}
{% if group_by %}
GROUP BY {{ group_by | join(', ') }}
{% endif %}
{% if order_by %}
ORDER BY {{ order_by }}
{% endif %}
LIMIT 500
""")
def generate_sql(
    intent: dict,
    start_date: str = "2024-01-01",
    end_date: str   = "2025-12-31"
) -> str:
    if intent.get("intent") == "unavailable":
        return "SELECT 'no_data' AS status WHERE 1=0"
    metrics  = intent.get("metrics", ["SUM(views) AS views"])
    group_by = intent.get("group_by", [])
    filters  = intent.get("filters", {})
    extra_filters = []
    for key, value in filters.items():
        if key == "date_range":
            parts = str(value).split(" to ")
            if len(parts) == 2:
                extra_filters.append(
                    f"timestamp BETWEEN '{parts[0].strip()}' "
                    f"AND '{parts[1].strip()}'"
                )
        elif isinstance(value, str):
            extra_filters.append(f"{key} = '{value}'")
        elif isinstance(value, (int, float)):
            extra_filters.append(f"{key} = {value}")
    order_by = "timestamp ASC" if "timestamp" in group_by else None
    rendered = SQL_TEMPLATE.render(
        metrics=metrics,
        start_date=start_date,
        end_date=end_date,
        extra_filters=extra_filters,
        group_by=group_by,
        order_by=order_by,
    )
    return " ".join(rendered.split())