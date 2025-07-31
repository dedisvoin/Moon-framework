"""
Интерактивный пример камеры
Демонстрирует управление камерой в реальном времени
"""

import sys
sys.path.append("./")

try:
    from PySGL.python.Window import Window, WindowEvents
    from PySGL.python.Views import FloatRect, View
    from PySGL.python.Engine.Camera import Camera2D
    from PySGL.python.Vectors import Vector2f
    from PySGL.python.Rendering.Shapes import RectangleShape
    from PySGL.python.Colors import *
    from PySGL.python.Inputs import *
    
    def main():
        print("=== Интерактивный пример камеры ===")
        print("Управление:")
        print("  WASD - движение игрока")
        print("  Стрелки - ручное управление камерой")
        print("  Q/E - поворот камеры")
        print("  Z/X - зум камеры")
        print("  SPACE - тряска камеры")
        print("  ESC - выход")
        
        # Создание окна
        window = Window(1024, 768, "Camera Example")
        window.set_wait_fps(60)
        events = WindowEvents()
        
        # Создание камеры
        camera = Camera2D(1024, 768)
        camera.set_window(window)
        camera.set_lerp_movement(0.1)
        camera.set_lerp_zoom(0.05)
        camera.set_lerp_rotate(0.08)
        
        # Создание игрока
        player = RectangleShape(40, 40)
        player.set_color(COLOR_BLUE)
        player.set_outline_color(COLOR_WHITE)
        player.set_outline_thickness(2)
        player_pos = Vector2f(400, 300)
        
        # Создание препятствий
        obstacles = []
        for i in range(5):
            for j in range(5):
                obstacle = RectangleShape(60, 60)
                obstacle.set_color(COLOR_RED)
                obstacle.set_position(i * 150 + 100, j * 150 + 100)
                obstacles.append(obstacle)
        
        # Основной цикл
        while window.is_open():
            if not window.update(events):
                break
                
            # Управление игроком
            speed = 200 * (1/60)  # Скорость в пикселях за кадр
            
            if is_key_pressed(Keys.W):
                player_pos.y -= speed
            if is_key_pressed(Keys.S):
                player_pos.y += speed
            if is_key_pressed(Keys.A):
                player_pos.x -= speed
            if is_key_pressed(Keys.D):
                player_pos.x += speed
            
            # Ручное управление камерой
            if is_key_pressed(Keys.Up):
                camera.get_view().move(0, -5)
            if is_key_pressed(Keys.Down):
                camera.get_view().move(0, 5)
            if is_key_pressed(Keys.Left):
                camera.get_view().move(-5, 0)
            if is_key_pressed(Keys.Right):
                camera.get_view().move(5, 0)
            
            # Поворот камеры
            if is_key_pressed(Keys.Q):
                current_angle = camera.get_view().get_angle()
                camera.set_target_angle(current_angle - 1)
            if is_key_pressed(Keys.E):
                current_angle = camera.get_view().get_angle()
                camera.set_target_angle(current_angle + 1)
            
            # Зум камеры
            if is_key_pressed(Keys.Z):
                camera.set_target_zoom(camera.get_zoom() * 1.02)
            if is_key_pressed(Keys.X):
                camera.set_target_zoom(camera.get_zoom() * 0.98)
            
            # Тряска камеры
            if is_key_pressed(Keys.Space):
                camera.shake(8)
            
            # Выход
            if is_key_pressed(Keys.Escape):
                break
            
            # Обновление камеры
            camera.follow(player_pos)
            camera.update()
            
            # Отрисовка
            window.clear(COLOR_DARK_GRAY)
            
            # Применяем камеру
            camera.apply(window)
            
            # Рисуем игрока
            player.set_position(*player_pos.as_tuple())
            window.draw(player)
            
            # Рисуем препятствия
            for obstacle in obstacles:
                window.draw(obstacle)
            
            # Возвращаем стандартный вид для UI
            camera.reapply(window)
            
            # Рисуем UI
            # Здесь можно добавить интерфейс
            
            window.display()
        
        print("Пример завершен")
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Этот пример требует полную установку PySGL")
    print("Убедитесь, что все модули доступны")
except Exception as e:
    print(f"Ошибка выполнения: {e}")
    print("Возможно, нативная библиотека недоступна")