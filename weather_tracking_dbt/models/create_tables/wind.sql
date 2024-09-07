{% set table = 'wind' %}

{% set column_types = [
    table + '_id',
    table + '_speed',
    table + '_unit',
    table + '_direction'
] %}

{{ create_table_list(column_types, table) }}
