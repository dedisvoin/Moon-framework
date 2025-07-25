import sys
sys.path.append("./")
from PySGL.python.Process import *

def test(process, arg):
    time.sleep(arg)
    print("Process waited:", arg)


p = Process().set_function(test, 1).create_thread()
p.start()
p = Process().set_function(test, 4).create_thread()
p.start()
p = Process().set_function(test, 2).create_thread()
p.start()

def cyclic_task(process: CyclicalProcess, name: str):
    print(f"[{name}] Cyclic task running at {time.strftime('%H:%M:%S')}")
    # Здесь может быть ваша логика
    time.sleep(0.1)  # Небольшая задержка для демонстрации

# Создание циклического процесса
cyclic_process = (CyclicalProcess()
                .set_function(cyclic_task, "Worker 1")
                .set_sleep(1.0)  # Интервал 1 секунда между выполнениями
                .create_thread()
                .start())

# Даем поработать 5 секунд
time.sleep(5)

# Остановка процесса
cyclic_process.stop()
print("Process stopped")

