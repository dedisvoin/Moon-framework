"""
Пример использования улучшенного модуля Views
Демонстрирует новые возможности и безопасность работы с View и FloatRect
"""

import sys
sys.path.append("./")

from PySGL.python.Views import FloatRect, View, ViewError
from PySGL.python.Engine.Camera import Camera2D

def main():
    print("=== Демонстрация улучшенного модуля Views ===\n")
    
    # 1. Создание FloatRect с валидацией
    print("1. Создание FloatRect:")
    try:
        rect = FloatRect(10, 20, 100, 50)
        print(f"   Создан: {rect}")
        print(f"   Позиция: {rect.get_position()}")
        print(f"   Размер: {rect.get_size()}")
    except Exception as e:
        print(f"   Ошибка: {e}")
    
    # 2. Попытка создать FloatRect с отрицательными размерами
    print("\n2. Попытка создать FloatRect с отрицательными размерами:")
    try:
        bad_rect = FloatRect(0, 0, -10, 20)
    except ValueError as e:
        print(f"   Корректно перехвачена ошибка: {e}")
    
    # 3. Цепные вызовы методов
    print("\n3. Цепные вызовы методов FloatRect:")
    rect.set_position(x=50).set_size(w=200)
    print(f"   После изменений: {rect}")
    
    # 4. Создание View
    print("\n4. Создание View:")
    try:
        view = View(rect)
        print(f"   Создан: {view}")
        print(f"   Центр: {view.get_center()}")
        print(f"   Размер: {view.get_size()}")
        print(f"   Угол: {view.get_angle()}°")
    except Exception as e:
        print(f"   Ошибка: {e}")
        return  # Выходим, если не удалось создать View
    
    # 5. Цепные вызовы методов View
    print("\n5. Цепные вызовы методов View:")
    view.set_center(400, 300).set_angle(45).zoom(1.5)
    print(f"   После изменений: {view}")
    
    # 6. Контекстный менеджер для временных изменений
    print("\n6. Контекстный менеджер для временных изменений:")
    print(f"   До временных изменений: {view}")
    
    try:
        with view.temporary_transform(center=(100, 100), angle=90) as temp_view:
            print(f"   Во время временных изменений: {temp_view}")
        
        print(f"   После временных изменений: {view}")
    except Exception as e:
        print(f"   Ошибка контекстного менеджера: {e}")
    
    # 7. Валидация параметров
    print("\n7. Валидация параметров:")
    try:
        view.set_size(-10, 20)  # Должна вызвать ошибку
    except ValueError as e:
        print(f"   Корректно перехвачена ошибка размера: {e}")
    except Exception as e:
        print(f"   Неожиданная ошибка: {e}")
    
    try:
        view.zoom(-1)  # Должна вызвать ошибку
    except ValueError as e:
        print(f"   Корректно перехвачена ошибка масштаба: {e}")
    except Exception as e:
        print(f"   Неожиданная ошибка: {e}")
    
    # 8. Пример использования камеры
    print("\n8. Пример использования камеры:")
    try:
        # Создаем камеру 2D
        camera = Camera2D(800, 600)
        print(f"   Создана камера: размер {camera.get_size()}")
        
        # Настраиваем параметры камеры
        camera.set_lerp_movement(0.1).set_lerp_zoom(0.05)
        camera.set_target_zoom(1.2)
        
        # Следим за точкой
        from PySGL.python.Vectors import Vector2f
        target_pos = Vector2f(400, 300)
        camera.follow(target_pos)
        print(f"   Камера следует за точкой: {target_pos}")
        
        # Добавляем эффект тряски
        camera.shake(10)
        print("   Добавлен эффект тряски")
        
        # Поворачиваем камеру
        camera.set_target_angle(15)
        print("   Установлен поворот на 15°")
        
        # Получаем View камеры
        camera_view = camera.get_view()
        print(f"   View камеры: {camera_view}")
        
    except Exception as e:
        print(f"   Ошибка работы с камерой: {e}")
    
    print("\n=== Демонстрация завершена ===")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nОшибка выполнения: {e}")
        print("Возможно, нативная библиотека PySGL.dll недоступна.")
        print("Убедитесь, что библиотека находится в папке dlls/")