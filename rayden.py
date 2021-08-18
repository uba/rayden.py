# -*- coding: utf-8 -*-

__author__ = 'Douglas Uba'

import argparse
from rayden.color import RGB
from rayden.render import RayTracer 
from rayden.scene import Reader

if __name__ == '__main__':
    # Create command-line parser
    parser = argparse.ArgumentParser(description='Rayden - Simple Python Ray Tracing', prog='rayden')
    parser.add_argument('--scene', '-s', help='Scene description file', type=str, dest='scene', required=True)
    parser.add_argument('--output', '-o', help='Output file', type=str, dest='output', required=True)
    parser.add_argument('--samplesPerPixel', '-sp', help='Samples per pixel', type=int, dest='spixel', default=1, required=False)
    parser.add_argument('--samplesPerShadow', '-ss', help='Samples per shadow', type=int, dest='sshadow', default=1, required=False)
    parser.add_argument('--depthComplexity', '-dp', help='Depth complexity (depth of field)', type=int, dest='depthComplexity', default=1, required=False)
    parser.add_argument('--dispersion', '-dis', help='Dispersion (depth of field)', type=int, dest='dispersion', default=5, required=False)
    parser.add_argument('--phong', help='Use classical Phong for specular component. Blinn-Phong, otherwise.', action='store_true', dest='phong')

     # Parse input
    args = parser.parse_args()

    # Render
    rt = RayTracer(Reader.read(args.scene), samplesPerPixel=args.spixel,
                   samplesPerShadow=args.sshadow, depthComplexity=args.depthComplexity,
                   dispersion=args.dispersion, Phong=args.phong)

    image = rt.render()
    image.save(args.output)
