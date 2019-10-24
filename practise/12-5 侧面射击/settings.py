class Settings():
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        self.ship_speed_factor = 1.5

        # 子弹设置
        self.bullet_speed_factor = 1
        self.bullet_width = 15
        self.bullet_height = 1
        self.bullet_color = 255, 0, 0
        self.bullets_allowed = 3
