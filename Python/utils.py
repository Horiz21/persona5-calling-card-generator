import os
from PIL import Image
from random import choice, gauss


def clip_gauss(start: float, end: float):
    mean = (start + end) / 2
    std_dev = (end - start) / 6
    sample = gauss(mean, std_dev)
    return (
        sample
        if sample >= start and sample <= end
        else start if sample <= start else end
    )


class OverlayMaker:
    def __init__(self, layers, colors):
        num = len(layers)
        size = Image.open(layers[0]).size
        self.image = Image.new("RGBA", size, (0, 0, 0, 0))
        for i in range(num):
            self.image.paste(
                im=Image.new("RGB", size, colors[i]),
                mask=Image.open(layers[i]),
            )

    def get_resized_overlay(self, size: tuple):
        width_resize_ratio = size[0] / self.image.width
        height_resize_ratio = size[1] / self.image.height
        final_resize_ratio = min(width_resize_ratio, height_resize_ratio)
        return self.image.resize(
            (
                int(self.image.width * final_resize_ratio),
                int(self.image.height * final_resize_ratio),
            ),
            resample=Image.LANCZOS,
        )


class FontManager:
    def __init__(self, fonts_root: str):
        self.fonts_path = [
            os.path.join(fonts_root, font)
            for font in os.listdir(fonts_root)
            if os.path.join(fonts_root, font).lower().endswith((".ttc", ".ttf", ".otf"))
        ]
        self.len = len(self.fonts_path)
        if self.len == 0:
            raise ValueError(
                f"The specified directory {fonts_root} does not contain any font files for the supported formats."
            )
        self.indexs = list(range(self.len))

    def reset(self):
        self.indexs = list(range(self.len))

    def remove(self, index):
        self.indexs.remove(index)

    def choice(self):
        index = choice(self.indexs)
        return index, self.fonts_path[index]


class Watermark:
    def __init__(self):
        self.end = [1] * 8

    def embed(self, text: str, img: Image):
        width, height = img.size
        pixels = img.load()

        bits = [int(bit) for byte in text.encode("utf-8") for bit in f"{byte:08b}"]
        bits.extend(self.end)

        for i, bit in enumerate(bits):
            if i >= width * height:
                break
            y, x = divmod(i, width)
            r, g, b = pixels[x, y]
            if (r & 1) != bit:  # Only modify necessary pixels
                r = (r & 0xFE) | bit
                pixels[x, y] = (r, g, b)

        return img

    def extract(self, img: Image):
        width, height = img.size
        pixels = img.load()
        bits = []

        for y in range(height):
            for x in range(width):
                bits.append(pixels[x, y][0] & 1)
                if bits[-8:] == self.end:
                    bits = bits[:-8]
                    break
            else:
                continue
            break

        n = len(bits)
        bytes_list = [
            int("".join(map(str, bits[i : i + 8])), 2) for i in range(0, n, 8)
        ]

        return bytes(bytes_list).decode("utf-8", errors="ignore")
