# -*- coding: utf-8 -*-

__author__ = 'Douglas Uba'

import json
from rayden.constants import AIR_REFRACTION_INDEX
from rayden.primitives import Plane, Sphere, Torus, Triangle
from rayden.lights import AreaLightSource, PointLightSource
from rayden.camera import Camera
from rayden.color import RGB
from rayden.material import Checkerboard, Material
from rayden.vector import Vec3

class Scene():
    def __init__(self, camera, ambient=RGB(0.0, 0.0, 0.0)):
        self.camera = camera
        self.lights = []
        self.primitives = []
        self.ambient = ambient

    def getCamera(self):
        return self.camera

    def addLightSource(self, light):
        self.lights.append(light)

    def setLightSources(self, lights):
        self.lights = lights

    def addPrimitive(self, p):
        self.primitives.append(p)

    def setPrimitives(self, primitives):
        self.primitives = primitives

class Reader():
    @staticmethod
    def read(file):
        with open(file) as f:
            return Reader.readScene(json.load(f))

    @staticmethod
    def readScene(data):
        camera = Reader.readCamera(data['camera'])
        scene = Scene(camera, Reader.readRGB(data['ambient']))
        scene.setLightSources(Reader.readLights(data['lights']))
        scene.setPrimitives(Reader.readObjects(data['objects']))
        return scene
        
    @staticmethod
    def readVec3(data):
        return Vec3(data[0], data[1], data[2])

    @staticmethod
    def readRGB(data):
        if(isinstance(data, str)):
            return RGB.fromName(data)
        return RGB(data[0], data[1], data[2])

    @staticmethod
    def readCamera(data):
        eye = Reader.readVec3(data['eye'])
        lookAt = Reader.readVec3(data['lookAt'])
        up = Reader.readVec3(data['up'])
        width, height = data['width'], data['height']
        return Camera(eye, lookAt, up, width, height)

    @staticmethod
    def readLights(data):
        lights = []
        for l in data:
            watts = l['watts']
            color = Reader.readRGB(l['color'])
            if l['type'] == 'area':
                a, b, c, d = Reader.readVec3(l['v1']), Reader.readVec3(l['v2']), \
                             Reader.readVec3(l['v3']), Reader.readVec3(l['v4'])
                lights.append(AreaLightSource(color, watts, a, b, c, d))
            elif l['type'] == 'point':
                lights.append(PointLightSource(Reader.readVec3(l['position']), color, watts))
        return lights

    @staticmethod
    def readObjects(data):
        objects = []
        for obj in data:
            if obj['type'] == 'sphere':
                sphere = Sphere(Reader.readVec3(obj['center']), obj['radius'])
                sphere.setMaterial(Reader.readMaterial(obj['material']))
                objects.append(sphere)
            elif obj['type'] == 'plane':
                plane = Plane(Reader.readVec3(obj['normal']), obj['distance'])
                plane.setMaterial(Reader.readMaterial(obj['material']))
                objects.append(plane)
            elif obj['type'] == 'triangle':
                triangle = Triangle(Reader.readVec3(obj['a']), Reader.readVec3(obj['b']), Reader.readVec3(obj['c']))
                triangle.setMaterial(Reader.readMaterial(obj['material']))
                objects.append(triangle)
            elif obj['type'] == 'torus':
                torus = Torus(obj['sweptRadius'], obj['tubeRadius'])
                torus.setMaterial(Reader.readMaterial(obj['material']))
                objects.append(torus)
        return objects

    @staticmethod
    def readMaterial(data):
        if 'checkerboard' in data:
            scale = data['checkerboard'].get('scale', 5.0)
            material = Checkerboard(Reader.readRGB(data['checkerboard']['color1']),
                Reader.readRGB(data['checkerboard']['color2']), scale)
        else:
            diffuse = Reader.readRGB(data['diffuse'])
            material = Material(diffuse)
        if('specular' in data):
            material.specular = Reader.readRGB(data['specular'])
        material.shininess = data.get('shininess', 0.0)
        material.reflectivity = data.get('reflectivity', 0.0)
        material.refractionIndex = data.get('refractionIndex', AIR_REFRACTION_INDEX)
        return material
