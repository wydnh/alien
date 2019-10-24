import sys
import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
import pygame.font

screen = pygame.display.set_mode((1000, 600))
bg_color = (20, 40, 50)
target_speed = 1
charactor_speed = 7
bullet_speed = 8
game_active = False
fail_times = 0
pygame.init()


class Target(Sprite):
    """建立被射击的矩形目标"""

    def __init__(self, screen):
        super(Target, self).__init__()
        self.screen = screen
        self.width, self.height = 50, 150
        self.screen_rect = self.screen.get_rect()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.right = self.screen_rect.right
        self.rect.centery = self.screen_rect.centery
        self.target_color = (255, 255, 255)
        self.y = float(self.rect.y)
        self.moving_direction = 1

    def blitme(self):
        self.screen.fill(self.target_color, self.rect)

    def update(self):
        self.y += target_speed * self.moving_direction
        self.rect.y = self.y


def check_boundaries(target):  # 检查矩形撞击边界和改变移动方向
    if target.rect.top <= target.screen_rect.top:
        target.moving_direction = 1
    if target.rect.bottom >= target.screen_rect.bottom:
        target.moving_direction = -1


class Charactor(Sprite):
    """建立可操纵的角色"""

    def __init__(self, screen):
        super(Charactor, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.rect.left = self.screen_rect.left + 5
        self.rect.centery = self.screen_rect.centery
        self.moving_up = False
        self.moving_dowm = False

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_up and self.rect.top >= self.screen_rect.top:
            self.rect.y -= charactor_speed
        if self.moving_dowm and self.rect.bottom <= self.screen_rect.bottom:
            self.rect.y += charactor_speed

    def centerer_charactor(self):
        self.rect.centery = self.screen_rect.centery


def keyup_events(event, charactor):  # 按键抬起
    if event.key == pygame.K_UP:
        charactor.moving_up = False
    if event.key == pygame.K_DOWN:
        charactor.moving_dowm = False


def keydowm_events(event, charactor, bullets):  # 按键落下
    if event.key == pygame.K_UP:
        charactor.moving_up = True
    if event.key == pygame.K_DOWN:
        charactor.moving_dowm = True
    if event.key == pygame.K_SPACE:
        bullet = Bullet(screen, charactor)
        bullets.add(bullet)


def check_events(charactor, bullets, stats, play_button, targets):  # 检查事件发生
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            keydowm_events(event, charactor, bullets)
        elif event.type == pygame.KEYUP:
            keyup_events(event, charactor)
        elif event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, charactor, bullets, targets)


def check_play_button(stats, play_button, mouse_x, mouse_y, charactor, bullets, targets):  # 检查开始按钮，并清零游戏
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)
        stats.game_active = True
        bullets.empty()
        targets.empty()
        target = Target(screen)
        targets.add(target)
        global fail_times
        fail_times = 0
        global target_speed
        target_speed = 1
        charactor.centerer_charactor()


class Bullet(Sprite):
    """建立子弹"""

    def __init__(self, screen, charactor):
        super(Bullet, self).__init__()
        self.screen = screen
        self.width, self.height = 15, 5
        self.bullet_color = (70, 200, 200)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.creat_bullet = False
        self.screen_rect = self.screen.get_rect()
        self.rect.left = charactor.rect.right
        self.rect.centery = charactor.rect.centery

    def blitme(self):
        pygame.draw.rect(self.screen, self.bullet_color, self.rect)

    def update(self):
        self.rect.x += bullet_speed


def bullet_target(targets, bullets, game_stat):  # 检查子弹撞击矩形
    collisions = pygame.sprite.groupcollide(bullets, targets, True, True)
    if collisions:
        game_stat.game_active = False
        pygame.mouse.set_visible(True)


def check_fail(bullets, game_stat):  # 检查失败次数，大于3则失败
    for bullet in bullets:
        if bullet.rect.left >= bullet.screen_rect.right:
            bullets.remove(bullet)
            global fail_times
            fail_times += 1
            global target_speed
            target_speed += 1
        if fail_times >= 3:
            game_stat.game_active = False
            pygame.mouse.set_visible(True)


class Game_stat():  # 游戏开始时是不活跃状态
    def __init__(self):
        self.game_active = False


class Button():
    """建立开始按钮"""

    def __init__(self, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


def run_game():
    target = Target(screen)
    targets = Group()
    charactor = Charactor(screen)
    bullets = Group()
    targets.add(target)
    stats = Game_stat()
    play_button = Button(screen, "play")
    while True:
        check_events(charactor, bullets, stats, play_button, targets)
        screen.fill(bg_color)
        charactor.blitme()
        if stats.game_active:
            check_boundaries(target)
            targets.update()
            charactor.update()
            bullets.update()
            bullet_target(targets, bullets, stats)
            check_fail(bullets, stats)
            for bullet in bullets.copy():
                if bullet.rect.x >= bullet.screen_rect.right:
                    bullets.remove(bullet)
            for bullet in bullets:
                bullet.blitme()
            for target in targets:
                target.blitme()
        if not stats.game_active:
            play_button.draw_button()
        pygame.display.flip()


run_game()
