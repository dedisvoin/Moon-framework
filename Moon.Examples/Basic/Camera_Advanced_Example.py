"""
Продвинутый пример использования камеры с View
Демонстрирует интеграцию Camera2D с улучшенным модулем Views
"""

import sys
sys.path.append("./")

from Moon.python.Views import FloatRect, View
from Moon.python.Engine.Camera import Camera2D
from Moon.python.Vectors import Vector2f

def camera_demo():
    print("=== Продвинутый пример использования камеры ===\n")
    
    try:
        # 1. Создание камеры
        print("1. Создание камеры:")
        camera = Camera2D(1024, 768)
        print(f"   Камера создана: размер {camera.get_size()}")
        
        # 2. Настройка параметров интерполяции
        print("\n2. Настройка параметров:")
        camera.set_lerp_movement(0.08)  # Плавное движение
        camera.set_lerp_zoom(0.05)      # Плавный зум
        camera.set_lerp_rotate(0.1)     # Плавный поворот
        print("   Настроены параметры интерполяции")
        
        # 3. Следование за одной целью
        print("\n3. Следование за одной целью:")
        player_pos = Vector2f(200, 150)
        camera.follow(player_pos)
        print(f"   Камера следует за игроком: {player_pos}")
        
        # Симуляция обновления
        for i in range(3):
            camera.update(1.0)
            center = camera.get_view().get_center()
            print(f"   Обновление {i+1}: центр камеры {center}")
        
        # 4. Следование за двумя целями с автомасштабированием
        print("\n4. Следование за двумя целями:")
        player1 = Vector2f(100, 100)
        player2 = Vector2f(500, 400)
        
        camera.set_using_two_target(True)
        camera.set_two_target_factor(0.3)  # Ближе к первому игроку
        camera.set_auto_scale_padding(100)  # Отступ для автомасштаба
        camera.follow(player1, player2)
        
        print(f"   Следование за двумя целями: {player1} и {player2}")
        
        # Симуляция движения целей
        for i in range(3):
            # Игроки расходятся
            player1.x -= 50
            player2.x += 50
            camera.update(1.0)
            
            center = camera.get_view().get_center()
            zoom = camera.get_zoom()
            print(f"   Кадр {i+1}: центр {center}, зум {zoom:.2f}")
        
        # 5. Эффекты камеры
        print("\n5. Эффекты камеры:")
        
        # Тряска камеры
        camera.shake(15)
        print("   Добавлена общая тряска")
        
        camera.shake_x(8)
        print("   Добавлена тряска по X")
        
        # Поворот камеры
        camera.set_target_angle(30)
        print("   Установлен поворот на 30°")
        
        # Зум
        camera.set_target_zoom(1.5)
        print("   Установлен зум 1.5x")
        
        # 6. Работа с View напрямую
        print("\n6. Работа с View:")
        view = camera.get_view()
        print(f"   Текущий View: {view}")
        
        # Временное изменение View
        with view.temporary_transform(center=(0, 0), angle=0) as temp_view:
            print(f"   Временный View: {temp_view}")
        
        print(f"   View после временных изменений: {view}")
        
        # 7. Ручное управление камерой
        print("\n7. Ручное управление (CameraMachine2D):")
        from Moon.python.Engine.Camera import CameraMachine2D
        
        manual_camera = CameraMachine2D(800, 600)
        manual_camera.set_position(Vector2f(100, 200))
        manual_camera.move(50, -30)
        
        print(f"   Позиция ручной камеры: {manual_camera.get_position()}")
        
        # Обновление ручной камеры
        manual_camera.update()
        manual_view = manual_camera.get_view()
        print(f"   View ручной камеры: {manual_view}")
        
    except Exception as e:
        print(f"Ошибка в демонстрации камеры: {e}")
        import traceback
        traceback.print_exc()

def performance_tips():
    print("\n=== Советы по производительности ===")
    print("1. Используйте меньшие значения lerp для более плавного движения")
    print("2. Отключайте автомасштабирование, если оно не нужно")
    print("3. Используйте CameraMachine2D для точного контроля")
    print("4. Применяйте эффекты тряски умеренно")
    print("5. Кэшируйте View, если он не изменяется часто")

if __name__ == "__main__":
    try:
        camera_demo()
        performance_tips()
    except ImportError as e:
        print(f"Ошибка импорта: {e}")
        print("Убедитесь, что все модули PySGL доступны")
    except Exception as e:
        print(f"Общая ошибка: {e}")
        print("Возможно, нативная библиотека PySGL.dll недоступна")