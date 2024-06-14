import os


def hex2d(hex_str):
    """
    将十六进制字符串转换为十进制字符串
    :param hex_str:
    :return:
    """
    return str(int(hex_str, 16))


def d2hex(decimal_num):
    """
    将十进制字符串转换为十六进制字符串
    :param decimal_num:
    :return:
    """
    return hex(int(decimal_num))[2:].upper()


def formathex(hex_str, length):
    """
    按照计算机底层的排列方式，将hex_str按照每个字节为一组的方式反向排列，并且填充到length字节
    :param hex_str:
    :param length:
    :return:
    """
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str
    hex_list = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]
    hex_list.reverse()
    while len(hex_list) < length:
        hex_list.append('00')
    return ''.join(hex_list).upper()


def read(fileLocation='./brokenImg/实验练习1', baseLocation='./base/backup.bmp'):
    """
    读取BMP文件
    :param fileLocation:
    :param baseLocation:
    :return:
    """
    with open(fileLocation, 'rb') as f:
        bmp_content = f.read()

    # 将BMP文件备份一份，存储在新的路径下
    # 如果baseLocation不存在，则创建该路径
    if not os.path.exists(baseLocation.replace("backup.bmp", "")):
        os.makedirs(baseLocation.replace("backup.bmp", ""))

    with open(baseLocation, 'wb') as f:
        f.write(bmp_content)
    return bmp_content.hex()


def save(bmp_content, saveLocation='./base/backup.bmp'):
    """
    将修改后的BMP文件保存到指定路径
    :param bmp_content: 一个长度为2n的十六进制的字符串
    :param saveLocation:
    :return:
    """
    with open(saveLocation, 'wb') as f:
        f.write(bytes.fromhex(bmp_content))


def modify(bmp_content, offset_start, offset_end, new_value):
    """
    修改BMP文件的内容(假设offset_start和offset_end是十进制下有效的偏移量，new_value是十六进制下的值)
    :param bmp_content:这是一个16进制的字符串
    :param offset_start:
    :param offset_end:
    :param new_value:新的十六进制的字符串值
    :return:
    """
    assert offset_start < offset_end, "offset_start must be less than offset_end"
    assert len(bmp_content) % 2 == 0, "bmp_content must have an even number of characters"
    assert len(str(new_value)) == 2, "new_value must be a two-digit hexadecimal number"
    # 将bmp_content中的字符两个为一组，组成一个新的列表
    bmp_content = [bmp_content[i:i + 2] for i in range(0, len(bmp_content), 2)]
    for i in range(offset_start, offset_end):
        bmp_content[i] = str(new_value)

    return ''.join(bmp_content)


if __name__ == '__main__':
    print(hex2d('10'), type(hex2d('10')))
    print(d2hex('10'), type(d2hex('10')))
    print(formathex('645d6', 4))