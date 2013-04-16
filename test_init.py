#/usr/bin/env python
# -*- coding: utf-8 -*-

import init
import unittest

class TestInit(unittest.TestCase):
    
    def test1(self):
        # Проверить, что функция перехода возвращает правильное новое значение клетки по заданным соседним.
        # Пусть это будет среднее арифметическое.
        neighbors = [[1, 2, 3],
                     [4, 5, 6],
                     [3, 2, 1]]
        self.assertEqual(init.transition(neighbors), 3.0)

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestInit)
	unittest.TextTestRunner(verbosity=2).run(suite)
