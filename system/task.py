import pathos.multiprocessing


class TaskConfig(object):
    """
    任务调度器
    @author 杨明树
    @date 2022-04-08
    """
    # 定时任务调度器
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()

    # 进程池
    pool: pathos.multiprocessing.ProcessPool = None

    @staticmethod
    def initialize(app):
        """调度器初始化"""
        from pathos.multiprocessing import ProcessPool as Pool
        from apscheduler.schedulers.background import BackgroundScheduler

        # 默认使用CPU核心数创建进程池大小，即调用os.cpu_count()
        TaskConfig.pool = Pool()

        if not TaskConfig.scheduler:
            TaskConfig.scheduler = BackgroundScheduler()
        TaskConfig.scheduler.__init__(app=app)
        TaskConfig.scheduler.start()
        if not TaskConfig.scheduler.running:
            from system.errors import ServerError
            raise ServerError('定时任务调度器启动失败！')

    @staticmethod
    def create_process_block(**kwargs):
        """创建一个进程任务,立即执行,异步阻塞"""
        p = TaskConfig.pool
        task = kwargs.get('task')
        parameter = kwargs.get('param')
        pipe_result = p.pipe(task, **parameter)
        return pipe_result

    @staticmethod
    def create_process_async(**kwargs):
        """创建一个进程任务,立即执行,异步非阻塞
        :rtype: object
        """
        p = TaskConfig.pool
        task = kwargs.get('task')
        parameter = kwargs.get('param')
        pipe_result = p.apipe(task, **parameter)
        return pipe_result

    @staticmethod
    def get_jobs():
        """获取调度器中正在执行的定时任务"""
        return TaskConfig.scheduler.get_jobs()
