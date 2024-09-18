from typing import List
from math import ceil
from PIL import Image, ImageDraw, ImageFont
from random import random, randint, gauss
from utils import clip_gauss


class Pattern:
    def __init__(self, mode, type):
        right = 0x00 if mode == "light" else 0xFF
        self.foreground = randint(0xE0, 0xFF) ^ right
        self.middleground = randint(0x30, 0x7F) ^ right
        self.background = randint(0x00, 0x5F) ^ right
        self.type = type

    def generate(self, width, height):
        self.image = Image.new("L", (width, height), self.background)
        line_width = randint(height // 100, height // 50) + 1
        spacing = randint(height // 50, height // 10) + 1
        draw = ImageDraw.Draw(self.image)
        if self.type in ["vertical", "grid"]:
            pos = 0
            for _ in range(ceil(width / spacing)):
                draw.line(((pos, 0), (pos, height)), self.middleground, line_width)
                pos += spacing
        if self.type in ["horizontal", "grid"]:
            pos = 0
            for _ in range(ceil(height / spacing)):
                draw.line(((0, pos), (width, pos)), self.middleground, line_width)
                pos += spacing


class CharacterStyle:
    def __init__(
        self,
        basesize: int = 24,
        rotate_sigma: float = 1.5,
        stretch: float | List[float] = [0.2, 0.4],
        swapcase_rate: float = 0.25,
    ):
        self.size = int(basesize)
        self.rotate_sigma = float(rotate_sigma)
        if isinstance(stretch, (int, float)):
            self.stretch = [float(stretch)] * 2
        elif len(stretch) == 1:
            self.stretch = [float(stretch[0])] * 2
        elif len(stretch) == 2:
            self.stretch = [float(item) for item in stretch]
        self.swapcase_rate = swapcase_rate


class Character:
    def __init__(
        self,
        character: str,
        style: CharacterStyle,
        pattern: Pattern,
    ):
        self.character = character
        self.style = style
        self.pattern = pattern
        self.random_size = float(style.size) * clip_gauss(0.8, 1.2)

    def generate(
        self,
        font_path: str,
    ):
        if self.character.isspace():
            space_image = Image.new("L", (ceil(self.random_size / 2), 0))
            self.image = space_image
            self.mask = space_image
            return

        if (
            self.character.encode("UTF-8").isalpha()
            and random() < self.style.swapcase_rate
        ):
            self.character = self.character.swapcase()

        font = ImageFont.truetype(font_path, self.random_size)

        horizontal_stretch, vertical_stretch = self.style.stretch

        ascent, descent = font.getmetrics()
        width = font.font.getsize(self.character)[0][0]
        height = ascent + descent

        image_width = int(width * (1 + 2 * horizontal_stretch))
        image_height = int(height * (1 + 2 * vertical_stretch))

        self.pattern.generate(image_width, image_height)
        self.image = self.pattern.image
        draw_image = ImageDraw.Draw(self.image)
        draw_image.text(
            xy=(width * horizontal_stretch, height * vertical_stretch),
            text=self.character,
            fill=self.pattern.foreground,
            font=font,
        )

        self.mask = Image.new("L", (image_width, image_height), 0)
        draw_mask = ImageDraw.Draw(self.mask)

        corners = [
            (0, 0),
            (0, 1 + vertical_stretch),
            (1 + horizontal_stretch, 1 + vertical_stretch),
            (1 + horizontal_stretch, 0),
        ]

        random_offsets = [
            (
                clip_gauss(0, horizontal_stretch),
                clip_gauss(0, vertical_stretch),
            )
            for _ in range(4)
        ]

        corners = [
            (corners[i][0] + random_offsets[i][0], corners[i][1] + random_offsets[i][1])
            for i in range(4)
        ]

        corners = [(corners[i][0] * width, corners[i][1] * height) for i in range(4)]
        corners = tuple(tuple(coordinate) for coordinate in corners)

        draw_mask.polygon(corners, fill=0xFF)
        crop_zone = self.mask.getbbox()
        degree = gauss(sigma=self.style.rotate_sigma)

        self.image = self.image.crop(crop_zone).rotate(degree, expand=True)
        self.mask = self.mask.crop(crop_zone).rotate(degree, expand=True)
