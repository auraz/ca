# -*- coding: UTF-8 -*-

import logging
from logging import debug, info
logging.basicConfig(
    level    = logging.WARNING,
    filename = 'model.log',
    filemode = 'w',
    format   = '%(message)s')


import sys
sys.path.append("..")

from mca.mca import *




class Model4(MCA):
    """������ 4.

        ��������� ���� ������.
        �����, �� ������ ��������:
        1.  ��������� ������� �������� ����� �������, ��� ���� � ��� ������
            ���� �� ������ ���� ������ ��������� � �������.
            ���������� ������ ���� ������� ��������� �������. ���� ��� ����
            ��������� (� ��� ������ ���� ���-�� ����), ����� ��������� � 2.
        2.  �������� ��������� ������� ��� ������� � ������ �� ����������
            ������ 3: ��� �����, ����������� �������� ��� �������.
        ��� ���������� �� ��� ���, ���� ��� ��������� �������� �� ��������
        ��� �����.
        """

    def run(self):
        """������ ������."""

        counter = 0
        while True:
            counter += 1

            self.spawn_a_nucleus()

            nuc = self.nuclei[random.randrange(len(self.nuclei))]
            info("A random nucleus is chosen. x = %s, y = %s, status = %s.", nuc.x, nuc.y, nuc.status)

            nuc.look_around()
            nuc.try_to_grow()

            if len(self.nuclei) == 0:
                info("There are no more nuclei. Stopping the model.")
                info("%s iterations have been carried out.", counter)
                print counter, "iterations have been carried out."
                break

        print "{} nuclei have grown to fibers.".format(len(self.fibers))


    def spawn_a_nucleus(self):
        """�������� ��������� �������.

            ��������� ������� �������� ����� �������. ���� � ��� ������ ����
            �������� ������ ������� ��� �������, �� ����� ������� ����� �������.
            """
        n = self.field_size
        x, y = random.randrange(n), random.randrange(n)
        if self.field[y][x] == 0:
            nuc = Nucleus(x, y, self)
            if nuc.is_anything_near():
                nuc.die()
            else:
                info("A random nucleus is spawned. x = %s, y = %s.", x, y)
                self.report()



if __name__ == '__main__':
    for i in range(10):
        Model4(
            field_size = 100,
            fiber_size =   4,
            gap        =   5).run()
        print