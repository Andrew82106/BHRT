from process import *
import tqdm
from Recovery import Recovery


class bmp24(Recovery):
    def __init__(self, bmp_content):
        super().__init__()
        self.file_head_size = 14
        self.image_head_size = 40
        self.head_size = self.file_head_size + self.image_head_size

        self.bfType = ['424d']
        self.bfSize = -1
        self.bfReserved1 = '0000'
        self.bfReserved2 = '0000'
        self.bfOffBits = 54
        self.image_data_size = -1
        self.bmp_content = bmp_content
        # bmp_content是16进制的字符串，每两个字符为一组，每组代表一个字节

        self.biSize = 40
        self.biWidth = -1
        self.biHeight = -1
        self.biPlanes = 1
        self.biBitCount = 24
        self.biCompression = '00000000'
        self.biSizeImage = -1
        self.biXPixPerMeter = 0
        self.biYPixPerMeter = 0
        self.biClrUsed = 0
        self.biClrImportant = 0
        self.possible_d = None
        self.all_resolution = []

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
        status = [0, 0, 0, 0, 0]
        # 0代表对应的参数不存在，1代表存在

        # 识别bfType并标记
        if self.bmp_content[:4] not in self.bfType:
            print("BMP File paramater byType lost")
            status[0] = 0
        else:
            status[0] = 1
            self.bmp_content = self.bmp_content[4:]

        # 识别bfSize并标记
        if int(hex2d(self.bmp_content[4:12])) == 0:
            print("BMP File paramater bfSize lost")
            status[1] = 0
        else:
            status[1] = 1
            self.bfSize = int(hex2d(formathex(self.bmp_content[4:12], 4)))
            self.image_data_size = self.bfSize - self.head_size

        # 识别bfReserved1并标记
        if self.bmp_content[12:16] != self.bfReserved1:
            print("BMP File paramater bfReserved1 lost")
            status[2] = 0
        else:
            status[2] = 1

        # 识别bfReserved2并标记
        if self.bmp_content[16:20] != self.bfReserved2:
            print("BMP File paramater bfReserved2 lost")
            status[3] = 0
        else:
            status[3] = 1

        # 识别bfOffBits并标记
        if int(hex2d(self.bmp_content[20:28])) == 0:
            print("BMP File paramater bfOffBits lost")
            status[4] = 0
        else:
            status[4] = 1
            self.bfOffBits = int(hex2d(formathex(self.bmp_content[20:28], 4)))

        return status

    def _recovery_bfType(self):
        self.bmp_content = self.bfType[0] + self.bmp_content[4:]
        self.bfType = self.bfType[0]

    def _recovery_bfSize(self):
        # 自动计算出bmp图片的大小（字节数量），不包含文件头
        bmp_size = len(self.bmp_content) // 2
        self.bmp_content = self.bmp_content[:4] + formathex(d2hex(bmp_size), 4) + self.bmp_content[12:]
        self.bfSize = bmp_size
        self.image_data_size = self.bfSize - self.head_size

    def _recovery_bfReserved1(self):
        self.bmp_content = self.bmp_content[:12] + self.bfReserved1 + self.bmp_content[16:]

    def _recovery_bfReserved2(self):
        self.bmp_content = self.bmp_content[:16] + self.bfReserved2 + self.bmp_content[20:]

    def _recovery_bfOffBits(self):
        self.bmp_content = self.bmp_content[:20] + formathex(d2hex('54'), 4) + self.bmp_content[28:]

    def recovery_file_head(self, status):
        len_bmp = len(self.bmp_content)
        if status[0] == 0:
            self._recovery_bfType()
        assert len_bmp == len(self.bmp_content), "error happend to length of bmp_content when recovery file head"
        if status[1] == 0:
            self._recovery_bfSize()
        assert len_bmp == len(self.bmp_content), "error happend to length of bmp_content when recovery file head"
        if status[2] == 0:
            self._recovery_bfReserved1()
        assert len_bmp == len(self.bmp_content), "error happend to length of bmp_content when recovery file head"
        if status[3] == 0:
            self._recovery_bfReserved2()
        assert len_bmp == len(self.bmp_content), "error happend to length of bmp_content when recovery file head"
        if status[4] == 0:
            self._recovery_bfOffBits()
        new_file_head = self.bmp_content[:28]
        assert len_bmp == len(self.bmp_content), f"error happend to length of bmp_content when recovery file head. length of bmp_content {len(self.bmp_content)} is not equal to original length {len_bmp}"
        return new_file_head

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
        status = [0] * 11

        # 检查biSize
        if int(hex2d(self.bmp_content[28:36])) == 40:
            status[0] = 1
            self.biSize = 40
        else:
            status[0] = 0
            print("BMP File paramater biSize lost")

        # 检查biWidth
        if int(hex2d(self.bmp_content[36:44])) > 0:
            status[1] = 1
            self.biWidth = int(hex2d(formathex(self.bmp_content[36:44], 4)))
        else:
            status[1] = 0
            print("BMP File paramater biWidth lost")

        # 检查biHeight
        if int(hex2d(self.bmp_content[44:52])) > 0:
            status[2] = 1
            self.biHeight = int(hex2d(formathex(self.bmp_content[44:52], 4)))
        else:
            status[2] = 0
            print("BMP File paramater biHeight lost")

        # 检查biPlanes
        if int(hex2d(formathex(self.bmp_content[52:56], 2))) == 1:
            status[3] = 1
            self.biPlanes = 1
        else:
            status[3] = 0
            print("BMP File paramater biPlanes lost")

        # 检查biBitCount
        if int(hex2d(formathex(self.bmp_content[56:60], 2))) == 24:
            status[4] = 1
            self.biBitCount = 24
        else:
            status[4] = 0
            print("BMP File paramater biBitCount lost")

        # 检查biCompression
        if int(hex2d(formathex(self.bmp_content[60:68], 4))) == 0:
            status[5] = 1
            self.biCompression = 0
        else:
            status[5] = 0
            print("BMP File paramater biCompression lost")

        # 检查biSizeImage
        if int(hex2d(formathex(self.bmp_content[68:76], 4))) > 0:
            status[6] = 1
            self.biSizeImage = int(hex2d(formathex(self.bmp_content[64:72], 4)))
        else:
            status[6] = 0
            print("BMP File paramater biSizeImage lost")

        # 检查biXPelsPerMeter
        if int(hex2d(formathex(self.bmp_content[76:84], 4))) > 0:
            status[7] = 1
            self.biXPixPerMeter = int(hex2d(formathex(self.bmp_content[72:80], 4)))
        else:
            status[7] = 0
            print("BMP File paramater biXPelsPerMeter lost")

        # 检查biYPelsPerMeter
        if int(hex2d(formathex(self.bmp_content[84:92], 4))) > 0:
            status[8] = 1
            self.biYPixPerMeter = int(hex2d(formathex(self.bmp_content[80:88], 4)))
        else:
            status[8] = 0
            print("BMP File paramater biYPelsPerMeter lost")

        # 检查biClrUsed
        if int(hex2d(formathex(self.bmp_content[92:100], 4))) == 0:
            status[9] = 1
            self.biClrUsed = 0
        else:
            status[9] = 0
            print("BMP File paramater biClrUsed lost")

        # 检查biClrImportant
        if int(hex2d(formathex(self.bmp_content[100:108], 4))) == 0:
            status[10] = 1
            self.biClrImportant = 0
        else:
            status[10] = 0
            print("BMP File paramater biClrImportant lost")

        return status


    def get_bmp_dimensions_from_dataLength(self):
        possible_dimensions = []

        for width in range(1, self.image_data_size):
            padding = (4 - (3 * width) % 4) % 4
            row_size = 3 * width + padding

            if self.image_data_size % row_size == 0:
                height = self.image_data_size // row_size
                possible_dimensions.append((width, height))
        # possible_dimensions中长宽差距最小的一对是最有可能正确的，因此对列表中的元素按照长宽差值的绝对值升序排序
        possible_dimensions.sort(key=lambda x: abs(x[0] - x[1]))
        self.possible_d = possible_dimensions
        return possible_dimensions

    def _recovery_biSize(self):
        self.bmp_content = self.bmp_content[:28] + formathex(d2hex(self.biSize), 4) + self.bmp_content[36:]

    def _recovery_biWidth(self, width=None):
        possible_dimensions = self.get_bmp_dimensions_from_dataLength()
        if possible_dimensions:
            self.biWidth = possible_dimensions[0][0] if width is None else width
            self.bmp_content = self.bmp_content[:36] + formathex(d2hex(self.biWidth), 4) + self.bmp_content[44:]

    def _recovery_biHeight(self, height=None):
        possible_dimensions = self.get_bmp_dimensions_from_dataLength()
        if possible_dimensions:
            self.biHeight = possible_dimensions[0][1] if height is None else height
            self.bmp_content = self.bmp_content[:44] + formathex(d2hex(self.biHeight), 4) + self.bmp_content[52:]

    def _recovery_biPlanes(self):
        self.bmp_content = self.bmp_content[:52] + formathex(d2hex(self.biPlanes), 2) + self.bmp_content[56:]
        self.biPlanes = 1

    def _recovery_biBitCount(self):
        self.bmp_content = self.bmp_content[:56] + formathex(d2hex(self.biBitCount), 2) + self.bmp_content[60:]
        self.biBitCount = 24

    def _recovery_biCompression(self):
        self.bmp_content = self.bmp_content[:60] + formathex(d2hex(self.biCompression), 4) + self.bmp_content[68:]
        self.biCompression = 0

    def _recovery_biSizeImage(self):
        self.biSizeImage = self.image_data_size
        self.bmp_content = self.bmp_content[:68] + formathex(d2hex(self.biSizeImage), 4) + self.bmp_content[76:]

    def _recovery_biXPixPerMeter(self):
        self.bmp_content = self.bmp_content[:76] + formathex(d2hex(self.biXPixPerMeter), 4) + self.bmp_content[84:]

    def _recovery_biYPixPerMeter(self):
        self.bmp_content = self.bmp_content[:84] + formathex(d2hex(self.biYPixPerMeter), 4) + self.bmp_content[92:]

    def _recovery_biClrUsed(self):
        self.bmp_content = self.bmp_content[:92] + formathex(d2hex(self.biClrUsed), 4) + self.bmp_content[100:]

    def _recovery_biClrImportant(self):
        self.bmp_content = self.bmp_content[:100] + formathex(d2hex(self.biClrImportant), 4) + self.bmp_content[108:]

    def recovery_image_head(self, status, fast=1):
        len_bmp = len(self.bmp_content)
        if status[0] == 0:
            self._recovery_biSize()
        if status[1] == 0:
            self._recovery_biWidth()
        if status[2] == 0:
            self._recovery_biHeight()
        if status[3] == 0:
            self._recovery_biPlanes()
        if status[4] == 0:
            self._recovery_biBitCount()
        if status[5] == 0:
            self._recovery_biCompression()
        if status[6] == 0:
            self._recovery_biSizeImage()
        if status[7] == 0:
            self._recovery_biXPixPerMeter()
        if status[8] == 0:
            self._recovery_biYPixPerMeter()
        if status[9] == 0:
            self._recovery_biClrUsed()
        if status[10] == 0:
            self._recovery_biClrImportant()
        new_image_head = self.bmp_content[28:108]

        if not fast:
            self.all_resolution.append(self.bmp_content)
            for width, height in tqdm.tqdm(self.possible_d, desc="recovery image head with all possible resolution"):
                self._recovery_biHeight(height)
                self._recovery_biWidth(width)
                self.all_resolution.append(self.bmp_content)


        assert len_bmp == len(self.bmp_content), "error happend to length of bmp_content when recovery image head"
        return new_image_head
