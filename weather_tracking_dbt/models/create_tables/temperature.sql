{% set table = 'temperature' %}

{# {% set column_types = {
    table + '_id':'text',
    table + '_value': 'numeric',
    table + '_unit': 'text',
    table + '_trend': 'text'
} %}

{{ create_table_dict(column_types, table) }} #}


{% set column_types = [
    table + '_id',
    table + '_value',
    table + '_unit',
    table + '_trend'
] %}

{# Not sure why, but when I first made temperature, 
I had to use the dict version of create table.
DBT kept tring to assign a text type to temperature_value
which would cause it to error out when it got to the model.
But once I ran it once, it now works with list! No idea what happened. #}
{# Seems like DBT caches the types once it works once? #}
{{ create_table_list(column_types, table) }}