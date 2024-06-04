# Persona 5 预告信生成器

**中文** | [English](README.md)

该 Python 脚本用于生成 Person 5 风格的预告信。

## 主要功能

- 生成 Persona 5 风格的预告信
- 支持自定义卡片背景、内容和文字样式
- 许多可自定义的细节

生成实例如下：

![预告信](examples/calling_card_example_2.png)

## 环境

要运行该脚本，至少需要安装 NumPy 和 Pillow（PIL）这两个库。对于使用 Anaconda 配置 Python 环境的用户来说，这两个库是默认安装的。

## 使用

对于熟悉 Python 的用户和愿意阅读代码的用户，只需要修改 `main()` 函数中 `card = CallingCard(...)` 的输入参数即可。

对于其他用户，一个易于使用的 GUI 正在开发中，可能会以网页形式呈现。由于作者的精力和在 Web 开发方面的知识和经验有限，这可能需要一些时间。

## 参数

### 基本参数

- `fonts_path`: 字体文件夹，存放 `.ttf`/`.otf` 等格式的字体文件。对于 Windows 用户，脚本默认指向用户字体文件夹。注意：**由于①系统的字体文件夹中存在一些特殊字体；②随机抽选字体过程中可能遇到字库不全的字体文件，可能致使显示错误，更好的做法是使用另一个文件夹来存放所有想要使用的字体**。
- `set_width`: 图像的宽度，单位是像素(px)。由于内容长度不确定，因此仅开放了宽度设置，长度会根据实际内容动态调整。
- `side_space`: 图像的内边距。输入 0.05 时，图像的内边距设为四边各 5%，即实际内容范围是图像宽度的 90%。
- `background`: 一个 `CardBackground` 类的实例，用于生成同心圆样式的卡片背景。有两个列表形式的参数，这两个列表的长度需一致。
  - `radii`: 从内到外的同心圆的半径增量。
  - `colors`: 从内到外的同心圆的颜色。可以使用 16 进制颜色值（例如: `#FFF` 或 `#FF0000`）。
- `contents`: 内容列表。内容是一系列的 `Paragraph` 实例。每个实例的构造函数具有四个形式参数。
  - `text`: 文本内容。
  - `align`: 对齐方式，必须是 `L`(居左)、`C`(居中)或者 `R`(居右)中的一个。
  - `type`: 内容类型，决定了字体的基础大小。必须是下列五值中的一个: 
    - `"salutation"`: 预告信收信人的称号（例如 `富含碳水化合物的`）
    - `"name"`: 预告信收信人的名称 (例如 `香蕉先生`)
    - `"body"`: 预告信的正文 (例如 `我们会择时夺取你的热量`)
    - `"signature"`: 预告信发信人的名称 (例如 `水果猎人`)
    - `"date"`: 日期
  - `stretch`: 外边距(Margin)的最大值，是含有两个 `float` 的列表，代表内容中的文本在横向和纵向的可扩展范围。脚本将从范围中采样一些值，产生夸张的四边形作为每个字的底纹。
- `smooth`: 是否进行平滑。由 PIL 生成的图像较为锐利，如果希望较为平滑的图像，可以将该值设置为 `True`，否则默认将不进行平滑操作。

### 高级参数

除了以上参数，生成器还有一些有趣的可自定义参数。不过，这些参数相对用的较少，也更复杂一些。

- `MODE`: Persona 5 的预告信中文字的两种配色方案：浅色底纹深色文字(`"light"`)，或者深色底纹浅色文字(`"dark"`)。
- `MODE_WEIGHT`: 上述配色方案的出现权重，默认为等概率的 `[1, 1]`。可自由调整为自己喜欢的权重，例如永远都是深色底纹浅色文字的 `[0, 1]`。
- `PATTERN`: Persona 5 的预告信中文字的四种底纹：纯色、竖条纹、横条纹或者格纹。
- `PATTERN_WEIGHT`: 上述底纹的出现权重，默认为 `[15, 2, 2, 1]`。可自由调整为自己喜欢的权重，例如永远都是格纹的 `[0, 0, 0, 1]`。
- `BASESIZE`: 一个存放内容类型和它们的基础大小的字典。实际文本将在 $[90\%, 110\%]\times \verb|BASESIZE|$ 的范围内浮动。

## 更新计划

- [x] 基础程序
- [x] 灰度颜色模式
- [x] 图像平滑选项
- [ ] 更多可自定义的细节
- [ ] GUI

## 许可证

```text
MIT License

Copyright (c) 2024 Horiz21

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
