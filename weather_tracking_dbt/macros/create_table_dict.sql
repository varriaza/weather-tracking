{% macro create_table_dict(column_types, table, warehouse='warehouse') %}
  
{# 
Example column_types:
column_types = {
    'column_name': 'int',
} 
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
{% for column, type in column_types.items() %}
    {% if not loop.last %}
    {# Add a comma #}
    null::{{ type }} as {{ column }},
    {% else %}
    {# No comma after the last column #}
    null::{{ type }} as {{ column }}
    {% endif %}
{% endfor %}

where false -- this means there will be zero rows

{% endif %}

{% endmacro %}