"""
异步任务调度模块
@author 杨明树
"""


class AsyncManager(object):
    """异步任务管理器"""
    import pathos
    process_pool: pathos.multiprocessing.ProcessPool
    thread_pool: pathos.threading.ThreadPool

    @staticmethod
    def initialize():
        import pathos
        AsyncManager.process_pool = pathos.multiprocessing.ProcessPool()
        AsyncManager.thread_pool = pathos.threading.ThreadPool()

    @staticmethod
    def async_process(func):
        """创建异步进程"""

        def wrapper(*args, **kwargs):
            result = AsyncManager.process_pool.apipe(func, *args, **kwargs)
            return result

        return wrapper

    @staticmethod
    def async_thread(func):
        """创建异步线程"""

        def wrapper(*args, **kwargs):
            result = AsyncManager.thread_pool.apipe(func, *args, **kwargs)
            return result

        return wrapper
