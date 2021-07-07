from pathlib import Path
import requests
from typing import Optional
from fabric import task
from patchwork import files
import tempfile

# External settings
REPO_NAME = "{{ cookiecutter.org_name }}/{{ cookiecutter.project_name }}"
CURRENT_TAG = None

# Internal settings
primary_host = "ws-01.infrabits.nl"
secondary_hosts = ["ws-02.infrabits.nl"]
load_ssh_configs = True


# Helper functions
def _get_current_release(c) -> Optional[str]:
    if files.exists(c, "/etc/systemd/{{ cookiecutter.prod_user }}.conf"):
        image_release = c.run(
            "grep DOCKER_IMAGE_RELEASE= /etc/systemd/{{ cookiecutter.prod_user }}.conf",
            hide=True,
            warn=True,
        ).stdout.strip()
        if image_release:
            return image_release.split("=")[1]
    return None


def _get_latest_release(c) -> Optional[str]:
    global CURRENT_TAG
    if not CURRENT_TAG:
        gh_user = (
            c.run("grep username= /etc/netrc-github", hide=True)
            .stdout.strip()
            .split("=")[1]
        )
        gh_pass = (
            c.run("grep password= /etc/netrc-github", hide=True)
            .stdout.strip()
            .split("=")[1]
        )

        r = requests.get(
            f"https://api.github.com/repos/{REPO_NAME}/releases/latest",
            auth=(gh_user, gh_pass),
        )
        r.raise_for_status()
        CURRENT_TAG = r.json()["tag_name"]
    return CURRENT_TAG


def _copy_unit_files(c, target_release):
    c.sudo("rm -f /etc/systemd/system/{{ cookiecutter.prod_user }}\@*.service")
    for unit in Path("docker/unit").glob("*.service"):
{%- if cookiecutter.celery_worker != 'y' %}
        # Celery is not enabled
        if unit.name.endswith('@celery-worker.service'):
            continue
{%- endif %}
        if c.host in secondary_hosts and not unit.name.endswith('@gunicorn.service'):
            continue
        c.put(unit.resolve().as_posix(), (Path("/tmp") / unit.name).as_posix())
        c.sudo(f'mv {(Path("/tmp") / unit.name).as_posix()}'
               f' {(Path("/etc/systemd/system") / unit.name).as_posix()}')


def _update_environment(c, target_release):
    with tempfile.NamedTemporaryFile(mode='w') as fh:
        fh.write('[Service]\n')
        fh.write(f"DOCKER_IMAGE_NAME={REPO_NAME}\n")
        fh.write(f"DOCKER_IMAGE_RELEASE={target_release}\n")
        fh.seek(0)

        c.put(fh.name, "/tmp/{{ cookiecutter.prod_user }}.conf")
        c.sudo("mv /tmp/{{ cookiecutter.prod_user }}.conf"
               " /etc/systemd/{{ cookiecutter.prod_user }}.conf")


def _reload_systemd(c):
    c.sudo('systemctl daemon-reload')
    for unit in Path("docker/unit").glob("*.service"):
{%- if cookiecutter.celery_worker != 'y' %}
        # Celery is not enabled
        if unit.name.endswith('@celery-worker.service'):
            continue
{%- endif %}
        if c.host in secondary_hosts and not unit.name.endswith('@gunicorn.service'):
            # Only deploy the worker on the primary host
            print(f'[{c.host}] skipping unit {unit.name}')
            continue
        print(f'[{c.host}] restarting {unit.name}')
        c.sudo(f'systemctl reload-or-restart {unit.name}', warn=True)


def _deploy_release(c, target_release):
    _copy_unit_files(c, target_release)
    _update_environment(c, target_release)
    _reload_systemd(c)


# Entrypoints
@task(hosts=[primary_host]+secondary_hosts, optional=["tag"])
def deploy(c, tag=None):
    current_release = _get_current_release(c)
    if current_release:
        print(f"Current release: {current_release}")
        print(f"To rollback run `fab deploy tag={current_release}`")
    else:
        print("No current release, first deployment....")

    target_release = tag if tag else _get_latest_release(c)
    print(f"Deploying: {target_release}")
    _deploy_release(c, target_release)
