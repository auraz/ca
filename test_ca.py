# -*- coding: utf-8 -*-

import unittest
import init
import field
from ca import *

field = field.Field(init.a)

class TestCellularAutomaton(unittest.TestCase):
    
    def setUp(self):
        self.ca = CellularAutomaton(field, init.average)
    
    # def test1(self):
    #     """testing the get_field() method ..."""
    #     self.assertEqual(self.ca.get_field(), field)
    
    # def test2(self):
    #     """testing the get_subfield() method."""
    #     self.assertEqual(self.ca.get_field().get_subfield(1, 2), [[9]])
    #     self.assertEqual(self.ca.get_field().get_subfield(1, 0, 4), [[0, 0, 0, 9]])
    #     self.assertEqual(self.ca.get_field().get_subfield(1, 1, 1, 4), [
    #                                                         [0],
    #                                                         [9],
    #                                                         [0],
    #                                                         [0],
    #                                                             ])
    #     self.assertEqual(self.ca.get_field().get_subfield(0, 2, 3, 4), [
    #                                                         [0, 9, 0],
    #                                                         [0, 0, 0],
    #                                                         [9, 0, 0],
    #                                                         [0, 0, 9],
    #                                                                   ])
    #     # Border cases:
    #     self.assertEqual(self.ca.get_field().get_subfield(-1, 2, 7), 
    #                                       [[None, 0, 9, 0, 0, 0, None]])

    #     self.assertEqual(self.ca.get_field().get_subfield(5, -1, 1, 4), [
    #                                                          [None],
    #                                                          [None],
    #                                                          [None],
    #                                                          [None],
    #                                                                 ])
    #     self.assertEqual(self.ca.get_field().get_subfield(-1, 4, 4, 3),
    #                                         [
    #                                          [None,  9  ,  0  ,  0  ],
    #                                          [None,  0  ,  0  ,  9  ],
    #                                          [None, None, None, None],
    #                                                                   ])
    
    # def test3(self):
    #     """testing the get_cell() method  ..."""
    #     self.assertEqual(self.ca.get_cell(0, 0), 0)
    #     self.assertEqual(self.ca.get_cell(1, 2), 9)
    #     self.assertEqual(self.ca.get_cell(2, 5), 9)
    #     self.assertEqual(self.ca.get_cell(-1, -1), None)
    #     self.assertEqual(self.ca.get_cell(5, 3), None)
    
    # def test3(self):
    #     """testing the are_neighbors(x1, y1, x2, y2) method"""
    #     self.assertTrue(self.ca.are_neighbors(5, 7, 5, 7,))
    #     self.assertTrue(self.ca.are_neighbors(4, 6, 4, 5,))
    #     self.assertTrue(self.ca.are_neighbors(2, 8, 1, 9,))
    #     self.assertFalse(self.ca.are_neighbors(4, 1, 7, 6,))
    
    def test1(self):
        """testing the next() method  ... ..."""
        self.ca.next()
        expected = [
                    [0.0, 0.0, 0.0, 1.5, 2.25],
                    [1.5, 1.0, 1.0, 1.0, 1.5],
                    [1.5, 1.0, 1.0, 0.0, 0.0],
                    [3.0, 2.0, 1.0, 0.0, 0.0],
                    [1.5, 2.0, 1.0, 1.0, 0.0],
                    [2.25, 3.0, 1.5, 1.5, 0.0],
                                               ]
        self.assertEqual(self.ca.field.get_inner(), expected)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCellularAutomaton)
    unittest.TextTestRunner(verbosity=2).run(suite)
