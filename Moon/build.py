import os
import time
from colorama import Fore



# SETTINGS ===================================================
WINDOWS_COMPILER_PATH = "g++"
LINUX_COMPILER_PATH = "g++"

SFML_PATH = "D:/SFML-2.6.2"

OUTPUT_PATH = "Moon/dlls"
SOURCE_PATH = "Moon/src"

COMPILE_TARGET = "linux"   # 'window' or 'linux'
# SETTINGS ===================================================






SUCCES = f'[{Fore.GREEN}✔{Fore.RESET}]'
WARNING = f'[{Fore.YELLOW}warn{Fore.RESET}]'
PASS = f'[{Fore.GREEN}yes{Fore.RESET}]'



def WINDOW_COMPILE_SCRIPT_GET(compiler_path: str, sfml_path: str, output_path: str, source_path: str) -> str:
    return f"{compiler_path} -shared -o {output_path}/Moon.dll {source_path}/Moon.cpp -static \
            -static-libstdc++ -static-libgcc \
            -I {sfml_path}/include -L {sfml_path}/lib \
            -DSFML_STATIC \
            -lsfml-audio-s -lsfml-graphics-s -lsfml-window-s -lsfml-system-s \
            -lopenal32 -lflac -lvorbisenc -lvorbisfile -lvorbis -logg \
            -lopengl32 -lgdi32 -lwinmm -lfreetype"


def LINUX_COMPILE_SCRIPT_GET(compiler_path: str, sfml_path: str, output_path: str, source_path: str) -> str:
    return f"g++ -shared -fPIC -o {output_path}/Moon.so {source_path}/Moon.cpp -I include -lsfml-audio -lsfml-graphics -lsfml-window -lsfml-system"


# Получение списка файлов в указанной директории
def GET_BUILDED_FILES(path: str):
    files = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            files.append(file)
    return files

# Основная функция сборки проекта
def build():

    start_time = time.time()

    # Получение списка всех файлов
    all_files = GET_BUILDED_FILES(SOURCE_PATH)

    # Фильтрация файлов, которые нужно собрать (начинаются с "BUILDED")
    builded_files = list(filter(lambda x: x[0:7] == "BUILDED", all_files))

    print(f"{Fore.CYAN}Initing{Fore.RESET}: Founded [{Fore.BLACK}{len(all_files)}{Fore.RESET}] files")
    for file in all_files:
        if file in builded_files:
            print(f"  |-> <{Fore.GREEN}need build{Fore.RESET}> {Fore.YELLOW}{file}{Fore.RESET}")
        else:
            print(f"  |->              {Fore.YELLOW}{file}{Fore.RESET} ")


    print(f"\n{Fore.CYAN}Initing{Fore.RESET}: {Fore.BLACK}Start building...{Fore.RESET}")



    print(f"{Fore.BLUE}Building{Fore.RESET}: Generating builded file...")
    file = open(SOURCE_PATH+"/Moon.cpp", 'w', encoding="utf-8")
    for bf in builded_files:
            fp = SOURCE_PATH + "/" + bf
            print(fp)
            bff = open(fr"{fp}", 'r', encoding="utf-8")
            file.write(bff.read() + "\n")
            bff.close()

    file.close()

    # Сборка файла
    if COMPILE_TARGET == 'window':
        script = WINDOW_COMPILE_SCRIPT_GET(WINDOWS_COMPILER_PATH, SFML_PATH, OUTPUT_PATH, SOURCE_PATH)
    elif COMPILE_TARGET == 'linux':
        script = LINUX_COMPILE_SCRIPT_GET(LINUX_COMPILER_PATH, SFML_PATH, OUTPUT_PATH, SOURCE_PATH)
    print(script)
    os.system(script)
    # Удаление временного файла
    # os.remove(BUILD_FILES_PATH + "/" + "BUILD.cpp")
    # print(f"{Fore.BLUE}Building{Fore.RESET}: Deleting file... {SUCCES}")

    print(f"{Fore.BLUE}Building{Fore.RESET}: Building finished {round(time.time() - start_time, 2)}ms {SUCCES}")



if __name__ == "__main__":
    build()
