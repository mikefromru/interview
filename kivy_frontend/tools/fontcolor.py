#!/usr/bin/python3
#-*- coding: utf-8 -*-

'''
Module for a conclusion of color input to the console
Work only in the Linux.

Example:
    import fontcolor
    print(fontcolor.red('object'))

'''

def red(obj):
    return '\x1b[1;31m{0}\x1b[0m'.format(obj)
def blue(obj):
    return '\x1b[1;34m{0}\x1b[0m'.format(obj)
def blue_light(obj):
    return '\x1b[1;36m{0}\x1b[0m'.format(obj)
def purle(obj):
    return '\x1b[1;35m{0}\x1b[0m'.format(obj)
def yellow(obj):
    return '\x1b[1;33m{0}\x1b[0m'.format(obj)
def fon(obj):
    return '\x1b[44;37m{0}\x1b[0m'.format(obj)
    
