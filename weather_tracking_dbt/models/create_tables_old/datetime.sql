{% set table = 'datetime' %}

{# {% set column_types = [
    table + '_id',
    'start_time',
    'end_time',
    'is_daytime'
] %}

{{ create_table_list(column_types, table) }} #}

{% set column_types = {
    table + '_id': 'text',
    'start_time': 'timestamp',
    'end_time': 'timestamp',
    'is_daytime': 'boolean'
} %}

{{ create_table_dict(column_types, table) }}