import time
import itertools
from threading import Thread, Lock, Semaphore
from typing import Any, Callable, Self

"""
Threader module
----------------
Small helper classes to run work in background threads. This module provides three
types of worker primitives used across the Moon framework:

- Worker: a simple one-shot worker that runs a callable in a background thread.
- CycleWorker: runs a callable repeatedly with a configurable delay between runs.
- PromiseWorker: executes a callable and stores its result (or exception) for
  later retrieval — similar to a very small, framework-specific "future".

This file only contains tiny helpers (no scheduling or pooling). The comments and
docstrings are intentionally verbose to match the style used in `Window.py`.
No runtime behaviour is changed.
"""

ID_COUNTER = itertools.count()


class WorkerUnit:
    """Base unit that provides a stable numeric id for workers.

    The id is generated from a module-level counter so every new instance gets
    a unique integer. Subclasses inherit this behaviour.
    """

    def __init__(self):
        # private id for the worker unit
        self.__id = next(ID_COUNTER)

    def get_id(self) -> int:
        """Return the worker's unique id.

        Returns:
            int: unique identifier assigned when the instance was created.
        """
        return self.__id

    def set_id(self, id: int):
        """Set a new id for the worker unit.

        This is provided for completeness and tests; in normal usage the id is
        assigned automatically at construction and shouldn't need changing.
        """
        self.__id = id


class Worker(WorkerUnit):
    """One-shot worker.

    Use case: run a short function in the background without caring about a
    return value. The supplied callable is run in a new Thread; it receives the
    `Worker` instance as the first argument, followed by any user arguments.
    """

    def __init__(self):
        super().__init__()
        # internal Thread object (None until start() is called)
        self.__thread: Thread | None = None
        # whether the created thread should be a daemon thread
        self.__daemon: bool = False

    def __str__(self) -> str:
        # Keep this light-weight: a short representation useful for debugging
        return f"Worker <{id=}"  # note: intentionally mirrors original formatting

    def set_daemon(self, value: bool) -> Self:
        """Mark the worker's thread as daemon (or not).

        Returns the instance for call chaining.
        """
        self.__daemon = value
        return self

    def get_daemon(self) -> bool:
        """Return whether the worker's thread will be a daemon."""
        return self.__daemon

    def start(self, func: Callable, *args, **kwargs):
        """Start the worker by spawning a Thread to run `func`.

        The target callable will be called with this Worker instance as the
        first positional argument, followed by any `args` and `kwargs` provided
        by the caller. The thread's daemon flag is controlled via
        `set_daemon` / `get_daemon`.
        """
        self.__thread = Thread(target=func, args=(self, *args), kwargs=kwargs, daemon=self.__daemon)
        self.__thread.start()

    def worked(self) -> bool:
        """Return True if the worker thread exists and is still running."""
        if self.__thread is None:
            return False
        return self.__thread.is_alive()


class CycleWorker(WorkerUnit):
    """Worker that repeatedly calls a function on a loop.

    Use this when you want a lightweight repeating task. The worker will call
    the provided function, sleep for `delay` seconds, then call again until
    `stop()` is called. The function receives the `CycleWorker` instance as
    its first argument, followed by the args/kwargs passed to `start()`.
    """

    def __init__(self):
        super().__init__()
        self.__thread: Thread | None = None
        self.__daemon: bool = False
        # delay between iterations (seconds)
        self.__delay: float = 0.0

        # runtime state
        self.__running: bool = True
        self.__function: Callable | None = None
        self.__args: tuple = ()
        self.__kwargs: dict = {}
        # number of iterations already executed
        self.__current_repeat_number: int = 0

    def __str__(self) -> str:
        return f"CycleWorker <{id=}"  # mirrors original formatting

    def set_daemon(self, value: bool) -> Self:
        self.__daemon = value
        return self

    def get_daemon(self) -> bool:
        return self.__daemon

    def set_delay(self, delay: float) -> Self:
        """Set the delay (in seconds) between function calls."""
        self.__delay = delay
        return self

    def get_delay(self) -> float:
        return self.__delay

    def stop(self):
        """Request the loop to finish after the current iteration.

        This flips the running flag; the thread will naturally exit its loop.
        """
        self.__running = False

    def reset(self):
        """Reset the worker so it can be started again.

        Note: this does not restart an existing thread; it clears the internal
        thread reference and marks the worker as runnable again.
        """
        self.__running = True
        self.__thread = None

    def __loop(self):
        # Private loop invoked inside the thread. Validate the function first.
        if self.__function is None:
            raise ValueError("Function not set")

        while True:
            # Call the user's function. It receives this CycleWorker as the
            # first parameter (consistent with Worker.start semantics).
            self.__function(self, *self.__args, **self.__kwargs)

            # Sleep between iterations. Small delays are OK; use 0 for tight
            # loops (but beware CPU usage).
            time.sleep(self.__delay)

            # Break out if stop() was requested.
            if not self.__running:
                break

            # Increment the iteration counter after a successful run.
            self.__current_repeat_number += 1

    def get_current_repeat(self) -> int:
        """Return how many iterations have already been completed."""
        return self.__current_repeat_number

    def start(self, func: Callable, *args, **kwargs):
        """Begin the repeating loop in a new thread.

        Args are stored and passed to the function each iteration. The thread
        will be created with the worker's daemon setting.
        """
        self.__function = func
        self.__args = args
        self.__kwargs = kwargs
        self.__thread = Thread(target=self.__loop, daemon=self.__daemon)
        self.__thread.start()

    def worked(self) -> bool:
        """Return True if the cycle thread exists and is alive."""
        if self.__thread is None:
            return False
        return self.__thread.is_alive()


class PromiseWorker(WorkerUnit):
    """Simple promise-like worker that captures a result or exception.

    Behaviour: set a promise callable with `set_promise`, then call `start()`
    to run it in a background thread. When finished, the result (or raised
    exception) will be stored and retrievable via `get_result()`; use
    `is_finish()` to check completion.
    """

    def __init__(self):
        super().__init__()
        # user-provided callable that should accept (worker, *args, **kwargs)
        self.__promise: Callable[["PromiseWorker", Any], Any] | None = None
        # holds the result or the exception instance raised by the promise
        self.__result: Any = None
        self.__daemon: bool = False

    def is_finish(self) -> bool:
        """Return True if the promise has completed (result is available)."""
        return self.__result is not None

    def get_result(self):
        """Return the stored result (or exception) from the promise.

        Note: callers should check `is_finish()` before calling this method to
        avoid receiving `None` while the promise is still running.
        """
        return self.__result

    def set_daemon(self, daemon: bool):
        """Set the daemon flag used when spawning the internal thread."""
        self.__daemon = daemon

    def get_daemon(self) -> bool:
        return self.__daemon

    def set_promise(self, promise: Callable[["PromiseWorker", Any], Any]):
        """Assign the callable that will run inside the worker thread."""
        self.__promise = promise

    def get_promise(self) -> Callable[["PromiseWorker", Any], Any] | None:
        return self.__promise

    def __promise_unit(self):
        """Internal wrapper executed inside the thread that calls the promise

        The result or any exception raised by the promise is captured into
        `self.__result` so callers can inspect it later.
        """
        if self.__promise is None:
            raise ValueError("PromiseWorker has no promise set")
        try:
            self.__result = self.__promise(self, *self.__args, **self.__kwargs)
        except Exception as e:
            # Store the exception so callers can see what went wrong.
            self.__result = e

    def start(self, *args, **kwargs):
        """Start the promise execution in a background thread.

        Any positional and keyword arguments are forwarded to the promise
        callable when it is executed.
        """
        self.__args = args
        self.__kwargs = kwargs
        self.__thread = Thread(target=self.__promise_unit, daemon=self.__daemon)
        self.__thread.start()


if __name__ == "__main__":
    # Small self-test / example: run a promise that sleeps and returns a sum.
    def resulter(w, a, b):
        time.sleep(2)
        return a + b


    pw = PromiseWorker()
    pw.set_promise(resulter)
    pw.start(5, 6)
    while True:
        if pw.is_finish():
            print(pw.get_result())
            break