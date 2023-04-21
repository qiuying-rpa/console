"""

By Ziqiu Li
Created at 2023/3/28 16:48
"""
import toml


def get_conf(key: str = None):
    def get_recursively(_conf, _key_list):
        if len(_key_list) == 1:
            return _conf.get(_key_list[0])
        else:
            return get_recursively(_conf.get(_key_list[0]), _key_list[1:])

    if key:
        conf = get_conf()
        if conf:
            key_list = key.split(".")
            return get_recursively(conf, key_list)
        else:
            return None
    else:
        try:
            with open("config.toml", "rt", encoding="utf-8") as f:
                conf = toml.load(f)
                return conf
        except IOError:
            return None


def set_conf(key: str, value, conf=None, direct_save=False):
    def set_recursively(_conf, _key_list):
        if len(_key_list) == 1:
            _conf[_key_list[0]] = value
        else:
            set_recursively(_conf[_key_list[0]], _key_list[1:])

    conf, key_list = conf or get_conf(), key.split(".")
    if conf and len(key_list) > 0:
        set_recursively(conf, key_list)

    if direct_save:
        update_conf(conf)

    return conf


def update_conf(conf: dict):
    if conf:
        with open("config.toml", "w", encoding="utf-8") as f:
            toml.dump(conf, f)
