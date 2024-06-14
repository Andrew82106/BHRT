# BMP Header Recover Tool: BMP 文件头和图像头恢复工具

该项目提供了一个用于恢复损坏的 BMP 文件头和图像头的工具。主要类 `bmp24` 继承自 `Recovery` 类，包含检查和恢复 BMP 文件头和图像头中各个字段的方法。当前该工具专为 24 位颜色深度的 BMP 文件设计。

## 功能

- **检查文件头**：识别 BMP 文件头中缺失或损坏的字段。
- **恢复文件头**：自动恢复 BMP 文件头中缺失或损坏的字段。
- **检查图像头**：识别 BMP 图像头中缺失或损坏的字段。
- **恢复图像头**：自动恢复 BMP 图像头中缺失或损坏的字段。
- **计算可能的图像尺寸**：根据图像数据大小计算可能的宽度和高度。
  
自动计算分辨率恢复样例（正确分辨率恢复结果与错误分辨率恢复结果）：

![恢复示例](./base/all_resolution/recovery_0.bmp)

![恢复示例](./base/all_resolution/recovery_11.bmp)

## 快速开始

### 前提条件

确保已安装以下库：

- `tqdm`：用于恢复过程中显示进度条。

可以使用 pip 安装所需库：

```bash
pip install tqdm
```

### 使用方法

1. **克隆项目：**

```bash
git clone https://github.com/Andrew82106/BHRT.git
cd BHRT
```

2. **准备损坏的 BMP 文件：**

将损坏的 BMP 文件放置在 `brokenImg/` 目录下，命名为``实验练习2``(无后缀名)

3. **运行主程序：**

```bash
python main.py
```

该程序会读取损坏的 BMP 文件，检查并恢复文件头和图像头，并将恢复后的文件保存在 `base/` 目录下。

当启用了``recovery_image_head``方法的``fast``参数后，程序不会尝试恢复所有可能的分辨率。否则程序将会把所有可能的分辨率的恢复结果放在`base/all_resolution` 目录下，恢复完成后可查看该文件夹下的文件即可得到最符合实际的恢复结果。

## 接口示例代码

### 导入所需模块

```python
from recovery24 import bmp24
from process import read, save

# 读取损坏的 BMP 文件
bmp_content = read('./brokenImg/实验练习2')

# 创建 bmp24 对象
bmp_recovery = bmp24(bmp_content)
```

### 检查和恢复 BMP 文件头

```python
# 检查文件头
file_head_status = bmp_recovery.check_file_head()

# 恢复文件头
new_file_head = bmp_recovery.recovery_file_head(file_head_status)

# 更新 bmp_content
bmp_content = bmp_recovery.bmp_content

# 保存恢复后的 BMP 文件
save(bmp_content, './base/recovered_file_head.bmp')
```

### 检查和恢复 BMP 图像头

```python
# 检查图像头
image_head_status = bmp_recovery.check_image_head()

# 恢复图像头
new_image_head = bmp_recovery.recovery_image_head(image_head_status)

# 更新 bmp_content
bmp_content = bmp_recovery.bmp_content

# 保存恢复后的 BMP 文件
save(bmp_content, './base/recovered_image_head.bmp')
```

### 恢复所有可能分辨率的图像头

```python
# 使用 fast=0 恢复所有可能分辨率的图像头
bmp_recovery.recovery_image_head(image_head_status, fast=0)

# 保存所有可能分辨率的恢复结果
for index, bmp_content in enumerate(bmp_recovery.all_resolution):
    save(bmp_content, f'./base/all_resolution/recovered_{index}.bmp')
```

## 接口说明

### `bmp24` 类

- **`check_file_head()`**

  - 检查 BMP 文件头中缺失或损坏的字段。
  - 返回一个状态列表，指示每个字段的存在（1）或不存在（0）。
- **`recovery_file_head(status)`**

  - 根据提供的状态列表恢复 BMP 文件头中缺失或损坏的字段。
  - 参数：
    - `status`：各个字段的状态列表。
  - 返回恢复后的文件头。
- **`check_image_head()`**

  - 检查 BMP 图像头中缺失或损坏的字段。
  - 返回一个状态列表，指示每个字段的存在（1）或不存在（0）。
- **`recovery_image_head(status, fast=1)`**

  - 根据提供的状态列表恢复 BMP 图像头中缺失或损坏的字段。
  - 参数：
    - `status`：各个字段的状态列表。
    - `fast`：是否快速模式。如果为 0，则尝试用所有可能的分辨率进行恢复；否则只恢复一个分辨率。
  - 返回恢复后的图像头。

### `process` 模块

- **`read(fileLocation, baseLocation)`**

  - 读取 BMP 文件内容。
  - 参数：
    - `fileLocation`：损坏的 BMP 文件路径。
    - `baseLocation`：备份 BMP 文件路径。
  - 返回 BMP 文件内容的十六进制字符串。
- **`save(bmp_content, saveLocation)`**

  - 保存恢复后的 BMP 文件内容。
  - 参数：
    - `bmp_content`：BMP 文件内容的十六进制字符串。
    - `saveLocation`：保存路径。
- **`modify(bmp_content, offset_start, offset_end, new_value)`**

  - 修改 BMP 文件内容的指定区域。
  - 参数：
    - `bmp_content`：BMP 文件内容的十六进制字符串。
    - `offset_start`：起始偏移量。
    - `offset_end`：结束偏移量。
    - `new_value`：新的十六进制值。

## 提醒

当前的 `bmp24` 库只能对 24 位颜色深度的 BMP 图像头进行恢复。如果您需要恢复其他位数的 BMP 图像头，可以基于 `Recovery.py` 定义的框架，提供其他位数图像的恢复代码。

欢迎对该项目进行改进和扩展！
