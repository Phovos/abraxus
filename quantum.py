from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class ProbabilisticBit:
    probability: float

@dataclass
class ProbabilisticByte:
    bits: List[ProbabilisticBit]

    def __post_init__(self):
        if len(self.bits) != 8:
            raise ValueError("A byte must consist of exactly 8 bits.")

@dataclass
class ProbabilisticWord:
    bytes: List[ProbabilisticByte]

    def __post_init__(self):
        if len(self.bytes) != 2:
            raise ValueError("A word must consist of exactly 2 bytes.")

@dataclass
class ProbabilisticDoubleWord:
    words: List[ProbabilisticWord]

    def __post_init__(self):
        if len(self.words) != 2:
            raise ValueError("A double word must consist of exactly 2 words (4 bytes).")

@dataclass
class ProbabilisticBitString:
    bits: List[ProbabilisticBit]

    def __post_init__(self):
        pass  # No specific length requirement for arbitrary bit strings

@dataclass
class QuantumState:
    alpha_squared: float
    beta_squared: float

    def __post_init__(self):
        if not (0 <= self.alpha_squared <= 1 and 0 <= self.beta_squared <= 1):
            raise ValueError("Probabilities must be between 0 and 1.")
        if abs(self.alpha_squared + self.beta_squared - 1) > 1e-6:
            raise ValueError("Probabilities must sum to 1 (normalization).")

    @staticmethod
    def from_byte(byte_value: int) -> 'QuantumState':
        alpha_squared = byte_value / 255
        beta_squared = 1 - alpha_squared
        return QuantumState(alpha_squared=alpha_squared, beta_squared=beta_squared)

    def to_byte(self) -> int:
        return int(self.alpha_squared * 255)


def main():
    print(f"{'Byte Value':<12} {'|alpha|^2':<12} {'|beta|^2':<12}")
    print('-' * 36)
    for byte_value in range(256):
        state = QuantumState.from_byte(byte_value)
        print(f"{byte_value:<12} {state.alpha_squared:<12.6f} {state.beta_squared:<12.6f}")

if __name__ == "__main__":
    main()