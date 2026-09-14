{% macro brl_to_eur(column_name, rate=0.18) %}
    round({{ column_name }} * {{ rate }}, 2)
{% endmacro %}