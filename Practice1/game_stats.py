import json
import os

class GameStats:
    """Отслеживание статистики для игры Alien Invasion."""

    def __init__(self, ai_game):
        """Инициализирует статистику."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Игра запускается в неактивном состоянии
        self.game_active = False

        # Загружаем рекорд из файла
        self.load_high_score()

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_score(self):
        """Загружает рекорд из файла."""
        try:
            if os.path.exists('high_score.json'):
                with open('high_score.json', 'r') as f:
                    self.high_score = json.load(f)
            else:
                self.high_score = 0
        except (json.JSONDecodeError, Exception) as e:
            print(f"Ошибка загрузки рекорда: {e}")
            self.high_score = 0

    def save_high_score(self):
        """Сохраняет рекорд в файл."""
        try:
            with open('high_score.json', 'w') as f:
                json.dump(self.high_score, f)
        except Exception as e:
            print(f"Ошибка сохранения рекорда: {e}")