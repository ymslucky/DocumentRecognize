"""
渲染服务
@author 杨明树
@date 2022-04-01
"""
import math
import os
import time

from fitz import Document, Matrix
from fitz.utils import get_pixmap

from jl_task.async_task import AsyncManager


class Renderer:
    """
    图片渲染器
    @author 杨明树
    @date 2022-04-01
    """

    @staticmethod
    @AsyncManager.async_process
    def pdf_to_png(**param):
        """渲染整个PDF文档为图片,单进程"""
        from system.utils import path_exchange

        file_path = param.get('file_path')
        with Document(file_path) as doc:
            filename = os.path.basename(file_path)
            [x, y, w, h] = param.get('img_rect', [0,0,1600,1600])
            scale = param.get('img_scale', 1.5)
            temp_path = param.get('temp_path', os.path.abspath('./temp/'))
            file_list = []
            for index, page in enumerate(doc):
                pm = get_pixmap(page, alpha=False, matrix=Matrix(scale, scale), clip=[x, y, x + w, y + h])
                picture_path = temp_path + f'pages/{filename.replace(".pdf", "")}_{index + 1}_{time.time()}页.png'
                picture_path = path_exchange(picture_path)
                pm.save(picture_path)
                file_list.append(picture_path)
            return file_list

    @staticmethod
    def pdf_to_png_multiprocess(**param):
        """渲染整个PDF文档为图片,多进程"""

        file_path = param.get('file_path')
        with Document(file_path) as doc:
            length = len(doc)
            cpus = os.cpu_count()
            step = math.floor(length / cpus)
            results = []
            file_list = []
            # 页数不多，就不用多进程加速
            if step < int(os.getenv('PROCESS_PAGE')) or length < int(os.getenv('PROCESS_FILE_SIZE')):
                res = Renderer.pdf_to_png(**param).get()
                file_list.extend(res)
            else:
                for index in range(0, length, step):
                    page_number = list(range(index, (index + step) if (index + step) < length else length))
                    param['page_number'] = page_number
                    res = Renderer.pdf_page_to_png(**param)
                    results.append(res)
            # 等待所有的处理结束
            for index, item in enumerate(results):
                # 阻塞
                path_list = item.get()
                file_list.extend(path_list)
            return file_list

    @staticmethod
    def pdf_page_to_png_multiprocess(**param):
        """渲染固定页面，多进程"""
        import math

        page_number: list = param.get('page_number')
        length = len(page_number)
        cpus = os.cpu_count()
        step = math.floor(length / cpus)
        results = []
        file_list = []
        if step < int(os.getenv('PROCESS_PAGE')) or length < int(os.getenv('PROCESS_FILE_SIZE')):
            res = Renderer.pdf_page_to_png(**param).get()
            file_list.extend(res)
        else:
            # 将需要渲染的所有页面分为 “CPU核心数” 份，每份创建一个进程进行渲染，即等分渲染任务，使用全核心完成
            for part_id in range(cpus):
                part_page: list = page_number[math.floor(part_id / cpus * length):math.floor((part_id + 1) / cpus * length)]
                render_param = param.copy()
                render_param['page_number'] = part_page
                res = Renderer.pdf_page_to_png(**render_param)
                results.append(res)
        # 等待所有的处理结束
        for index, item in enumerate(results):
            # 阻塞
            path_list = item.get()
            file_list.extend(path_list)
        return file_list

    @staticmethod
    @AsyncManager.async_process
    def pdf_page_to_png(**param):
        """PDF页面转换为PNG图片，单进程"""
        import time
        from system.utils import path_exchange

        file_path = param.get('file_path')
        temp_path = param.get('temp_path', os.path.abspath('./temp/'))
        path_list = []
        with Document(file_path) as doc:
            filename = os.path.basename(file_path)
            [x, y, w, h] = param.get('img_rect', [0,0,1600,1600])
            scale = param.get('img_scale', 1.5)
            page_number = param.get('page_number', [0])

            for index, page_num in enumerate(page_number):
                page = doc[page_num]
                pm = get_pixmap(page, alpha=False, matrix=Matrix(scale, scale), clip=[x, y, x + w, y + h])
                picture_path = temp_path + f'pages/{filename.replace(".pdf", "")}_{page_num + 1}_{time.time()}页.png'
                picture_path = path_exchange(picture_path)
                pm.save(picture_path)
                path_list.append(picture_path)
        return path_list
