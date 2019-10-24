import pygame

import sys

from rain import Rain


def check_events():
    """按键检查"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def get_col_numbers(settings, rain):  # 对于每一行来说，变化的是x坐标，列在变化
    """一行可以存放的雨滴数"""
    col_numbers = int(settings.screen_width / (2 * rain.rect.width))
    return col_numbers


def get_row_numbers(settings, rain):
    """可存放雨滴的行数"""
    row_numbers = int(settings.screen_height / (1 * rain.rect.height))
    return row_numbers


def create_rain(settings, screen, rains, col_number, row_number):
    rain = Rain(settings, screen)
    rain_width = rain.rect.width
    rain.x = rain_width + 2 * rain_width * col_number
    rain.rect.x = rain.x  # rect存放整数
    rain.y = rain.rect.y + 2 * rain.rect.height * row_number
    rain.rect.y = rain.y
    rains.add(rain)


def create_rains(settings, screen, rains):
    rain = Rain(settings, screen)  # 这句是要写的，不写的话get_col_numbers()中的rain将出现NameError
    col_numbers = get_col_numbers(settings, rain)
    row_numbers = get_row_numbers(settings, rain)
    for row_number in range(row_numbers):
        for col_number in range(col_numbers):
            create_rain(settings, screen, rains, col_number, row_number)


def change_direction(settings, rains):
    """每次循环都下降 settings.drop_speed 距离"""
    for rain in rains.sprites():
        rain.rect.y += settings.drop_speed


def update_rains(settings, screen, rains):
    """如果一个雨滴到底部了, 新建一个雨滴, 把 x 左标赋值给它, 再把自己删除添加新雨滴"""
    for rain in rains.sprites():
        if rain.check_edges():
            new_rain = Rain(settings, screen)
            new_rain.rect.x = rain.rect.x
            rains.remove(rain)
            rains.add(new_rain)
        print(len(rains))
