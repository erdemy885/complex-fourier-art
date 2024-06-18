from svgpathtools import svg2paths
import numpy as np
import cmath
from vector import vector

#reads svg into list of points with length sample_count
#returns list of complex numbers that represent points 
#in a coordinate plane of the svg centered at origin
def read_svg(file, sample_count):
    paths = svg2paths(file)[0]
    samples = sample_count
    points = []

    for path in paths:
        path_points = [path.point(t) for t in np.linspace(0, 1, samples)]
        points.extend(path_points)

    #flip y-coords
    points = [complex(point.real, -point.imag) for point in points]

    #center shape at origin
    centroid = np.mean(points)
    points = [point - centroid for point in points]
    return points

#extracts fourier coefficients from points
#returns list of fourier coefficients as well as the frequency of their respective vector
#in format (n, c) where n is the frequency and c is the complex fourier coefficient
def get_coefficients(points, num_vector_pairs):
    dt = 1/len(points)
    coefficients = []

    for n in range(-num_vector_pairs, num_vector_pairs):
        #f(t) * e^(-n*2pi*i*t) * dt
        #t * dt to normalize t from 0-1
        #no need to take average since input range is 1
        integral = [points[t] * cmath.exp(1j * -n * 2 * cmath.pi * t * dt) * dt for t in range(len(points))]
        coefficients.append((n, sum(integral)))

    #sort by magnitude
    coefficients = sorted(coefficients, key=lambda x: abs(x[1]), reverse=True)
    return coefficients


def get_vectors(coefficients):
    vectors = []
    for i in range(len(coefficients)):
        n, c = coefficients[i]
        if i == 0:
            v = vector(0j, c, n)
        else:
            v = vector(vectors[i-1].head, c, n)
        vectors.append(v)
    return vectors
