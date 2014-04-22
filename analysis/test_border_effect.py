# -*- coding: utf-8 -*-

import unittest
from border_effect import *

class TestBorderEffect(unittest.TestCase):

    def test_non_blank_cells(self):
        g = [
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
        self.assertEqual(non_blank_cells(g, 0), 14)
        self.assertEqual(non_blank_cells(g, 1), 12)
        self.assertEqual(non_blank_cells(g, 2), 10)
        self.assertEqual(non_blank_cells(g, 3),  0)
        self.assertEqual(non_blank_cells(g, 4),  0)



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBorderEffect)
    unittest.TextTestRunner(verbosity=2).run(suite)
