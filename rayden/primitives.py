# -*- coding: utf-8 -*-

__author__ = 'Douglas Uba'

from abc import ABC, abstractmethod
import numpy as np
from rayden.constants import MAX_DISTANCE, EPSILON
from rayden.math import fqs
from rayden.vector import Vec3

class Primitive(ABC):
    def __init__(self):
        self.material = None

    @abstractmethod
    def intercept(self, ray):
        pass

    @abstractmethod
    def getNormalAt(self, p):
        pass

    def setMaterial(self, material):
        self.material = material

    def getMaterial(self):
        return self.material
        
class Sphere(Primitive):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def intercept(self, ray):
        b = 2 * ray.direction.dot(ray.origin - self.center)
        c = abs(self.center) + abs(ray.origin) - 2 * self.center.dot(ray.origin) - (self.radius * self.radius)
        disc = (b ** 2) - (4 * c)
        sq = np.sqrt(np.maximum(0, disc))
        h0 = (-b - sq) * 0.5
        h1 = (-b + sq) * 0.5
        h = np.where((h0 > 0) & (h0 < h1), h0, h1)
        pred = (disc >= 0) & (h > EPSILON)
        return np.where(pred, h, MAX_DISTANCE)

    def getNormalAt(self, p):
        return (p - self.center).normalized()

class Plane(Primitive):
    def __init__(self, normal, distance):
        self.normal = normal.normalized()
        self.distance = distance

    def intercept(self, ray):
        c = ray.direction.dot(self.normal) # case == 0?
        t = -1.0 * ((self.normal.dot(ray.origin) + self.distance) / c)
        pred = (t >= EPSILON) & (np.abs(c) > EPSILON)
        return np.where(pred, t, MAX_DISTANCE)

    def getNormalAt(self, p):
        return self.normal

class Triangle(Primitive):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.edge1 = b - a
        self.edge2 = c - a
        self.normal = (self.c - self.a).cross(self.b - self.a).normalized()

    def intercept(self, ray):
        h = ray.direction.cross(self.edge2)
        delta = self.edge1.dot(h)
        pred_delta = (delta <= -EPSILON) | (delta >= EPSILON)
        f = 1.0/delta
        s = ray.origin - self.a
        u = f * s.dot(h)
        pred_u = (u >= 0.0) & (u <= 1.0)
        q = s.cross(self.edge1)
        v = f * ray.direction.dot(q)
        pred_v = (v >= 0.0) & (u + v <= 1.0)
        t = f * self.edge2.dot(q)
        pred_t = (t > EPSILON)
        pred = (pred_delta) & (pred_u) & (pred_v) & (pred_t)
        return np.where(pred, t, MAX_DISTANCE)

    def getNormalAt(self, p):
        return self.normal

class Torus(Primitive):
    def __init__(self, sweptRadius, tubeRadius):
        self.sweptRadius = sweptRadius
        self.tubeRadius = tubeRadius

    def intercept(self, ray):
        ox, oy, oz = ray.origin.x, ray.origin.y, ray.origin.z
        dx, dy, dz = ray.direction.x, ray.direction.y, ray.direction.z
        sum_d_sqrd = dx * dx + dy * dy + dz * dz
        e = ox * ox + oy * oy + oz * oz - self.sweptRadius * self.sweptRadius - self.tubeRadius * self.tubeRadius
        f = ox * dx + oy * dy + oz * dz
        four_a_sqrd	= 4.0 * self.sweptRadius * self.sweptRadius
        coeffs = [
            e * e - four_a_sqrd * (self.tubeRadius * self.tubeRadius - oy * oy), #c0
            4.0 * f * e + 2.0 * four_a_sqrd * oy * dy, #c1
            2.0 * sum_d_sqrd * e + 4.0 * f * f + four_a_sqrd * dy * dy, #c2
            4.0 * sum_d_sqrd * f, # c3
            sum_d_sqrd * sum_d_sqrd #c4
        ]
        c = np.empty((coeffs[1].shape[0], 5), dtype=np.float64)
        c[:,0], c[:,1], c[:,2], c[:,3], c[:,4] = coeffs[4], coeffs[3], coeffs[2], coeffs[1], coeffs[0]
        roots = fqs.quartic_roots(c)
        roots[np.iscomplex(roots)] = MAX_DISTANCE
        t = np.min(np.real(roots), axis=1)
        t = t.astype(np.float64)
        t[t <= EPSILON] = MAX_DISTANCE
        return t

    def getNormalAt(self, p):
        pSquared = self.sweptRadius * self.sweptRadius + self.tubeRadius * self.tubeRadius
        sumSquared = p.x * p.x + p.y * p.y + p.z * p.z
        normal = Vec3(4.0 * p.x * (sumSquared - pSquared),
                      4.0 * p.y * (sumSquared - pSquared + 2.0 * self.sweptRadius * self.sweptRadius),
                      4.0 * p.z * (sumSquared - pSquared))
        return normal.normalized()