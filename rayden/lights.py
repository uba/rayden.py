# -*- coding: utf-8 -*-

__author__ = 'Douglas Uba'

from abc import ABC, abstractmethod
import numpy as np
from rayden.vector import Vec3

class AbstractLightSource(ABC):
    def __init__(self, color, watts=100.0):
        self.color = color
        self.watts = watts

    @abstractmethod
    def getPosition(self):
        pass

class PointLightSource(AbstractLightSource):
    def __init__(self, position, color, watts=100.0):
        super().__init__(color, watts)
        self.position = position

    def getPosition(self):
        return self.position
        
class AreaLightSource(AbstractLightSource):
    def __init__(self, color, watts, a, b, c, d):
        super().__init__(color, watts)
        self.vertices = [a,b,c,d]
        self.edge01 = a - b
        self.edge02 = a - c
        self.edge03 = a - d

    def getPosition(self):
        return self.__generatePosition(1.0, self.vertices[2],
                                      np.random.random_sample(), self.edge01,
                                      np.random.random_sample(), self.edge03)
        
    def __generatePosition(self, a, v1, b, v2, c, v3):
        pos = Vec3()
        pos.x = a * v1.x + b * v2.x + c * v3.x
        pos.y = a * v1.y + b * v2.y + c * v3.y
        pos.z = a * v1.z + b * v2.z + c * v3.z
        return pos
        