#!/usr/bin/python
# -*- coding: utf-8 -*-

global _global_dict
_global_dict = {}


class GlobalVar:

    # def __init__(self):
    #     global _global_dict
    @classmethod
    def set_value(cls, name, value):
        _global_dict[name] = value

    @classmethod
    def get_value(cls, name, def_value='none-device'):
        try:
            return _global_dict[name]
        except KeyError:
            return def_value
