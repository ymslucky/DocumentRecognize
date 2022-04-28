from unittest import TestCase


class TestDocumentBase(TestCase):
    """文档模型类单元测试"""

    def setUp(self) -> None:
        """前置处理"""
        from business.models import DocumentBase
        from system.utils import get_project_path
        self.doc = DocumentBase(get_project_path() + 'test/test_resources/报关单.pdf')

        from system.task import TaskConfig
        from flask import Flask
        TaskConfig.initialize(Flask(__name__))

    def tearDown(self) -> None:
        """后置处理"""
        pass

    def test_recognize(self):
        doc = self.doc
        doc.recognize()

