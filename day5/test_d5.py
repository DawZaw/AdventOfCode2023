import unittest

from day_5 import split_range

class TestSplitRange(unittest.TestCase):
    def test_range1_end_before_range2(self):
        range1 = (10, 15)
        range2 = (20, 30)
        self.assertEqual(split_range(range1, range2), [(10, 15)]) 
        
    def test_range1_end_inside_range2(self):
        range1 = (10, 25)
        range2 = (20, 30)
        self.assertEqual(split_range(range1, range2), [(10, 20), (20, 25)]) 
        
    def test_range1_end_after_range2(self):
        range1 = (10, 35)
        range2 = (20, 30)
        self.assertEqual(split_range(range1, range2), [(10, 20), (20, 30), (30, 35)]) 
        
    def test_range1_inside_range2(self):
        range1 = (22, 28)
        range2 = (20, 30)
        self.assertEqual(split_range(range1, range2), [(22, 28)])
        
    def test_range1_start_inside_end_after_range2(self):
        range1 = (25, 35)
        range2 = (20, 30)
        self.assertEqual(split_range(range1, range2), [(25, 30), (30, 35)])
        
    def test_range1_after_range2(self):
        range1 = (35, 40)
        range2 = (20, 30)
        self.assertEqual(split_range(range1, range2), [(35, 40)])

if __name__ == "__main__":
    unittest.main(exit=False)