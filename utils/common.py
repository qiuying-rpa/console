"""

By Ziqiu Li
Created at 2023/3/28 16:48
"""
import importlib


def get_conf():
    try:
        toml = importlib.import_module('tomllib')
        with open('config.toml', 'rb') as f:
            conf = toml.load(f)
    except ImportError:
        toml = importlib.import_module('toml')
        with open('config.toml', 'rt') as f:
            conf = toml.loads(f.read())

    return conf

