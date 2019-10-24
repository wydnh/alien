import sys

import pygame


def run():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('按键')
    bg_color = (230, 230, 230)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                print(event.key)
                if event.key == pygame.K_UP:
                    bg_color = (255, 0, 0)

        screen.fill(bg_color)
        pygame.display.flip()


run()
