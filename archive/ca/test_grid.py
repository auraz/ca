# -*- coding: utf-8 -*-

import unittest
from grid import Grid

class TestGrid(unittest.TestCase):

    def setUp(self):
        self.grid = Grid([
                          [0   , 1   , 2   , 3   , 4   ],
                          [0.5 , 1.4 , 2.3 , 3.2 , 4.1 ],
                          ['a' , 'b' , 'c' , 'd' , 'e' ],
                          [None, []  , ()  , {}  , ''  ],
                          [None, [1] , '23', 4   , 5   ],
                          [5   , 6   , 7   , 8   , 9   ],
                                                         ])
    
    def test1_1(self):
        """testing the  width() method"""
        self.assertEqual(self.grid.width(), 5)

    def test1_2(self):
        """testing the height() method"""
        self.assertEqual(self.grid.height(), 6)
    
    def test2_1(self):
        """testing list features: item access"""
        self.assertEqual(self.grid[4][2], '23')
        self.assertEqual(self.grid[3][0], None)
        self.assertEqual(self.grid[0][4],  4  )
        self.assertEqual(self.grid[5]   , [5, 6, 7, 8, 9])

    def test2_2(self):
        """testing list features: slicing ..."""
        self.assertEqual(self.grid[3:5],
            [
             [None, []  , ()  , {}  , ''  ],
             [None, [1] , '23', 4   , 5   ],
                                            ])
        self.assertEqual(self.grid[2::2],
            [
             ['a' , 'b' , 'c' , 'd' , 'e' ],
             [None, [1] , '23', 4   , 5   ],
                                            ])
        self.assertEqual(self.grid[0][::2], [0, 2, 4])
        self.assertEqual(self.grid[:],   self.grid  )

    def test3_1(self):
        """testing the get_subgrid() method: single cell  ..."""
        self.assertEqual(self.grid.get_subgrid(1, 2), [['b']])
        self.assertEqual(self.grid.get_subgrid(4, 1), [[4.1]])
        self.assertEqual(self.grid.get_subgrid(0, 5), [[ 5 ]])
    
    def test3_2(self):
        """testing the get_subgrid() method: single row.. ..."""
        self.assertEqual(self.grid.get_subgrid(1, 4, 4),
                                       [[[1], '23', 4, 5]])
    
    def test3_3(self):
        """testing the get_subgrid() method: single column..."""
        self.assertEqual(self.grid.get_subgrid(1, 1, 1, 5),
            [
             [1.4],
             ['b'],
             [[ ]],
             [[1]],
             [ 6 ],
                   ])
    
    def test3_4(self):
        """testing the get_subgrid() method: rectangular area"""
        self.assertEqual(self.grid.get_subgrid(1, 2, 3, 4), 
            [
             ['b' , 'c' , 'd' ],
             [[]  , ()  , {}  ],
             [[1] , '23', 4   ],
             [6   , 7   , 8   ],
                                ])

    def test4(self):
        """testing the __str__() method"""
        self.assertEqual(str(self.grid), 
"""[
 [0, 1, 2, 3, 4]
 [0.5, 1.4, 2.3, 3.2, 4.1]
 ['a', 'b', 'c', 'd', 'e']
 [None, [], (), {}, '']
 [None, [1], '23', 4, 5]
 [5, 6, 7, 8, 9]
]"""
)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGrid)
    unittest.TextTestRunner(verbosity=2).run(suite)
