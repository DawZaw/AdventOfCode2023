import unittest
from day_3 import mult_neighbours


def star(arr: list[str]) -> int:
    total: int = 0
    for x, row in enumerate(arr):
        for y, char in enumerate(row):
            if char == "*":
                total += mult_neighbours(arr, x, y)
    return total


class TestMult(unittest.TestCase):
    def test_topleft_topright(self):
        test = [
            ".123.123.",
            "....*....",
            ".........",
        ]
        self.assertEqual(star(test), 15129)

    def test_topleft_middleright(self):
        test = [
            ".123.....",
            "....*123.",
            ".........",
        ]
        self.assertEqual(star(test), 15129)

    def test_topleft_bottomright(self):
        test = [
            ".123.....",
            "....*....",
            ".....123.",
        ]
        self.assertEqual(star(test), 15129)

    def test_middleleft_topright(self):
        test = [
            ".....123.",
            ".123*....",
            ".........",
        ]
        self.assertEqual(star(test), 15129)

    def test_middleleft_middleright(self):
        test = [
            ".........",
            ".123*123.",
            ".........",
        ]
        self.assertEqual(star(test), 15129)

    def test_middleleft_bottomright(self):
        test = [
            ".........",
            ".123*....",
            ".....123.",
        ]
        self.assertEqual(star(test), 15129)

    def test_bottomleft_topright(self):
        test = [
            ".....123.",
            "....*....",
            ".123.....",
        ]
        self.assertEqual(star(test), 15129)

    def test_bottomleft_middleright(self):
        test = [
            ".........",
            "....*123.",
            ".123.....",
        ]
        self.assertEqual(star(test), 15129)

    def test_bottomleft_bottomright(self):
        test = [
            ".........",
            "....*....",
            ".123.123.",
        ]
        self.assertEqual(star(test), 15129)

    def test_middleleft_topleft(self):
        test = [
            ".123.....",
            ".123*....",
            ".........",
        ]
        self.assertEqual(star(test), 15129)

    def test_middleleft_bottomleft(self):
        test = [
            ".........",
            ".123*....",
            ".123.....",
        ]
        self.assertEqual(star(test), 15129)

    def test_middleright_topright(self):
        test = [
            ".....123.",
            "....*123.",
            ".........",
        ]
        self.assertEqual(star(test), 15129)

    def test_middleright_bottomright(self):
        test = [
            ".........",
            "....*123.",
            ".....123.",
        ]
        self.assertEqual(star(test), 15129)


if __name__ == "__main__":
    unittest.main(exit=False)
