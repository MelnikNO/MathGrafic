import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Класс для управления снарядами, выпущенными кораблем."""

    def __init__(self, ai_game, power_shot=False):
        """Создает объект снаряда в текущей позиции корабля."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Усиленный снаряд больше и ярче
        if power_shot:
            self.color = (255, 100, 0)  # Оранжевый
            self.rect = pygame.Rect(0, 0,
                                    self.settings.bullet_width * 3,
                                    self.settings.bullet_height * 2)
            self.damage = 2  # Уничтожает 2 пришельцев
        else:
            self.color = self.settings.bullet_color
            self.rect = pygame.Rect(0, 0,
                                    self.settings.bullet_width,
                                    self.settings.bullet_height)
            self.damage = 1

        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """Перемещает снаряд вверх по экрану."""
        # Обновление позиции снаряда в вещественном формате
        self.y -= self.settings.bullet_speed
        # Обновление позиции прямоугольника
        self.rect.y = self.y

    def draw_bullet(self):
        """Вывод снаряда на экран."""
        pygame.draw.rect(self.screen, self.color, self.rect)