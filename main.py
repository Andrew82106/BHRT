from process import read, save
from recovery24 import bmp24

if __name__ == '__main__':
    bmp = read('./brokenImg/实验练习2')
    r = bmp24(bmp)
    status = r.check_file_head()
    n_head = r.recovery_file_head(status)
    status1 = r.check_image_head()
    n_image_head = r.recovery_image_head(status1)
    new_bmp = r.bmp_content
    save(new_bmp, './base/recovery.bmp')

    r.recovery_image_head(status1, fast=0)

    for index, bmp_content in enumerate(r.all_resolution):
        save(bmp_content, f'./base/all_resolution/recovery_{index}.bmp')
    print("end")