{{ name | escape | underline }}

- `full name`: :mod:`{{ fullname | escape }}`
- `type`: {{ objtype }}

.. automodule:: {{ fullname }}

.. currentmodule:: {{fullname}}

{% if attributes %}
.. rubric:: Attributes

.. autosummary::
   :toctree:
    {% for item in attributes %}
        {{ item }}
    {% endfor %}

{% endif %}

{% if functions %}
.. rubric:: Functions

.. autosummary::
   :toctree:
    {% for function in functions %}
    {{ function }}
    {% endfor %}

{% endif %}

{% if exceptions %}
.. rubric:: Exceptions

.. autosummary::
   :toctree:
    {% for exc in exceptions %}
    {{ exc}}
    {% endfor %}

{% endif %}

{% if classes %}
.. rubric:: Classes

.. autosummary::
    :toctree:
    {% for class in classes %}
    {{ class }}
    {% endfor %}

.. inheritance-diagram:: {{ fullname }}
    :parts: 1

{% endif %}
