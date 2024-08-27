# Persona 5 预告信生成器

![标题](title.png)

Persona 5 预告信生成器（Persona 5 Calling Card Generator, P5CCG）是一款帮助用户轻松创建符合 Persona 5 风格预告信的工具。无论是个人项目还是同人作品，只需几分钟，即可制作出个性化的预告信。

## 主要功能

- 生成 Persona 5 风格的预告信
- 自定义卡片背景、内容和文字样式等细节
- 易用的图形用户界面（GUI）

生成示例如下：

![预告信](persona5_card.png)

## GUI 用户指南

本部分适用于不熟悉 Python 的普通用户。

P5CCG 的图形用户界面基于 Avalonia 构建，运行环境需安装 .NET Runtime。如果您不确定是否已安装该环境，可以直接进入下一步安装、下载与启动 P5CCG。如果已安装，程序将直接运行；如果未安装，系统将弹出提示窗口，并引导您前往微软官方网站下载 .NET Runtime。运行程序前，建议创建一个专用的字体文件夹，将想要使用的字体存放其中，并在运行时指向该文件夹。

### 获取与启动 P5CCG

访问本仓库的 Release 页面，下载已打包的压缩包（目前仅提供 Windows 版本）。解压后，双击运行根目录下的 `P5CCG.exe` 文件。

### 使用 GUI 界面生成、预览与导出

打开软件后，P5CCG 将展示一个简洁的图形界面。在界面中，您可以填写或选择以下内容：页面比例、字体目录、背景颜色、文本内容、段落样式。点击“生成”按钮将随机生成一封预告信，满意后可使用“导出”选项将生成的预告信保存到本地。

### 注意事项

P5CCG 有时可能无法正确识别默认的用户字体目录。如前文所述，建议创建一个专属的字体库，用于存放候选字体。这样不仅可以确保字体能够正确加载，还能防止因字体库不全导致的乱码或空白。

## 高级用户指南

P5CCG 的图像生成功能由 Python 脚本提供。对于熟悉 Python 或愿意阅读代码的用户，只需阅读并修改 `demo.py` 文件中 `main()` 函数内 `card = CallingCard(...)` 的输入参数。运行该脚本至少需要安装 Pillow（PIL）。通过源代码使用 P5CCG 时，可根据需求进行更自由的配置和生成。

### 类与参数

#### `CallingCard` 类

直接创建预告信的类是 `CallingCard` 类。此处由此展开介绍构造该类时的形式参数。

- `set_width`: 图像的宽度，单位是像素(px)。
- `set_height`：图像的高度，单位是像素(px)。
- `padding`: 图像的内边距。或者为一个 `int` 值，代表 `四边` 的内边距；或者长度为 1/2/4 的整型列表，代表 `[四边]`/`[左右边,上下边]`/`[左边,上边,右边,下边]` 的内边距。
- `background`: `CardBackground` 类的实例。见 [后文](#cardbackground-类)。
- `paragraphs`: `Paragraph` 实例的列表。见 [后文](#paragarph-类)。
- `fonts_path`: 字体文件夹，存放 `.ttf`/`.otf` 等格式的字体文件。对于 Windows 用户，脚本默认指向用户字体文件夹。注意：**由于：①系统的字体文件夹中存在一些特殊字体；②随机抽选字体过程中可能遇到字库不全的字体文件，可能致使显示错误，更好的做法是使用另一个文件夹来存放所有想要使用的字体**。
- `antialias`: 整型，用于抗锯齿。P5CCG 将首先生成长、宽各 `antialias` 倍的图像，然后再使用 Lanczos 重采样算法缩小回目标尺寸，得到较为平滑的图像。该值为 `1` 时，抗锯齿关闭。

#### `CardBackground` 类

`CardBackground` 类的实例用于生成同心圆样式的卡片背景。有两个列表形式的参数，这两个列表的**长度需一致**。

- `radii`: 从内到外的同心圆的半径增量。
- `colors`: 从内到外的同心圆的颜色。可以使用 16 进制颜色值（例如: `"#FFF"` 或 `"#FF0000"`）。

在 `default_styles.py` 中提供了一个常量 `PERSONA5_BACKGROUND`，即红黑相见的默认样式。

`CardBackground` 的颜色可以有一至多个。

#### `Paragarph` 类

每个 `Paragarph` 实例的构造函数具有两个形式参数。

- `text`: 文本内容。
- `style`: `ParagarphStyle` 类的实例，指明该段落样式。

`ParagarphStyle` 类是 `Paragraph` 类的样式，每个 `Paragraph` 类都有独立的样式。样式的构造函数需要传入：

- `align`: 对齐方式，必须是 `"L"` 或 `"Left"`、`"C"` 或 `"Center"` 或 `"Centre"`、`"R"` 或 `"Right"` 中的一个，大小写不敏感。
- `float`: 单字纵向浮动，整型，单位是像素(px)。程序会将当前所有字的图像在垂直方向居中，然后对每个字进行 `[-float, float]` 的浮动（竖直方向位移）。
- `shift`: 字间横向偏移，单位是像素(px)。或者为一个 `int` 值，代表横向字距固定为 `shift` 值；或者是一个长度为 2 的整型列表，分别代表字距在 `shift` 的区间范围内随机取样。是列表时，右值应当不小于左值。
- `character_style`：段落内文字样式。见 [后文](#character-类)。

`default_styles.py` 文件设定了一些默认的样式，例如 `TITLE_PARAGRAPH` 和 `CONTENT_PARAGRAPH` 等。

#### `Character` 类

`Character` 类一般不会被手动调用。它的构造函数需要传入：

- `character`: 单个需要渲染的字。
- `style`: `CharacterStyle` 对象，渲染样式。
- `pattern`: `Pattern`，单个文字的底纹。

在重要的 `CharacterStyle` 类的构造函数中，需要传入：

- `basesize`: 内容的字体基础大小。实际文本大小是该值乘以一个服从正态分布 $N(1,0.1)$ 的系数，并且限制范围为在 $[75\%, 125\%]$。
- `rotate_sigma`: 字体旋转的标准差。实际文本将服从 $N(0,\verb|rotate_sigma|)$ 的正态分布进行旋转，单位为度(deg)。
- `stretch`: 外边距(Margin)的最大值，是含有两个 `float` 的列表，代表内容中的文本在横向和纵向的可扩展范围。脚本将从范围中采样一些值，产生夸张的四边形作为每个字的底纹形状。
- `swapcase_rate`: 转换原文字母大小写的概率，应当是一个 $[0,1]$ 间的数字。仅对 ASCII 中的拉丁字母生效。

`Pattern` 暂不具备可设置项。不过，可以修改下面的全局参数进行调整。

- `SCHEME`: 文字的两种配色方案：浅色底纹深色文字(`"light"`)，或者深色底纹浅色文字(`"dark"`)。
- `SCHEME_WEIGHT`: 上述配色方案的出现权重，默认为等概率的 `[1, 1]`。可自由调整为自己喜欢的权重，例如永远都是深色底纹浅色文字的 `[0, 1]`。
- `PATTERN`: 文字的四种底纹图案：纯色、竖条纹、横条纹或者格纹。
- `PATTERN_WEIGHT`: 上述底纹的出现权重，默认为 `[15, 2, 2, 1]`。可自由调整为自己喜欢的权重，例如永远都是格纹的 `[0, 0, 0, 1]`。

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
