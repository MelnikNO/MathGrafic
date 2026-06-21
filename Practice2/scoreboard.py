import pygame.font


class Scoreboard:
    """Класс для вывода игровой информации."""

    def __init__(self, ai_game):
        """Инициализирует атрибуты подсчета очков."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Настройки шрифта для вывода счета
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Подготовка изображений счетов
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_aliens_count()  # ДОБАВЛЯЕМ

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Вывод счета в правой верхней части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Преобразует рекордный счет в графическое изображение."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "Record: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Рекорд выравнивается по центру верхней стороны
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Преобразует уровень в графическое изображение."""
        level_str = f"Level: {self.stats.level}"

        # Цвет зависит от уровня
        if self.stats.level < 3:
            color = (0, 255, 0)  # Зеленый
        elif self.stats.level < 6:
            color = (255, 255, 0)  # Желтый
        elif self.stats.level < 10:
            color = (255, 150, 0)  # Оранжевый
        else:
            color = (255, 0, 0)  # Красный

        self.level_image = self.font.render(level_str, True, color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Сообщает количество оставшихся кораблей."""
        ships_str = f"Ships: {self.stats.ships_left}"
        self.ships_image = self.font.render(ships_str, True, self.text_color, self.settings.bg_color)

        # Корабли выводятся в левом верхнем углу
        self.ships_rect = self.ships_image.get_rect()
        self.ships_rect.left = 20
        self.ships_rect.top = 20

    def prep_aliens_count(self):
        """Отображает количество пришельцев на экране."""
        aliens_count = len(self.ai_game.aliens)
        count_str = f"Aliens: {aliens_count}"
        self.aliens_count_image = self.font.render(count_str, True, (255, 100, 100), self.settings.bg_color)
        self.aliens_count_rect = self.aliens_count_image.get_rect()
        self.aliens_count_rect.left = 20
        self.aliens_count_rect.top = 70  # Под количеством кораблей

    def check_high_score(self):
        """Проверяет, появился ли новый рекорд."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
            # Сохраняем новый рекорд
            self.stats.save_high_score()

    def show_score(self):
        """Выводит очки, уровень и количество кораблей на экран."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.ships_image, self.ships_rect)
        self.screen.blit(self.aliens_count_image, self.aliens_count_rect)  # ДОБАВЛЯЕМ