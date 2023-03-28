"""

By Ziqiu Li
Created at 2023/3/28 16:48
"""
import os
import tomllib


def get_conf():
    # toml_path = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), 'config.toml')
    with open('config.toml', 'rb') as f:
        conf = tomllib.load(f)
    return conf

