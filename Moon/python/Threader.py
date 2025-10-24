import time
import itertools
from threading import Thread
from typing import Any, Callable, Self

ID_COUNTER = itertools.count()

class WorkerUnit:
    def __init__(self):
        self.__id = next(ID_COUNTER)

    def get_id(self) -> int:
        return self.__id

    def set_id(self, id: int):
        self.__id = id


class Worker(WorkerUnit):
    def __init__(self):
        super().__init__()
        self.__thread: Thread | None = None
        self.__daemon: bool = False

    def __str__(self) -> str:
        return f"Worker <{id=}"

    def set_daemon(self, value: bool) -> Self:
        self.__daemon = value
        return self

    def get_daemon(self) -> bool:
        return self.__daemon

    def start(self, func: Callable, *args, **kwargs):
        self.__thread = Thread(target=func, args=(self, *args), kwargs=kwargs, daemon=self.__daemon)
        self.__thread.start()

    def worked(self) -> bool:
        if self.__thread is None:
            return False
        return self.__thread.is_alive()

class CycleWorker(WorkerUnit):
    def __init__(self):
        super().__init__()
        self.__thread: Thread | None = None
        self.__daemon: bool = False
        self.__delay: float = 0.0

        self.__running: bool = True
        self.__function: Callable | None = None
        self.__args: tuple = ()
        self.__kwargs: dict = {}
        self.__current_repeat_number: int = 0

    def __str__(self) -> str:
        return f"CycleWorker <{id=}"

    def set_daemon(self, value: bool) -> Self:
        self.__daemon = value
        return self

    def get_daemon(self) -> bool:
        return self.__daemon

    def set_delay(self, delay: float) -> Self:
        self.__delay = delay
        return self

    def get_delay(self) -> float:
        return self.__delay

    def stop(self):
        self.__running = False

    def reset(self):
        self.__running = True
        self.__thread = None

    def __loop(self):
        if self.__function is None:
            raise ValueError("Function not set")

        while True:
            self.__function(self, *self.__args, **self.__kwargs)
            time.sleep(self.__delay)
            if not self.__running:
                break
            self.__current_repeat_number += 1

    def get_current_repeat(self) -> int:
        return self.__current_repeat_number

    def start(self, func: Callable, *args, **kwargs):
        self.__function = func
        self.__args = args
        self.__kwargs = kwargs
        self.__thread = Thread(target=self.__loop, daemon=self.__daemon)
        self.__thread.start()

    def worked(self) -> bool:
        if self.__thread is None:
            return False
        return self.__thread.is_alive()

class PromiseWorker(WorkerUnit):
    def __init__(self):
        super().__init__()
        self.__promise: Callable[["PromiseWorker", Any], Any] | None = None
        self.__result: Any = None
        self.__daemon: bool = False

    def set_daemon(self, daemon: bool):
        self.__daemon = daemon

    def get_daemon(self) -> bool:
        return self.__daemon

    def set_promise(self, promise: Callable[["PromiseWorker", Any], Any]):
        self.__promise = promise

    def get_promise(self) -> Callable[["PromiseWorker", Any], Any] | None:
        return self.__promise

    def __promise_unit(self):
        if self.__promise is None:
            raise ValueError("PromiseWorker has no promise set")
        try:
            self.__result = self.__promise(self, *self.__args, **self.__kwargs)
        except Exception as e:
            self.__result = e

    def start(self, *args, **kwargs):
        self.__function = self.__promise
        self.__args = args
        self.__kwargs = kwargs
        self.__thread = Thread(target=self.__promise_unit, daemon=self.__daemon)
        self.__thread.start()

# w = CycleWorker()
# w2 = CycleWorker()

# def test(worker: CycleWorker):
#     print(f"worker {worker.get_id()}, repeat {worker.get_current_repeat()}")
#     if worker.get_current_repeat() >= 10:
#         worker.stop()
#         print(f"Worker {worker.get_id()} stopped after {worker.get_current_repeat()} repeats.")

# w.set_delay(0.1)
# w.start(test)

# w2.set_delay(1)
# w2.start(test)
