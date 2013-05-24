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

    def test2(self):
        """testing sum(neighbors)"""
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
        self.assertEqual(init.sum(neighbors), 27)
        self.assertEqual(init.sum(neighbors_border_case), 21)
        self.assertEqual(init.sum(neighbors_corner_case), 10)

    def test3_1(self):
        """Testing life(neighbors): Any live cell with fewer than two live neighbours dies, as if caused by under-population."""
        neighbors1 = [
                      [0, 0, 0],
                      [0, 1, 0],
                      [0, 0, 0],
                                ]
        neighbors2 = [
                      [0, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1],
                                ]
        neighbors3 = [
                      [0, 1, None],
                      [0, 1, None],
                      [0, 0, None],
                                   ]
        self.assertEqual(init.life(neighbors1), 0)
        self.assertEqual(init.life(neighbors2), 0)
        self.assertEqual(init.life(neighbors3), 0)

    def test3_2(self):
        """Testing life(neighbors): Any live cell with two or three live neighbours lives on to the next generation."""
        neighbors1 = [
                      [0, 0, 1],
                      [1, 1, 0],
                      [0, 0, 0],
                                ]
        neighbors2 = [
                      [0, 0, 0],
                      [0, 1, 0],
                      [1, 1, 1],
                                ]
        neighbors3 = [
                      [0, 1, None],
                      [1, 1, None],
                      [0, 0, None],
                                   ]
        neighbors4 = [
                      [None, None, None],
                      [ 1  ,  1  , None],
                      [ 1  ,  1  , None],
                                         ]
        self.assertEqual(init.life(neighbors1), 1)
        self.assertEqual(init.life(neighbors2), 1)
        self.assertEqual(init.life(neighbors3), 1)
        self.assertEqual(init.life(neighbors4), 1)

    def test3_3(self):
        """Testing life(neighbors): Any live cell with more than three live neighbours dies, as if by overcrowding."""
        neighbors1 = [
                      [1, 1, 1],
                      [1, 1, 1],
                      [1, 1, 1],
                                ]
        neighbors2 = [
                      [1, 0, 1],
                      [0, 1, 0],
                      [0, 1, 1],
                                ]
        neighbors3 = [
                      [ 1  ,  1  , None],
                      [ 1  ,  1  , None],
                      [ 1  ,  1  , None],
                                         ]
        self.assertEqual(init.life(neighbors1), 0)
        self.assertEqual(init.life(neighbors2), 0)
        self.assertEqual(init.life(neighbors3), 0)


    def test3_4(self):
        """Testing life(neighbors): Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction."""
        neighbors1 = [
                      [1, 1, 1],
                      [0, 0, 0],
                      [0, 0, 0],
                                ]
        neighbors2 = [
                      [0, 0, 0],
                      [0, 0, 1],
                      [1, 0, 1],
                                ]
        neighbors3 = [
                      [ 1  ,  1  , None],
                      [ 1  ,  0  , None],
                      [None, None, None],
                                         ]
        self.assertEqual(init.life(neighbors1), 1)
        self.assertEqual(init.life(neighbors2), 1)
        self.assertEqual(init.life(neighbors3), 1)

    def test3_5(self):
        """Testing life(neighbors): Any dead cell with other than three live neighbours remains dead."""
        neighbors1 = [
                      [0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0],
                                ]
        neighbors2 = [
                      [0, 0, 0],
                      [0, 0, 0],
                      [0, 1, 0],
                                ]
        neighbors3 = [
                      [0, 0, 1],
                      [0, 0, 1],
                      [1, 0, 1],
                                ]
        neighbors4 = [
                      [1, 1, 1],
                      [1, 0, 1],
                      [1, 1, 1],
                                ]
        neighbors5 = [
                      [None,  1  ,  1  ],
                      [None,  0  ,  0  ],
                      [None,  0  ,  0  ],
                                         ]
        self.assertEqual(init.life(neighbors1), 0)
        self.assertEqual(init.life(neighbors2), 0)
        self.assertEqual(init.life(neighbors3), 0)
        self.assertEqual(init.life(neighbors4), 0)
        self.assertEqual(init.life(neighbors5), 0)






if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInit)
    unittest.TextTestRunner(verbosity=2).run(suite)
