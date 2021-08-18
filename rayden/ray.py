# -*- coding: utf-8 -*-

__author__ = 'Douglas Uba'

from rayden.vector import Vec3
from rayden.utils import extract

class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalized()
        self.distance = 0.0
        self.filter = None

    def setDistance(self, distance, filter=None):
        self.distance = distance
        self.filter = filter

    def findDestination(self):
        return self.origin.extract(self.filter) + (self.direction.extract(self.filter) * extract(self.filter, self.distance))

    def getDirection(self):
        return self.direction.extract(self.filter)

    def inverted(self):
        return self.getDirection().inverted()
        
