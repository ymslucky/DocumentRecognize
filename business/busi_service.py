"""
业务逻辑
@author 杨明树
@date 2022-04-01
"""


class Process:
    """
    通用文档识别
    @author 杨明树
    @author 2022-04-01
    """

    def processing(self, x, y, width, height):
        """通用处理方式"""
        pass


class ProcessDelivery(Process):
    """签收单专用识别"""

    def processing(self, x, y, width, height):
        """签收单通用识别"""
        pass

    def ingram_processing(self):
        """英迈签收单专用识别"""
        pass
