# fractal.py
# Fractal generator.

import numpy as np
import math

def gaussian(x, a, b, c, d=0):

    """Gaussian gradient."""

    return a * math.exp(-(x - b)**2 / (2 * c**2)) + d

def gradient(x, width=100, map=[], spread=1):

    """Gaussian color gradient. map should be a list of control points for the
    gradient. Each control point should be a tuple of two values: the location 
    the point as a value between 0 and 1, and the color of the point as a 
    tuple of three values between 0 and 1. For example, a valid gradient map 
    may be: [
    [0.0, (0, 0, 0)],
    [0.20, (0, 0, .5)],
    [1.00, (1.0, 1.0, 1.0)]
    ]. Note that a valid gradient map must include a point at 0.0 and 1.0, and
    be sorted by location."""

    width = float(width)
    r = sum([gaussian(x, p[1][0], p[0] * width, width/(spread*len(map))) for p in map])
    g = sum([gaussian(x, p[1][1], p[0] * width, width/(spread*len(map))) for p in map])
    b = sum([gaussian(x, p[1][2], p[0] * width, width/(spread*len(map))) for p in map])
    return min(1.0, r), min(1.0, g), min(1.0, b)

class FractalGenerator:

    """The base fractal generator object."""

    def __init__(self):

        """Create the fractal generator object."""

        raise NotImplementedError()
    
    def generate(self, height, width):

        """Generate the fractal image. Takes the image height and width (in 
        pixels) as parameters, and returns the output image."""

        raise NotImplementedError()
    
class CustomFractal(FractalGenerator):

    """The custom fractal generator."""

    def __init__(self, function, bounds_x=(0.0, 0.1), bounds_y=(0.0, 1.0), colormap=[
            [0.0, (0, 0.0274509803921569, 0.392156862745098)],
            [0.16, (0.12549019607843137, 0.4196078431372549, 0.796078431372549)],
            [0.42, (0.9294117647058824, 1.0, 1.0)],
            [0.6425, (1.0, 0.6666666666666666, 0.0)],
            [0.8575, (0.0, 0.00784313725490196, 0.0)],
            [1.0, (0.0, 0.00784313725490196, 0.0)]
        ]):

        """Create the custom fractal generator. function should be a function 
        taking the x and y coordinates of the current pixel as arguments, 
        returning a value between 0 and 1 for the color. Takes the x and
        y bounds as parameters. The generator also takes a parameter for the 
        colormap."""

        assert len(bounds_x) == 2, "bounds_x must have two values"
        assert len(bounds_y) == 2, "bounds_y must have two values"
        assert len(colormap) >= 2, "colormap must have at least two points"

        self.function = function

        self.bounds_x = bounds_x
        self.bounds_y = bounds_y

        self.colormap = colormap

    def generate(self, height, width):

        """Generate the custom fractal image. Takes the image height and 
        width (in pixels) as parameters, and returns the output image."""

        # Create the output image.
        pix = np.zeros((height, width, 3), np.int8)

        # Generate the image.
        for i, x in enumerate(np.linspace(*self.bounds_x, width)):
            for j, y in enumerate(np.linspace(*self.bounds_y, height)):
                # Set the pixel.
                r, g, b = gradient(self.function(x, y), 1, self.colormap)
                pix[j][i] = (255 * r, 255 * g, 255 * b)

        return pix
    
class MandelbrotFractal(FractalGenerator):

    """The Mandelbrot set fractal generator."""

    def __init__(self, bounds_real=(-2.0, 0.5), bounds_imag=(-1.0, 1.0), bound_limit=1000.0, iter_limit=100, colormap=[
            [0.0, (0, 0.0274509803921569, 0.392156862745098)],
            [0.16, (0.12549019607843137, 0.4196078431372549, 0.796078431372549)],
            [0.42, (0.9294117647058824, 1.0, 1.0)],
            [0.6425, (1.0, 0.6666666666666666, 0.0)],
            [0.8575, (0.0, 0.00784313725490196, 0.0)],
            [1.0, (0.0, 0.00784313725490196, 0.0)]
        ], threads=1):

        """Create the Mandelbrot set fractal generator. Takes the real and
        imaginary bounds as parameters, along with the bound limit and 
        iteration limit. Bounds default to (-2.0, 0.5) along the real axis and
        (-1.0, 1.0) along the imaginary axis. The bound limit defaults to 
        1000.0 the iteration limit defaults to 100. The generator also takes a 
        parameter for the colormap."""

        assert len(bounds_real) == 2, "bounds_real must have two values"
        assert len(bounds_imag) == 2, "bounds_imag must have two values"
        assert len(colormap) >= 2, "colormap must have at least two points"

        self.bounds_real = bounds_real
        self.bounds_imag = bounds_imag

        self.bound_limit = bound_limit
        self.iter_limit = iter_limit

        self.colormap = colormap

    def generate(self, height, width):

        """Generate the Mandelbrot fractal image. Takes the image height and 
        width (in pixels) as parameters, and returns the output image."""

        # Create the output image.
        pix = np.zeros((height, width, 3), np.int8)

        # Generate the image.
        for i, x in enumerate(np.linspace(*self.bounds_real, width)):
            for j, y in enumerate(np.linspace(*self.bounds_imag, height)):
                # Calculate the location of the given pixel on the complex 
                # plane.
                c = complex(x, y)

                # Perform the Mandelbrot iteration while z remains bounded.
                z = c
                num_iterations = 0
                while abs(z) < self.bound_limit and num_iterations < self.iter_limit:
                    # z = z^2 + c
                    z = z ** 2 + c

                    # Increment the iteration.
                    num_iterations += 1

                # Set the pixel.
                r, g, b = gradient(num_iterations / self.iter_limit, 1, self.colormap)
                pix[j][i] = (255 * r, 255 * g, 255 * b)

        return pix
    
class JuliaFractal(FractalGenerator):

    """The Julia set fractal generator."""

    def __init__(self, c=-0.8+0.156j, bounds_real=(-2.0, 0.5), bounds_imag=(-1.0, 1.0), bound_limit=1000.0, iter_limit=100, colormap=[
            [0.0, (0, 0.0274509803921569, 0.392156862745098)],
            [0.16, (0.12549019607843137, 0.4196078431372549, 0.796078431372549)],
            [0.42, (0.9294117647058824, 1.0, 1.0)],
            [0.6425, (1.0, 0.6666666666666666, 0.0)],
            [0.8575, (0.0, 0.00784313725490196, 0.0)],
            [1.0, (0.0, 0.00784313725490196, 0.0)]
        ], threads=1):

        """Create the Julia set fractal generator. Requires c. Takes the real 
        and imaginary bounds as parameters, along with the bound limit and 
        iteration limit. Bounds default to (-2.0, 0.5) along the real axis and
        (-1.0, 1.0) along the imaginary axis. The bound limit defaults to 
        1000.0 the iteration limit defaults to 100. The generator also takes a 
        parameter for the colormap."""

        assert len(bounds_real) == 2, "bounds_real must have two values"
        assert len(bounds_imag) == 2, "bounds_imag must have two values"
        assert len(colormap) >= 2, "colormap must have at least two points"

        self.c = c

        self.bounds_real = bounds_real
        self.bounds_imag = bounds_imag

        self.bound_limit = bound_limit
        self.iter_limit = iter_limit

        self.colormap = colormap

    def generate(self, height, width):

        """Generate the Mandelbrot fractal image. Takes the image height and 
        width (in pixels) as parameters, and returns the output image."""

        # Create the output image.
        pix = np.zeros((height, width, 3), np.int8)

        # Generate the image.
        for i, x in enumerate(np.linspace(*self.bounds_real, width)):
            for j, y in enumerate(np.linspace(*self.bounds_imag, height)):
                # Calculate the location of the given pixel on the complex 
                # plane.
                z = complex(x, y)

                # Perform the Mandelbrot iteration while z remains bounded.
                
                num_iterations = 0
                while abs(z) < self.bound_limit and num_iterations < self.iter_limit:
                    # z = z^2 + c
                    z = z ** 2 + self.c

                    # Increment the iteration.
                    num_iterations += 1

                # Set the pixel.
                r, g, b = gradient(num_iterations / self.iter_limit, 1, self.colormap)
                pix[j][i] = (255 * r, 255 * g, 255 * b)

        return pix