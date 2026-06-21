import pygame
from pygame.sprite import Sprite
import os


class Ship(Sprite):
    """Класс для управления кораблем."""

    def __init__(self, ai_game):
        """Инициализирует корабль и задает его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Загружает изображение корабля и изменяет размер
        try:
            original_image = pygame.image.load('images/ship.png')
            self.image = pygame.transform.smoothscale(original_image, (70, 80))  # Размер корабля
        except:
            # Создаем простой корабль если изображение не найдено
            print("Не найден ship.png, создаю простой корабль")
            self.image = pygame.Surface((60, 80))
            self.image.fill((0, 255, 0))  # Зеленый цвет

        self.rect = self.image.get_rect()

        # Каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom

        # Сохранение вещественной координаты центра корабля
        self.x = float(self.rect.x)

        # Флаги перемещения
        self.moving_right = False
        self.moving_left = False

        self.shield_active = False
        self.shield_timer = 0
        self.power_shot_active = False
        self.power_shot_timer = 0

    def update(self):
        """Обновляет позицию корабля с учетом флагов."""
        # Обновляется атрибут x, не rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Обновление атрибута rect на основании self.x
        self.rect.x = self.x

        # Обновление таймеров бонусов
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False
                print("🛡️ Щит отключен")

        if self.power_shot_active:
            self.power_shot_timer -= 1
            if self.power_shot_timer <= 0:
                self.power_shot_active = False
                print("⚡ Усиленный выстрел отключен")

    def blitme(self):
        """Рисует корабль в текущей позиции."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Размещает корабль в центре нижней стороны."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)