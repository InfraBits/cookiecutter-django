{%- if cookiecutter.celery_worker == 'y' %}
from .celery import app as celery_app
{%- endif %}

__version__ = "0.0.1"
{%- if cookiecutter.celery_worker == 'y' %}
__all__ = ('celery_app', )
{%- endif %}
