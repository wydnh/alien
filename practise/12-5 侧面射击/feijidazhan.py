import sys

import pygame

from settings import Settings

from ship import Ship

from pygame.sprite import Group

from bullet import Bullet


def run():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('飞机大作战')

    ship = Ship(ai_settings, screen)

    bullets = Group()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    ship.moving_right = True
                if event.key == pygame.K_LEFT:
                    ship.moving_left = True
                if event.key == pygame.K_UP:
                    ship.moving_up = True
                if event.key == pygame.K_DOWN:
                    ship.moving_down = True
                elif event.key == pygame.K_SPACE:
                    if len(bullets) < ai_settings.bullets_allowed:
                        new_bullet = Bullet(ai_settings, screen, ship)
                        bullets.add(new_bullet)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    ship.moving_right = False
                if event.key == pygame.K_LEFT:
                    ship.moving_left = False
                if event.key == pygame.K_UP:
                    ship.moving_up = False
                if event.key == pygame.K_DOWN:
                    ship.moving_down = False

        ship.update()

        bullets.update()

        for bullet in bullets.copy():
            if bullet.rect.left > ai_settings.screen_width:
                bullets.remove(bullet)

        screen.fill(ai_settings.bg_color)

        for bullet in bullets.sprites():
            bullet.draw_bullet()

        ship.blitme()

        pygame.display.flip()


run()
