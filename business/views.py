"""
业务视图函数
@author 杨明树
@date 2022-04-01
"""
import logging
import os

from flask import Blueprint, request

from business import models
from business.models import DocumentBase
from jl_task.async_task import AsyncManager
from power.render import Renderer
from system.errors import Success
from system.ftp import FtpTools
from system.utils import get_project_path, time_check

busi_router = Blueprint('business', __name__)


@time_check
def remove_temp_file(files):
    """删除本地临时文件"""
    try:
        for file in files:
            os.remove(file)
    except Exception as e:
        logger = logging.getLogger('DRLog')
        logger.warning(f'未能删除生成的临时文件, 错误信息：{e}')


@time_check
def upload_files(files, remote_dir):
    """批量上传文件"""
    FtpTools.batch_upload(local_file_list=files, remote_dir=remote_dir)


def base_control(model=DocumentBase):
    """通用处理流程"""
    param = request.get_json()

    # 从 FTP 下载文件到本地
    remote_file = param.get('uploadFilePath')
    local_file = get_project_path() + os.getenv('TEMP_DIR') + os.path.basename(remote_file)
    FtpTools.download(local_file, remote_file)

    # 渲染整页
    param = {
        'file_path': local_file,
        'temp_path': get_project_path() + os.getenv('TEMP_DIR'),
        'img_scale': 2
    }
    page_png_list = Renderer.pdf_to_png_multiprocess(**param)

    doc = model(local_file)
    return_list = doc.recognize()

    remote_dir = '/' + os.getenv('FTP_DIR')
    ret_data = []
    upload_page_list = []
    for index, key in enumerate(return_list):
        row = {
            'page_image': remote_dir + os.path.basename(page_png_list[index]),
            'page_cut_image': remote_dir + os.path.basename(key),
            'text': return_list[key]
        }
        ret_data.append(row)
        upload_page_list.append(page_png_list[index])
        upload_page_list.append(key)

    # 异步上传文件,删除文件
    @AsyncManager.async_process
    def end_process():
        # 上传
        upload_files(upload_page_list, f'/{os.getenv("FTP_DIR")}')
        # 删除临时文件
        files = list(return_list.keys())
        files.append(local_file)
        files.extend(page_png_list)
        remove_temp_file(files=files)

    end_process()

    return Success(data=ret_data)


@busi_router.route('/delivery', methods=['POST'])
def delivery():
    """
    签收单识别
    @:param uploadFilePath 上传文件地址
    @author 杨明树
    @date 2022-04-01
    """
    response = base_control(model=models.Delivery)

    return response


@busi_router.route('/delivery/ingram', methods=['POST'])
@time_check
def delivery_ingram():
    """
    英迈签收单识别
    @:param uploadFilePath 上传文件地址
    @author 杨明树
    @date 2022-04-13
    """
    response = base_control(model=models.IngramDelivery)

    return response


@busi_router.route('/checkList', methods=['POST', 'GET'])
def check_list():
    """
    查货单识别
    @:param uploadFilePath 上传文件地址
    @author 杨明树
    @date 2022-04-13
    """
    response = base_control(model=models.CheckList)

    return response


@busi_router.route('/manifest', methods=['POST'])
def manifest():
    """
    载货清单识别
    @:param uploadFilePath 上传文件地址
    @author 杨明树
    @date 2022-04-13
    """
    response = base_control(model=models.Manifest)

    return response
