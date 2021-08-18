# -*- coding: utf-8 -*-

__author__ = 'Douglas Uba'

import numpy as np
from rayden.ray import Ray
from rayden.vector import Vec3

class Camera():
    def __init__(self, eye, lookAt, up, width, height):
        # Camera parameters
        self.eye = eye
        self.lookAt = lookAt
        self.up = up
        self.width = width
        self.height = height

        # Setup camera coordinates
        self.direction = (lookAt - eye).normalized()
        self.u = up.cross(self.direction).normalized()
        self.v = self.direction.cross(self.u)
        
        # Build screen position
        res = float(self.width) / float(self.height)
        corners = (-1.0, 1.0/res + 0.25, 1.0, -1.0/res + 0.25)
        self.x = np.tile(np.linspace(corners[0], corners[2], self.width), self.height)
        self.y = np.repeat(np.linspace(corners[1], corners[3], self.height), self.width)

        # Buil ray-direction (i.e. a vector from eye to screen plane)
        self.eye2screen = (self.u * self.x) + (self.v * self.y) + self.direction

    def getRays(self, sampling=False):
        if not sampling:
            return Ray(self.eye, self.eye2screen)
        # Generate random samples
        rx = np.random.random(self.eye2screen.x.shape)/self.width
        ry = np.random.random(self.eye2screen.y.shape)/self.height
        return Ray(self.eye, Vec3(self.eye2screen.x + rx, self.eye2screen.y + ry, self.eye2screen.z))
