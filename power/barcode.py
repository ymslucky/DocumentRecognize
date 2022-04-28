"""
条码识别服务
@author 杨明树
@date 2022-04-01
"""


class Barcode:
    """
    条码识别
    @author 杨明树
    @date 2022-04-01
    """

    @staticmethod
    def decode(img_path, regular=None):
        """条码解析"""
        from pyzbar.pyzbar import decode
        from PIL import Image
        import re

        results = []
        with Image.open(img_path) as img:
            items = decode(img)
            for item in items:
                data = str(item.data, 'utf-8')
                if regular and re.match(pattern=regular, string=data):
                    results.append(data)
        return results

    @staticmethod
    def locate():
        """条码定位(未使用)"""
        from system.errors import ServerError
        raise ServerError('条码定位功能暂未支持，禁止使用！')
        # return [0, 0, 0, 0]
