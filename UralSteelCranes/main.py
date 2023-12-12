import json
import os
import time
import pygame
from Cranes import Crane


def load_image(name, size_of_sprite=None, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if size_of_sprite:
        image = pygame.transform.scale(image, (size_of_sprite[0], size_of_sprite[1]))
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def generate_map(y):
    field = list()
    y = y
    for i in range(7):
        row = list()
        x = 18
        for j in range(61):
            row.append((x, y, j, i))
            if (j - 2) % 7 == 0:
                x += 19
            else:
                x += 18
        y += 18
        field.append(row)
    return field


class Hook:
    def __init__(self, crane):
        self.crane = crane
        self.flag = False
        self.hook_img = load_image('hook.png', color_key=-1)
        self.pos = [470, 100]
        self.laddle_img = load_image('laddle.jpg', color_key=-1)
        if not crane.laddle:
            self.pos_2 = [400, 140]
            self.move = True
        else:
            self.pos_2 = [400, 700]
            self.move = False

        self.cycle()

    def update_window(self):
        screen.fill('white')
        pygame.draw.rect(screen, 'yellow', (50, 5, 1036, 60))
        pygame.draw.circle(screen, 'black', (40, 35), 40)
        pygame.draw.circle(screen, 'black', (1086, 35), 40)
        screen.blit(self.hook_img, self.pos)
        pygame.draw.line(screen, 'gray', (543, 0), (543, self.pos[1] + 2), 40)
        pygame.draw.rect(screen, 'black', (473, 0, 140, 70))
        screen.blit(self.laddle_img, self.pos_2)

        pygame.draw.rect(screen, 'blue', (10, 100, 100, 20), 4)

    def cycle(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if self.pos[0] <= pos[0] <= self.pos[0] + 164 and self.pos[1] <= pos[1] <= \
                            self.pos[1] + 227:
                        self.flag = True
                    elif 10 <= pos[0] <= 110 and 100 <= pos[1] <= 120:
                        return

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.flag = False
                elif event.type == pygame.MOUSEMOTION and self.flag:
                    pos = event.pos
                    self.pos[1] = pos[1]
                    if self.move:
                        self.pos_2[1] = pos[1] + 40

            if self.move and not self.crane.laddle and self.pos_2[1] == 700:
                self.move = False
                self.pos_2[1] += 20
            elif self.pos[1] == self.pos_2[1] - 40:
                self.move = True


            self.update_window()
            pygame.display.flip()
            clock.tick(FPS)


FPS = 60
drag = False
pygame.init()
clock = pygame.time.Clock()
SIZE = WIDTH, HEIGHT = 1126, 950
screen = pygame.display.set_mode(SIZE)
font = pygame.font.SysFont('Arialms', 24)

workshop = load_image('workshop.png')
field_7 = generate_map(76)
field_8 = generate_map(311)
field_9 = generate_map(546)
field_10 = generate_map(781)

crane_7 = Crane([18, 63], [7, 127], 7)
shadow_7 = Crane([18, 63], [7, 127], 7, True)
crane_8 = Crane([250, 298], [7, 127], 8)
shadow_8 = Crane([250, 298], [7, 127], 8, True)
crane_9 = Crane([650, 533], [7, 127], 9)
shadow_9 = Crane([650, 533], [7, 127], 9, True)
crane_10 = Crane([1080, 768], [7, 127], 10)
shadow_10 = Crane([1080, 768], [7, 127], 10, True)
cranes = (crane_7, crane_8, crane_9, crane_10)
shadows = (shadow_7, shadow_8, shadow_9, shadow_10)

aggregates = {'кп1а': (3, 3), 'кп2а': (7, 3), 'мнлз2': (19, 5), 'мнлз1': (31, 5), 'ск2': (33, 2),
              'ск1': (47, 2), 'вк2': (40, 3), 'вк1': (44, 3), 'кп2б': (55, 2), 'л1': (36, 2),
              'л2': (30, 1)}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for crane in cranes:
                if crane.cords[1] <= pos[1] <= crane.cords[1] + 127 and \
                        crane.cords[0] <= pos[0] <= crane.cords[0] + 18:
                    crane.get_dragged()
            for i in range(4):
                if 900 <= pos[0] <= 1126 and 10 + 235 * i <= pos[1] <= 42 + 235 * i:
                    cranes[i].laddle = not cranes[i].laddle
                    a = Hook(cranes[i])
        elif event.type == pygame.MOUSEBUTTONUP:
            for i in range(4):
                cranes[i].get_dragged(False, eval(f'field_{cranes[i].number}'))
        elif event.type == pygame.MOUSEMOTION:
            for crane in cranes:
                if crane.dragged:
                    rel = event.rel
                    pos = event.pos
                    crane.drag_n_drop(rel, pos)

    # движение тени
    flag = False
    for i in range(4):
        pos = cranes[i].get_pos()
        if pos != shadows[i].get_pos() or cranes[i].laddle != shadows[i].laddle:
            shadows[i].laddle = cranes[i].laddle
            shadows[i].move(*pos, eval(f'field_{cranes[i].number}'))
            with open(f'K:/python/python/uralsteel/uralsteel/visual/static/visual/jsons/crane_{cranes[i].number}.json', 'w', encoding='utf-8') as f:
                json.dump({cranes[i].number: [shadows[i].get_pos(), cranes[i].laddle]}, f)
            flag = True
    if flag:
        time.sleep(0.5)

    # цех и краны
    screen.fill('white')
    for i in range(4):
        screen.blit(workshop, (0, 50 + i * 235))
        crane_condition = font.render(f'Координаты крана {7 + i}:', True, 'black')
        screen.blit(crane_condition, (10, 10 + 235 * i))
        cranes[i].show(screen)
        shadows[i].show(screen)

    # Координаты
    for i in range(4):
        crane_cords = font.render(str(shadows[i].get_pos()), True, 'black')
        screen.blit(crane_cords, (255, 10 + 235 * i))

    # Окно работы с крюком
    for i in range(4):
        pos = shadows[i].get_pos()
        if pos == cranes[i].get_pos() and tuple(pos) in aggregates.values():
            if cranes[i].laddle:
                text = font.render('Поставить ковш', True, 'black')
                x, width = 900, 181
            else:
                text = font.render('Взять ковш', True, 'black')
                x, width = 949, 130
            screen.blit(text, (x + 1, 10 + 235 * i))
            pygame.draw.rect(screen, 'blue', (x, 10 + 235 * i, width, 32), 3)

    pygame.display.flip()
    clock.tick(FPS)
