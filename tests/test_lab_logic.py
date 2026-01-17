import unittest
import numpy as np
from src.features.lab.logic import (
    apply_output_sharpening,
    apply_saturation,
)


class TestLabLogic(unittest.TestCase):
    def test_output_sharpening(self) -> None:
        """Sharpening should increase local variance."""
        # Create a simple square
        img = np.zeros((100, 100, 3), dtype=np.float32)
        img[25:75, 25:75, :] = 0.5

        res = apply_output_sharpening(img, amount=1.0, scale_factor=1.0)

        # Sharpening should increase variance on edges
        self.assertGreater(np.var(res), np.var(img))

    def test_saturation(self) -> None:
        """Saturation should modify color intensity."""
        # Pure Red (H=0, S=1, V=1)
        img = np.zeros((10, 10, 3), dtype=np.float32)
        img[:, :, 0] = 1.0

        # Reduce saturation to 0 (Greyscale)
        desat = apply_saturation(img, 0.0)

        # Desaturated pure primary should result in high value (white in this context for HSV)
        self.assertAlmostEqual(desat[0, 0, 0], 1.0)
        self.assertAlmostEqual(desat[0, 0, 1], 1.0)
        self.assertAlmostEqual(desat[0, 0, 2], 1.0)

        # Increase saturation of a pale color
        # Pale Red: R=1.0, G=0.5, B=0.5
        img2 = np.ones((10, 10, 3), dtype=np.float32) * 0.5
        img2[:, :, 0] = 1.0

        sat = apply_saturation(img2, 2.0)
        # S should become 1.0 -> Pure Red
        self.assertAlmostEqual(sat[0, 0, 0], 1.0, delta=1e-5)
        self.assertAlmostEqual(sat[0, 0, 1], 0.0, delta=1e-5)
        self.assertAlmostEqual(sat[0, 0, 2], 0.0, delta=1e-5)


if __name__ == "__main__":
    unittest.main()
