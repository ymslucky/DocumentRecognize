import os


def get_project_path():
    """得到项目路径"""
    return os.path.abspath(os.path.dirname(__file__) + '/../') + '\\'


def temp_file_clear():
    """删除临时文件"""
    path = os.path.abspath(get_project_path() + os.getenv('TEMP_DIR')) + '\\'
    if os.path.exists(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for directory in dirs:
                os.rmdir(os.path.join(root, directory))
    import logging
    logger = logging.getLogger('DRLog')
    logger.info('已执行定时任务：临时文件清除！')


def time_check(func):
    """函数计时"""

    def wrap(*args, **kwargs):
        from logging import getLogger
        import time
        start_time = time.time()
        res = func(*args, **kwargs)
        logger = getLogger("DRLog")
        logger.info(f'{func}耗时: {time.time() - start_time}')
        return res

    return wrap


def path_exchange(file_path: str):
    """路径转换"""
    import re

    file_path = re.sub(r'[\\]+', '/', file_path)
    file_path = re.sub(r'[/]+', '/', file_path)

    return file_path


def sort_dict(dictionary: dict, reverse=False):
    """字典排序, 按照键值"""
    sorted_dict = sorted(dictionary.items(), key=lambda e: int(str(e[0]).split('_')[1]), reverse=reverse)
    n_dict = {}
    for index, item in enumerate(sorted_dict):
        n_dict[item[0]] = item[1]
    return n_dict


def async_task(func):
    """异步任务装饰器"""

    def wrapper(**kwargs):
        from system.task import TaskConfig
        pipe_result = TaskConfig.create_process_async(task=func, param=kwargs)
        return pipe_result

    return wrapper

if __name__ == '__main__':
    dic = {

    }