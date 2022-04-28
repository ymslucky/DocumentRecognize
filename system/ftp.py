#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
from ftplib import FTP
import os
import sys
import time
import socket

from system.utils import async_task


class MyFTP:
    """
    FTP工具类
    来源：网络获取
    博客地址：http://blog.csdn.net/ouyang_peng/

    @author 欧阳鹏
    @date 2022-04-06
    """

    ftp = None
    logger = logging.getLogger('DRLog')

    def __init__(self):
        """ 初始化 FTP 客户端
        @:param host ip地址
        @:param port 端口号
        """
        self.ftp = FTP()
        # 重新设置下编码方式
        # self.ftp.encoding = 'gbk'

        self.logger = logging.getLogger('DRLog')
        self.file_list = []

    @staticmethod
    def initialize():
        """FTP初始化"""
        MyFTP.ftp = FTP()
        MyFTP.ftp.encoding = 'gbk'
        MyFTP.logger = logging.getLogger('DRLog')

    @staticmethod
    def login():
        """初始化 FTP 客户端"""
        try:
            timeout = 60
            socket.setdefaulttimeout(timeout)
            # 0主动模式 1 #被动模式
            MyFTP.ftp.set_pasv(True)
            MyFTP.ftp.connect(os.getenv('FTP_SERVER'), int(os.getenv('FTP_PORT')))
            MyFTP.ftp.login(os.getenv('FTP_USERNAME'), os.getenv('FTP_PASSWORD'))
            MyFTP.logger.info('FTP连接成功')

        except Exception as err:
            MyFTP.logger.error("FTP 连接或登录失败 ，错误信息：%s" % err)
            raise err

    # def is_same_size(self, local_file, remote_file):
    #     """
    #     判断远程文件和本地文件大小是否一致
    #     @:param local_file 本地文件
    #     @:param remote_file 远程文件
    #     """
    #     try:
    #         remote_file_size = self.ftp.size(remote_file)
    #     except Exception as err:
    #         # self.logger.info("is_same_size() 错误描述为：%s" % err)
    #         remote_file_size = -1
    #
    #     try:
    #         local_file_size = os.path.getsize(local_file)
    #     except Exception as err:
    #         # self.logger.info("is_same_size() 错误描述为：%s" % err)
    #         local_file_size = -1
    #
    #     self.logger.info('local_file_size:%d  , remote_file_size:%d' % (local_file_size, remote_file_size))
    #     if remote_file_size == local_file_size:
    #         return 1
    #     else:
    #         return 0

    @staticmethod
    def download_file(local_file, remote_file):
        """从ftp下载文件
            参数:
                local_file: 本地文件
                remote_file: 远程文件
        """
        file_handler = None
        try:
            MyFTP.login()
            buf_size = 1024
            file_handler = open(local_file, 'wb')
            MyFTP.ftp.retrbinary('RETR %s' % remote_file, file_handler.write, buf_size)
        except Exception as err:
            MyFTP.logger.info('下载文件出错，出现异常：%s ' % err)
            raise err
        finally:
            if file_handler:
                file_handler.close()
            MyFTP.close()

    def download_file_tree(self, local_path, remote_path):
        """从远程目录下载多个文件到本地目录
                       参数:
                         local_path: 本地路径
                         remote_path: 远程路径
                """
        print("download_file_tree()--->  local_path = %s ,remote_path = %s" % (local_path, remote_path))
        try:
            self.ftp.cwd(remote_path)
        except Exception as err:
            self.logger.info('远程目录%s不存在，继续...' % remote_path + " ,具体错误描述为：%s" % err)
            return

        if not os.path.isdir(local_path):
            self.logger.info('本地目录%s不存在，先创建本地目录' % local_path)
            os.makedirs(local_path)

        self.logger.info('切换至目录: %s' % self.ftp.pwd())

        self.file_list = []
        # 方法回调
        self.ftp.dir(self.get_file_list)

        remote_names = self.file_list
        self.logger.info('远程目录 列表: %s' % remote_names)
        for item in remote_names:
            file_type = item[0]
            file_name = item[1]
            local = os.path.join(local_path, file_name)
            if file_type == 'd':
                print("download_file_tree()---> 下载目录： %s" % file_name)
                self.download_file_tree(local, file_name)
            elif file_type == '-':
                print("download_file()---> 下载文件： %s" % file_name)
                self.download_file(local, file_name)
            self.ftp.cwd("..")
            self.logger.info('返回上层目录 %s' % self.ftp.pwd())
        return True

    @staticmethod
    def upload_file(local_file, remote_file):
        """从本地上传文件到ftp
           参数:
             local_path: 本地文件
             remote_path: 远程文件
        """
        from system import errors

        if not os.path.isfile(local_file):
            MyFTP.logger.info('%s 不存在' % local_file)
            raise errors.ServerError('识别服务器无法上传文件！')

        file_handler = None
        try:
            MyFTP.login()
            buf_size = 1024
            file_handler = open(local_file, 'rb')
            MyFTP.ftp.storbinary('STOR %s' % remote_file, file_handler, buf_size)
        except Exception as e:
            MyFTP.logger.error("上传文件失败！")
        finally:
            if file_handler:
                file_handler.close()
            MyFTP.close()

    @staticmethod
    def upload_file_unclose(local_file, remote_file):
        """从本地上传文件到ftp
           参数:
             local_path: 本地文件
             remote_path: 远程文件
        """
        from system import errors

        if not os.path.isfile(local_file):
            MyFTP.logger.info('%s 不存在' % local_file)
            return

        file_handler = None
        try:
            buf_size = 1024
            file_handler = open(local_file, 'rb')
            MyFTP.ftp.storbinary('STOR %s' % remote_file, file_handler, buf_size)
        except Exception as e:
            MyFTP.logger.error("上传文件失败！")
            raise e
        finally:
            if file_handler:
                file_handler.close()

    @staticmethod
    def upload_file_tree(local_path, remote_path):
        """
        将本地目录下的所有文件上传至FTP
        @:param local_path 本地路径
        @:param remote_path 远程路径
        """
        from system import errors

        try:
            MyFTP.login()
            if not os.path.isdir(local_path):
                MyFTP.logger.info('本地目录 %s 不存在' % local_path)
                raise errors.ServerError('识别服务器无法上传文件！')

            MyFTP.ftp.cwd(remote_path)

            local_name_list = os.listdir(local_path)
            for local_name in local_name_list:
                src = os.path.join(local_path, local_name)
                # if os.path.isdir(src):
                #     try:
                #         MyFTP.ftp.mkd(local_name)
                #     except Exception as err:
                #         MyFTP.logger.info("目录已存在 %s ,具体错误描述为：%s" % (local_name, err))
                #     MyFTP.logger.info("upload_file_tree()---> 上传目录： %s" % local_name)
                #     MyFTP.upload_file_tree(src, local_name)
                # else:
                MyFTP.upload_file_unclose(src, local_name)
            MyFTP.ftp.cwd("..")
        except Exception as e:
            MyFTP.logger.error(e)
            raise e
        finally:
            if MyFTP.ftp:
                MyFTP.close()

    @staticmethod
    def close():
        """ 退出ftp
        """
        if MyFTP.ftp:
            MyFTP.ftp.quit()
        MyFTP.logger.info("FTP连接已断开！")

    def get_file_list(self, line):
        """ 获取文件列表
            参数：
                line：
        """
        file_arr = self.get_file_name(line)
        # 去除  . 和  ..
        if file_arr[1] not in ['.', '..']:
            self.file_list.append(file_arr)

    def get_file_name(self, line):
        """ 获取文件名
            参数：
                line：
        """
        pos = line.rfind(':')
        while (line[pos] != ' '):
            pos += 1
        while (line[pos] == ' '):
            pos += 1
        file_arr = [line[0], line[pos:]]
        return file_arr


if __name__ == "__main__":
    host_address = "192.168.0.95"
    username = "liuxiang"
    password = "xiangftp!123"
    my_ftp = MyFTP(host_address)
    my_ftp.login(username, password)

    # 下载单个文件
    # my_ftp.download_file("G:/ftp_test/XTCLauncher.apk", "/App/AutoUpload/ouyangpeng/I12/Release/XTCLauncher.apk")

    # 下载目录
    # my_ftp.download_file_tree("G:/ftp_test/", "App/AutoUpload/ouyangpeng/I12/")

    # 上传单个文件
    # my_ftp.upload_file("G:/ftp_test/Release/XTCLauncher.apk", "/App/AutoUpload/ouyangpeng/I12/Release/XTCLauncher.apk")
    # my_ftp.upload_file("G:/ftp_test/Python编程快速上手__让繁琐工作自动化.pdf", "/App/AutoUpload/ouyangpeng/I12/Release/Python编程快速上手__让繁琐工作自动化.pdf")

    my_ftp.upload_file_tree('E:/PyCharmProject/DocumentRecognize/temp/files', '/TEMP/')

    my_ftp.close()
