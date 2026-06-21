import sys
from time import sleep
import pygame
from sound_manager import SoundManager
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from bonus import Bonus, BonusType
import random


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.sound_manager = SoundManager()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self._load_background()

        # Создание экземпляров для хранения статистики
        self.stats = GameStats(self)

        # СОЗДАЕМ ГРУППЫ ДО SCOREBOARD
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bonuses = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()

        self.sb = Scoreboard(self)

        self._create_fleet()

        # Создание кнопки Play
        self.play_button = Button(self, "Play")

        # Инициализация отображения кораблей
        self.sb.prep_ships()


    def _load_background(self):
        """Загружает фоновое изображение."""
        self.background = pygame.image.load('images/background.jpg')
        self.background = pygame.transform.scale(self.background, (self.settings.screen_width, self.settings.screen_height))
        self.use_background_image = True
        print("Фоновое изображение успешно загружено")

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_bonuses()

            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        """Запускает новую игру."""
        self.settings.initialize_dynamic_settings()
        self.settings.level = 1  # Сбрасываем уровень в настройках

        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.sb.prep_aliens_count()

        # Очистка всех объектов
        self.aliens.empty()
        self.bullets.empty()
        self.bonuses.empty()
        self.alien_bullets.empty()

        self._create_fleet()
        self.ship.center_ship()

        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.stats.save_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()
        elif event.key == pygame.K_s:
            # Сохранение игры (только если активна)
            if self.stats.game_active:
                from save_manager import SaveManager
                SaveManager.save_game(self.stats, self.settings)

        elif event.key == pygame.K_l:
            # Загрузка игры
            from save_manager import SaveManager
            data = SaveManager.load_game()
            if data:
                self._load_saved_game(data)

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            # Проверяем, активен ли усиленный выстрел
            power_shot = self.ship.power_shot_active
            new_bullet = Bullet(self, power_shot=power_shot)
            self.bullets.add(new_bullet)
            self.sound_manager.play('laser')

            # Если усиленный, создаем второй снаряд
            if power_shot:
                new_bullet2 = Bullet(self, power_shot=True)
                # Смещаем второй снаряд в сторону
                new_bullet2.rect.x -= 15
                self.bullets.add(new_bullet2)
                new_bullet3 = Bullet(self, power_shot=True)
                new_bullet3.rect.x += 15
                self.bullets.add(new_bullet3)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""
        # Обновление позиций снарядов
        self.bullets.update()

        # Удаление снарядов, вышедших за край экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Обработка коллизий снарядов с пришельцами."""
        # Словарь для хранения уничтоженных пришельцев и их позиций
        destroyed_aliens_positions = []

        for bullet in self.bullets.copy():
            hit_aliens = pygame.sprite.spritecollide(bullet, self.aliens, True)
            if hit_aliens:
                for alien in hit_aliens:
                    destroyed_aliens_positions.append((alien.rect.centerx, alien.rect.centery))

                if hasattr(bullet, 'damage') and bullet.damage > 1:
                    extra_aliens = list(self.aliens)[:bullet.damage - 1]
                    for alien in extra_aliens:
                        destroyed_aliens_positions.append((alien.rect.centerx, alien.rect.centery))
                        alien.kill()

                self.stats.score += self.settings.alien_points * len(hit_aliens)
                self.sound_manager.play('explosion')
                bullet.kill()

        # Создаем бонусы
        for x, y in destroyed_aliens_positions:
            self._spawn_bonus(x, y)

        self.sb.prep_score()
        self.sb.check_high_score()
        self.sb.prep_aliens_count()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
            self.sb.prep_aliens_count()
            self.sound_manager.play('level_up')
            self._show_level_info()

    def _update_aliens(self):
        """
        Проверяет, достиг ли флот края экрана,
        с последующим обновлением позиций всех пришельцев во флоте.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коллизий с учетом щита
        if not self.ship.shield_active:  # Если щит не активен
            if pygame.sprite.spritecollideany(self.ship, self.aliens):
                self._ship_hit()
        else:
            # Если щит активен, пришельцы отталкиваются
            for alien in self.aliens.sprites():
                if pygame.Rect.colliderect(self.ship.rect, alien.rect):
                    alien.rect.y += 30  # Отбрасываем пришельца
                    self.sound_manager.play('hit')

        self._check_aliens_bottom()

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем."""
        if self.stats.ships_left > 0:
            # Уменьшение ships_left и обновление панели счета
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.sound_manager.play('game_over')

    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Происходит то же, что при столкновении с кораблем
                self._ship_hit()
                break

    def _create_fleet(self):
        """Создает флот пришельцев."""
        if not self.aliens:
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size

            # Используем обновленное количество пришельцев
            number_aliens_x = min(self.settings.aliens_per_row,
                                  self.settings.screen_width // (2 * alien_width))

            ship_height = self.ship.rect.height
            available_space_y = (self.settings.screen_height -
                                 (3 * alien_height) - ship_height)
            # Используем множитель рядов
            number_rows = int(available_space_y // (3 * alien_height) * self.settings.rows_multiplier)

            for row_number in range(number_rows):
                for alien_number in range(number_aliens_x):
                    self._create_alien(alien_number, row_number)

            # Обновляем счетчик пришельцев
            self.sb.prep_aliens_count()

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        if hasattr(self, 'use_background_image') and self.use_background_image:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(self.settings.bg_color)

        # Отрисовка игровых объектов поверх фона
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Отрисовка бонусов
        for bonus in self.bonuses.sprites():
            bonus.draw()

        # Вывод информации о счете
        self.sb.show_score()

        # Кнопка Play отображается в том случае, если игра неактивна
        if not self.stats.game_active:
            self.play_button.draw_button()

        if self.ship.shield_active:
            pygame.draw.circle(self.screen, (0, 150, 255, 100),
                               self.ship.rect.center, 45, 3)

        pygame.display.flip()


    def _load_saved_game(self, data):
        """Загружает сохраненную игру."""
        # Сброс текущего состояния
        self.aliens.empty()
        self.bullets.empty()

        # Восстановление статистики
        self.stats.level = data['level']
        self.stats.score = data['score']
        self.stats.ships_left = data['lives']
        self.stats.high_score = data.get('high_score', 0)

        # Обновление отображения
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.sb.prep_high_score()

        # Восстановление скорости для текущего уровня
        # (применяем ускорение нужное количество раз)
        self.settings.initialize_dynamic_settings()
        for _ in range(self.stats.level - 1):
            self.settings.increase_speed()

        # Создание флота и размещение корабля
        self._create_fleet()
        self.ship.center_ship()

        # Активация игры
        self.stats.game_active = True
        pygame.mouse.set_visible(False)

        print(f"Игра загружена: Уровень {self.stats.level}, Очки {self.stats.score}")


    def _spawn_bonus(self, x, y):
        """С вероятностью создает бонус."""
        # 15% шанс выпадения бонуса
        if random.random() < 0.15:
            bonus_types = [BonusType.EXTRA_LIFE, BonusType.SHIELD, BonusType.POWER_SHOT]
            bonus_type = random.choice(bonus_types)
            bonus = Bonus(self, x, y, bonus_type)
            self.bonuses.add(bonus)

    def _update_bonuses(self):
        """Обновляет бонусы и проверяет столкновения с кораблем."""
        self.bonuses.update()

        # Проверка столкновения бонусов с кораблем
        for bonus in self.bonuses.copy():
            if pygame.Rect.colliderect(self.ship.rect, bonus.rect):
                # Передаем scoreboard как дополнительный параметр
                bonus.apply(self.ship, self.stats, self.settings, self.sound_manager, self.sb)
                bonus.kill()

        # Удаляем бонусы, вышедшие за экран
        for bonus in self.bonuses.copy():
            if bonus.rect.top > self.settings.screen_height:
                bonus.kill()

    def _show_level_info(self):
        """Показывает информацию о новом уровне."""
        info = self.settings.get_level_info()

        # Создаем полупрозрачный фон
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Заголовок
        font_big = pygame.font.SysFont(None, 72)
        title = font_big.render(f"🚀 УРОВЕНЬ {self.stats.level}!", True, (255, 255, 0))
        title_rect = title.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2 - 100))
        self.screen.blit(title, title_rect)

        # Информация
        font = pygame.font.SysFont(None, 32)
        y_pos = self.settings.screen_height // 2 - 20
        messages = [
            f"👾 Пришельцев в ряду: {info['aliens_per_row']}",
            f"⚡ Скорость: {info['alien_speed']}x",
            f"💀 Очки за убийство: {info['alien_points']}",
            f"📉 Скорость падения: {info['fleet_drop_speed']}"
        ]

        for msg in messages:
            text = font.render(msg, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.settings.screen_width // 2, y_pos))
            self.screen.blit(text, text_rect)
            y_pos += 40

        # Подсказка
        font_small = pygame.font.SysFont(None, 24)
        hint = font_small.render("Нажмите любую клавишу для продолжения...", True, (200, 200, 200))
        hint_rect = hint.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2 + 150))
        self.screen.blit(hint, hint_rect)

        pygame.display.flip()

        # Ждем нажатия клавиши
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting = False
                    break
                elif event.type == pygame.QUIT:
                    sys.exit()
            pygame.time.delay(50)


if __name__ == '__main__':
    # Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()