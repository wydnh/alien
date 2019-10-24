import pygame
import sys
from random import randint
from pygame.sprite import Sprite
from pygame.sprite import Group
from time import sleep


class Doll(Sprite):
    def __init__(self, screen, speed_factor):
        super(Doll, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.moving_right = False
        self.moving_left = False
        self.speed_factor = speed_factor

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.speed_factor
        if self.moving_left and self.rect.left > 0:
            self.rect.centerx -= self.speed_factor


class Water(Sprite):
    def __init__(self, screen, dropspeed):
        super(Water, self).__init__()
        self.screen = screen
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.rect.centerx = randint(1, 1000)
        self.rect.top = 0
        self.y = float(self.rect.y)
        self.dropspeed = dropspeed

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.y += self.dropspeed
        self.rect.y = self.y


def catch_water(doll, waters, screen, dropspeed, stats):
    """判断doll和waters是否接触 判断waters是否落到了屏幕下 及采取的措施"""
    # 判断 doll 和 water 是否发生了接触, 并在接触后清除 water
    pygame.sprite.spritecollide(doll, waters, True, collided=None)

    # # 判断 doll 和 waters里的sprite是否发生了接触, 如果接触了返回接触的sptite,并停止遍历waters
    # if pygame.sprite.spritecollideany(doll, waters):
    #     waters.empty()

    for water in waters:
        if water.rect.top >= water.screen_rect.bottom:
            if stats.doll_left > 0:
                waters.empty()
                stats.doll_left -= 1
                doll.rect.centerx = doll.screen_rect.centerx
                sleep(0.5)
                break
            else:
                stats.active = False

    if len(waters) == 0:
        water = Water(screen, dropspeed)
        waters.add(water)


def check_keydown_events(event, doll):
    if event.key == pygame.K_RIGHT:
        doll.moving_right = True
    elif event.key == pygame.K_LEFT:
        doll.moving_left = True


def check_keyup_events(event, doll):
    if event.key == pygame.K_RIGHT:
        doll.moving_right = False
    elif event.key == pygame.K_LEFT:
        doll.moving_left = False


def event_check(doll):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, doll)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, doll)


class Stats():
    def __init__(self, doll_limit):
        self.doll_limit = doll_limit
        self.reset_stats()
        self.active = True

    def reset_stats(self):
        self.doll_left = self.doll_limit


def rungame():
    pygame.init()
    bg_color = (20, 40, 50)
    screen = pygame.display.set_mode((1000, 600))
    dropspeed = 1.5
    speed_factor = 2
    doll_limit = 3

    water = Water(screen, dropspeed)
    waters = Group()
    waters.add(water)
    doll = Doll(screen, speed_factor)
    stats = Stats(doll_limit)

    while True:
        event_check(doll)

        if stats.active:
            doll.update()
            waters.update()
            catch_water(doll, waters, screen, dropspeed, stats)

        screen.fill(bg_color)
        doll.blitme()
        waters.draw(screen)
        pygame.display.flip()


rungame()
