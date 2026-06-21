import pygame


class ProgressBar:
    """Отображает прогресс уничтожения пришельцев на уровне."""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ai_game = ai_game

        self.width = 200
        self.height = 20
        self.x = 20
        self.y = 70  # Под информацией о кораблях

        self.color_bg = (50, 50, 50)
        self.color_fg = (0, 255, 0)

    def draw(self):
        """Рисует полосу прогресса."""
        # Общее количество пришельцев, которое должно быть на уровне
        total_aliens = self._get_total_aliens()
        current_aliens = len(self.ai_game.aliens)

        if total_aliens > 0:
            progress = 1 - (current_aliens / total_aliens)
        else:
            progress = 1

        # Фон
        pygame.draw.rect(self.screen, self.color_bg,
                         (self.x, self.y, self.width, self.height))

        # Прогресс
        pygame.draw.rect(self.screen, self.color_fg,
                         (self.x, self.y, self.width * progress, self.height))

        # Граница
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.x, self.y, self.width, self.height), 2)

        # Текст
        font = pygame.font.SysFont(None, 16)
        text = font.render(f"{int(progress * 100)}%", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        self.screen.blit(text, text_rect)

    def _get_total_aliens(self):
        """Вычисляет общее количество пришельцев на уровне."""
        if not hasattr(self.settings, 'aliens_per_row'):
            return 100

        alien = None
        if self.ai_game.aliens:
            alien = self.ai_game.aliens.sprites()[0]
        else:
            # Если пришельцев нет, используем примерный размер
            return 50

        alien_width, alien_height = 70, 60
        number_aliens_x = min(self.settings.aliens_per_row,
                              self.settings.screen_width // (2 * alien_width))

        ship_height = 80
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = int(available_space_y // (3 * alien_height) * self.settings.rows_multiplier)

        return number_aliens_x * number_rows