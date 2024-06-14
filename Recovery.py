class Recovery:
    """
    恢复类
    """
    def __init__(self):
        pass

    def recovery_image_head(self, status, fast=1):
        """
        恢复图像头
        :param status: 各个参数丢失情况汇总，为一个由0和1组成的列表
        :param fast: 是否重建所有可能分辨率，如果为0，则只重建所有可能分辨率，否则只重建一个分辨率
        :return:
        """
        raise Exception("方法需要被重写，否则不能调用")

    def check_image_head(self):
        """
        检查图片头（image_head_size的40字节中各个参数是否存在）
        具体而言，函数依次检查：
        1. 检查biSize是否存在
        2. 检查biWidth是否存在
        3. 检查biHeight是否存在
        4. 检查biPlanes是否存在
        5. 检查biBitCount是否存在
        6. 检查biCompression是否存在
        7. 检查biSizeImage是否存在
        8. 检查biXPelsPerMeter是否存在
        9. 检查biYPelsPerMeter是否存在
        10. 检查biClrUsed是否存在
        11. 检查biClrImportant是否存在
        :return:
        """
        raise Exception("方法需要被重写，否则不能调用")

    def recovery_file_head(self, status):
        """
        恢复文件头
        :param status: 各个参数丢失情况汇总，为一个由0和1组成的列表
        :return:
        """
        raise Exception("方法需要被重写，否则不能调用")

    def check_file_head(self):
        """
        检查文件头（file_head_size的14字节中各个参数是否存在）
        具体而言，函数依次检查：
        1. 文件头标识符（bfType）
        2. 文件大小（bfSize）
        3. 保留字1（bfReserved1）
        4. 保留字2（bfReserved2）
        5. 数据偏移量（bfOffBits）
        :return:
        """
        raise Exception("方法需要被重写，否则不能调用")