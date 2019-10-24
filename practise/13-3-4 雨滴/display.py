import pygame

from settings import Settings

import func as f

from pygame.sprite import Group


def display():
    """主函数----显示雨滴效果"""
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption('Raining')
    rains = Group()
    f.create_rains(settings, screen, rains)

    while True:
        f.check_events()

        f.change_direction(settings, rains)
        f.update_rains(settings, screen, rains)

        screen.fill(settings.bg_color)
        rains.draw(screen)
        pygame.display.flip()


display()
