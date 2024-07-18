import math
import cmath
import numpy as np
from scipy.spatial.transform import Rotation as R


class QuantumInfoDynamics:
    def __init__(self, dimensions=3):
        self.dimensions = dimensions
        self.state = np.random.rand(dimensions)
        self._normalize()

    @property
    def state(self):
        return self._state.copy()

    @state.setter
    def state(self, value):
        self._state = value
        self._normalize()

    def _normalize(self):
        self._state /= np.linalg.norm(self._state)

    def rotate(self, axis, angle):
        r = R.from_rotvec(np.array(axis) * angle)
        self.state = r.apply(self.state)
        self._normalize()

    def interact(self, other):
        interaction = np.cross(self.state, other.state)
        self.state += interaction
        other.state += interaction
        self._normalize()
        other._normalize()

    def measure(self):
        return np.linalg.norm(self.state) ** 2


class TripartiteState:
    def __init__(self, *args):
        if len(args) != 4:
            raise ValueError(
                "TripartiteState must be initialized with exactly 4 arguments"
            )
        self.q = list(map(complex, args))

    @property
    def q(self):
        return self._q.copy()

    @q.setter
    def q(self, value):
        self._q = value

    def __mul__(self, other):
        a1, b1, c1, d1 = self.q
        a2, b2, c2, d2 = other.q
        return TripartiteState(
            a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
            a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
            a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2,
        )

    def conjugate(self):
        return TripartiteState(*[x.conjugate() for x in self.q])

    @property
    def norm(self):
        return math.sqrt(sum(abs(x) ** 2 for x in self.q))


def rotate(state, axis, angle):
    half_angle = angle / 2
    sin_half = cmath.sin(half_angle)
    cos_half = cmath.cos(half_angle)

    # Extract real and imaginary parts of complex number
    real_part = np.real(sin_half)
    imag_part = np.imag(sin_half)

    # Convert complex number to Euler angles
    if axis[0] == 1:
        euler_angles = np.array([0, np.arctan2(imag_part, real_part), 0])
    elif axis[1] == 1:
        euler_angles = np.array([0, np.arctan2(real_part, imag_part), 0])
    elif axis[2] == 1:
        euler_angles = np.array(
            [np.arctan2(np.imag(cos_half), np.real(cos_half)), 0, 0]
        )

    r = R.from_euler("zxy", euler_angles)

    state_q_list = list(state.q)  # Convert the tuple to a list
    rotated_state_q = []
    for q in state_q_list:
        q_real = q.real
        q_imag = q.imag
        q_x = q_real
        q_y = q_imag
        q_z = 0  # You could also use np.real(q) and np.imag(q) if you want to keep the phase
        result = r.apply([[q_x, q_y, q_z]]).T[0]
        if len(result) == 3:
            rotated_state_q.append(complex(*result))
        else:
            rotated_state_q.append(q)

    return TripartiteState(*rotated_state_q)


def main():
    # Example usage
    initial_state = TripartiteState(1, 0, 0, 0)  # Pure information state
    rotated_state = rotate(
        initial_state, (0, 1, 0), math.pi / 4
    )  # Rotate towards matter

    # Example usage
    qid1 = QuantumInfoDynamics()
    qid2 = QuantumInfoDynamics()

    print("Initial states:")
    print(qid1.state, qid2.state)

    qid1.rotate([0, 1, 0], np.pi / 4)
    qid2.rotate([1, 0, 0], np.pi / 3)

    print("After rotation:")
    print(qid1.state, qid2.state)

    qid1.interact(qid2)

    print("After interaction:")
    print(qid1.state, qid2.state)

    print("Measurements:")
    print(qid1.measure(), qid2.measure())


if __name__ == "__main__":
    main()
