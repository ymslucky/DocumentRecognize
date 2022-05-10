import os

from system.utils import get_project_path


def temp_file_clear():
    """删除临时文件"""
    TEMP_DIR = os.path.abspath(get_project_path() + os.getenv('TEMP_DIR')) + '/'
    if os.path.exists(TEMP_DIR):
        for root, dirs, files in os.walk(TEMP_DIR, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
    import logging
    logger = logging.getLogger('DRLog')
    logger.info('已执行定时任务：临时文件清除！')
