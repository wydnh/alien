import pygame


class Ship():
    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/feiji.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.left = self.screen_rect.left
        self.rect.bottom = self.screen_rect.bottom

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

    def update(self):
        """根据移动标志调整飞船的位置"""
        # 更新飞船的center值,而不是rect
        # if self.moving_right:
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # self.rect.centerx += 1
            self.centerx += self.ai_settings.ship_speed_factor

        # if self.moving_left:
        if self.moving_left and self.rect.left > 0:
            # self.rect.centerx -= 1
            self.centerx -= self.ai_settings.ship_speed_factor

        if self.moving_up and self.rect.top > 0:
            # self.rect.centery -= 1
            self.centery -= self.ai_settings.ship_speed_factor

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            # self.rect.centery -= 1
            self.centery += self.ai_settings.ship_speed_factor

        # 根据self.center更新rect对象
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def blitme(self):
        self.screen.blit(self.image, self.rect)
