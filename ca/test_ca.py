# -*- coding: utf-8 -*-

import unittest
import init
import field
from ca import *

field = field.Field(init.a)

class TestCellularAutomaton(unittest.TestCase):
    
    def setUp(self):
        self.ca = CellularAutomaton(field, init.average)
    
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
