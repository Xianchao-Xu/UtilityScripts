#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Container:
    def __init__(self):
        self.dict = dict()


if __name__ == '__main__':
    c = Container()
    d = c.dict.get('key1', dict())  # get并不会将key1设置为键，只是返回默认值
    d['1'] = 1
    print(c.dict)
    d = c.dict.setdefault('key1', dict())  # setdefault会将键和默认值设置为键值对
    d['1'] = 1
    print(d)
    print(c.dict)
    d = c.dict.setdefault('key1', dict())
    d['2'] = 2
    print(c.dict)
