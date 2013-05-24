# -*- coding: utf-8 -*-

import unittest
from field import *

class TestField(unittest.TestCase):

    def setUp(self):
        self.field = Field([
                            [1,  2,  3 ],
                            [4,  5,  6 ],
                            [7,  8,  9 ],
                            [10, 11, 12],
                                         ])
    
    def test1(self):
        """testing the surround() method"""
        self.field.surround()
        self.assertEqual(self.field, [
                                      [None, None, None, None, None],
                                      [None,  1  ,  2  ,  3  , None],
                                      [None,  4  ,  5  ,  6  , None],
                                      [None,  7  ,  8  ,  9  , None],
                                      [None,  10 ,  11 ,  12 , None],
                                      [None, None, None, None, None],
                                                                     ])

    def test2(self):
        """testing the get_inner() method"""
        self.field.surround()
        self.assertEqual(self.field.get_inner(), [
                                                  [1,  2,  3 ],
                                                  [4,  5,  6 ],
                                                  [7,  8,  9 ],
                                                  [10, 11, 12],
                                                               ])
    
    def test3(self):
        """testing the neighbors(x, y) method"""
        self.field.surround()
        self.assertEqual(self.field.neighbors(1, 2), [[4,  5,  6 ],
                                                   [7,  8,  9 ],
                                                   [10, 11, 12]])
        
        self.assertEqual(self.field.neighbors(0, 1), [[None, 1, 2],
                                                   [None, 4, 5],
                                                   [None, 7, 8]])
        
        self.assertEqual(self.field.neighbors(2, 0), [[None, None, None],
                                                   [2,    3,    None],
                                                   [5,    6,    None]])




if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestField)
    unittest.TextTestRunner(verbosity=2).run(suite)
