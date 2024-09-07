{% set table = 'humidity' %}

{% set column_types = [
    table + '_id',
    table + '_value',
    table + '_unit'
] %}

{{ create_table_list(column_types, table) }}
