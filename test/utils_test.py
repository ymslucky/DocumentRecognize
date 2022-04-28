import os
from unittest import TestCase


class UtilsTest(TestCase):
    """工具类单元测试"""

    def setUp(self) -> None:
        """前置处理"""
        from dotenv import load_dotenv
        from system.utils import get_project_path
        load_dotenv(get_project_path() + 'user.env')

    def tearDown(self) -> None:
        """后置处理"""
        super().tearDown()

    def test_get_project_path(self):
        from system.utils import get_project_path
        self.assertEqual('E:\\PyCharmProject\\DocumentRecognize\\', get_project_path())

    def test_temp_file_clear(self):
        from system.utils import temp_file_clear, get_project_path

        # 新建测试文件
        file1 = get_project_path() + 'temp/page_1.txt'
        file2 = get_project_path() + 'temp/page_2.txt'
        file3 = get_project_path() + 'temp/Page/'
        f1 = open(file1, 'w')
        f2 = open(file2, 'w')
        os.mkdir(file3)
        f1.close()
        f2.close()

        temp_file_clear()

        if os.getenv('TEMP_DIR'):
            listdir = os.listdir(os.path.abspath(get_project_path() + os.getenv('TEMP_DIR')))
            self.assertEqual(0, len(listdir))
