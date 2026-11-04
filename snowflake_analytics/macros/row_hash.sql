{% macro row_hash(columns) %}

    SHA2(
        TO_JSON(
            ARRAY_CONSTRUCT(
                {% for column in columns %}
                    {{ column }}
                    {% if not loop.last %},{% endif %}
                {% endfor %}
            )
        ),
        256
    )

{% endmacro %}