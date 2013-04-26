# -*- coding: utf-8 -*-

import unittest
from field import *

class TestField(unittest.TestCase):

    def setUp(self):
        self.field = Field([
							[0   , 1   , 2   , 3   , 4   ],
							[0.5 , 1.4 , 2.3 , 3.2 , 4.1 ],
							['a' , 'b' , 'c' , 'd' , 'e' ],
							[None, []  , ()  , {}  , ''  ],
							[None, [1] , '23', 4   , 5   ],
							[5   , 6   , 7   , 8   , 9   ],
							                               ])
    
    def test1(self):
    	"""testing list features: item access"""
    	self.assertEqual(self.field[4][2], '23')
    	self.assertEqual(self.field[3][0], None)
    	self.assertEqual(self.field[0][4],  4  )
    	self.assertEqual(self.field[5]   , [5, 6, 7, 8, 9])

    def test2(self):
    	"""testing list features: slicing"""
    	self.assertEqual(self.field[3:5],
    		[
			 [None, []  , ()  , {}  , ''  ],
			 [None, [1] , '23', 4   , 5   ],
										    ])
    	self.assertEqual(self.field[2::2],
    		[
			 ['a' , 'b' , 'c' , 'd' , 'e' ],
			 [None, [1] , '23', 4   , 5   ],
										    ])
    	self.assertEqual(self.field[0][::2], [0, 2, 4])
    	self.assertEqual(self.field[:],   self.field  )

    def test3(self):
        """testing the get_subfield() method: single cell  ..."""
        self.assertEqual(self.field.get_subfield(1, 2), [['b']])
        self.assertEqual(self.field.get_subfield(4, 1), [[4.1]])
        self.assertEqual(self.field.get_subfield(0, 5), [[ 5 ]])
    
    def test4(self):
        """testing the get_subfield() method: single row.. ..."""
        self.assertEqual(self.field.get_subfield(1, 4, 4),
        	           				   [[[1], '23', 4, 5]])
    
    def test5(self):
        """testing the get_subfield() method: single column..."""
        self.assertEqual(self.field.get_subfield(1, 1, 1, 5),
        	[
             [1.4],
             ['b'],
             [[ ]],
             [[1]],
             [ 6 ],
                   ])
    
    def test6(self):
        """testing the get_subfield() method: rectangular area"""
        self.assertEqual(self.field.get_subfield(1, 2, 3, 4), 
        	[
			 ['b' , 'c' , 'd' ],
			 [[]  , ()  , {}  ],
			 [[1] , '23', 4   ],
			 [6   , 7   , 8   ],
                                ])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestField)
    unittest.TextTestRunner(verbosity=2).run(suite)
