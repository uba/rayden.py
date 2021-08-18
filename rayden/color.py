# -*- coding: utf-8 -*-

__author__ = 'Douglas Uba'

from colour import Color
import numpy as np

class RGB():
    def __init__(self, r=1.0, g=1.0, b=1.0):
        (self.r, self.g, self.b) = (r, g, b)
        
    @staticmethod
    def fromName(name):
        color = Color(name)
        return RGB(color.red, color.green, color.blue)

    def __add__(self, other):
        return RGB(self.r + other.r, self.g + other.g, self.b + other.b)

    def __mul__(self, other):
        return RGB(self.r * other, self.g * other, self.b * other)

    def place(self, cond):
        r = RGB(np.zeros(cond.shape), np.zeros(cond.shape), np.zeros(cond.shape))
        np.place(r.r, cond, self.r)
        np.place(r.g, cond, self.g)
        np.place(r.b, cond, self.b)
        return r

    def components(self):
        return (self.r, self.g, self.b)

    def __str__(self):
        return '({}, {}, {})'.format(self.r, self.g, self.b)
