# -*- coding: utf-8 -*-

import unittest
from border_effect import *

class TestBorderEffect(unittest.TestCase):

    def setUp(self):
        self.grid = [
                     [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],    # ..ooo.....
                     [0, 0, 1, 2, 1, 0, 0, 0, 0, 0],    # ..o#o.....
                     [0, 0, 1, 1, 1, 0, 0, 1, 1, 1],    # ..ooo..ooo
                     [0, 0, 0, 0, 0, 0, 0, 1, 2, 1],    # .......o#o
                     [0, 0, 0, 0, 0, 0, 0, 1, 1, 1],    # .......ooo
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # ..........
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # ..........
                     [1, 1, 1, 0, 0, 1, 1, 1, 0, 0],    # ooo..ooo..
                     [1, 1, 1, 0, 0, 1, 2, 1, 0, 0],    # ooo..o#o..
                     [1, 2, 1, 0, 0, 1, 1, 1, 0, 0],    # o#o..ooo..
                                                    ]
    def test_non_blank_cells(self):
        self.assertEqual(non_blank_cells(self.grid, 0), 14)
        self.assertEqual(non_blank_cells(self.grid, 1), 12)
        self.assertEqual(non_blank_cells(self.grid, 2), 10)
        self.assertEqual(non_blank_cells(self.grid, 3),  0)
        self.assertEqual(non_blank_cells(self.grid, 4),  0)

    def test_non_blank_concentration(self):
        self.assertAlmostEqual(non_blank_concentration(self.grid, 0), 14/36.0)
        self.assertAlmostEqual(non_blank_concentration(self.grid, 1), 12/28.0)
        self.assertAlmostEqual(non_blank_concentration(self.grid, 2), 0.5)
        self.assertAlmostEqual(non_blank_concentration(self.grid, 3), 0)
        self.assertAlmostEqual(non_blank_concentration(self.grid, 4), 0)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBorderEffect)
    unittest.TextTestRunner(verbosity=2).run(suite)
