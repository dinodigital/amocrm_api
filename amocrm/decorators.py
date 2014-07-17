# -*- coding: utf-8 -*-
from functools import wraps


empty = type('empty', (), {})


def amo_request(method=None):
    def decor(func):
        @wraps(func)
        def call_func(*args, **kwargs):
            self = args[0]
            return self.request(method, data=func(*args, **kwargs))
        return call_func
    return decor


def to_amo_obj(func):
    @wraps(func)
    def call_func(*args, **kwargs):
        self = args[0]
        return self.convert_to_obj(func(*args, **kwargs))
    return call_func


class lazy_property(object):

    def __init__(self, calculate_function):
        self._calculate = calculate_function

    def __get__(self, obj, _=None):
        if obj is None:
            return self
        value = self._calculate(obj)
        if value is not None:
            setattr(obj, self._calculate.func_name, value)
        return value


class lazy_dict_property(object):

    def __init__(self, calculate_function):
        self.__delegate()
        self.fake = empty()
        self.fake._calculate = calculate_function

    def __get__(self, obj, _=None):
        self.fake._obj = obj
        return self.fake

    def __delegate(self):
        for method_name in dict.__dict__.keys():
            if hasattr(empty, method_name):
                continue
            meth = self.__dispatch(method_name)
            setattr(empty, method_name, meth)

    def __dispatch(self, name):
        def __wrapper(*args, **kwargs):
            args = list(reversed(args))
            this = args.pop()
            value = this._calculate(this._obj)
            setattr(this._obj, this._calculate.func_name, value)
            return getattr(value, name)(*list(reversed(args)), **kwargs)
        return __wrapper