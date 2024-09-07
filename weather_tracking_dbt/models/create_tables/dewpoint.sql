
{% set table = 'dewpoint' %}

{% set column_names = [
    table + '_id',
    table + '_value',
    table + '_unit'
] %}

{{ create_table_list(column_names, table) }}