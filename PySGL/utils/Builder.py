import os
import sys
import shutil
import argparse

def parse_arguments():
    """Разбор аргументов командной строки"""
    parser = argparse.ArgumentParser(description='Скрипт сборки PySGL проекта')
    
    parser.add_argument('source_file', help='Исходный Python-файл для сборки')
    parser.add_argument('--output-name', '-o', default=None, 
                       help='Имя выходного исполняемого файла (без расширения)')
    parser.add_argument('--build-dir', '-b', default='build',
                       help='Временная папка для сборки')
    parser.add_argument('--output-dir', '-d', default=None,
                       help='Куда переместить собранный проект')
    parser.add_argument('--clean', '-c', action='store_true',
                       help='Очистить папку сборки перед началом')
    parser.add_argument('--no-dlls', action='store_true',
                       help='Не копировать DLLs')
    parser.add_argument('--python-path', '-p', default=sys.executable,
                       help='Путь к интерпретатору Python (по умолчанию: текущий)')
    
    return parser.parse_args()

def prepare_build_environment(args):
    """Подготовка папки сборки"""
    if args.clean and os.path.exists(args.build_dir):
        shutil.rmtree(args.build_dir)
    
    if not os.path.exists(args.build_dir):
        os.makedirs(args.build_dir)

def build_project(args):
    """Запуск сборки через Nuitka"""
    python_path = args.python_path
    source_file = args.source_file
    output_name = args.output_name or os.path.basename(source_file).split('.')[0]
    
    build_command = (
        f'"{python_path}" -m nuitka {source_file} '
        '--onefile --standalone --verbose '
        '--remove-output --show-progress '
        f'--output-filename={output_name}.exe'
    )
    
    print(f"Сборка {source_file}...")
    exit_code = os.system(build_command)
    
    if exit_code != 0:
        raise RuntimeError(f"Ошибка сборки (код {exit_code})")

def finalize_build(args):
    """Перенос собранных файлов в финальную папку"""
    output_name = args.output_name or os.path.basename(args.source_file).split('.')[0]
    exe_file = f"{output_name}.exe"
    
    # Копирование DLLs (если не отключено)
    if not args.no_dlls:
        dlls_src = "PySGL/dlls"
        dlls_dst = os.path.join(args.build_dir, "dlls")
        if os.path.exists(dlls_src):
            shutil.copytree(dlls_src, dlls_dst)
        else:
            print(f"⚠ Предупреждение: папка DLLs не найдена ({dlls_src})")
    
    # Перенос .exe в папку сборки
    if os.path.exists(exe_file):
        shutil.move(exe_file, os.path.join(args.build_dir, exe_file))
    else:
        raise FileNotFoundError(f"Собранный файл {exe_file} не найден")
    
    # Перенос в финальную папку (если указана)
    if args.output_dir:
        final_dir = os.path.join(args.output_dir, f"build.{output_name}")
        shutil.move(args.build_dir, final_dir)
        print(f"✅ Сборка завершена! Результат: {final_dir}")
    else:
        print(f"✅ Сборка завершена! Результат: {args.build_dir}")

def main():
    try:
        args = parse_arguments()
        prepare_build_environment(args)
        build_project(args)
        finalize_build(args)
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()