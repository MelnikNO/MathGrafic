import pickle
import os


class SaveManager:
    """Класс для сохранения и загрузки прогресса игры."""

    SAVE_FILE = 'savefile.pkl'

    @staticmethod
    def save_game(stats, settings):
        """Сохраняет текущий прогресс."""
        data = {
            'level': stats.level,
            'score': stats.score,
            'lives': stats.ships_left,
            'high_score': stats.high_score
        }
        try:
            with open(SaveManager.SAVE_FILE, 'wb') as f:
                pickle.dump(data, f)
            print("Игра сохранена!")
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return False

    @staticmethod
    def load_game():
        """Загружает сохраненный прогресс."""
        try:
            if os.path.exists(SaveManager.SAVE_FILE):
                with open(SaveManager.SAVE_FILE, 'rb') as f:
                    data = pickle.load(f)
                print("Игра загружена!")
                return data
            else:
                print("Файл сохранения не найден")
                return None
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return None

    @staticmethod
    def delete_save():
        """Удаляет файл сохранения."""
        if os.path.exists(SaveManager.SAVE_FILE):
            os.remove(SaveManager.SAVE_FILE)
            print("Сохранение удалено")