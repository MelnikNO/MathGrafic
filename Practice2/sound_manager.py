import pygame
import os


class SoundManager:
    """Класс для управления звуковыми эффектами."""

    def __init__(self):
        """Инициализирует звуковой менеджер."""
        pygame.mixer.init()
        self.sounds = {}
        self.music_volume = 0.5
        self.sfx_volume = 0.7

        # Загружаем все звуки
        self._load_sounds()

    def _load_sounds(self):
        """Загружает все звуковые файлы."""
        sound_files = {
            'laser': 'sounds/Laser_Shot.wav',
            'explosion': 'sounds/explosion.wav',
            'hit': 'sounds/attack_hit.wav',
            'level_up': 'sounds/round_end.wav',
            'game_over': 'sounds/death.wav'
        }

        for name, path in sound_files.items():
            try:
                if os.path.exists(path):
                    self.sounds[name] = pygame.mixer.Sound(path)
                    self.sounds[name].set_volume(self.sfx_volume)
                    print(f"Загружен звук: {name}")
                else:
                    # Если файл не найден, просто пропускаем
                    print(f"Звук {name} не найден по пути {path}, пропускаем")
                    self.sounds[name] = None
            except Exception as e:
                print(f"Ошибка загрузки {name}: {e}")
                self.sounds[name] = None

    def play(self, sound_name):
        """Воспроизводит звук по имени."""
        if sound_name in self.sounds:
            sound = self.sounds[sound_name]
            if sound is not None:
                sound.play()
            # Если sound is None, просто игнорируем
        else:
            print(f"Звук {sound_name} не найден")

    def set_sfx_volume(self, volume):
        """Устанавливает громкость звуковых эффектов."""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            if sound is not None:
                sound.set_volume(self.sfx_volume)