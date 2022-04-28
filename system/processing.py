import os
import time
from multiprocessing import Pool


def mi(*args):
    queue = args[0]
    key = args[1]
    queue.put([key, f'PID: {os.getpid()}'])
    time.sleep(3)


def create_process(method, *args):
    """创建一个子进程任务"""
    iterator = (args[0], args[1])

    with Pool(5) as p:
        for x in range(5):
            p.apply_async(method, iterator)
        p.close()
        p.join()
