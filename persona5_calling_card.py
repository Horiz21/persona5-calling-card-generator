import os
from typing import Union
import numpy as np
from math import ceil, sqrt
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from random import randint, uniform, choices, random, normalvariate

MODE = ["light", "dark"]
MODE_WEIGHT = [1, 1]
PATTERN = ["flat", "horizontal", "vertical", "grid"]
PATTERN_WEIGHT = [15, 2, 2, 1]

BASESIZE = {
    "salutation": 72,
    "name": 96,
    "body": 54,
    "signature": 36,
    "date": 32,
}


class FontManager:
    def __init__(self, root):
        self.paths = [os.path.join(root, filename) for filename in os.listdir(root)]

    def choice(self):
        return choices(self.paths)[0]


class Pattern:
    def __init__(self, mode, type):
        right = 0x00 if mode == "light" else 0xFF
        self.foreground = randint(0xE0, 0xFF) ^ right
        self.middleground = randint(0x30, 0x7F) ^ right
        self.background = randint(0x00, 0x5F) ^ right
        self.type = type

    def generate(self, width, height):
        image = Image.new("L", (width, height), self.background)
        line_width = randint(height // 100, height // 50) + 1
        spacing = randint(height // 50, height // 15) + 1
        draw = ImageDraw.Draw(image)
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
        return image


class Character:
    def __init__(self, character, pattern, stretch, swapcase_rate):
        self.character = character
        self.pattern = pattern
        self.stretch = stretch
        self.swapcase_rate = swapcase_rate

    def generate(
        self,
        font_path,
        font_size,
    ):
        if self.character.isspace():
            space_image = Image.new("L", (ceil(font_size / 2), 0))
            self.image = space_image
            self.mask = space_image
            return

        if self.character.encode("UTF-8").isalpha() and random() < self.swapcase_rate:
            self.character = self.character.swapcase()

        font = ImageFont.truetype(font_path, font_size)

        horizon_stretch, vertical_stretch = self.stretch

        ascent, descent = font.getmetrics()
        width = font.font.getsize(self.character)[0][0]
        height = ascent + descent

        image_width = int(width * (1 + 2 * horizon_stretch))
        image_height = int(height * (1 + 2 * vertical_stretch))

        self.image = self.pattern.generate(image_width, image_height)
        draw_image = ImageDraw.Draw(self.image)
        draw_image.text(
            xy=(width * horizon_stretch, height * vertical_stretch),
            text=self.character,
            fill=self.pattern.foreground,
            font=font,
        )

        self.mask = Image.new("L", (image_width, image_height), 0)
        draw_mask = ImageDraw.Draw(self.mask)

        corners = np.array(
            [
                (0, 0),
                (0, 1 + vertical_stretch),
                (1 + horizon_stretch, 1 + vertical_stretch),
                (1 + horizon_stretch, 0),
            ]
        )
        corners += np.random.uniform(
            0, [horizon_stretch, vertical_stretch], size=(4, 2)
        )
        corners *= np.array([width, height])
        corners = tuple(tuple(coordinate) for coordinate in corners)

        draw_mask.polygon(corners, fill=0xFF)
        crop_zone = self.mask.getbbox()
        degree = normalvariate(sigma=4)

        self.image = self.image.crop(crop_zone).rotate(degree, expand=True)
        self.mask = self.mask.crop(crop_zone).rotate(degree, expand=True)


class Paragraph:
    def __init__(self, text, align, type, stretch):
        self.text = text
        self.align = align
        self.type = type
        self.stretch = stretch

        self.images = []
        self.masks = []

        self.work_images = []
        self.work_masks = []

        self.height = 0

    def horizontal_arrange(self, spacing):
        num_image = len(self.work_images)
        height = max(image.height for image in self.work_images) + spacing * 2
        width = sum(image.width for image in self.work_images) + spacing * num_image
        posx = 0

        horizon_image = Image.new("L", (width, height), 0)
        horizon_mask = Image.new("L", (width, height), 0)

        for image, mask in zip(self.work_images, self.work_masks):
            posy = (height - image.height) // 2 + randint(-spacing, spacing)
            horizon_image.paste(image, (posx, posy))
            horizon_mask.paste(mask, (posx, posy))
            posx += image.width + randint(-spacing, spacing)

        crop_zone = horizon_image.getbbox()
        horizon_image = horizon_image.crop(crop_zone)
        horizon_mask = horizon_mask.crop(crop_zone)

        self.work_images.clear()
        self.work_masks.clear()

        self.images.append(horizon_image)
        self.masks.append(horizon_mask)

    def generate(self, content_max_width, spacing, fonts_path):
        self.font_manager = FontManager(fonts_path)

        now_width = 0
        i = 0

        while i < len(self.text):
            if self.text[i] in ["\n", "\r"]:
                self.horizontal_arrange(spacing)
                now_width = 0
                i += 1
                continue

            character = Character(
                self.text[i],
                pattern=Pattern(
                    mode=choices(MODE, weights=MODE_WEIGHT)[0],
                    type=choices(PATTERN, weights=PATTERN_WEIGHT)[0],
                ),
                stretch=self.stretch,
                swapcase_rate=0.25,
            )
            character.generate(
                font_path=self.font_manager.choice(),
                font_size=BASESIZE[self.type] * uniform(0.9, 1.1),
            )

            if now_width + character.image.width <= content_max_width:
                self.work_images.append(character.image)
                self.work_masks.append(character.mask)
                now_width += character.image.width
                i += 1
            else:
                self.horizontal_arrange(spacing)
                now_width = 0
                continue
        self.horizontal_arrange(spacing)
        self.height = sum(image.height for image in self.images)


class CardBackground:
    def __init__(self, radii: list[float], colors: list[str]):
        self.radii = radii
        self.colors = colors

    def generate(self, width, height):
        self.image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(self.image)

        x_center = width // 2
        y_center = height // 2
        diagonal = sqrt(x_center**2 + y_center**2)

        element_count = len(self.radii)
        repeat_count = ceil(diagonal / sum(self.radii))

        multipliers = [repeat_count] * element_count

        for i in range(repeat_count * element_count):
            current_radius = np.matmul(multipliers, self.radii)
            draw.ellipse(
                (
                    x_center - current_radius,
                    y_center - current_radius,
                    x_center + current_radius,
                    y_center + current_radius,
                ),
                fill=self.colors[~i % element_count],
            )
            multipliers[~np.argmax(multipliers[::-1])] -= 1


class CallingCard:
    def __init__(
        self,
        set_width: int,
        side_space: float,
        background: CardBackground,
        contents: list[Paragraph],
        smooth: bool = False,
    ):
        self.image_width = set_width
        self.side_space = side_space
        self.content_max_width = int(set_width * (1 - 2 * side_space))

        self.background = background
        self.contents = contents

        self.blur_radius = 1 if smooth else 0

    def generate(self, fonts_path: str):
        for content in self.contents:
            content.generate(
                content_max_width=self.content_max_width,
                spacing=0,
                fonts_path=fonts_path,
            )
        content_height = sum(para.height for para in self.contents)
        self.image_height = ceil(content_height / (1 - 2 * self.side_space))
        self.background.generate(self.image_width, self.image_height)

        total_image = Image.new("L", (self.content_max_width, content_height), 0)
        total_mask = Image.new("L", (self.content_max_width, content_height), 0)
        nowy = 0
        for content in self.contents:
            cnt = len(content.images)
            for i in range(cnt):
                image = content.images[i]
                mask = content.masks[i]
                if content.align == "L":
                    posx = 0
                elif content.align == "C":
                    posx = (self.content_max_width - image.width) // 2
                elif content.align == "R":
                    posx = self.content_max_width - image.width
                total_image.paste(image, (posx, nowy))
                total_mask.paste(mask, (posx, nowy))
                nowy += image.height

        self.image = self.background.image.filter(
            ImageFilter.GaussianBlur(self.blur_radius)
        )
        left_top = (
            int(self.image_width * self.side_space),
            int(self.image_height * self.side_space),
        )
        self.image.paste(
            total_image,
            left_top,
            total_mask.filter(ImageFilter.GaussianBlur(self.blur_radius)),
        )

    def save(self, path, name):
        self.image.save(os.path.join(path, name))


def main():
    fonts_path = os.path.join(
        os.path.expanduser("~"),
        "AppData/Local/Microsoft/Windows/Fonts",
    )
    # fonts_path = os.path.join(os.path.dirname(__file__), "fonts")

    card = CallingCard(
        set_width=1920,
        side_space=0.05,
        background=CardBackground(
            radii=[120, 150],
            colors=["#F00", "#000"],
        ),
        contents=[
            Paragraph("富含碳水化合物、纤维和钾的", "C", "salutation", [0.2, 0.4]),
            Paragraph("Musa nana Lour.", "C", "name", [0.2, 0.5]),
            Paragraph(
                """你那一点可怜的价值，
能请到除了猴子以外的员工吗？
我们早已洞悉你内心最隐秘的恐惧，
你试图用廉价的糖分来掩盖自己的羸弱！
现在，是时候让你正视自己的可悲本质了。
我们会在预定时间来偷走你的热量，
祝你好运。""",
                "C",
                "body",
                [0.2, 0.2],
            ),
            Paragraph("心灵怪盗团", "R", "signature", [0.2, 0.2]),
            Paragraph("20XY年Z月W日", "R", "date", [0.2, 0.2]),
        ],
        smooth=True,
    )
    card.generate(fonts_path=fonts_path)
    card.save(path="", name="card.png")


if __name__ == "__main__":
    main()
