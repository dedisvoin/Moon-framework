"""
Пример с двумя камерами и персонажами
Левая половина экрана - первая камера, правая - вторая
"""

import sys
sys.path.append("./")

try:
    from Moon.python.Window import Window, WindowEvents
    from Moon.python.Views import FloatRect, View
    from Moon.python.Engine.Camera import Camera2D
    from Moon.python.Vectors import Vector2f
    from Moon.python.Rendering.Shapes import CircleShape
    from Moon.python.Colors import *
    from Moon.python.Inputs import *
    
    def main():
        print("=== Пример с двумя камерами ===")
        print("Управление:")
        print("  WASD - первый игрок (синий)")
        print("  Стрелки - второй игрок (красный)")
        print("  ESC - выход")
        
        # Создание окна
        window = Window(1200, 600, "Dual Camera Example")
        window.set_wait_fps(60)
        events = WindowEvents()
        
        # Создание камер
        camera1 = Camera2D(600, 600)  # Левая половина
        camera1.set_lerp_movement(0.1)
        
        camera2 = Camera2D(600, 600)  # Правая половина
        camera2.set_lerp_movement(0.1)
        camera2.set_target_zoom(3)
        
        # Создание вьюпортов для разделения экрана
        left_viewport = FloatRect(0, 0, 0.5, 1.0)   # Левая половина (0-50%)
        right_viewport = FloatRect(0.5, 0, 0.5, 1.0) # Правая половина (50-100%)
        
        camera1.get_view().set_viewport(left_viewport)
        camera2.get_view().set_viewport(right_viewport)
        camera1.set_target_angle(60)
        
        # Создание игроков
        player1 = CircleShape(20)
        player1.set_color(COLOR_BLUE)
        player1_pos = Vector2f(200, 300)
        
        player2 = CircleShape(20)
        player2.set_color(COLOR_RED)
        player2_pos = Vector2f(800, 300)
        
        # Создание препятствий в едином мире
        obstacles = []
        
        # Препятствия разбросаны по всему миру
        for i in range(8):
            for j in range(5):
                obstacle = CircleShape(15)
                obstacle.set_color(COLOR_GREEN)
                obstacle.set_position(i * 150 + 100, j * 120 + 80)
                obstacles.append(obstacle)
        
        # Основной цикл
        while window.is_open():
            if not window.update(events):
                break
            if window.get_resized():
                win_size = window.get_size().xy
                camera1.set_size(win_size[0] / 2, win_size[1])
                camera2.set_size(win_size[0] / 2, win_size[1])
            
            # Управление первым игроком (WASD)
            speed = 10
            if KeyBoardInterface.get_press("w"):
                player1_pos.y -= speed
            if KeyBoardInterface.get_press("s"):
                player1_pos.y += speed
            if KeyBoardInterface.get_press("a"):
                player1_pos.x -= speed
            if KeyBoardInterface.get_press("d"):
                player1_pos.x += speed
            
            # Управление вторым игроком (стрелки)
            if KeyBoardInterface.get_press("up"):
                player2_pos.y -= speed
            if KeyBoardInterface.get_press("down"):
                player2_pos.y += speed
            if KeyBoardInterface.get_press("left"):
                player2_pos.x -= speed
            if KeyBoardInterface.get_press("right"):
                player2_pos.x += speed

            
            # Обновление камер
            camera1.follow(player1_pos)
            camera1.update()
            
            camera2.follow(player2_pos)
            camera2.update()
            
            # Отрисовка
            window.clear(COLOR_BLACK)
            
            # Функция отрисовки мира
            def draw_world():
                # Рисуем всех игроков
                player1.set_position(*player1_pos.as_tuple())
                player2.set_position(*player2_pos.as_tuple())
                window.draw(player1)
                window.draw(player2)
                
                # Рисуем все препятствия
                for obstacle in obstacles:
                    window.draw(obstacle)
            
            # Отрисовка с первой камеры (левая половина)
            camera1.apply(window)
            draw_world()
            
            # Отрисовка со второй камеры (правая половина)
            camera2.apply(window)
            draw_world()
            
            # Возвращаем стандартный вид для UI
            window.set_view(window.get_default_view())
            
            window.display()
        
        print("Пример завершен")
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Этот пример требует полную установку PySGL")
except Exception as e:
    print(f"Ошибка выполнения: {e}")
    print("Возможно, нативная библиотека недоступна")