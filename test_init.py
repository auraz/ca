#/usr/bin/env python
# -*- coding: utf-8 -*-

import init
import unittest

class TestInit(unittest.TestCase):
    
    def test1(self):
        """testing average(neighbors)"""
        neighbors = [
                     [1, 2, 3],
                     [4, 5, 6],
                     [3, 2, 1],
                               ]
        neighbors_border_case = [
                                 [1, 2, None],
                                 [3, 4, None],
                                 [5, 6, None],
                                              ]
        neighbors_corner_case = [
                                 [None,  1  ,  2  ],
                                 [None,  3  ,  4  ],
                                 [None, None, None],
                                                    ]
        self.assertEqual(init.average(neighbors), 3.0)
        self.assertEqual(init.average(neighbors_border_case), 3.5)
        self.assertEqual(init.average(neighbors_corner_case), 2.5)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInit)
    unittest.TextTestRunner(verbosity=2).run(suite)
