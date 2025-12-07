import os
import sys
import shutil
import argparse
import time
from datetime import datetime

os.system('cls')

# --- Константы путей ---
# (Предполагается, что эти пути существуют относительно места запуска скрипта)
ICON_PATH = "Moon/data/icons/default_app_icon.png"
FONT_PATH = "Moon/data/fonts/GNF.ttf"
DLLS_SRC_DIR = "Moon/dlls"

# --- Настройка Colorama ---
try:
    import colorama
    from colorama import Fore, Back, Style
    colorama.init()
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Заглушки для цветов если colorama не установлена
    class Colors:
        RED = YELLOW = GREEN = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
        LIGHTRED_EX = LIGHTYELLOW_EX = LIGHTGREEN_EX = LIGHTCYAN_EX = LIGHTMAGENTA_EX = ""
    Fore = Back = Style = Colors()

# --- Улучшенные функции вывода ---

def print_color(text, color=Fore.WHITE, style=Style.NORMAL):
    """Печать текста с цветом и стилем"""
    if COLORAMA_AVAILABLE:
        print(f"{style}{color}{text}{Style.RESET_ALL}")
    else:
        print(text)

def print_header(text):
    """Печать заголовка с разделителями"""
    separator = '═' * 60
    if COLORAMA_AVAILABLE:
        print(f"\n{Style.BRIGHT}{Fore.CYAN}{separator}{Style.RESET_ALL}")
        print(f"{Style.BRIGHT}{Fore.CYAN}{text:^60}{Style.RESET_ALL}")
        print(f"{Style.BRIGHT}{Fore.CYAN}{separator}{Style.RESET_ALL}")
    else:
        print(f"\n{'=' * 60}")
        print(f"{text:^60}")
        print(f"{'=' * 60}")

def print_section_header(text):
    """Печать заголовка секции"""
    print_color(f"\n{Style.BRIGHT}{Fore.MAGENTA}--- {text} ---{Style.RESET_ALL}")

def print_success(text):
    """Печать успешного сообщения"""
    print_color(f"✅ УСПЕХ: {text}", Fore.GREEN, Style.BRIGHT)

def print_warning(text):
    """Печать предупреждения"""
    print_color(f"⚠️  ПРЕДУПРЕЖДЕНИЕ: {text}", Fore.YELLOW, Style.BRIGHT)

def print_error(text):
    """Печать ошибки"""
    print_color(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {text}", Fore.RED, Style.BRIGHT)

def print_info(text):
    """Печать информационного сообщения"""
    print_color(f"ℹ️  {text}", Fore.BLUE)

def print_step(text):
    """Печать шага процесса"""
    print_color(f"\n➡️  ШАГ: {text}", Fore.CYAN, Style.BRIGHT)
    print_color("-" * (len(text) + 12), Fore.CYAN) # Добавим разделитель под шагом

# --- Логика скрипта ---

def parse_arguments():
    """Разбор аргументов командной строки"""
    parser = argparse.ArgumentParser(description='Скрипт сборки PySGL проекта с использованием Nuitka.')

    parser.add_argument('source_file', help='Исходный Python-файл для сборки.')
    parser.add_argument('--output-name', '-o', default=None,
                        help='Имя выходного исполняемого файла (без расширения).')
    parser.add_argument('--build-dir', '-b', default='build',
                        help='Временная папка для сборки (по умолчанию: build).')
    parser.add_argument('--output-dir', '-d', default=None,
                        help='Конечный каталог, куда будет перемещена собранная папка проекта.')
    parser.add_argument('--clean', '-c', action='store_true',
                        help='Очистить папку сборки перед началом.')
    parser.add_argument('--no-dlls', action='store_true',
                        help='Не копировать дополнительные DLLs из Moon/dlls.')
    parser.add_argument('--python-path', '-p', default=sys.executable,
                        help='Путь к интерпретатору Python (по умолчанию: текущий).')
    parser.add_argument('--data-dir', default=None,
                        help='Каталог с данными (текстуры, звуки и т.д.) для копирования.')
    parser.add_argument('--no-console', action='store_true',
                        help='Скрыть консоль при запуске exe-файла (только для Windows).')
    parser.add_argument('--keep-temp', '-k', action='store_true',
                        help='Сохранить временные папки Nuitka в папке сборки.')

    return parser.parse_args()

def get_nuitka_version(python_path):
    """Получение версии Nuitka"""
    try:
        import subprocess
        result = subprocess.run([python_path, '-m', 'nuitka', '--version'], capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n')[0] # Берем только первую строку
    except Exception as e:
        return f"Не удалось определить ({e})"

def show_build_configuration(args):
    """Показать конфигурацию сборки и запросить подтверждение"""
    print_header("КОНФИГУРАЦИЯ СБОРКИ ПРОЕКТА MOON")

    default_output_name = os.path.basename(args.source_file).split('.')[0]

    # Получение версии Nuitka
    nuitka_version = get_nuitka_version(args.python_path)

    config_items = [
        ("Исходный файл", args.source_file),
        ("Выходное имя EXE", args.output_name or default_output_name),
        ("Временная папка", args.build_dir),
        ("Конечная папка", args.output_dir or f"Сборка останется в: {args.build_dir}"),
        ("Очистка перед сб.", "Да" if args.clean else "Нет"),
        ("Копировать доп. DLL", "Нет (флаг --no-dlls)" if args.no_dlls else f"Да (из {DLLS_SRC_DIR})"),
        ("Python интерпретатор", args.python_path),
        ("Версия Nuitka", nuitka_version),
        ("Каталог данных", args.data_dir or "Не указан"),
        ("Консольный режим", "СКРЫТЬ (Windows-only)" if args.no_console else "ПОКАЗАТЬ"),
        ("Сохранить временные", "Да" if args.keep_temp else "Нет"),
        ("Путь к иконке", ICON_PATH),
        ("Путь к шрифту", FONT_PATH),
        ("Дата сборки", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ]

    for key, value in config_items:
        key_styled = f"{Style.BRIGHT}{Fore.CYAN}{key:<25}{Style.RESET_ALL}"
        value_styled = f"{Fore.WHITE}{value}{Style.RESET_ALL}"
        print(f"{key_styled} {value_styled}")

    print_color("\n" + '═' * 60, Fore.CYAN, Style.BRIGHT)

    response = input(f"{Style.BRIGHT}Начать сборку с указанной конфигурацией? (y/N): {Style.RESET_ALL}").strip().lower()
    return response in ['y', 'yes', 'д', 'да']

def prepare_build_environment(args):
    """Подготовка папки сборки"""
    print_step("Подготовка среды сборки и рабочего каталога")

    if args.clean and os.path.exists(args.build_dir):
        print_info(f"Обнаружен флаг --clean. Очистка папки сборки: {args.build_dir}")
        shutil.rmtree(args.build_dir)
        time.sleep(0.5) # Небольшая пауза после удаления

    if not os.path.exists(args.build_dir):
        print_info(f"Создание папки сборки: {args.build_dir}")
        os.makedirs(args.build_dir)
    else:
        print_info(f"Папка {args.build_dir} уже существует и будет использоваться.")

def copy_resource_file(source_path, dest_dir_name, args):
    """Общая функция для копирования иконки или шрифта"""
    if not os.path.exists(source_path):
        print_warning(f"Исходный ресурс не найден: {source_path}")
        return None

    resource_filename = os.path.basename(source_path)
    dest_path = os.path.join(args.build_dir, dest_dir_name)
    resource_dst = os.path.join(dest_path, resource_filename)

    # Создаем папку, если ее нет
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    try:
        print_info(f"Копирование '{resource_filename}' в '{dest_path}'")
        shutil.copy2(source_path, resource_dst)
        print_success(f"Ресурс скопирован: {resource_dst}")
        return resource_dst
    except Exception as e:
        print_error(f"Не удалось скопировать ресурс {resource_filename}: {e}")
        return None

def copy_data_directory(args):
    """Копирование каталога данных в папку сборки"""
    if not args.data_dir:
        return

    print_step("Копирование каталога данных проекта")
    
    if args.data_dir and os.path.exists(args.data_dir):
        data_dst_name = os.path.basename(args.data_dir)
        data_dst = os.path.join(args.build_dir, data_dst_name)
        
        if os.path.exists(data_dst):
            print_info(f"Очистка существующего каталога данных в билде: {data_dst_name}")
            shutil.rmtree(data_dst)

        try:
            print_info(f"Копирование рекурсивно: {args.data_dir} -> {data_dst}")
            shutil.copytree(args.data_dir, data_dst)
            print_success(f"Каталог данных '{data_dst_name}' скопирован.")
        except Exception as e:
            print_error(f"Ошибка при копировании каталога данных: {e}")
            raise
    else:
        print_warning(f"Каталог данных не найден: {args.data_dir}. Пропуск шага.")

def copy_extra_dlls(args):
    """Копирование дополнительных DLLs (если не отключено)"""
    if args.no_dlls:
        print_info("Копирование дополнительных DLLs пропущено (флаг --no-dlls).")
        return

    print_step("Копирование дополнительных DLLs")

    dlls_dst = os.path.join(args.build_dir, os.path.basename(DLLS_SRC_DIR))
    
    if not os.path.exists(DLLS_SRC_DIR):
        print_warning(f"Папка дополнительных DLLs не найдена: {DLLS_SRC_DIR}. Пропуск шага.")
        return

    if os.path.exists(dlls_dst):
        print_info(f"Очистка существующих DLLs в билде: {dlls_dst}")
        shutil.rmtree(dlls_dst)

    try:
        print_info(f"Копирование содержимого '{DLLS_SRC_DIR}' в '{dlls_dst}'")
        shutil.copytree(DLLS_SRC_DIR, dlls_dst)
        print_success("Дополнительные DLLs успешно скопированы.")
    except Exception as e:
        print_error(f"Ошибка при копировании DLLs: {e}")
        raise

def build_project(args):
    """Запуск сборки через Nuitka"""
    python_path = args.python_path
    source_file = args.source_file
    output_name = args.output_name or os.path.basename(source_file).split('.')[0]

    # --- Формирование команды Nuitka ---
    build_params = [
        f'"{python_path}" -m nuitka',
        source_file,
        # Используем --onefile и --standalone вместе (Nuitka предпочтет --onefile,
        # но --standalone может быть полезен для других режимов)
        '--onefile',
        '--standalone',
        f'--show-progress', # Показать прогресс
        f'--show-scons',    # Показать команду Scons, чтобы лучше понять ошибки
        f'--output-filename={output_name}.exe',
        f'--windows-icon-from-ico={ICON_PATH}' # Применяем иконку
    ]

    # Убираем флаг --remove-output если нужно сохранить временные файлы
    if not args.keep_temp:
        build_params.append('--remove-output')
        print_info("Временные файлы Nuitka будут удалены (--remove-output)")
    else:
        print_info("Временные файлы Nuitka будут сохранены (флаг --keep-temp)")

    # Добавляем специфичные флаги для Windows
    if os.name == 'nt':
        # Принудительное использование MinGW64 (может понадобиться для C-расширений)
        # Внимание: с Python 3.13 может не работать, как было сказано ранее!
        # Но оставляем, т.к. пользователь его использовал.
        build_params.append('--mingw64')

        # Добавляем параметр для скрытия консоли
        if args.no_console:
            build_params.append('--windows-console-mode=disable')
            print_info("Режим сборки: Windows-GUI (БЕЗ КОНСОЛИ)")
        else:
            print_info("Режим сборки: Windows-Console (С КОНСОЛЬЮ)")
    
    # Рекомендуемый флаг для PySGL/Pygame-подобных проектов
    # print_info("Добавление ключа --assume-yes-for-imports для надежного включения скрытых импортов.")
    # build_params.append('--assume-yes-for-imports=PyQt5,PySide6,pygame') 
    # (Раскомментировать, если это нужно для PySGL)

    build_command = ' '.join(build_params)

    print_header("ЗАПУСК NUITKA")
    print_info(f"Выполняемая команда: {build_command}")
    print_step(f"Запуск компиляции {source_file} в {output_name}.exe...")

    start_time = time.time()
    
    # Используем os.system, т.к. это самый простой способ
    # для запуска команды, которая сама выводит много логов.
    exit_code = os.system(build_command)
    
    build_time = time.time() - start_time

    if exit_code != 0:
        # В случае ошибки Nuitka, exit_code обычно не равен 0
        raise RuntimeError(f"Nuitka завершилась с ошибкой (код завершения: {exit_code}). Пожалуйста, проверьте логи выше.")

    print_success(f"Nuitka сборка завершена успешно за {build_time:.2f} секунд.")

def move_temp_files_to_build_dir(args):
    """Перемещение временных файлов Nuitka в папку сборки"""
    print_step("Перемещение временных файлов Nuitka")
    
    source_file = args.source_file
    base_name = os.path.basename(source_file).split('.')[0]
    
    # Nuitka создает несколько временных папок:
    # 1. {имя_файла}.build/ - основная папка сборки
    # 2. {имя_файла}.dist/ - папка дистрибутива (для standalone)
    # 3. {имя_файла}.onefile-build/ - для onefile режима
    
    temp_folders = [
        f"{base_name}.build",
        f"{base_name}.dist", 
        f"{base_name}.onefile-build"
    ]
    
    moved_count = 0
    temp_dest_dir = os.path.join(args.build_dir, "nuitka_temp")
    
    # Создаем папку для временных файлов
    if not os.path.exists(temp_dest_dir):
        os.makedirs(temp_dest_dir)
    
    for folder in temp_folders:
        if os.path.exists(folder):
            try:
                dest_path = os.path.join(temp_dest_dir, folder)
                
                # Если папка уже существует в назначении, удаляем ее
                if os.path.exists(dest_path):
                    shutil.rmtree(dest_path)
                
                print_info(f"Перемещение '{folder}' -> '{temp_dest_dir}'")
                shutil.move(folder, dest_path)
                moved_count += 1
                print_success(f"Временная папка '{folder}' перемещена.")
            except Exception as e:
                print_warning(f"Не удалось переместить временную папку '{folder}': {e}")
    
    if moved_count > 0:
        print_success(f"Перемещено {moved_count} временных папок Nuitka в: {temp_dest_dir}")
    else:
        print_info("Временные папки Nuitka не найдены (возможно, уже были удалены).")

def finalize_build(args):
    """Перенос собранных файлов в финальную папку"""
    print_header("ФИНАЛИЗАЦИЯ СБОРКИ И ПЕРЕМЕЩЕНИЕ ФАЙЛОВ")

    output_name = args.output_name or os.path.basename(args.source_file).split('.')[0]
    exe_file = f"{output_name}.exe"

    # --- Перемещение временных файлов Nuitka (если нужно) ---
    if args.keep_temp:
        move_temp_files_to_build_dir(args)
    
    # --- Копирование ресурсов ---
    copy_resource_file(ICON_PATH, "icons", args)
    copy_resource_file(FONT_PATH, "fonts", args)
    
    # Копирование DLLs и данных
    copy_extra_dlls(args)
    copy_data_directory(args)

    # --- Перенос .exe в папку сборки ---
    if os.path.exists(exe_file):
        print_step(f"Перемещение исполняемого файла: {exe_file}")
        
        # Переносим только EXE в папку build_dir, т.к. Nuitka с --onefile
        # создает его в корневой папке.
        shutil.move(exe_file, os.path.join(args.build_dir, exe_file))
        print_success(f"Исполняемый файл перемещен в: {os.path.join(args.build_dir, exe_file)}")
    else:
        raise FileNotFoundError(f"Собранный файл '{exe_file}' не найден. Проверьте логи Nuitka на наличие ошибок.")

    # --- Перенос в финальную папку (если указана) ---
    if args.output_dir:
        final_dir_name = f"{output_name}_build_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        final_dir = os.path.join(args.output_dir, final_dir_name)
        
        # Гарантируем существование конечной папки
        if not os.path.exists(args.output_dir):
             os.makedirs(args.output_dir)

        print_step(f"Перемещение всей сборки в конечный каталог")
        print_info(f"Перенос '{args.build_dir}' -> '{final_dir}'")
        
        # Переименовываем и перемещаем папку сборки
        shutil.move(args.build_dir, final_dir)
        
        print_success(f"Сборка завершена! Результат: {final_dir}")
        return final_dir
    else:
        print_success(f"Сборка завершена! Результат: {args.build_dir}")
        return args.build_dir

# --- Основная функция ---

def main():
    start_time = time.time()
    
    # ASCII арт и заголовок
    if COLORAMA_AVAILABLE:
        print(Fore.BLUE,'''

                    MOON  BUILD  SYSTEM
                      (by Pavlov Ivan)
                                            ''', Fore.RESET)
    
    print_header("MOON BUILD SYSTEM V2.0")

    try:
        if not COLORAMA_AVAILABLE:
            print_warning("Модуль Colorama не установлен. Цветовой вывод отключен. Установите: pip install colorama")
        
        print_info(f"Скрипт запущен: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        args = parse_arguments()

        if not os.path.exists(args.source_file):
            raise FileNotFoundError(f"Исходный файл не найден: {args.source_file}")

        # Показать конфигурацию и запросить подтверждение
        if not show_build_configuration(args):
            print_error("Сборка отменена пользователем.")
            sys.exit(0)

        # Процесс сборки
        prepare_build_environment(args)
        build_project(args)
        result_dir = finalize_build(args)

        # Финальный отчет
        total_time = time.time() - start_time
        minutes, seconds = divmod(total_time, 60)

        print_header("СБОРКА УСПЕШНО ЗАВЕРШЕНА! 🎉")
        print_success(f"Общее время сборки: {int(minutes)} мин {seconds:.2f} сек")
        print_success(f"Итоговый каталог: {result_dir}")
        
        print_info(f"Режим консоли: {'СКРЫТ' if args.no_console else 'ПОКАЗАН'}")
        print_info(f"Временные файлы: {'СОХРАНЕНЫ в nuitka_temp/' if args.keep_temp else 'УДАЛЕНЫ'}")
        
        if COLORAMA_AVAILABLE:
            print(f"\n{Style.BRIGHT}{Fore.GREEN}🚀 Готово! Ваш проект собран и находится в указанном каталоге.{Style.RESET_ALL}")
        else:
            print("\n🚀 Готово! Ваш проект собран и находится в указанном каталоге.")

    except (RuntimeError, FileNotFoundError) as e:
        total_time = time.time() - start_time
        print_error(f"Сборка прервана. Причина: {str(e)}")
        print_error(f"Общее время до ошибки: {total_time:.2f} секунд.")
        print_header("❌ СБОРКА ПРЕРВАНА")
        sys.exit(1)
    except Exception as e:
        total_time = time.time() - start_time
        print_error(f"Произошла непредвиденная ошибка: {type(e).__name__}: {str(e)}")
        print_error(f"Общее время до ошибки: {total_time:.2f} секунд.")
        print_header("❌ СБОРКА ПРЕРВАНА")
        sys.exit(1)

if __name__ == "__main__":
    main()