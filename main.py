import pygame
import Runner.MyRunner.methods as methods
import os, sys
import pygame.display
from pygame.locals import *
import random
from abc import ABCMeta, abstractclassmethod


# Абстрактные и родительские классы

class GameState:
    __metaclass__ = ABCMeta
    #asd
    @abstractclassmethod
    def update(self):
        """ Обновление """

    @abstractclassmethod
    def render(self):
        """Рендер текущего состояния"""


class Object:
    __metaclass__ = ABCMeta

    @abstractclassmethod
    def get_surface(self):
        """"""

    @abstractclassmethod
    def get_rect(self):
        """"""

    @abstractclassmethod
    def get_position(self):
        """"""

# Все что выше меня устраивает

class Menu(GameState):
    spriteList = []
    menu_state = {"Start": True, "First Time": True}

    def __init__(self):
        self.background = ImgObj('img/menu-bg.jpg', 800, 600)
        self.start_btn = ImgObj('img/Start-selected.png', 0, 0)
        self.start_btn.set_position(75, 200)
        self.exit_btn = ImgObj('img/Exit.png', 0, 0)
        self.exit_btn.set_position(75, 300)
        self.spriteList.append((self.background, self.background.position))
        self.spriteList.append((self.start_btn, self.start_btn.position))
        self.spriteList.append((self.exit_btn, self.exit_btn.position))

    def update(self):
        self.listener()
        if self.menu_state["Start"]:
            self.spriteList[1][0].set_image("img/Start-selected.png")
            self.spriteList[2][0].set_image("img/Exit.png")
        else:
            self.spriteList[1][0].set_image("img/Start.png")
            self.spriteList[2][0].set_image("img/Exit_selected.png")

    def listener(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit(0)
                if event.key == K_DOWN or event.key == K_s or event.key == K_UP or event.key == K_w:
                    self.menu_state["Start"] = not self.menu_state["Start"]
                if event.key == K_RETURN or event.key == K_SPACE:
                    if self.menu_state["Start"]:
                        State.set_state(Game())
                    else:
                        exit(0)
            elif event.type == QUIT:
                exit(0)

    def render(self):
        pass


class State:
    current_state = Menu()

    @staticmethod
    def init():
        pygame.init()
        State.set_state(Menu)
        State.screen = pygame.display.set_mode((800, 600))

    @staticmethod
    def get_state():
        return State.current_state

    @staticmethod
    def set_state(state):
        State.current_state = state
        State.update()

    @staticmethod
    def update():
        State.get_state().update()

    @staticmethod
    def render():
        State.get_state().render()
        pygame.display.flip()


class Game(GameState):

    def __init__(self):
        Game.game_background = ImgObj("img/game_bg.png", State.width, State.height)
        Game.all_sprites = []
        Game.hero = Player()
        Game.enemy = Enemy()
        Game.all_sprites.append((Game.game_background, Game.game_background.position))
        Game.all_sprites.append((Game.hero, Game.hero.position))
        Game.all_sprites.append((Game.enemy, Game.enemy.position))

    @staticmethod
    def update():
        for each in Game.all_sprites:
            each.update()

    @staticmethod
    def get_sprite_group():
        return Game.all_sprites


def main():
    State.init()

    while True:
        State.update()
        State.render()


class ImgObj(pygame.sprite.Sprite):
    def __init__(self, img, width, height):
        super(ImgObj, self).__init__()
        self.image = pygame.image.load(img)
        if width and height != 0:
            self.image = pygame.transform.smoothscale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.position = (0, 0)

    def set_position(self, offset_top, offset_left):
        self.position = (offset_top, offset_left)

    def move(self, offset_top, offset_left):
        self.rect.move(offset_top, offset_left)

    def set_image(self, img):
        self.image = pygame.image.load(img)
        pass


class Player(ImgObj):
    def __init__(self):
        super(Player, self).__init__("img/hero.jpg", 75, 75)
        self.rect = self.image.get_rect()
        self.position = (150, 300)
        self.jmp = False  # in air
        self.grounded = True  # in ground

    def listener(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit(0)
                if event.key == K_UP:
                    if not self.jmp and self.grounded:
                        self.jmp = True
                        self.grounded = False
                if self.jmp:
                    self.rect.move_ip(0, -14)
                    if self.rect.top < 250:
                        self.jmp = False
                self.rect.move_ip(0, 7)
                if self.rect.bottom > 550:
                    self.jmp = False
                    self.rect.bottom = 550
                    self.grounded = True
            elif event.type == QUIT:
                exit(0)

    def update(self):
        self.listener()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load('img/hero.jpg')
        self.image = pygame.transform.smoothscale(self.image, (175, 75))
        self.image.set_colorkey(None)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(850, 470)
        self.position = (500, 500)

    def update(self):
        self.position = (self.position[0] - 10, self.position[1])
        if self.rect.left < -50:
            self.kill()


class FlyingEnemy(Enemy):
    def __init__(self):
        self.image = pygame.image.load('plane.png')
        self.image = pygame.transform.smoothscale(self.image, (125, 125))
        # self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(800, random.randrange(50, 400))


if __name__ == '__main__':
    main()

"""

def menu(menu_state, all):
    menu_state = menu_listener(menu_state)
    if menu_state == 0:

    else:
        start_button = ImgObj('img/Start.png', 0, 0)

    all.append(start_button)
    return menu_state


def menu_listener(menu_state):
    global running

    return menu_state


def main():
    State.init()
    print(State.get_state())
    global running
    pygame.init()
    screen = Screen
    all_sprites = []
    enemies_sprites = pygame.sprite.Group()

    state = "Menu"
    menu_state = 0
    # background = pygame.Surface(screen.get_size())

    counter = 0

    # game loop
    while running:
        if state == "Menu":  #
            menu_state = menu(menu_state, all_sprites)

        elif state == "Game":
            counter += 1

        render(screen, all_sprites)

      
        
        start = time.time()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        screen.blit(background, (0, 0))

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        if random.randrange(0, 5000) > 4000:
            if random.randrange(1, 3) == 1:
                asv = Enemy()
                enemies_sprites.add(asv)
                all_sprites.add(asv)
                counter = 0
            else:
                asv = FlyingEnemy()
                enemies_sprites.add(asv)
                all_sprites.add(asv)
                counter = 0

        for one in enemies_sprites:
            one.update()

        
        scoreboard = pygame.font.Font(None, 60)
        scoreboard.set_bold(True)
        text = scoreboard.render(str(score), True, (255, 255, 255))
        screen.blit(text, (350, 50))

        finish = time.time()
        time.sleep(max(0, 0.01666666 - (finish - start)))

        if pygame.sprite.spritecollideany(player, enemies_sprites):
            player.kill()
            pygame.font.init()

            gameover = pygame.font.Font(None, 60)
            gameover.set_bold(True)
            text = gameover.render("YOU SOCUK", True, (255, 255, 255))
            screen.blit(text, (200, 200))
            pygame.display.flip()
            time.sleep(2)
            break
        pygame.display.flip()
        """
