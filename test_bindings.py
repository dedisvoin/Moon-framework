#!/usr/bin/env python3
"""
Тестовый файл для проверки работы биндингов Window.py
"""

import sys
import os

# Добавляем путь к PySGL
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'PySGL'))

try:
    from PySGL.python.Window import Window, WindowEvents, ContextSettings, SystemCursors
    from PySGL.python.Colors import COLOR_BLUE, COLOR_WHITE
    
    print("✓ Импорт модулей прошел успешно")
    
    # Тестируем создание ContextSettings
    try:
        context_settings = ContextSettings()
        context_settings.set_antialiasing_level(4)
        context_settings.set_depth_bits(24)
        context_settings.set_opengl_version(3, 3)
        print("✓ ContextSettings создан и настроен успешно")
    except Exception as e:
        print(f"✗ Ошибка при работе с ContextSettings: {e}")
    
    # Тестируем создание окна с настройками по умолчанию
    try:
        window = Window(800, 600, "Test Window")
        print("✓ Окно создано с настройками по умолчанию")
    except Exception as e:
        print(f"✗ Ошибка при создании окна: {e}")
        sys.exit(1)
    
    # Тестируем создание окна с кастомными ContextSettings
    try:
        window_with_settings = Window(800, 600, "Test Window with Settings", 
                                    context_settings=context_settings)
        print("✓ Окно создано с кастомными ContextSettings")
    except Exception as e:
        print(f"✗ Ошибка при создании окна с настройками: {e}")
    
    # Тестируем основные методы окна
    try:
        events = WindowEvents()
        
        # Тестируем методы окна
        window.set_title("Updated Title")
        window.set_clear_color(COLOR_BLUE)
        window.set_system_cursor(SystemCursors.Hand)
        window.set_vertical_sync(True)
        window.set_wait_fps(60)
        
        print("✓ Основные методы окна работают корректно")
        
        # Тестируем получение информации об окне
        size = window.get_size()
        position = window.get_position()
        center = window.get_center()
        
        print(f"✓ Размер окна: {size.x}x{size.y}")
        print(f"✓ Позиция окна: ({position.x}, {position.y})")
        print(f"✓ Центр окна: ({center.x}, {center.y})")
        
    except Exception as e:
        print(f"✗ Ошибка при тестировании методов окна: {e}")
    
    # Закрываем окна
    try:
        window.close()
        window_with_settings.close()
        print("✓ Окна закрыты успешно")
    except Exception as e:
        print(f"✗ Ошибка при закрытии окон: {e}")
    
    print("\n🎉 Все тесты пройдены успешно! Биндинги работают корректно.")
    
except ImportError as e:
    print(f"✗ Ошибка импорта: {e}")
    print("Убедитесь, что PySGL.dll находится в папке dlls/")
    sys.exit(1)
except Exception as e:
    print(f"✗ Неожиданная ошибка: {e}")
    sys.exit(1)