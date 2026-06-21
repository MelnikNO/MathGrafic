class Settings:
    """Класс для хранения всех настроек игры Alien Invasion."""

    def __init__(self):
        """Инициализирует статические настройки игры."""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Настройки корабля
        self.ship_limit = 3

        # Параметры снаряда
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 60)
        self.bullets_allowed = 3

        # Настройки пришельцев
        self.fleet_drop_speed = 5

        # Темп ускорения игры
        self.speedup_scale = 1.05
        # Темп роста стоимости пришельцев
        self.score_scale = 1.5

        # Параметры сложности
        self.aliens_per_row = 8
        self.rows_multiplier = 1.0
        self.min_fleet_drop_speed = 5
        self.max_fleet_drop_speed = 20
        self.alien_shoot_chance = 0.001
        self.max_aliens_per_row = 20

        self.initialize_dynamic_settings()

        # Для отслеживания уровня
        self.level = 1

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.ship_speed = 1.0
        self.bullet_speed = 2.0
        self.alien_speed = 0.3
        self.fleet_direction = 1
        self.alien_points = 50
        self.fleet_drop_speed = 5
        self.alien_shoot_chance = 0.001
        self.aliens_per_row = 8
        self.rows_multiplier = 1.0

    def increase_speed(self):
        """Увеличивает настройки скорости и сложность."""
        # Базовое ускорение
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

        # Увеличение скорости падения
        self.fleet_drop_speed = min(
            self.fleet_drop_speed * self.speedup_scale,
            self.max_fleet_drop_speed
        )

        # Увеличение шанса выстрела
        self.alien_shoot_chance = min(
            self.alien_shoot_chance * self.speedup_scale * 1.2,
            0.05
        )

        # Увеличение количества пришельцев
        if self.aliens_per_row < self.max_aliens_per_row:
            self.aliens_per_row += 2

        # Каждые 2 уровня добавляем новый ряд
        if self.level % 2 == 0 and self.rows_multiplier < 3.0:
            self.rows_multiplier += 0.2

        # Увеличиваем уровень
        self.level += 1

        # Выводим информацию в консоль
        print(f"\n📊 УРОВЕНЬ {self.level}")
        print(f"  ├─ Пришельцев в ряду: {self.aliens_per_row}")
        print(f"  ├─ Рядов: {self.rows_multiplier:.1f}")
        print(f"  ├─ Скорость пришельцев: {self.alien_speed:.2f}")
        print(f"  ├─ Скорость падения: {self.fleet_drop_speed:.1f}")
        print(f"  ├─ Очки за убийство: {self.alien_points}")
        print(f"  └─ Шанс выстрела: {self.alien_shoot_chance * 100:.2f}%")

    def get_level_info(self):
        """Возвращает информацию о текущих настройках уровня."""
        return {
            'alien_speed': round(self.alien_speed, 2),
            'ship_speed': round(self.ship_speed, 2),
            'bullet_speed': round(self.bullet_speed, 2),
            'fleet_drop_speed': round(self.fleet_drop_speed, 2),
            'aliens_per_row': self.aliens_per_row,
            'alien_points': self.alien_points,
            'shoot_chance': f"{self.alien_shoot_chance * 100:.2f}%",
            'rows': round(self.rows_multiplier, 1)
        }