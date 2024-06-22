import os
from typing import List
from math import ceil, sqrt
from PIL import Image, ImageDraw, ImageFilter
from paragraph import Paragraph
from font_manager import FONTS_PATH


class CardBackground:
    def __init__(
        self,
        radii: List[float] = [120, 150],
        colors: List[str] = ["#F00", "#000"],
    ):
        self.radii = radii
        self.colors = colors

    def generate(self, width: int, height: int):
        self.image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(self.image)

        x_center = width // 2
        y_center = height // 2
        diagonal = sqrt(x_center**2 + y_center**2)

        element_count = len(self.radii)
        repeat_count = ceil(diagonal / sum(self.radii))

        multipliers = [repeat_count] * element_count

        for i in range(repeat_count * element_count):
            current_radius = sum(m * r for m, r in zip(multipliers, self.radii))
            draw.ellipse(
                (
                    x_center - current_radius,
                    y_center - current_radius,
                    x_center + current_radius,
                    y_center + current_radius,
                ),
                fill=self.colors[~i % element_count],
            )
            multipliers[~multipliers[::-1].index(max(multipliers[::-1]))] -= 1


class CallingCard:
    def __init__(
        self,
        set_width: int,
        padding: int | List[int],
        background: CardBackground,
        paragraphs: List[Paragraph],
        fonts_path: str,
        smooth: bool = False,
    ):
        self.image_width = set_width

        if isinstance(padding, int):
            self.padding = [padding] * 4
        elif len(padding) == 1:
            self.padding = padding * 4
        elif len(padding) == 2:
            self.padding = padding * 2
        elif len(padding) == 4:
            self.padding = padding

        self.content_max_width = set_width - self.padding[0] - self.padding[2]

        self.background = background
        self.paragraphs = paragraphs

        self.fonts_path = fonts_path

        self.blur_radius = 1 if smooth else 0

    def generate(self):
        for paragraph in self.paragraphs:
            paragraph.generate(
                content_max_width=self.content_max_width,
                fonts_path=self.fonts_path,
            )
        content_height = sum(paragraph.height for paragraph in self.paragraphs)
        self.image_height = content_height + self.padding[1] + self.padding[3]
        self.background.generate(self.image_width, self.image_height)

        total_image = Image.new("L", (self.content_max_width, content_height), 0)
        total_mask = Image.new("L", (self.content_max_width, content_height), 0)
        nowy = 0
        for paragraph in self.paragraphs:
            cnt = len(paragraph.images)
            for i in range(cnt):
                image = paragraph.images[i]
                mask = paragraph.masks[i]
                if paragraph.style.align.lower() in ["l", "left"]:
                    posx = 0
                elif paragraph.style.align.lower() in ["c", "center", "centre"]:
                    posx = (self.content_max_width - image.width) // 2
                elif paragraph.style.align.lower() in ["r", "right"]:
                    posx = self.content_max_width - image.width
                total_image.paste(image, (posx, nowy))
                total_mask.paste(mask, (posx, nowy))
                nowy += image.height

        self.image = self.background.image.filter(
            ImageFilter.GaussianBlur(self.blur_radius)
        )
        self.image.paste(
            total_image,
            (self.padding[0], self.padding[1]),
            total_mask.filter(ImageFilter.GaussianBlur(self.blur_radius)),
        )

    def save(
        self,
        path: str = "",
        name: str = "persona5_card.png",
    ):
        self.image.save(os.path.join(path, name))
