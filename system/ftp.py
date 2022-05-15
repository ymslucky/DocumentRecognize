import ftplib
from ftplib import FTP
import os


class FtpTools(object):
    """FTP工具类"""

    @staticmethod
    def login(ftp: FTP):
        """登录"""
        username = os.getenv('FTP_USERNAME')
        password = os.getenv('FTP_PASSWORD')
        ftp.login(user=username, passwd=password)

    @staticmethod
    def connect():
        """连接FTP"""
        ftp = FTP()

        ftp.set_pasv(True)
        ftp.encoding = 'gbk'

        server = os.getenv('FTP_SERVER')
        port = int(os.getenv('FTP_PORT'))
        ftp.connect(host=server, port=port)

        FtpTools.login(ftp)

        return ftp

    @staticmethod
    def download(local_file, remote_file):
        """下载远程文件"""
        with FtpTools.connect() as client, open(local_file, 'wb') as file_handler:
            buf_size = 1024
            client.retrbinary('RETR %s' % remote_file, file_handler.write, buf_size)

    # @staticmethod
    # def batch_download(local_dir, remote_dir):
    #     """批量下载远程文件"""
    #     with FtpTools.connect() as client:
    #         client.cwd(remote_dir)

    @staticmethod
    def upload(local_file, remote_file):
        """上传本地文件至服务器"""
        if not os.path.exists(local_file) or not os.path.isfile(local_file):
            raise Exception('文件不存在，无法上传！')

        with FtpTools.connect() as client, open(local_file, 'rb') as file_handler:
            buf_size = 1024
            client.storbinary('STOR %s' % remote_file, file_handler, buf_size)

    @staticmethod
    def batch_upload(local_file_list, remote_dir):
        """批量上传"""
        with FtpTools.connect() as client:
            FtpTools.mkdir(client, remote_dir)
            buf_size = 1024
            for _, file in enumerate(local_file_list):
                with open(file, 'rb') as file_handler:
                    client.storbinary(f'STOR {remote_dir + os.path.basename(file)}', file_handler, buf_size)

    @staticmethod
    def mkdir(ftp_client, remote_dir):
        """在服务器创建目录"""
        try:
            ftp_client.cwd(remote_dir)
        except ftplib.error_perm:
            ftp_client.mkd(remote_dir)
