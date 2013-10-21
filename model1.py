"""Это черновик!

Даёт большой output, поэтому лучше перенаправлять его в файл. Как-то так:
python model1.py > out.txt
"""

from nucleus import *
import random

n = 100
fiber_size = 4
gap = 5
ratio = 0.1


# Создаём таблицу n x n, заполненную нулями (что означает отсутствие зародышей)
field = Grid([[0 for i in range(n)] for i in range(n)])
print_field(field)


nuclei = []
fibers = []
while len(nuclei) < ratio * n**2:
    x, y = random.randrange(n), random.randrange(n)
    if field[y][x] == 0:
        nuc = Nucleus(x, y)
        print 'No {}: x = {}, y = {}'.format(len(nuclei), nuc.x, nuc.y)
        field[y][x] = nuc
        nuclei.append(nuc)
print_field(field)


while len(nuclei) > 0:
# for i in range(10):

    # Випадково вибираємо зародок зі списку.
    nuc = nuclei[random.randrange(len(nuclei))]
    print
    print "Nuc chosen.", nuc.__dict__

    # Перевіряємо його мертву зону. Якщо там щось є - зародок вмирає.
    if nuc.status == 'n':
        if is_anything_near(nuc, field, n, gap):
            nuclei.remove(nuc)
            nuc.kill(field)
            print "Nuc killed. There are now {} nuclei and {} fibers. The field looks now like this:".\
                                    format(len(nuclei), len(fibers))
            print_field(field)
            continue
        print "Nothing found in the dead zone, let's the nuc live."
    # Перевіряємо смужки зліва, справа, зверху, знизу.
    # Якщо там щось є, то зародок не може рости у відповідному напрямку.

    xl = nuc.x - nuc.left - gap - 1
    xr = nuc.x + nuc.right + gap + 1
    yu = nuc.y - nuc.up - gap - 1
    yd = nuc.y + nuc.down + gap + 1
    dims = 0
    print "xl = {}, xr = {}, yu = {}, yd = {}".format(xl, xr, yu, yd)

    # left & rigth:
    if nuc.left + nuc.right + 1 == fiber_size:
        can_grow_left = False
        can_grow_right = False
        dims += 1
        print "Already reached the size in x dimension. Can't grow left or right."
    else:
        print "Not reached the size in x dimension yet."
        if xl < 0:
            print "Near the left border."
            if nuc.x - nuc.left == 0:
                can_grow_left = False
            else:
                can_grow_left = True
            print "Can grow left:", can_grow_left
        else:
            can_grow_left = True
            print "Checking for y in range({}, {})".format(max(yu + 1, 0), min(yd, n))
            for y in range(max(yu + 1, 0), min(yd, n)):
                print field[y][xl]
                if field[y][xl] != 0:
                    can_grow_left = False
                    print "Something found on the left. Can't grow left."
                    break
            # print "The way left is clear. Can grow left."
        if xr > n - 1:
            print "Near the right border."
            if nuc.x + nuc.right == n - 1:
                can_grow_right = False
            else:
                can_grow_right = True
            print "Can grow right:", can_grow_right
        else:
            can_grow_right = True
            print "Checking for y in range({}, {})".format(max(yu + 1, 0), min(yd, n))
            for y in range(max(yu + 1, 0), min(yd, n)):
                print field[y][xr]
                if field[y][xr] != 0:
                    can_grow_right = False
                    print "Something found on the right. Can't grow right."
                    break
            # print "The way right is clear. Can grow right."

    # up & down
    # print "Figuring out if it can grow up or down."
    if nuc.up + nuc.down + 1 == fiber_size:
        can_grow_up = False
        can_grow_down = False
        dims += 1
        print "Already reached the size in y dimension. Can't grow up or down."
    else:
        print "Not reached the size in y dimension yet."
        if yu < 0:
            print "Near the top border."
            if nuc.y - nuc.up == 0:
                can_grow_up = False
            else:
                can_grow_up = True
            print "Can grow up:", can_grow_up
        else:
            can_grow_up = True
            print "Checking for x in range({}, {})".format(max(xl + 1, 0), min(xr, n))
            for x in range(max(xl + 1, 0), min(xr, n)):
                print field[yu][x],
                if field[yu][x] != 0:
                    can_grow_up = False
                    print "Something found on the up. Can't grow up."
                    break
            # print "The way up is clear. Can grow up."
        if yd > n - 1:
            print "Near the bottom border."
            if nuc.y + nuc.down == n - 1:
                can_grow_down = False
            else:
                can_grow_down = True
            print "Can grow down:", can_grow_down
        else:
            can_grow_down = True
            print "Checking for x in range({}, {})".format(max(xl + 1, 0), min(xr, n))
            for x in range(max(xl + 1, 0), min(xr, n)):
                print field[yd][x],
                if field[yd][x] != 0:
                    can_grow_down = False
                    print "Something found on the down. Can't grow down."
                    break
            # print "The way down is clear. Can grow down."

    if dims == 2:
        nuclei.remove(nuc)
        fibers.append(nuc)
        nuc.status = 'f'
        print "*/Reached nirvana!!! Congrats. There are now {} nuclei and {} fibers.".format(len(nuclei), len(fibers))
    elif not (can_grow_left or can_grow_right or can_grow_up or can_grow_down):
        print "*/Sorry guy... You can't grow so you'll dye."
        nuclei.remove(nuc)
        nuc.kill(field)
        print "There are now {} nuclei and {} fibers".format(len(nuclei), len(fibers))
        print "Now the field looks now like this:"
        print_field(field)
    else:
        choices = [can_grow_left, can_grow_right, can_grow_up, can_grow_down]
        directions = [nuc.grow_to_left, nuc.grow_to_right, nuc.grow_to_up, nuc.grow_to_down]
        can_grow = [directions[i] for i in range(4) if choices[i]]
        grow_to = random.choice(can_grow)
        if can_grow_left:
            print 'Can grow left.'
        if can_grow_right:
            print 'Can grow right.'
        if can_grow_up:
            print 'Can grow up.'
        if can_grow_down:
            print 'Can grow down.'
        print "choices = {}, grow_to = {}, let's grow.".format(choices, grow_to)
        grow_to(field)
        nuc.status = 'g'
        print "Now the field looks now like this:"
        print_field(field)




print "There are now {} nuclei and {} fibers".format(len(nuclei), len(fibers))

