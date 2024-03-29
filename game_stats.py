from game_functions import load_high_score


class GameStats():
    """跟踪游戏的统计信息"""

    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings

        self.reset_stats()

        # 在任何情况下都不应重置最高得分
        self.high_score = load_high_score()

        # 让游戏一开始处于非活动状态
        self.game_active = False

    def reset_stats(self):
        """初始化在游戏运行期间可能发生变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
