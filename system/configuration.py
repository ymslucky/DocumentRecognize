import logging

from dotenv import load_dotenv
from flask import Flask

import os


class SystemConfiguration:
    """
    系统配置类
    @author 杨明树
    @date 2022-03-31
    """
    # 程序实例
    APP = Flask(__name__)
    # 日志
    logger = logging.getLogger('DRLog')
    # 配置文件的默认路径
    from system.utils import get_project_path
    CONFIG_PATH = get_project_path() + 'user.env'

    @staticmethod
    def initialize(config_path=None):
        """
        初始化
        :param config_path: 自定义配置文件路径
        """
        SystemConfiguration.blueprint_init()
        SystemConfiguration.load_config(config_path)
        SystemConfiguration.dir_init()
        SystemConfiguration.ocr_init()
        SystemConfiguration.log_init()
        SystemConfiguration.task_scheduler_init()

        SystemConfiguration.logger.info('文档识别系统已启动！路由信息如下：')
        for item in SystemConfiguration.APP.url_map.iter_rules():
            SystemConfiguration.logger.info(f'{item.rule} - Method{item.methods}')

    @staticmethod
    def blueprint_init():
        """蓝图初始化"""
        from business.views import busi_router
        # 将蓝图注册进应用
        SystemConfiguration.APP.register_blueprint(busi_router, url_prefix='/api')
        SystemConfiguration.logger.info('已注册蓝图!')

    @staticmethod
    def load_config(config_path=None):
        """加载用户配置"""
        if config_path:
            SystemConfiguration.CONFIG_PATH = config_path
        status = load_dotenv(SystemConfiguration.CONFIG_PATH)
        SystemConfiguration.logger.info(f'加载用户配置——{status}!')

    @staticmethod
    def ocr_init():
        """初始化OCR引擎"""
        from power.ocr import OCR
        OCR.initialize()

    @staticmethod
    def dir_init():
        """文件目录初始化"""
        from system.utils import get_project_path
        # 目录初始化
        LOG_FILE_PATH = os.path.abspath(get_project_path() + os.getenv('LOG_FILE_PATH'))
        if not os.path.exists(LOG_FILE_PATH):
            os.mkdir(LOG_FILE_PATH)
        OCR_LOG_PATH = os.path.abspath(get_project_path() + os.getenv('OCR_LOG_PATH'))
        if not os.path.exists(OCR_LOG_PATH):
            os.mkdir(OCR_LOG_PATH)
        TEMP_DIR = os.path.abspath(get_project_path() + os.getenv('TEMP_DIR'))
        if not os.path.exists(TEMP_DIR):
            os.mkdir(TEMP_DIR)
        PAGES_DIR = TEMP_DIR + '/pages'
        if not os.path.exists(PAGES_DIR):
            os.mkdir(PAGES_DIR)

    @staticmethod
    def log_init():
        """系统日志初始化"""
        from system.utils import get_project_path
        from datetime import date

        logger = logging.getLogger('DRLog')
        logger.handlers.clear()
        logger.setLevel('INFO')
        log_file = get_project_path() + os.getenv('LOG_FILE_PATH') + (date.today().isoformat() + '.log')
        system_log_handler = logging.FileHandler(log_file)
        system_log_handler.setFormatter(logging.Formatter(os.getenv('LOG_FORMATTER')))
        logger.addHandler(system_log_handler)

    @staticmethod
    def task_scheduler_init():
        """任务调度器初始化"""
        from jl_task import jl_task_initialize
        jl_task_initialize(SystemConfiguration.APP)
