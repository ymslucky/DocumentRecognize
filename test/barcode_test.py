import os
import unittest


class BarcodeTest(unittest.TestCase):
    """条码解析单元测试"""

    def setUp(self) -> None:
        """前置处理"""
        from system.utils import get_project_path
        self.img_path = get_project_path() + 'test/test_resources/查货单_1.png'

    def tearDown(self) -> None:
        """后置处理"""
        pass

    def test_explain(self):
        from power.barcode import Barcode
        res = Barcode.decode(self.img_path)
        self.assertEqual('22032615', res[0])

