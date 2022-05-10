import os

from system.utils import time_check, get_project_path


class DocumentBase:
    """
    通用文档格式
    @author 杨明树
    @date 2022-04-01
    """

    def __init__(self, file_path) -> None:
        """初始化"""
        from fitz import Document

        self.file_path = file_path
        with Document(file_path) as doc:
            self.start_x, self.start_y, self.width, self.height = doc[0].rect

    def image_correction(self):
        """
        基于轮廓的图像矫正
        @author 杨明树
        @date 2022-04-01
        """
        pass

    def render(self, scale=2.5, rect=None):
        """渲染页面"""
        if not rect:
            rect = [self.start_x, self.start_y, self.width, self.height]
        param = {
            'img_rect': rect,
            'file_path': self.file_path,
            'temp_path': get_project_path() + os.getenv('TEMP_DIR'),
            'img_scale': scale,
        }
        from power.render import Renderer
        file_list: list = Renderer.pdf_to_png_multiprocess(**param)
        return file_list

    def rec_logic(self, file_list: list, regular=None):
        """识别逻辑"""
        from power.ocr import OCR
        from power.barcode import Barcode

        results = {}
        for index, png in enumerate(file_list):
            # 条码识别
            results[png] = Barcode.decode(img_path=png, regular=regular)
            if not results[png] or len(results[png]) == 0:
                # OCR，指定区域识别
                results[png] = OCR.recognize(img_path=png, filter=(True if regular else False), regular=regular)
        return results

    def recognize(self, scale=2.5, rect=None, regular: dict = None):
        """文档识别"""
        # 1. 文档格式转换，PDF -> PNG
        file_list = self.render(scale, rect)
        # 2. 图像信息提取（OCR）
        if regular:
            results = self.rec_logic(file_list, regular)
        else:
            results = self.rec_logic(file_list)
        # 3. 按照键值排序
        from system.utils import sort_dict

        results = sort_dict(results)
        return results


class Delivery(DocumentBase):
    """
    九立标准签收单
    识别区域
    @author 杨明树
    @date 2022-03-31
    """

    def render(self, scale=5, rect=None):
        """标准签收单渲染"""
        if not rect:
            rect = [500, 0, 300, 100]
        return super().render(scale, rect)

    def rec_logic(self, file_list: list, regular=r'^HOME[\d]+'):
        """标准签收单识别逻辑"""
        from power.barcode import Barcode
        from power.render import Renderer
        from power.ocr import OCR

        results = {}
        problem = []
        for index, png in enumerate(file_list):
            # 条码识别
            results[png] = Barcode.decode(img_path=png, regular=regular)
            if not results[png] or len(results[png]) == 0:
                results[png] = OCR.recognize(img_path=png, filter=True if regular else False, regular=regular)
                if not results[png] or len(results[png]) == 0:
                    # 记录未能提取出数据的页码
                    problem.append(index)
                    results.pop(png)

        # 对未能提取出数据的页面重新渲染，重新识别（低分辨率、整页识别）
        if problem:
            param = {
                'file_path': self.file_path,
                'temp_path': get_project_path() + os.getenv('TEMP_DIR'),
                'img_rect': [self.start_x, self.start_y, self.width, self.height],
                'page_number': problem,
                'img_scale': 2.5
            }
            rec_again = Renderer.pdf_page_to_png_multiprocess(**param)
            for index, png in enumerate(rec_again):
                # 条码整页识别
                results[png] = Barcode.decode(img_path=png, regular=regular)
        return results


class IngramDelivery(DocumentBase):
    """
    英迈签收单
    @author 杨明树
    @date 2022-03-31
    """

    def render(self, scale=2.5, rect=None):
        return super().render(scale, rect)

    def rec_logic(self, file_list: list, regular=r'[\d]{2}-[\d]{5}-[\d]{2}'):
        """识别逻辑"""

        return super().rec_logic(file_list, regular)


class CheckList(DocumentBase):
    """
    查货单
    识别区域：x=400, y=0, w=300, h=100
    文本过滤：8位纯数字
    @author 杨明树
    @date 2022-04-14
    """

    def rec_logic(self, file_list: list, regular=None):
        from power.barcode import Barcode

        results = {}
        for index, png in enumerate(file_list):
            # 条码识别
            results[png] = Barcode.decode(img_path=png, regular=regular)
        return results

    def recognize(self, scale=2.5, rect=None, regular=r'[0-9]{8}'):
        """查货单识别"""
        if not rect:
            rect = [400, 0, 300, 100]
        return super().recognize(scale, rect, regular)


class Manifest(DocumentBase):
    """
    载货清单
    文本过滤：13位纯数字
    @author 杨明树
    @date 2022-04-14
    """

    def recognize(self, scale=2.5, rect=None, regular=r'[0-9]{13}'):
        """查货单识别"""
        if not rect:
            rect = [500, 0, 500, 200]
        return super().recognize(scale, rect, regular)
