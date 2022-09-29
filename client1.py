#
import pygame as pg

class menu():

    def __init__(self, color_menu, color_option, x, y, w, h, font, main, options):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pg.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pg.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pg.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = rect.center))

    def update(self, event_list):
        mpos = pg.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.active_option
                    
        return -1

class Button:

    def __init__(self, unactive_color, focus_on_color, pressed_color, x, y, w, h, font, text, text_color):
        self.butt_uc = pg.Surface((w, h))
        self.butt_uc.fill(unactive_color)
        self.butt_fc = pg.Surface((w, h))
        self.butt_fc.fill(focus_on_color)
        self.butt_pc = pg.Surface((w, h))
        self.butt_pc.fill(pressed_color)
        self.text_img = font.render(text, 1, text_color)
        self.rect_text = self.text_img.get_rect()
        
        self.butt_uc.blit(self.text_img, (w // 2 - self.rect_text.centerx, h // 2 - self.rect_text.centery))
        self.butt_fc.blit(self.text_img, (w // 2 - self.rect_text.centerx, h // 2 - self.rect_text.centery))
        self.butt_pc.blit(self.text_img, (w // 2 - self.rect_text.centerx, h // 2 - self.rect_text.centery))
        self.y, self.x, self.w, self.h = y, x, w, h
    def draw(self, surf):
        position = pg.mouse.get_pos()
        if self.x < position[0] < self.x + self.w and self.y < position[1] < self.y + self.h:
            if not pg.mouse.get_pressed()[0]:
                surf.blit(self.butt_fc, (0, 0))
            else:
                surf.blit(self.butt_pc, (0, 0))

        else:
            surf.blit(self.butt_uc, (0, 0))

        
        

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((128, 64))

COLOR_INACTIVE = (0, 200, 0)
COLOR_ACTIVE = (200, 0, 0)
COLOR_LIST_INACTIVE = (255, 100, 100)
COLOR_LIST_ACTIVE = (255, 150, 150)

list1 = menu(
    [COLOR_INACTIVE, COLOR_ACTIVE],
    [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
    48, 5, 80,10, 
    pg.font.SysFont(None, 12), 
    "Difficulty", ["Easy", "Hard"])
list2 = menu(
    [COLOR_INACTIVE, COLOR_ACTIVE],
    [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
    48, 35, 80,10, 
    pg.font.SysFont(None, 12), 
    "Resolution", ["64x128", "128x256"])

exit_button = Button(COLOR_INACTIVE, COLOR_ACTIVE, COLOR_LIST_ACTIVE, 1, 1, 40, 40, pg.font.SysFont(None, 12), 'EXit', (0, 0, 0))
running= True
while running:
    clock.tick(30)

    event_list = pg.event.get()
    for event in event_list:
        if event.type == pg.QUIT:
            running= False

    selected_option = list1.update(event_list)
    if selected_option >= 0:
        list1.main = list1.options[selected_option]
        if selected_option == 0:
            #Пишите здесь код, который будет выполняться, если выбран пункт easy
            print('Easy')
        if selected_option == 1:
            #Пишите здесь код, который будет выполняться, если выбран пункт hard 
            print('Hard')
    selected_option = list2.update(event_list)
    if selected_option >= 0:
        list2.main = list2.options[selected_option]
        if selected_option == 0:
            #Пишите здесь код, который будет выполняться, если выбран пункт easy
            print('64x128')
            list1 = menu(
                [COLOR_INACTIVE, COLOR_ACTIVE],
                [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
                48, 5, 80,10, 
                pg.font.SysFont(None, 12), 
                "Difficulty", ["Easy", "Hard"])
            list2 = menu(
                [COLOR_INACTIVE, COLOR_ACTIVE],
                [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
                48, 35, 80,10, 
                pg.font.SysFont(None, 12), 
                "Resolution", ["64x128", "128x256"])
            exit_button = Button(COLOR_INACTIVE, COLOR_ACTIVE, COLOR_LIST_ACTIVE, 1, 1, 40, 40, pg.font.SysFont(None, 12), 'EXit', (0, 0, 0))
            
            screen = pg.display.set_mode((128, 64))
        if selected_option == 1:
            #Пишите здесь код, который будет выполняться, если выбран пункт hard 
            print('128x256')
            screen = pg.display.set_mode((256, 128))
            list1 = menu(
                [COLOR_INACTIVE, COLOR_ACTIVE],
                [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
                96, 5, 160,20, 
                pg.font.SysFont(None, 24), 
                "Difficulty", ["Easy", "Hard"])
            list2 = menu(
                [COLOR_INACTIVE, COLOR_ACTIVE],
                [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
                96, 65, 160,20, 
                pg.font.SysFont(None, 24), 
                "Resolution", ["64x128", "128x256"])
            exit_button = Button(COLOR_INACTIVE, COLOR_ACTIVE, COLOR_LIST_ACTIVE, 2, 2, 80, 80, pg.font.SysFont(None, 24), 'EXit', (0, 0, 0))
    screen.fill((255, 255, 255))
    list1.draw(screen)
    list2.draw(screen)
    exit_button.draw(screen)
    pg.display.flip()
    
pg.quit()
exit()
