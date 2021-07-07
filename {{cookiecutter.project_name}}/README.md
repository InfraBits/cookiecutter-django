{{ cookiecutter.project_name }}
===============================

Project template created with `infrabits/cookiecutter-django`.

Environment configuration
-------------------------

The core environment configuration is contained within `infrabits/ansible`,
but effectivly can be replaced with any system supporting `systemd` & `docker`.

Deployment
----------

All deployments are driven by the contained `fabfile` and can be executed via `fab deploy`.

Local development
-----------------

All local development can be done within a virtual env;

* `python3 -m virtualenv -p $(which python3) ve`
* `source ve/bin/actiate`
* `pip install --upgrade -r requirements.txt -r requirements-dev.txt`

Dependancies
------------

All requirements should be frozen and automatically updated via `pyup`.
