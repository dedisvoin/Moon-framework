import os
import shutil
from time import sleep, time

def next_version():
    # сделай чтобы открывался файл pyproject.toml и версия менялась не следующую
    with open('pyproject.toml', 'r') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        if lines[i].startswith('version'):
            version_line = lines[i]
            # Извлекаем текущий номер версии
            current_version = version_line.split('=')[1].strip().strip('"')

            # Разделяем на мажорную, минорную и патч-версию
            parts = list(map(int, current_version.split('.')))

            # Увеличиваем патч-версию
            parts[-1] += 1

            # Собираем новую версию
            new_version = ".".join(map(str, parts))

            # Заменяем строку версии
            lines[i] = f'version = "{new_version}"\n'
            break

    with open('pyproject.toml', 'w') as f:
        f.writelines(lines)

    print(f"Version updated to: {new_version}")

next_version()

input("Press Enter to continue...")

start_time = time()
if os.path.exists('dist'):
    shutil.rmtree('dist')



KEY = open(r"C:\Users\WhoIsWho\Desktop\moon_token.txt", 'r').read()
os.system("python -m build")


import threading

def enter_key():
    import keyboard

    sleep(5)

    keyboard.write(KEY, delay=0.01)
    keyboard.send("enter")


threading.Thread(target=enter_key).start()


os.system("python -m twine upload dist/*")

if os.path.exists('dist'):
    shutil.rmtree('dist')

if os.path.exists('MoonFramework.egg-info'):
    shutil.rmtree('MoonFramework.egg-info')

end_time = time()
print(f"Time taken: {end_time - start_time}s")
