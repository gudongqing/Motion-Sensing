# -*- coding: utf-8 -*-


_global_dict = {}


def init():
    """
    初始化
    :return:
    """
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    """
    定义一个全局变量
    :param key:
    :param value:
    :return:
    """
    _global_dict[key] = value


def get_value(key, def_value=None):
    """
    获得一个全局变量,不存在则返回默认值
    :param key:
    :param def_value:
    :return:
    """
    try:
        return _global_dict[key]
    except KeyError:
        return def_value

