import base64
import math
import random
import struct
from pathlib import Path


ROWS = 200
COLS = 200
NUM_MATRICES = 5
OUTPUT_DIR = Path(__file__).resolve().parent / "inputs"


def generate_matrix(seed: int) -> list[float]:
    """Create a deterministic ROWS x COLS matrix with values in [-1.0, 1.0)."""
    rng = random.Random(seed)
    limit = math.sqrt(6.0 / (ROWS + COLS))
    return [rng.uniform(-limit, limit) for _ in range(ROWS * COLS)]


def encode_matrix_to_base64(values: list[float]) -> str:
    """Pack float values into IEEE 754 binary16 (little-endian) and encode as Base64."""
    buffer = bytearray()
    for value in values:
        buffer.extend(struct.pack("<e", value))
    return base64.b64encode(buffer).decode("ascii")


def write_matrices():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for idx in range(1, NUM_MATRICES + 1):
        values = generate_matrix(seed=idx)
        encoded = encode_matrix_to_base64(values)
        target_path = OUTPUT_DIR / f"200x200_{idx}.txt"
        target_path.write_text(encoded + "\n", encoding="utf-8")
        print(f"Wrote {target_path.name} ({len(encoded)} Base64 chars)")


def main():
    write_matrices()


if __name__ == "__main__":
    main()
