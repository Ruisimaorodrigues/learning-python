{% macro days_between(start_date, end_date) %}
    case
        when {{ start_date }} is null or {{ end_date }} is null then null
        else datediff('day', {{ start_date }}, {{ end_date }})
    end
{% endmacro %}