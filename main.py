import math

import numpy

import render_engine
import pygame
import random
from settings import *

WIDTH = 1024
HEIGHT = 512
FPS = 240

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
gloves = pygame.image.load('rec\\gloves.png').convert_alpha()
gloves = pygame.transform.scale(gloves, (800, 400))
gl1 = pygame.image.load('rec\\glc1.png').convert_alpha()
gl1 = pygame.transform.scale(gl1, (1024, 300))
gl1.set_colorkey(WHITE)
gl2 = pygame.image.load('rec\\gl2.png').convert_alpha()
gl2 = pygame.transform.scale(gl2, (600, 400))
gl2.set_colorkey(WHITE)
gl3 = pygame.image.load('rec\\gl3.png').convert_alpha()
gl3 = pygame.transform.scale(gl3, (1000, 600))
gl3.set_colorkey(WHITE)
sky = pygame.image.load('rec\\sky2.png').convert_alpha()
deagles = [pygame.transform.scale(
    pygame.transform.scale(pygame.image.load(f'rec\\deagle\\{i + 1}.png').convert_alpha(), (200, 100)), (600, 300)) for
           i in range(5)]
deagles[0].set_colorkey(WHITE)
deagles[1].set_colorkey(WHITE)
deagles[2].set_colorkey(WHITE)
deagles[3].set_colorkey(WHITE)
deagles[4].set_colorkey(WHITE)
akrs = [pygame.image.load(f'rec\\akr\\{i + 1}.png').convert_alpha() for
           i in range(3)]
akrs[0].set_colorkey(WHITE)
akrs[1].set_colorkey(WHITE)
akrs[2].set_colorkey(WHITE)
# skys = []
"""for i in range(360):
    try:
        sky2 = pygame.image.load( f'rec\\skys\\sky{i}.png').convert_alpha()
    except:
        sky2 = pygame.transform.rotate(sky, i)
        #pygame.image.save(sky2, f'rec\\skys\\sky{i}.png')
    skys.append(sky2)
    print(i)"""
sound_deagle = pygame.mixer.Sound('rec\\sounds\\shoot\\deagle.ogg')
pygame.mixer.music.load('rec\\sounds\\fone.mp3')
pygame.mixer.music.play(-1)
engine = render_engine.Engine3D()
engine.load_texture(1, 'rec\\brick128.png')
engine.load_texture(2, 'rec\\wood128.png')
engine.load_texture(3, 'rec\\metal128.png')
engine.load_texture(4, 'rec\\scifi128.png')
engine.load_texture(5, 'rec\\door128.png')
engine.load_texture(6, 'rec\\end128.png')
blood = pygame.transform.scale(pygame.image.load('rec\\bloodsplat3_strip15.png').convert_alpha(), (2400, 160))
bloods = [pygame.Surface((160, 160)) for i in range(15)]
for i in range(15):
    bloods[i].set_colorkey(BLACK)
    bloods[i].blit(blood,(i * 160, 0))
stakers = []
stakers.append(engine.load_sprite(0, [f'rec\\sprites\\stalker\\{i + 1}.png' for i in range(4)], 2.5, 14, 0.4, 0.4, 300))
#stakers.append(engine.load_sprite(1, [f'rec\\sprites\\stalker\\{i + 1}.png' for i in range(4)], 1.5, 4, 0.4, 0.4, 300))
#stakers.append(engine.load_sprite(2, [f'rec\\sprites\\stalker\\{i + 1}.png' for i in range(4)], 2.5, 16, 0.4, 0.4, 300))
stalkers_status = [0]
# Цикл игры
running = True
scrn = pygame.Surface((256, 128))
scr = pygame.Surface((1024, 512))
iterat = 0
wearon = 1
scoop1 = 4
scoop2 = 10
scoop_width = 4
shoot_track = 0
sttt1 = 0
START_PAGE = 0
GAME_PAGE = 1
page = START_PAGE
font = pygame.font.SysFont('Consolas', 30)
text_load = font.render('Загружено',1, WHITE)
mission_failed_text = font.render('Миссия провалена', 1, RED)
mission_complete_text = font.render('Мишан комплитэ', 1, GREEN)
mission_failed = False
mission_complete = False
kills = 0
screen.blit(text_load, (0,0))
while running:
    if page == START_PAGE:
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    if not mission_failed:
                        page = GAME_PAGE
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)
        if mission_failed:
            screen.blit(mission_failed_text, (200, 200))
        pygame.display.flip()
    if page == GAME_PAGE:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:

                    if wearon == 1 and shoot_track > 9:
                        shoot_track = 0
                        sound_deagle.play()
                        trace = engine.trace_ray()
                        if trace[2] == 500:
                            engine.sprites[int(trace[2] - 500)][4] -= 50 / trace[0]
                    if wearon == 2 and shoot_track > 47:
                        shoot_track = 0
                        sound_deagle.play()
                        trace = engine.trace_ray()
                        if trace[2] == 500:
                            engine.sprites[int(trace[2] - 500)][4] -= 100 / trace[0]

                    if wearon == 3 and shoot_track > 47:
                        shoot_track = 0
                        screen.blit(gl3, (120, 30))
                        trace = engine.trace_ray()
                        if trace[2] == 500 and trace[0] < 1:
                            engine.sprites[int(trace[2] - 500)][4] -= 50
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    page = START_PAGE
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)
                if event.key == pygame.K_3:
                    wearon = 3
                if event.key == pygame.K_2:
                    wearon = 2
                if event.key == pygame.K_1:
                    wearon = 1
                if event.key == pygame.K_q:
                    print(engine.x, engine.y)
                if event.key == pygame.K_SPACE:
                    if abs(engine.map[int(engine.x)][int(engine.y) + 1]) == DOOR_CODE:
                        engine.map[int(engine.x)][int(engine.y) + 1] = -engine.map[int(engine.x)][int(engine.y) + 1]
                    if abs(engine.map[int(engine.x)][int(engine.y) - 1]) == DOOR_CODE:
                        engine.map[int(engine.x)][int(engine.y) - 1] = -engine.map[int(engine.x)][int(engine.y) - 1]
                    if abs(engine.map[int(engine.x) - 1][int(engine.y)]) == DOOR_CODE:
                        engine.map[int(engine.x) - 1][int(engine.y)] = -engine.map[int(engine.x) - 1][int(engine.y)]
                    if abs(engine.map[int(engine.x) + 1][int(engine.y)]) == DOOR_CODE:
                        engine.map[int(engine.x) + 1][int(engine.y)] = -engine.map[int(engine.x) + 1][int(engine.y)]
        for i in range(len(stakers)):
            if engine.sprites[i][4] > 0:
                x1 = engine.x - engine.sprites[i][0]
                y1 = engine.y - engine.sprites[i][1]
                x1 /=200
                y1 /=200
                if math.sqrt((engine.x - engine.sprites[i][0]) ** 2  + (engine.y - engine.sprites[i][1]) ** 2) < 0.25:
                    mission_failed = True
                    page = START_PAGE
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)
                    screen.blit(mission_failed_text, (200, 200))
                if engine.map[int(engine.sprites[i][0] + x1)][int(engine.sprites[i][1] + y1)]<=0:
                    engine.sprites[i][0] += x1
                    engine.sprites[i][1] += y1
        butt_pressed = pygame.mouse.get_pressed()
        if butt_pressed[0]:
            if wearon == 1 and shoot_track > 9:
                shoot_track = 0
                sound_deagle.play()
                trace = engine.trace_ray()
                if trace[2] == 500:
                    engine.sprites[int(trace[2] - 500)][4] -= 50 / trace[0]
        pressed_keys = pygame.key.get_pressed()
        rel = pygame.mouse.get_rel()
        if pressed_keys[pygame.K_w]:
            engine.fwd(wearon * 0.02)
        if pressed_keys[pygame.K_s]:
            engine.back(wearon * 0.02)
        if pressed_keys[pygame.K_a]:
            engine.left(wearon * 0.02)
        if pressed_keys[pygame.K_d]:
            engine.right(wearon * 0.02)
        engine.rotate_right(rel[0] / 4)
        # Обновление
        for i in range(len(stakers)):
            if engine.sprites[i][4] < 0 and stalkers_status[i] == 0:
                stalkers_status[i] = 1
                sttt1 = 0
                engine.load_sprite(i, [f'rec\\sprites\\stalker_dead\\{i + 1}.png' for i in range(4)], engine.sprites[i][0], engine.sprites[i][1], 0.4, 0.4, -1)
        if sttt1 > 720 and stalkers_status[0] == 1:
            stalkers_status[0] = 0
            engine.load_sprite(i, [f'rec\\sprites\\stalker\\{i + 1}.png' for i in range(4)], random.randint(2,10) / 2,
                               random.randint(25, 38) / 2, 0.4, 0.4, 300)
        # Рендеринг
        screen.fill(BLACK)
        screen.blit(sky, (-int(((engine.angle%360 / 360) * WIDTH * 4)), 0))
        # screen.blit(skys[int(engine.angle)], (WIDTH // 2 - skys[int(engine.angle)].get_rect().centerx, -skys[int(engine.angle)].get_rect().centery))
        engine.render(scrn)
        scr = pygame.transform.scale(scrn, (1024, 512))
        scr.set_colorkey(BLACK)
        screen.blit(scr, (0, 0))


        if wearon == 3:
            if shoot_track < 20:
                screen.blit(gl3, (120, 30))
            elif pressed_keys[pygame.K_w] or pressed_keys[pygame.K_a] or pressed_keys[pygame.K_s] or pressed_keys[pygame.K_d]:
                if iterat % 120 > 60:
                    screen.blit(gl1, (0, 220))
                    #screen.blit(gl3, (120, 30))
                else:
                    screen.blit(gl2, (430, 150))
            else:
                screen.blit(gloves, (120, 200))
        if wearon == 2:
            if shoot_track < 48:
                if shoot_track < 10:
                    pygame.draw.line(screen, (255, 128, 0), (WIDTH // 2, HEIGHT // 2), (700, 360), width = 6)
                screen.blit(deagles[shoot_track // 12 + 1], (360, 220))
                if shoot_track == 47:
                    sound_deagle.stop()
            elif pressed_keys[pygame.K_w] or pressed_keys[pygame.K_a] or pressed_keys[pygame.K_s] or pressed_keys[pygame.K_d]:
                if iterat % 120 > 60:
                    screen.blit(deagles[2], (360, 220))
                else:
                    screen.blit(deagles[1], (360, 220))
            else:
                screen.blit(deagles[0], (360, 220))
        if wearon == 1:
            if shoot_track < 10:
                if shoot_track < 5:
                    pygame.draw.line(screen, (255, 128, 0), (WIDTH // 2, HEIGHT // 2), (700, 360), width=6)
                    screen.blit(akrs[0], (0, 0))
                else:
                    screen.blit(akrs[2], (0, 0))
                if shoot_track == 9:
                    sound_deagle.stop()
            elif pressed_keys[pygame.K_w] or pressed_keys[pygame.K_a] or pressed_keys[pygame.K_s] or pressed_keys[
                pygame.K_d]:
                screen.blit(akrs[1], (0, 0))
            else:
                screen.blit(akrs[1], (0, 0))

        pygame.draw.line(screen, GREEN, (WIDTH // 2 - scoop1, HEIGHT // 2), (WIDTH // 2 - scoop2, HEIGHT // 2),
                         width=scoop_width)
        pygame.draw.line(screen, GREEN, (WIDTH // 2 + scoop1, HEIGHT // 2), (WIDTH // 2 + scoop2, HEIGHT // 2),
                         width=scoop_width)
        pygame.draw.line(screen, GREEN, (WIDTH // 2, HEIGHT // 2 - scoop1), (WIDTH // 2, HEIGHT // 2 - scoop2),
                         width=scoop_width)
        pygame.draw.line(screen, GREEN, (WIDTH // 2, HEIGHT // 2 + scoop1), (WIDTH // 2, HEIGHT // 2 + scoop2),
                         width=scoop_width)
        if shoot_track<15:
            screen.blit(bloods[shoot_track], (WIDTH // 2 -80, HEIGHT // 2 - 80))
        fps = clock.get_fps()
        if iterat % 50 == 0:
            pygame.display.set_caption(f'FotoDOOM - fps:{int(fps)}')
        if stalkers_status[0] == 1:
            sttt1 += 1
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()
        iterat += 1
        shoot_track += 1

pygame.quit()
