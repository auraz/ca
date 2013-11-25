# -*- coding: UTF-8 -*-

from model4 import *

class Model5(Model4):
    """Модель 5.

        Сначала полностью выполняем Модель 4.
        После этого проходимся по всему полю и дополнительно засеваем зародыши
        там, где это возможно (чтобы у каждого была пустая мёртвая зона),
        то есть в больших порах.
        Далее они все пытаются расти и сформировать дополнительные волокна.
        """

    def run(self):
        """Запуск модели."""
        
        Model4.run(self)
        
        n = self.field_size
        for x in range(n):
            for y in range(n):
                if self.field[y][x] == 0:
                    nuc = Nucleus(x, y, self)
                    if nuc.is_anything_near():
                        nuc.die()
        print len(self.nuclei), "additional nuclei have been spawned."

        while len(self.nuclei) > 0:
            nuc = self.nuclei[random.randrange(len(self.nuclei))]
            info("A random nucleus is chosen. x = %s, y = %s, status = %s.", nuc.x, nuc.y, nuc.status)

            if nuc.status == 'n' and nuc.is_anything_near():
                nuc.die()
                continue
            
            nuc.look_around()
            nuc.try_to_grow()
        
        print len(self.fibers), "nuclei have grown to fibers."



if __name__ == '__main__':
    for i in range(10):
        Model5(
            field_size = 100,
            fiber_size =   4,
            gap        =   5).run()
        print