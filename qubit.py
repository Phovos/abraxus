import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ComplexQubit:
    def __init__(self, alpha_real_bytes, alpha_imag_bytes):
        self.alpha_real = self._bytes_to_float(alpha_real_bytes)
        self.alpha_imag = self._bytes_to_float(alpha_imag_bytes)
        self._normalize()

    def _bytes_to_float(self, byte_pair):
        # Convert 2 bytes to a float between -1 and 1
        return int.from_bytes(byte_pair, 'big', signed=True) / 32768

    def _normalize(self):
        # Ensure |α|² + |β|² = 1
        norm = np.sqrt(self.alpha_real**2 + self.alpha_imag**2)
        if norm > 1:
            self.alpha_real /= norm
            self.alpha_imag /= norm

    @property
    def alpha(self):
        return complex(self.alpha_real, self.alpha_imag)

    @property
    def beta(self):
        beta_real = np.sqrt(1 - (self.alpha_real**2 + self.alpha_imag**2))
        return complex(beta_real, 0)

    def measure(self):
        prob_zero = np.abs(self.alpha)**2
        return 0 if np.random.random() < prob_zero else 1

    def apply_hadamard(self):
        new_alpha = (self.alpha + self.beta) / np.sqrt(2)
        new_real_bytes = int(new_alpha.real * 32768).to_bytes(2, 'big', signed=True)
        new_imag_bytes = int(new_alpha.imag * 32768).to_bytes(2, 'big', signed=True)
        return ComplexQubit(new_real_bytes, new_imag_bytes)

    def bloch_coordinates(self):
        theta = 2 * np.arccos(np.abs(self.alpha))
        phi = np.angle(self.beta / self.alpha) if np.abs(self.alpha) > 0 else 0
        return np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)

def visualize_bloch_sphere(qubits):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Draw Bloch sphere
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    ax.plot_wireframe(x, y, z, color="gray", alpha=0.1)
    
    # Plot qubit states
    for qubit in qubits:
        x, y, z = qubit.bloch_coordinates()
        ax.scatter(x, y, z)
    
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.title("Qubit States on Bloch Sphere")
    plt.show()

# Example usage
qubits = [
    ComplexQubit((0,0), (0,0)),  # |0⟩
    ComplexQubit((255,255), (0,0)),  # |1⟩
    ComplexQubit((181,0), (0,0)),  # |+⟩
    ComplexQubit((181,0), (181,0)),  # |+i⟩
]

visualize_bloch_sphere(qubits)

# Demonstrate measurement
q = ComplexQubit((181,0), (0,0))  # |+⟩ state
measurements = [q.measure() for _ in range(1000)]
print(f"Measurement results for |+⟩: {sum(measurements)/len(measurements):.2f} ones")

# Demonstrate Hadamard gate
q = ComplexQubit((0,0), (0,0))  # |0⟩ state
q_after_h = q.apply_hadamard()
print(f"|0⟩ after Hadamard: α={q_after_h.alpha:.2f}, β={q_after_h.beta:.2f}")