# rayden.py
Rayden - Simple Python Ray Tracing

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
