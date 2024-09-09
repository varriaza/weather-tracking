{% set table = 'location' %}

{% set column_types = [
    table + '_id',
    table + '_type',
    'coordinates',
    table + '_elevation_value',
    table + '_elevation_units'
 ] %}

{{ create_table_list(column_types, table) }}
