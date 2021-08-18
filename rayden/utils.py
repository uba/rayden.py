# -*- coding: utf-8 -*-

__author__ = 'Douglas Uba'

import numbers
import numpy as np

def extract(cond, x):
    if isinstance(x, numbers.Number): return x
    return np.extract(cond, x)

def vec2np(vec):
    return np.array((vec.x, vec.y, vec.z))

def np2vec(array):
    from rayden.vector import Vec3
    return Vec3(array[0], array[1], array[2])
    