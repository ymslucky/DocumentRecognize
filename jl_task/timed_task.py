"""
定时任务
@author 杨明树
"""


class SchedulerConfig(object):
    """任务调度器配置类"""
    import os
    from apscheduler.executors.pool import ThreadPoolExecutor
    # 配置时区
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    # 线程池配置，最大{CPU核心数}个线程
    SCHEDULER_EXECUTORS = {
        'default': ThreadPoolExecutor(os.cpu_count())
    }
    '''
    1.超时任务不堆积
    2.最大同时执行实例20
    3.最大超时时间1小时
    '''
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 20,
        'misfire_grace_time': 3600
    }
    # 调度器API开关开启
    SCHEDULER_API_ENABLED = True


class TaskScheduler(object):
    from flask import Flask
    from flask_apscheduler import APScheduler

    scheduler: APScheduler

    @staticmethod
    def initialize(application: Flask):
        application.config.from_object(SchedulerConfig())

        from flask_apscheduler import APScheduler
        from apscheduler.schedulers.background import BackgroundScheduler
        TaskScheduler.scheduler = APScheduler(BackgroundScheduler(timezone='Asia/Shanghai'))
        TaskScheduler.scheduler.init_app(application)
        TaskScheduler.scheduler.start()
