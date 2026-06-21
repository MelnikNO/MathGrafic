import pygame
from pygame.sprite import Sprite
import random


class BonusType:
    """Типы бонусов."""
    EXTRA_LIFE = 'life'
    SHIELD = 'shield'
    POWER_SHOT = 'power_shot'


class Bonus(Sprite):
    """Класс для бонусов."""

    def __init__(self, ai_game, x, y, bonus_type):
        """Инициализирует бонус."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.ai_game = ai_game  # Сохраняем ссылку на игру

        self.bonus_type = bonus_type
        self.speed = 1.5

        # Цвета для разных бонусов
        colors = {
            BonusType.EXTRA_LIFE: (0, 255, 0),  # Зеленый
            BonusType.SHIELD: (0, 150, 255),  # Синий
            BonusType.POWER_SHOT: (255, 200, 0)  # Золотой
        }

        # Создаем прямоугольник бонуса
        self.rect = pygame.Rect(0, 0, 30, 30)
        self.rect.centerx = x
        self.rect.y = y

        self.color = colors.get(bonus_type, (255, 255, 255))

        # Для анимации
        self.animation_offset = 0

        # Таймер жизни бонуса (исчезает через 5 секунд)
        self.born = pygame.time.get_ticks()

    def update(self):
        """Обновляет позицию бонуса."""
        # Движение вниз
        self.rect.y += self.speed

        # Анимация мерцания
        self.animation_offset = (self.animation_offset + 1) % 20

        # Проверка времени жизни
        current_time = pygame.time.get_ticks()
        if current_time - self.born > 5000:  # 5 секунд
            self.kill()

    def draw(self):
        """Рисует бонус на экране."""
        # Основной квадрат
        pygame.draw.rect(self.screen, self.color, self.rect)
        # Обводка
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2)

        # Символ в центре (используем текстовые метки вместо эмодзи для совместимости)
        font = pygame.font.SysFont(None, 20)
        symbols = {
            BonusType.EXTRA_LIFE: '+1',
            BonusType.SHIELD: 'S',
            BonusType.POWER_SHOT: 'P'
        }
        symbol = symbols.get(self.bonus_type, '?')
        text = font.render(symbol, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)

    def apply(self, ship, stats, settings, sound_manager, scoreboard=None):
        """Применяет эффект бонуса."""
        if self.bonus_type == BonusType.EXTRA_LIFE:
            stats.ships_left += 1
            if scoreboard:
                scoreboard.prep_ships()
            sound_manager.play('level_up')
            print("❤️ +1 жизнь!")

        elif self.bonus_type == BonusType.SHIELD:
            # Включаем щит на 5 секунд
            ship.shield_active = True
            ship.shield_timer = 300  # 5 секунд при 60 FPS
            sound_manager.play('level_up')
            print("🛡️ Щит активирован!")

        elif self.bonus_type == BonusType.POWER_SHOT:
            # Усиленный выстрел на 5 секунд
            ship.power_shot_active = True
            ship.power_shot_timer = 300
            sound_manager.play('level_up')
            print("⚡ Усиленный выстрел!")

        self.kill()