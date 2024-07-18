import numpy as np


class ComplexHilbertSpace:
    def __init__(self, dimension):
        self.dimension = dimension

    def inner_product(self, x, y):
        return np.dot(x, np.conjugate(y))

    def norm(self, x):
        return np.sqrt(self.inner_product(x, x).real)


# Example tokens as vectors
token1 = np.array([1 + 2j, 3 + 4j])
token2 = np.array([5 + 6j, 7 + 8j])

hilbert_space = ComplexHilbertSpace(dimension=2)

# Calculate inner product and norm
inner_prod = hilbert_space.inner_product(token1, token2)
norm_token1 = hilbert_space.norm(token1)

print(f"Inner Product: {inner_prod}")
print(f"Norm of Token 1: {norm_token1}")
