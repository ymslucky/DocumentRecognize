def jl_task_initialize(application):
    """任务模块初始化"""
    from jl_task.async_task import AsyncManager
    AsyncManager.initialize()

    from jl_task.timed_task import TaskScheduler
    TaskScheduler.initialize(application)
