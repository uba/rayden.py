# -*- coding: utf-8 -*-

__author__ = 'Douglas Uba'

from abc import ABC, abstractmethod
import numpy as np
from rayden.color import RGB
from rayden.constants import AIR_REFRACTION_INDEX
from rayden.noise.simplexnoise import raw_noise_3d, scaled_octave_noise_3d
from rayden.vector import Vec3

class Material():
    def __init__(self, diffuse):
        self.diffuse = diffuse
        self.specular = RGB.fromName('black')
        self.shininess = 0.0
        self.reflectivity = 0.0
        self.refractionIndex = AIR_REFRACTION_INDEX
        self.normalMap = None

    def getColors(self, p=None):
        return self.diffuse, self.specular

    def getReflectivity(self):
        return self.reflectivity

    def hasReflectivity(self):
        return self.reflectivity != 0.0

    def getShininess(self):
        return self.shininess

    def hasShininess(self):
        return self.shininess != 0.0

    def getRefractionIndex(self):
        return self.refractionIndex

    @staticmethod
    def flatColor(color):
        material = Material(color)
        return material

    @staticmethod
    def glass():
        material = Material(RGB(0.1, 0.1, 0.1))
        material.specular = RGB(0.05, 0.05, 0.05)
        material.shininess = 96.0
        material.refractionIndex = 1.1
        return material

    @staticmethod
    def mirror(color=RGB.fromName('black')):
        material = Material(color)
        material.specular = RGB(0.05, 0.05, 0.05)
        material.shininess = 200.0
        material.reflectivity = 1.0
        return material

    @staticmethod
    def bronze():
        material = Material(RGB(0.714, 0.4284, 0.18144))
        material.specular = RGB(0.393548, 0.271906, 0.166721)
        material.shininess = 25.6
        material.reflectivity = 1.0
        return material

class Checkerboard(Material):
    def __init__(self, color1=RGB.fromName('white'), color2=RGB.fromName('black'), scale=6.0):
        super().__init__(None)
        self.color1 = color1
        self.color2 = color2
        self.scale = scale

    def getColors(self, p):
        sines = np.sin(self.scale * p.x) * np.sin(self.scale * p.y) * np.sin(self.scale * p.z)
        r = np.where(sines < 0, self.color1.r, self.color2.r)
        g = np.where(sines < 0, self.color1.g, self.color2.g)
        b = np.where(sines < 0, self.color1.b, self.color2.b)
        return RGB(r, g, b), self.specular

class NormalMap():
    def __init__(self, scale, amount):
        self.scale = scale
        self.amount = amount
        self.noise = np.zeros(0)
    
    def modify(self, normal, p):
        if(p.x.shape[0] != self.noise.shape[0]):
            scaled = p * self.scale
            self.noise = []
            for x, y, z in zip(scaled.x, scaled.y, scaled.z):
                self.noise.append(raw_noise_3d(x, y, z))
            self.noise = np.array(self.noise)
        return (normal + Vec3(self.noise, self.noise, self.noise) * self.amount).normalized()

class Wood(Material):
    def __init__(self, color1=RGB(0.1043, 0.0737, 0.0517), color2=RGB(0.4215, 0.2686, 0.1888), scale=10.0):
        super().__init__(None)
        self.color1 = color1
        self.color2 = color2
        self.scale = scale
        self.noise = np.zeros(0)

    def getColors(self, p):
        if(p.x.shape[0] != self.noise.shape[0]):
            scaled = p * self.scale
            self.noise = []
            for x, y, z in zip(scaled.x, scaled.y, scaled.z):
                self.noise.append(raw_noise_3d(x, y, z) * 5.0)
            self.noise = np.array(self.noise)
            self.noise = self.noise - self.noise.astype(np.int)
        return self.color1 * self.noise + self.color2 * (1.0 - self.noise), self.specular

class Turbulence(Material):
    def __init__(self, color1=RGB(1.0, 1.0, 1.0), color2=RGB(0.0, 0.0, 1.0), scale=8.0):
        super().__init__(None)
        self.color1 = color1
        self.color2 = color2
        self.scale = scale
        self.numberOfOctaves = 4
        self.noise = np.zeros(0)

    def getColors(self, p):
        if(p.x.shape[0] != self.noise.shape[0]):
            scaled = p * self.scale
            self.noise = []
            for x, y, z in zip(scaled.x, scaled.y, scaled.z):
                self.noise.append(scaled_octave_noise_3d(self.numberOfOctaves, 0.5, 1.0, 0.0, 1.0, x, y, z))
            self.noise = np.array(self.noise)
        return self.color1 * self.noise + self.color2 * (1.0 - self.noise), self.specular
       
