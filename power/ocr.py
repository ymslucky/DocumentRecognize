import os


class OCR:
    """
    光学字符识别
    @author 杨明树
    @date 2022-04-01
    """
    TesseractOCR = None
    MMOCR = None
    from paddleocr import PaddleOCR
    from system.utils import get_project_path
    PaddleOCR = PaddleOCR(enable_mkldnn=os.getenv('USE_MKLDNN'),
                          use_angle_cls=os.getenv('USE_ANGLE_CLS'),
                          # label_list=['0', '180'],
                          use_gpu=os.getenv('USE_GPU'),
                          cls_model_dir=get_project_path() + 'interface/ch_PP-OCRv2_cls_infer',
                          det_model_dir=get_project_path() + 'interface/ch_PP-OCRv2_det_infer',
                          rec_model_dir=get_project_path() + 'interface/ch_PP-OCRv2_rec_infer')

    @staticmethod
    def initialize() -> None:
        """
        OCR引擎初始化
        参数设置：
        1.enable_mkldnn —— 启用MKLDNN加速库（因为公司没有显卡，是使用 CPU 进行识别，所以开启加速库来提高效率，仅 Inter CPU 支持）
        2.use_angle_cls —— 启用方向分类器
        3.label_list —— 设置方向分类器支持的角度，默认为['0', '180']，且仅支持这两个方向
        4.use_gpu —— 禁用GPU
        @author 杨明树
        @date 2022-04-06
        """
        import logging
        from datetime import date
        from system.utils import get_project_path

        log_file = get_project_path() + os.getenv('OCR_LOG_PATH') + (date.today().isoformat() + '.log')
        ocr_log_file_handler = logging.FileHandler(log_file)
        ocr_log_file_handler.setFormatter(logging.Formatter(os.getenv('OCR_LOG_FORMATTER')))
        log = logging.getLogger('ppocr')  # PaddleOCR默认的日志
        log.handlers.clear()
        log.addHandler(ocr_log_file_handler)

    @staticmethod
    def recognize(img_path, filter=False, regular=None):
        """OCR识别"""
        import re

        results = OCR.PaddleOCR.ocr(img_path, det=True, cls=True)
        datalist = []
        for line in results:
            if filter:
                match = re.search(regular, line[1][0])
                if match is not None:
                    datalist.append(match.group())
            else:
                datalist.append(line)
        return datalist
