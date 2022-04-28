import os
import unittest


class OCRTest(unittest.TestCase):
    """OCR单元测试"""

    def setUp(self) -> None:
        """前置处理"""
        from power.render import Renderer

        self.renderer = Renderer(os.path.abspath('./test_resources/测试资源.pdf'))
        self.renderer.pdf_page_to_png(page_number=[0], img_scale=2)
        self.img_path = self.renderer.temp_dir + '测试资源_1.png'

        from system.configuration import SystemConfiguration
        SystemConfiguration().load_config()
        SystemConfiguration.dir_init()

    def tearDown(self) -> None:
        """后置处理"""
        # 关闭文档
        self.renderer.close()
        # 删除临时文件
        files = os.listdir(self.renderer.temp_dir)
        for index, file in enumerate(files):
            os.remove(self.renderer.temp_dir + file)

    def test_recognize(self):
        from power.ocr import OCR
        result = OCR().recognize(self.img_path)
        # for item in result:
        #     print(item)
        self.assertIsNotNone(result)

    def test_recognize_filter(self):
        from power.ocr import OCR
        result = OCR().recognize(self.img_path, True, 'HOME[\d]+')
        self.assertEqual('HOME202111010683', result[0])
