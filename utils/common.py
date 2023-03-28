"""

By Ziqiu Li
Created at 2023/3/28 16:48
"""
import tomllib


def get_conf():
    with open('config.toml', 'rb') as f:
        conf = tomllib.load(f)
    return conf

