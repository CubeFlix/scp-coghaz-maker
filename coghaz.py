# coghaz.py

import numpy as np
import random, math
import fractal
from PIL import Image, ImageFont, ImageDraw, ImageOps

def corrupt(src, offset, axis='y'):

    """Corrupt an image."""

    if axis == 'y':
        offset_pix = np.zeros_like(src)
        offset_pix[:-offset] = src[offset:]
        return src + offset_pix
    elif axis == 'x':
        offset_pix = np.zeros_like(src)
        offset_pix[:][:-offset] = src[:][offset:]
        return src + offset_pix

class CognitohazardGenerator:

    """The base cognitohazard generator."""

    def __init__(self):

        """Create the base cognitohazard generator."""

        raise NotImplementedError()
    
    def generate(self, file, height, width):

        """Generate the cognitohazard."""

        raise NotImplementedError()

class PerlmanGreeneGenerator:

    """Perlman-Greene memetic kill agent generator."""

    def __init__(self, text=None, font=None):

        """Create the Perlman-Greene memetic kill agent. Optional text string
        and font parameter."""

        self.text = text
        self.font = font
        if self.font:
            import sys
            if getattr(sys, 'frozen', False):
                import os
                self.fontobj = ImageFont.truetype(os.path.join(sys._MEIPASS, self.font), 10)
            else:
                self.fontobj = ImageFont.truetype(self.font, 10)
    
    def generate(self, file, height, width):

        """Generate the Perlman-Greene cognitohazard."""

        # Generate the random bounds.
        radians = random.uniform(0.0, 6.28)
        real_bound = math.cos(radians) * 0.5 - 0.5
        real_size = random.uniform(0.75, 1.5)
        imag_bound = math.sin(radians) * 0.5 - 0.5
        imag_size = random.uniform(0.75, 1.5)

        mandel1 = fractal.MandelbrotFractal((real_bound, real_bound + real_size), \
                                            (imag_bound, imag_bound + imag_size), \
                                            random.randint(500, 1000), \
                                            random.randint(50, 100), \
                                            colormap=[
                                                [0.0, (0.0, 0.0, 0.0)],
                                                [random.uniform(0.1, 0.5), (random.random() / 2, random.random() / 2, random.random() / 2)],
                                                [random.uniform(0.6, 0.9), (random.random() / 2, random.random() / 2, random.random() / 2)],
                                                [1.0, (0.0, 0.0, 0.0)]
                                            ])
        pix_mandel1 = mandel1.generate(height, width)
        pix_mandel1 = corrupt(pix_mandel1, random.randint(40, 70), 'y')

        print("Generated Perlman-Greene.M1")

        # Generate the random bounds.
        radians = random.uniform(0.0, 6.28)
        real_bound = math.cos(radians) * 0.5 - 0.5
        real_size = random.uniform(0.75, 1.5)
        imag_bound = math.sin(radians) * 0.5 - 0.5
        imag_size = random.uniform(0.75, 1.5)

        mandel2 = fractal.MandelbrotFractal((real_bound, real_bound + real_size), \
                                            (imag_bound, imag_bound + imag_size), \
                                            random.randint(500, 1000), \
                                            random.randint(50, 100), \
                                            colormap=[
                                                [0.0, (0.0, 0.0, 0.0)],
                                                [random.uniform(0.1, 0.5), (random.random() / 2, random.random() / 2, random.random() / 2)],
                                                [random.uniform(0.6, 0.9), (random.random() / 2, random.random() / 2, random.random() / 2)],
                                                [1.0, (0.0, 0.0, 0.0)]
                                            ])
        pix_mandel2 = mandel2.generate(height, width)
        pix_mandel2 = corrupt(pix_mandel2, random.randint(50, 100), 'x')

        print("Generated Perlman-Greene.M2")

        # Generate the random bounds.
        radians = random.uniform(0.0, 6.28)
        real_bound = math.cos(radians) * 0.5 - 0.5
        real_size = random.uniform(0.75, 1.5)
        imag_bound = math.sin(radians) * 0.5 - 0.5
        imag_size = random.uniform(0.75, 1.5)

        julia1 = fractal.JuliaFractal(-0.8 + 0.156j,
                                      (real_bound, real_bound + real_size), \
                                      (imag_bound, imag_bound + imag_size), \
                                      random.randint(500, 1000), \
                                      random.randint(50, 100), \
                                      colormap=[
                                          [0.0, (0.0, 0.0, 0.0)],
                                          [random.uniform(0.1, 0.5), (random.random() / 2, random.random() / 2, random.random() / 2)],
                                          [random.uniform(0.6, 0.9), (random.random() / 2, random.random() / 2, random.random() / 2)],
                                          [1.0, (0.0, 0.0, 0.0)]
                                      ])
        pix_julia1 = julia1.generate(height, width)
        pix_julia1 = corrupt(pix_julia1, random.randint(50, 100), 'x')

        print("Generated Perlman-Greene.J1")

        pix = pix_mandel2 + pix_mandel1 + pix_julia1
        img = Image.fromarray(pix, 'RGB')
        img = ImageOps.invert(img)
        
        if self.text and self.font:
            draw = ImageDraw.Draw(img)
            size = self.fontobj.getsize(self.text)
            draw.text((random.randint(0, width - size[0]), random.randint(0, height - size[1])), self.text, fill='black', font=self.fontobj, align='left')

        img.save(file)

        print("Finished generating Perlman-Greene")