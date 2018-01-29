import pygame
import pygame.display
from pygame.locals import *
import random
import methods
import time


class ImgObj(pygame.sprite.Sprite):
    def __init__(self, img_path, colorkey=None, scale=None, position=None):
        super(ImgObj, self).__init__()
        self.surface, self.rect = methods.load_image(img_path, colorkey, scale, position)
        if position is not None:
            self.rect.move(position)

        self.acceleration_x = 0
        self.acceleration_y = 0
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self):
        self.velocity_x += self.acceleration_x
        self.velocity_y += self.acceleration_y
        self.rect.move_ip(self.velocity_x, self.velocity_y)

    def updater(self):
        pass


class State:
    current_state = True
    screen = pygame.display.set_mode((800, 600))

    @staticmethod
    def init():
        pygame.init()
        State.current_state = Menu()
        State.screen = pygame.display.set_mode((800, 600))

    @staticmethod
    def set_state(state):
        State.current_state = state
        State.update()

    @staticmethod
    def update():
        State.current_state.update()

    @staticmethod
    def render():
        State.screen.fill((0, 0, 0))
        State.current_state.render()
        pygame.display.flip()


class Menu:
    sprite_list = []
    menu_state = {"Start": True, "First Time": True}

    def __init__(self):
        self.background = ImgObj('img/Menu/menu-bg.jpg', scale=(800, 600))
        self.start_btn = ImgObj('img/Menu/Start-selected.png', position=(75, 200))
        self.exit_btn = ImgObj('img/Menu/Exit.png', position=(75, 300))
        self.sprite_list.append(self.background)
        self.sprite_list.append(self.start_btn)
        self.sprite_list.append(self.exit_btn)

    def update(self):
        self.listener()
        if self.menu_state["Start"]:
            self.start_btn.surface, self.start_btn.rect = methods.load_image("img/Menu/Start-selected.png",
                                                                             position=(75, 200))
            self.exit_btn.surface, self.exit_btn.rect = methods.load_image("img/Menu/Exit.png", position=(75, 300))
        else:
            self.start_btn.surface, self.start_btn.rect = methods.load_image("img/Menu/Start.png", position=(75, 200))
            self.exit_btn.surface, self.exit_btn.rect = methods.load_image("img/Menu/Exit_selected.png",
                                                                           position=(75, 300))

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
        for sprite in self.sprite_list:
            State.screen.blit(sprite.surface, sprite.rect)


class Game:
    sprite_list = []

    def __init__(self):
        self.game_background = ImgObj("img/Game/game_bg.png", scale=(952, 600))
        self.hero = Player()
        self.hero.rect.move(50, 450)
        # self.enemy = Enemy()
        self.sprite_list.append(self.game_background)
        self.sprite_list.append(self.hero)
        # self.all_sprites.append(self.enemy)

    def update(self):
        for sprite in self.sprite_list:
            sprite.updater()

    def render(self):
        for sprite in self.sprite_list:
            State.screen.blit(sprite.surface, sprite.rect)


def main():
    State.init()
    while True:
        start = time.time()
        State.update()
        State.render()
        finish = time.time()
        time.sleep(max(0, 0.01666666 - (finish - start)))


# Все что выше меня устраивает

class Player(ImgObj):
    def __init__(self):
        super(Player, self).__init__("img/Game/Hero/Run/1.png", scale=(75, 75), position=(-150, 450), colorkey=-1)
        self.jmp = False  # in air
        self.grounded = True  # in ground
        self.acceleration_y = 1
        self.velocity_x = 2
        self.run_sprites = []
        for i in range(1, 8):
            self.run_sprites.append(
                (methods.load_image("img/Game/Hero/Run/" + str(i) + ".png", colorkey=-1, scale=1)))
        self.animations = 0

    def updater(self):
        self.listener()
        if self.rect.left >= 100:
            self.rect.left = 100
            self.velocity_x = 0
        if self.grounded:
            self.surface, dontchange = self.run_sprites[self.animations//5]
            self.animations += 1
            self.animations = self.animations % 35
            self.acceleration_y = 0
            self.velocity_y = 0
        if self.rect.bottom > 530:
            self.jmp = False
            self.grounded = True
            self.animations = 0
            self.rect.bottom = 530
            self.velocity_y = 0
        self.update()

    def listener(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit(0)
                if event.key == K_UP:
                    if not self.jmp and self.grounded:
                        self.jmp = True
                        self.grounded = False
                        self.velocity_y = -25
                        self.acceleration_y = 1
            elif event.type == QUIT:
                exit(0)


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
