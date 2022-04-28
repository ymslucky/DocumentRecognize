import os
from unittest import TestCase

from power.render import Renderer
from system.utils import time_check


class TestTaskConfig(TestCase):
    """任务调度单元测试"""

    def setUp(self) -> None:
        """前置处理"""
        from system.task import TaskConfig
        from flask import Flask
        TaskConfig.initialize(Flask(__name__))

        from dotenv import load_dotenv
        from system.utils import get_project_path
        load_dotenv(get_project_path() + 'user.env')

    def tearDown(self) -> None:
        """后置处理"""
        from system.task import TaskConfig
        TaskConfig.scheduler.shutdown()

    def test_add_task(self):
        def func():
            print('123')

        from system.task import TaskConfig

        self.assertEqual(0, len(TaskConfig.get_jobs()))
        TaskConfig.scheduler.add_job(func=func, trigger='cron', second='0-59')
        self.assertEqual(1, len(TaskConfig.get_jobs()))

    @time_check
    def test_create_process(self):
        from fitz import Document
        from system.utils import get_project_path
        from system.task import TaskConfig

        file_path = get_project_path() + 'test/test_resources/测试资源.pdf'
        length = len(Document(file_path))
        cpus = os.cpu_count()

        for id in range(0, length, int(length / cpus)):
            param = {
                'img_rect': [0, 0, 1000, 1000],
                'file_path': file_path,
                'temp_path': get_project_path() + os.getenv('TEMP_DIR'),
                'img_scale': 2,
                'page_number': [x for x in range(id, id + int(length / cpus))]
            }
            TaskConfig.create_process_async(task=Renderer.pdf_page_to_png, param=param)
        TaskConfig.pool.close()
        TaskConfig.pool.join()
