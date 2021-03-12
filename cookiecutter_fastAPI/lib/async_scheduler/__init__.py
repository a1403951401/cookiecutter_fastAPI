import asyncio
import os
from asyncio import Task, BoundedSemaphore
from asyncio.exceptions import CancelledError
from threading import Lock
from typing import Union, Dict, Coroutine, Any, TextIO


class AsyncScheduler:
    __slots__ = ('_lock', '_task_semaphore', '_task_map', 'stack_limit', 'stack_file')

    max_workers: int
    _lock: Lock
    _task_bucket: BoundedSemaphore
    _task_map: Dict[Task, Coroutine]
    stack_limit: Union[bool, int]
    stack_file: TextIO

    def __init__(self, max_workers=None, stack_limit: Union[bool, int] = 0, stack_file: TextIO = None):
        if max_workers is None:
            max_workers = min(32, (os.cpu_count() or 1) + 4)
        if max_workers <= 0:
            raise ValueError("max_workers must be greater than 0")
        self._lock = Lock()
        self._task_semaphore = BoundedSemaphore(max_workers)
        self._task_map = {}

        self.stack_limit = stack_limit
        self.stack_file = stack_file

    @property
    def loop(self):
        return asyncio.get_event_loop()

    def _task_done(self, task: Task) -> None:
        with self._lock:
            coroutine = self._task_map.pop(task)
            try:
                if task.exception() and self.stack_limit:
                    task.print_stack(limit=None if self.stack_limit is True else self.stack_limit, file=self.stack_file)
            except CancelledError:
                coroutine.close()

    async def __task(self, coroutine: Coroutine, delay=0) -> Any:
        await asyncio.sleep(delay)
        async with self._task_semaphore:
            return await coroutine

    def create_task(self, coroutine: Coroutine, delay: Union[int, float] = 0) -> Task:
        """
        创建 任务
        :param coroutine: 协程任务对象
        :param delay:     等待间隔
        :return:          Task 对象
        """
        with self._lock:
            task = self.loop.create_task(self.__task(coroutine, delay))
            self._task_map[task] = coroutine
            task.add_done_callback(self._task_done)
            return task

    def __len__(self) -> int:
        with self._lock:
            return len(self._task_map)

    @property
    def task(self) -> list:
        with self._lock:
            return list(self._task_map.keys())
