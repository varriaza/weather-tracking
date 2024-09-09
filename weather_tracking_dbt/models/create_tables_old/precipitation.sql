{% set table = 'precipitation' %}

{% set column_types = [
    table + '_id',
    'probability_of_precip_value',
    'probability_of_precip_unit'
] %}

{{ create_table_list(column_types, table) }}
