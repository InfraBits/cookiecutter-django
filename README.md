Django cookiecutter template
============================

This template provides a base Django project structure,
along with configured tests & dependancy updates.

Configuration options
---------------------

* `org_name` - GitHub organisation name
* `project_name` - GitHub repo name/general project name
* `prod_user` - Production username (used for binding config paths)
* `prod_uid` - Production UID (used for dropping privileges)
* `celery_worker` - Should a celery worker be deployed

The `prod_user` & `prod_uid` settings should match those in
`infrabits/ansible`'s `inventory/group_vars/all/sites.yml`.
