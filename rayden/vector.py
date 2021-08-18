# -*- coding: utf-8 -*-

__author__ = 'Douglas Uba'

import numpy as np
from rayden.utils import extract, vec2np, np2vec

class Vec3():
    def __init__(self, x=1.0, y=1.0, z=1.0):
        (self.x, self.y, self.z) = (x, y, z)

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vec3(self.x * other, self.y * other, self.z * other)

    def __div__(self, other):
        return Vec3(self.x / other, self.y / other, self.z / other)

    def dot(self, other):
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

    def cross(self, other):
        return Vec3(self.y * other.z - self.z * other.y,
                    self.z * other.x - self.x * other.z,
                    self.x * other.y - self.y * other.x)

    def __abs__(self):
        return self.dot(self)

    def magnitude(self):
        return np.sqrt(self.dot(self))

    def magnitudeSquared(self):
        return self.dot(self)

    def normalize(self):
        norm = self.magnitude()
        (self.x, self.y, self.z) = (self.x / norm, self.y / norm, self.z / norm)

    def normalized(self):
        mag = np.sqrt(abs(self))
        return self * (1.0 / np.where(mag == 0, 1, mag))

    def invert(self):
        (self.x, self.y, self.z) = (-self.x, -self.y, -self.z)

    def inverted(self):
       return self * -1

    def angle(self, other):
        return np.arccos(self.dot(other))

    def loadUnit(self):
        (self.x, self.y, self.z) = (1.0, 1.0, 1.0)

    def extract(self, cond):
        return Vec3(extract(cond, self.x), extract(cond, self.y), extract(cond, self.z))

    def reflect(self, normal):
        return (((normal * self.dot(normal)) * 2) - self).normalized()

    def refract(self, normal, n1, n2):
        # for self.dot(normal) < 0.0
        # wi incident on front-side of surface
        norm = vec2np(normal)
        n = np.full(normal.x.shape, n2/n1)

        # for self.dot(normal) >= 0.0
        # wi incident on back-side of surface
        pred = self.dot(normal) >= 0.0
        norm = np.where(pred, -1 * norm, norm)
        n = np.where(pred, n1/n2, n)

        w = self.inverted()
        d = w.dot(np2vec(norm))
        det = 1 - (n * n) * (1 - d * d)

        # Guard
        det = np.where(det < 0.0, 0.0, det)

        norm = np2vec(norm)
        
        # Compute refract ray
        refract = (((w - (norm * d)) * -n) - (norm * np.sqrt(det))).normalized()
         
        # For total reflection case
        reflect = vec2np(w.reflect(normal))

        # Adjusting...
        refract = vec2np(refract)
        refract = np.where(det == 0.0, reflect, refract)
        refract = np2vec(refract)

        return refract

    def place(self, cond):
        r = Vec3(np.zeros(cond.shape), np.zeros(cond.shape), np.zeros(cond.shape))
        np.place(r.x, cond, self.x)
        np.place(r.y, cond, self.y)
        np.place(r.z, cond, self.z)
        return r

    def components(self):
        return (self.x, self.y, self.z)

    def __str__(self):
        return '({}, {}, {})'.format(self.x, self.y, self.z)
