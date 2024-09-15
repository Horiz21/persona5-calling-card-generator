import os
from PIL import Image
from random import choice


class FontManager:
    def __init__(self, root: str):
        self.paths = [os.path.join(root, filename) for filename in os.listdir(root)]
        self.len = len(self.paths)
        self.work_paths = list(range(self.len))

    def reset(self):
        self.work_paths = list(range(self.len))

    def remove(self, index):
        self.work_paths.remove(index)

    def choice(self):
        index = choice(self.work_paths)
        return index, self.paths[index]


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
