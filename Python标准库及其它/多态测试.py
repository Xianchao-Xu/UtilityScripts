#!/usr/bin/env python
# -*- coding: utf-8 -*-


class BaseClass:
    def __init__(self):
        self.name = 'base'

    def say_hello(self):
        print(self.name)
        print('from BaseClass')


class ClassA(BaseClass):
    def __init__(self):
        super(BaseClass, self).__init__()
        self.name = 'class A'

    def say_hello(self):
        print(self.name)
        print('from class A')


class ClassB(BaseClass):
    def __init__(self):
        super(ClassB, self).__init__()
        self.name = 'class B'

    def say_hello(self):
        print(self.name)
        print('from class B')


if __name__ == '__main__':
    base_list: list[BaseClass] = list()
    a = ClassA()
    b = ClassB()
    base_list.append(a)
    base_list.append(b)
    for instance in base_list:
        print(isinstance(instance, BaseClass), isinstance(instance, ClassA), isinstance(instance, ClassB))
        instance.say_hello()
