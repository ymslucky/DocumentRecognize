"""
视图函数
@author 杨明树
@date 2022-03-31
"""
import os
import time

from flask import Blueprint

from system.errors import Success

sys_router = Blueprint('system', __name__)


@sys_router.route('/add_task')
def add_task():
    from system.configuration import SystemConfiguration as sc
    sc.task.scheduler.add_job(print_number, 'cron', second='0-59')

    jobs = sc.task.get_jobs()
    res = []
    for item in jobs:
        res.append(item.name)

    return Success(res)


@sys_router.route('/rec')
def rec_test():
    from system.utils import get_project_path
    from power.barcode import Barcode
    from power.render import Renderer

    file_path = get_project_path() + '查货单.pdf'
    param = {
        'file_path': file_path,
        'img_rect': [0, 0, 1000, 1000],
        'img_scale': 2,
        'temp_path': get_project_path() + os.getenv('TEMP_DIR')
    }
    Renderer.pdf_to_png(**param)

    pic = param['temp_path'] + os.path.basename(file_path).replace('.pdf', '') + '_1.png'
    res = Barcode.decode(pic)
    return Success(res)


@sys_router.route('/render')
def render():
    from business.models import IngramDelivery, DocumentBase, Delivery
    from system.utils import get_project_path
    # doc = DocumentBase(get_project_path() + 'temp/艾睿签收单.pdf')
    # doc = IngramDelivery(get_project_path() + 'test/test_resources/英迈签收单.pdf')
    doc = Delivery(get_project_path() + 'test/test_resources/艾睿签收单.pdf')
    fl = doc.recognize()
    return Success(data=fl)


@sys_router.route('/get_process_info')
def get_process_info():
    from system.task import TaskConfig
    return Success(TaskConfig.pool.nodes)


def print_number():
    """测试定时任务"""
    print(f'这是一个定时任务 {time.time()}')
