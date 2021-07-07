import collections
import yaml
import os
from pathlib import Path


def _load_yaml(path):
    if path.is_file():
        with path.open('r') as fh:
            return yaml.load(fh, Loader=yaml.SafeLoader)
    return {}


def deep_merge_dict(base, merge):
    for k, v in merge.items():
        if isinstance(base.get(k), dict) and isinstance(v, collections.Mapping):
            base[k] = deep_merge_dict(base[k], v)
        else:
            base[k] = v
    return base


def load_config(base_dir):
    # Defaults
    cfg = {
        'django': {
            'secret_key': 'development do not use',
            'debug': True,
            'allowed_hosts': ['localhost', '127.0.0.1'],
            'admins': [],
        },
        'mysql': {
            'name': '{{ cookiecutter.project_name }}_dev',
            'host': '127.0.0.1',
            'user': 'root',
            'password': '',
        },
        'redis': {
            'url': 'redis://127.0.0.1:6379/1',
        },
        'sendgrid': {
            'api_key': 'development',
        },
        'csp': {
            'report_only': True,
        }
    }
    cfg = deep_merge_dict(cfg, _load_yaml(base_dir / 'config.yaml'))
    if runtime_cfg := os.environ.get("{{ cookiecutter.project_name|upper }}_CONFIG"):
        cfg = deep_merge_dict(cfg, _load_yaml(Path(runtime_cfg)))
    return cfg
