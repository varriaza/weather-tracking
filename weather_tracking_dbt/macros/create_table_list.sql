{% macro create_table_list(column_names, table, warehouse='warehouse') %}
  
{# 
Example column_names:
column_names = ['column_name_1', 'column_name_2']
#}

{%- set source_relation = adapter.get_relation(
      database=source(warehouse, table).database,
      schema=source(warehouse, table).schema,
      identifier=source(warehouse, table).name) -%}

{% set table_exists=source_relation is not none   %}

{% if table_exists %}

select
    *
from {{ source(warehouse, table) }}


{% else %}

select
{# Loop through our list of columns #}
{% for column in column_names %}
    {% if not loop.last %}
    {# Add a comma #}
    null as {{ column }},
    {% else %}
    {# No comma after the last column #}
    null as {{ column }}
    {% endif %}
{% endfor %}
where false -- this means there will be zero rows

{% endif %}

{% endmacro %}