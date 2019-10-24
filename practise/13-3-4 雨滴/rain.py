import pygame

from pygame.sprite import Sprite


class Rain(Sprite):
    """雨滴"""

    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.image = pygame.image.load('images/rain.bmp')
        self.rect = self.image.get_rect()

        self.y = float(self.rect.y)

    def check_edges(self):
        # 判断雨滴是否到了最底下
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom:
            return True

    # def blitme(self):
    #     self.screen.blit(self.image, self.rect)
