# -*- coding: utf-8 -*-

__author__ = 'Douglas Uba'

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from rayden.camera import Camera
from rayden.vector import Vec3

if __name__ == '__main__':
    # Setup camera
    eye = Vec3(0.0, 0.0, -1.0)
    lookAt = Vec3(0.0, 0.0, 1.0)
    up = Vec3(0.0, 1.0, 0.0)
    (width, height) = (8, 8)
    camera = Camera(eye, lookAt, up, width, height)

    # Generate set of rays
    rays = camera.getRays(sampling=False)

    # Plot rays and screen plane
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    plt.plot([eye.x], [eye.y], [eye.z], 'ro', zdir='y')
    plt.plot(rays.direction.x, rays.direction.y, 'bo', zs=0, zdir='y')
    X = np.full(len(rays.direction.x), eye.x)
    Y = np.full(len(rays.direction.y), eye.y)
    Z = np.full(len(rays.direction.z), eye.z)
    plt.quiver(X, Z, Y, rays.direction.x, rays.direction.z, rays.direction.y, arrow_length_ratio=0.1, linewidths=0.5)
    
    plt.show()
    