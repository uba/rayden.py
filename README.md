# rayden.py
Rayden - Simple Python Ray Tracing

## Features
- **Geometry**: Sphere, Plane, Triangle, Torus
- **Light**: Point, Area (rectangle)
- **Material**: Diffuse, Specular, Mirror, Glass, Checkerboard, Procedural Textures, Normal Map
- **Distributed Ray Tracing**: samples per pixel and shadow
- **Depth of Field**: depth and dispersion setup
- Scene description from JSON file
- Using *numpy* and *multiprocessing*
- FQS - Fast Quartic and Cubic solver (https://github.com/NKrvavica/fqs) for computing roots of a quartic equation (torus intersection)
- 2D, 3D and 4D Simplex Noise functions from https://github.com/dangillet/space_tactical/blob/master/simplexnoise.py

## Usage
```
rayden.py --help
usage: rayden [-h] --scene SCENE --output OUTPUT [--samplesPerPixel SPIXEL] [--samplesPerShadow SSHADOW]
              [--depthComplexity DEPTHCOMPLEXITY] [--dispersion DISPERSION] [--phong]

Rayden - Simple Python Ray Tracing

optional arguments:
  -h, --help            show this help message and exit
  --scene SCENE, -s SCENE
                        Scene description file
  --output OUTPUT, -o OUTPUT
                        Output file
  --samplesPerPixel SPIXEL, -sp SPIXEL
                        Samples per pixel
  --samplesPerShadow SSHADOW, -ss SSHADOW
                        Samples per shadow
  --depthComplexity DEPTHCOMPLEXITY, -dp DEPTHCOMPLEXITY
                        Depth complexity (depth of field)
  --dispersion DISPERSION, -dis DISPERSION
                        Dispersion (depth of field)
  --phong               Use classical Phong for specular component. Blinn-Phong, otherwise.
```

## Examples                                                 
```
rayden.py -s ./scenes/red-sphere.json -o ./results/red-sphere.png
```
<img src="results/red-sphere.png" width="256px"/>

```
rayden.py -s ./scenes/red-sphere-shadow.json
```
<img src="results/red-sphere-shadow.png" width="256px"/>

```
rayden.py -s ./scenes/hello-rayden.json
```
<img src="results/hello-rayden.png" width="256px"/>

```
rayden.py -s ./scenes/hello-rayden.json --samplesPerPixel 4
```
<img src="results/hello-rayden-4px.png" width="256px"/>

```
rayden.py -s ./scenes/hello-rayden.json --samplesPerPixel 16
```
<img src="results/hello-rayden-16px.png" width="256px"/>

```
rayden.py -s ./scenes/hello-rayden.json --samplesPerPixel 16 --samplesPerShadow 4
```
<img src="results/hello-rayden-16px-4shadow.png" width="256px"/>

```
rayden.py -s ./scenes/hello-rayden.json --samplesPerPixel 16 --samplesPerShadow 4 --depthComplexity 8
```
<img src="results/hello-rayden-16px-4shadow-8depth.png" width="256px"/>

```
rayden.py -s ./scenes/hello-rayden.json --samplesPerPixel 16 --samplesPerShadow 4 --depthComplexity 8 --dispersion 10
```
<img src="results/hello-rayden-16px-4shadow-8depth-10dispersion.png" width="256px"/>

```
rayden.py -s ./scenes/hello-rayden.json --samplesPerPixel 16 --samplesPerShadow 4 --depthComplexity 8 --dispersion 16
```
<img src="results/hello-rayden-16px-4shadow-8depth-16dispersion.png" width="256px"/>

```
rayden.py -s ./scenes/pyramid.json
```
<img src="results/pyramid.png" width="256px"/>

```
rayden.py -s ./scenes/torus.json
```
<img src="results/torus.png" width="256px"/>

```
rayden.py -s ./scenes/torus-mirror.json
```
<img src="results/torus-mirror.png" width="256px"/>

```
rayden.py -s ./scenes/torus-glass.json
```
<img src="results/torus-glass.png" width="256px"/>
