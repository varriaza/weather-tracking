{% set table = 'datetime' %}

{# {% set column_types = [
    table + '_id',
    'start_time',
    'end_time',
    'date',
    'is_daytime'
] %}

{{ create_table_list(column_types, table) }} #}

{% set column_types = {
    table + '_id': 'text',
    'start_time': 'time',
    'end_time': 'time',
    'date': 'date',
    'is_daytime': 'boolean'
} %}

{{ create_table_dict(column_types, table) }}