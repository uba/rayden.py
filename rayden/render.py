# -*- coding: utf-8 -*-

__author__ = 'Douglas Uba'

from abc import ABC, abstractmethod
from functools import reduce
import multiprocessing
import numpy as np
from PIL import Image
from rayden.color import RGB
from rayden.constants import EPSILON, MAX_DISTANCE, AIR_REFRACTION_INDEX
from rayden.ray import Ray
from rayden.utils import extract
from rayden.vector import Vec3

class Renderer(ABC):
    def __init__(self, scene, refractionIndex=AIR_REFRACTION_INDEX):
        self.camera = scene.getCamera()
        self.scene = scene
        self.refractionIndex = refractionIndex

    @abstractmethod
    def render(self):
        pass

class RayTracer(Renderer):
    def __init__(self, scene,
                 refractionIndex=AIR_REFRACTION_INDEX,
                 samplesPerPixel=16,
                 samplesPerShadow=5,
                 depthComplexity=1,
                 dispersion=5.0,
                 Phong=False): # Blinn-Phong, otherwise
        super().__init__(scene, refractionIndex)
        self.samplesPerPixel = samplesPerPixel
        self.samplesPerShadow = samplesPerShadow
        self.depthComplexity = depthComplexity
        self.dispersion = dispersion
        self.Phong = Phong
        self.maxProcessNumber = multiprocessing.cpu_count() * 4

    def render(self):
        manager = multiprocessing.Manager()
        results = manager.dict()
        jobs = []
        # Start processes
        for i in range(self.samplesPerPixel):
            rays = self.camera.getRays(sampling=True)
            p = multiprocessing.Process(target=self.depthAndTrace, args=(i, rays, results))
            jobs.append(p)
            p.start()
            if(len(jobs) >= self.maxProcessNumber):
              # Wait...
              for proc in jobs:
                  proc.join()
              jobs = []
        # Wait...
        for proc in jobs:
            proc.join()

        # Composition-stack
        color = RGB(0,0,0)
        for key in results:
            color += results[key]
        color = color * (1/float(self.samplesPerPixel))

        rgb = [Image.fromarray((255 * np.clip(c, 0, 1).reshape((self.camera.height, self.camera.width))).astype(np.uint8), 'L') for c in color.components()]
        return Image.merge('RGB', rgb)

    def depthAndTrace(self, i, rays, results):
        if self.depthComplexity == 1:
            results[i] = self.__trace(rays)
            return
        # else
        color = RGB(0,0,0)
        for j in range(self.depthComplexity):
            rx = np.random.random()/100.0
            ry = np.random.random()/100.0
            displacement = Vec3(self.dispersion * rx, self.dispersion * ry, 0.0)
            # Rebuild rays
            neweye = self.camera.eye + displacement
            w = (self.camera.lookAt - neweye).normalized()
            u = self.camera.up.cross(w).normalized()
            v = w.cross(u)
            rays.origin = neweye
            rays.direction = ((u * self.camera.x) + (v * self.camera.y) + w).normalized()
            color += self.__trace(rays)
        results[i] = color * (1/float(self.depthComplexity))

    def __trace(self, rays):
        distances = [p.intercept(rays) for p in self.scene.primitives]
        nearest = reduce(np.minimum, distances)
        color = RGB(0, 0, 0)
        for (p, d) in zip(self.scene.primitives, distances):
            hit = (nearest != MAX_DISTANCE) & (d == nearest)
            if np.any(hit):
                rays.setDistance(d, hit)
                color += self.__evaluate(p, rays).place(hit)
        return color

    def __evaluate(self, primitive, rays):
        # Get intersection info
        hitPoint = rays.findDestination()

        # Get normal at intersection point
        normal = primitive.getNormalAt(hitPoint)

        # Modify normal by material, if necessary
        if primitive.material.normalMap is not None:
            normal = primitive.material.normalMap.modify(normal, hitPoint)

        # Epsilon hitPoint
        hitPointEps = hitPoint + normal * 0.0001

        # Ambient color
        color = RGB(0.0, 0.0, 0.0)

        # Shade for each light
        for light in self.scene.lights:
            contribution = RGB(0.0, 0.0, 0.0)
            for i in range(self.samplesPerShadow):
                # Ambient color
                contribution += self.scene.ambient 

                # To check visibility
                direction_to_light = light.getPosition() - hitPoint

                # Mimimum distance used to known if primitive is coverted
                min_distance_to_light = direction_to_light.magnitude()

                # Build ray to light
                ray2light = Ray(hitPointEps, direction_to_light.normalized())

                # Compute distances for each primitive
                light_distances = [p.intercept(ray2light) for p in self.scene.primitives]

                # Retrieve nearest
                light_nearest = reduce(np.minimum, light_distances)

                # Ilumination function (0 or 1)
                iluminated = light_distances[self.scene.primitives.index(primitive)] == light_nearest
                iluminated[light_nearest > min_distance_to_light] = True
                
                # Compute angles
                alpha = np.maximum(normal.dot(direction_to_light.normalized()), 0)

                # Distance squared to light
                distance_squared = direction_to_light.magnitudeSquared()

                # Compute vectors in/out
                vin = direction_to_light.normalized()
                vout = (self.camera.eye - hitPoint).normalized()

                # Light attenuation
                lightAttenuation = 1.0/(np.pi * distance_squared)

                response = self.__brdf(hitPoint, vin, vout, normal, primitive.material)
                contribution += (response * alpha * light.watts) * iluminated * lightAttenuation

            # Weight by samplesPerShadow
            color += contribution * (1/float(self.samplesPerShadow))

        if primitive.material.hasReflectivity():
            reflectRay = Ray(hitPointEps, rays.inverted().reflect(normal))
            color += self.__trace(reflectRay) * primitive.material.getReflectivity()

        indexRef = primitive.material.getRefractionIndex()
        if indexRef != self.refractionIndex:
            refractRay = Ray(hitPoint, rays.getDirection().refract(normal, self.refractionIndex, indexRef))
            color += self.__trace(refractRay)

        return color

    def __brdf(self, hitPoint, vin, vout, normal, material):
        # Getting material parameters
        kd, ks = material.getColors(hitPoint)
        n = material.getShininess()

        # diffuse component
        result = kd * (1.0/np.pi)

        # specular component (Phong)
        if(self.Phong):
            sd = vin.reflect(normal)
            alpha = np.maximum(sd.dot(vout), 0)
            factor = pow(alpha, n)
            result += ((ks * (n + 2.0) * factor) * (1.0/(2.0 * np.pi)))
        else: # specular component Blinn-Phong
            sd = (vin + vout).normalized()
            alpha = np.maximum(sd.dot(normal), 0)
            factor = pow(alpha, n)
            result += ((ks * (n + 2.0) * factor) * (1.0/(2.0 * np.pi)))

        return result
