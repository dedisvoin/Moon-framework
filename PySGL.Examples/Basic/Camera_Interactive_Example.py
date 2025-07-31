"""
Интерактивный пример камеры
Демонстрирует управление камерой в реальном времени
"""

import sys
sys.path.append("./")

try:
    from PySGL.python.Window import Window, WindowEvents, ContextSettings
    from PySGL.python.Views import FloatRect, View
    from PySGL.python.Engine.Camera import Camera2D
    from PySGL.python.Vectors import Vector2f
    from PySGL.python.Rendering.Shapes import RectangleShape
    from PySGL.python.Colors import *
    from PySGL.python.Inputs import KeyBoardInterface
    
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
        window = Window(1024, 768, "Camera Example", context_settings=ContextSettings().set_antialiasing_level(20))
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
        player.set_origin(20, 20)
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
            speed = 10 # Скорость в пикселях за кадр
            
            if KeyBoardInterface.get_press("w"):
                player_pos.y -= speed
            if KeyBoardInterface.get_press("s"):
                player_pos.y += speed
            if KeyBoardInterface.get_press("a"):
                player_pos.x -= speed
            if KeyBoardInterface.get_press("d"):
                player_pos.x += speed
            
            # Ручное управление камерой
            if KeyBoardInterface.get_press("up"):
                camera.get_view().move(0, -5)
            if KeyBoardInterface.get_press("down"):
                camera.get_view().move(0, 5)
            if KeyBoardInterface.get_press("left"):
                camera.get_view().move(-5, 0)
            if KeyBoardInterface.get_press("right"):
                camera.get_view().move(5, 0)
            
            # Поворот камеры
            if KeyBoardInterface.get_press("q"):
                current_angle = camera.get_view().get_angle()
                camera.set_target_angle(current_angle - 10)
            if KeyBoardInterface.get_press("e"):
                current_angle = camera.get_view().get_angle()
                camera.set_target_angle(current_angle + 10)
            
            # Зум камеры
            if KeyBoardInterface.get_press("z"):
                camera.set_target_zoom(camera.get_zoom() + 0.4)
            if KeyBoardInterface.get_press("x"):
                camera.set_target_zoom(camera.get_zoom() - 0.4)
            
            # Тряска камеры
            if KeyBoardInterface.get_press("space"):
                camera.shake(8)
            
            # Выход
            if KeyBoardInterface.get_press("esc"):
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