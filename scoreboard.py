import pygame.font

from pygame.sprite import Group

from ship import Ship


class Scoreboard():
    """显示得分的类"""

    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及的属性"""
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 准备图像
        self.prep_image()

    def prep_image(self):
        """准备包含初始得分, 最高得分, 等级的图像"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_ships(self):
        """显示还剩下多少艘飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship.rect.width * ship_number
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_level(self):
        """将等级转换渲染为图像"""
        # 获取level的image
        self.level_image = pygame.font.SysFont(None, 48).render('Level: ' + str(self.stats.level), True,
                                                                self.text_color, self.ai_settings.bg_color)
        # 设置level的显示位置
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_high_score(self):
        """将最高得分转换为渲染的图像, 并设置位置"""
        # 圆整high_score, 并添加千位分隔符
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)

        # 获取high_score的image
        self.high_score_image = pygame.font.SysFont(None, 48).render(high_score_str, True, self.text_color,
                                                                     self.ai_settings.bg_color)
        # 设置high_score的显示位置
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_score(self):
        """将得分转换为一幅渲染的图,并设置它的显示位置"""
        # score_str = str(self.stats.score)

        # 将分数圆整到10的倍数
        rounded_score = round(self.stats.score, -1)
        # 字符串格式设置指令
        score_str = "{:,}".format(rounded_score)

        self.score_image = pygame.font.SysFont(None, 48).render(score_str, True, self.text_color,
                                                                self.ai_settings.bg_color)

        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """在屏幕上显示得分"""
        # 显示当前得分
        self.screen.blit(self.score_image, self.score_rect)
        # 显示最高得分
        self.screen.blit(self.high_score_image, self.high_score_rect)
        # 显示等级
        self.screen.blit(self.level_image, self.level_rect)
        # 绘制飞船编组
        self.ships.draw(self.screen)
