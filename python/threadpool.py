# -*- coding: utf-8 -*-
#

import logging
import time
import queue, threading
from threading import Condition, Lock
from threading import Thread


class _Worker(Thread):
    """
    worker thread which get task from queue to execute
    """

    def __init__(self, thread_name, work_queue, parent):
        threading.Thread.__init__(self, name=thread_name)
        self.__logger = logging.getLogger(thread_name)
        self.__parent = parent
        self.__workQueue = work_queue
        self.stop = False

    def run(self):
        while not self.stop:
            try:
                callback = self.__workQueue.get(timeout=10)
                task = callback[0]
                param = callback[1]
                if task is None:
                    continue
                try:
                    if param is not None:
                        task(*param)
                    else:
                        task()
                except Exception as e:
                    self.__logger.exception("")
                finally:
                    self.__parent.complete_task()
            except IOError:
                pass
            except queue.Empty:
                pass
            except Exception as e:
                self.__logger.error("%s get task from queue failed: %s", self.name, e)


class _ThreadPool(object):

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
            cls.__logger = logging.getLogger("thread_pool")
        return cls._instance

    def initialize(self, worker_count=2):
        self.__work_queue = queue.Queue()
        self._unfinished_tasks = 0
        self._condition = Condition(Lock())
        self.__worker_count = worker_count
        self.__workers = []
        for i in range(self.__worker_count):
            worker = _Worker("_Worker-" + str(i + 1), self.__work_queue, self)
            worker.start()
            self.__workers.append(worker)

    def stop(self):
        """
        Wait for each of them to terminate
        """
        while self.__workers:
            worker = self.__workers.pop()
            worker.stop = True
            self.__work_queue.put(None)

    def add_task(self, callback):
        if callback is not None:
            self._condition.acquire()
            self._unfinished_tasks += 1
            # self.__logger.info("add_task: num:%d", self._unfinished_tasks)
            self._condition.release()
            self.__work_queue.put((callback, None))

    def add_task_with_param(self, callback, param):
        if callback is not None:
            self._condition.acquire()
            self._unfinished_tasks += 1
            # self.__logger.info("add_task_with_param: num:%d", self._unfinished_tasks)
            self._condition.release()
            self.__work_queue.put((callback, param))

    def complete_task(self):
        self._condition.acquire()
        try:
            unfinished = self._unfinished_tasks - 1
            if unfinished <= 0:
                if unfinished < 0:
                    self.__logger.error('task_done() called too many times')
                self._condition.notify_all()
            self._unfinished_tasks = unfinished
            self.__logger.info('Thread pool has %d unfinished tasks', self._unfinished_tasks)
        finally:
            self._condition.release()

    def clear_task(self):
        self._condition.acquire()
        while not self.__work_queue.empty():
            try:
                task = self.__work_queue.get()
                self._unfinished_tasks -= 1
                self.__logger.error('Thread pool has unfinished task:%s', str(task))
            except Exception as ex:
                self.__logger.error("%s clear_task: %r failed due to %s", self.name, str(ex))
        self._condition.release()

    def wait_for_complete(self, timeout=None):
        start = time.time()
        self._condition.acquire()
        try:
            while self._unfinished_tasks:
                self._condition.wait(600)
                if timeout is not None:
                    current = time.time()
                    if (current - start) > timeout:
                        self.__logger.info('Thread pool timeout')
                        break
        finally:
            self._condition.release()


ThreadPool = _ThreadPool.instance()
