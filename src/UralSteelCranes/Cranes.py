import pygame


class Crane:
    def __init__(self, cords, size, number, shadow=False):
        self.number = number
        self.cords = cords
        self.size = size
        self.hook = [cords[0] + size[0] // 2, cords[1] + size[1] // 2]
        self.dragged = False
        self.pos = [0, 0]
        self.shadow = shadow
        self.laddle = False

    def drag_n_drop(self, rel, pos):
        self.cords[0] += rel[0]
        self.hook = [self.cords[0] + self.size[0] // 2, pos[1]]

    def set_pos(self, field):
        for row in field:
            for col in row:
                if abs(self.cords[0] - col[0]) <= 9 and abs(self.hook[1] - col[1]) <= 9:
                    self.pos = [col[2], col[3]]
                    self.cords[0] = col[0] - 3
                    self.hook = [self.cords[0] + self.size[0] // 2, col[1]]
                    return

    def show(self, screen):
        if self.shadow:
            pygame.draw.circle(screen, pygame.Color('green'), self.hook, 5)
        elif self.laddle:
            pygame.draw.rect(screen, pygame.Color('Blue'), self.cords + self.size)
            pygame.draw.circle(screen, pygame.Color('red'), self.hook, 10)
        else:
            pygame.draw.rect(screen, pygame.Color('Blue'), self.cords + self.size)
            pygame.draw.circle(screen, pygame.Color('Blue'), self.hook, 10)

    def move(self, x, y, field):
        if x == self.pos[0]:
            pass
        elif x > self.pos[0]:
            self.pos[0] += 1
            self.cords[0] += 18
        else:
            self.pos[0] -= 1
            self.cords[0] -= 18
        if y == self.pos[1]:
            pass
        elif y > self.pos[1]:
            self.pos[1] += 1
            self.hook[1] += 18
        else:
            self.pos[1] -= 1
            self.hook[1] -= 18
        self.set_pos(field)

    def get_dragged(self, flag=True, field=None):
        self.dragged = flag
        if not flag:
            self.set_pos(field)

    def get_pos(self):
        return self.pos
