import generate_vectors
import pickle
import sys

points = generate_vectors.read_svg(f"{sys.argv[1]}.svg", 10000)
coefficients = generate_vectors.get_coefficients(points, 1000)

with open(f'{sys.argv[1]}.pkl', 'wb') as f:
    pickle.dump(coefficients, f)