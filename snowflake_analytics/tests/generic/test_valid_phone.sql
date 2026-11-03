{% test valid_phone(model, column_name) %}

    select *
    from {{ model }}
    where {{ column_name }} is not null
      and not regexp_contains(
          {{ column_name }},
          r'^[0-9]+$'
      )

{% endtest %}