import os
import numpy as np
from math import ceil, floor, sqrt
from PIL import Image, ImageDraw, ImageFont
from random import randint, uniform, choices, random, normalvariate

MODE = ["light", "dark"]
PATTERN = ["horizontal", "grid", "vertical", "flat"]
PATTERN_WEIGHT = [2, 2, 1, 15]

TRANSPARENT = (0, 0, 0, 0)

BASESIZE = {
    "salutation": 72,
    "name": 96,
    "body": 54,
    "signature": 36,
    "date": 28,
}


class FontManager:
    def __init__(self, root):
        self.paths = [os.path.join(root, filename) for filename in os.listdir(root)]

    def choice(self):
        return choices(self.paths)[0]


class Pattern:
    def __init__(self, mode, type):
        if mode == "dark":
            self.background = (randint(0, 95),)
            self.middleground = (randint(48, 127),)
            self.foreground = (randint(224, 255),)
        else:
            self.background = (randint(160, 255),)
            self.middleground = (randint(128, 208),)
            self.foreground = (randint(0, 32),)
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
            space_width = ceil(font_size / 2)
            space_image = Image.new("RGBA", (space_width, 0), TRANSPARENT)
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
        self.mask = Image.new("RGBA", (image_width, image_height), TRANSPARENT)
        draw = ImageDraw.Draw(self.image)
        draw_alpha = ImageDraw.Draw(self.mask)
        dots = [
            (
                width * (0 + horizon_stretch) - uniform(0, width * horizon_stretch),
                height * (0 + vertical_stretch) - uniform(0, height * vertical_stretch),
            ),
            (
                width * (1 + horizon_stretch) + uniform(0, width * horizon_stretch),
                height * (0 + vertical_stretch) - uniform(0, height * vertical_stretch),
            ),
            (
                width * (1 + horizon_stretch) + uniform(0, width * horizon_stretch),
                height * (1 + vertical_stretch) + uniform(0, height * vertical_stretch),
            ),
            (
                width * (0 + horizon_stretch) - uniform(0, width * horizon_stretch),
                height * (1 + vertical_stretch) + uniform(0, height * vertical_stretch),
            ),
        ]
        minx = floor(min(x[0] for x in dots))
        miny = floor(min(x[1] for x in dots))
        maxx = ceil(max(x[0] for x in dots))
        maxy = ceil(max(x[1] for x in dots))
        crop_coordinate = (minx, miny, maxx, maxy)
        rotate_degree = normalvariate(sigma=4)

        draw_alpha.polygon(dots, fill=(0, 0, 0))
        draw.text(
            xy=(width * horizon_stretch, height * vertical_stretch),
            text=self.character,
            fill=self.pattern.foreground,
            font=font,
        )
        self.image = self.image.crop(crop_coordinate).rotate(rotate_degree, expand=True)
        self.mask = self.mask.crop(crop_coordinate).rotate(rotate_degree, expand=True)


class Paragraph:
    def __init__(self, text, align, type, stretch):
        self.text = text
        self.align = align
        self.type = type
        self.stretch = stretch
        self.images = []

        self.work_images = []
        self.work_masks = []

        self.height = 0

    def horizontal_arrange(self, spacing):
        num_image = len(self.work_images)
        height = max(image.height for image in self.work_images) + spacing * 2
        width = sum(image.width for image in self.work_images) + spacing * num_image
        posx = 0

        horizon_image = Image.new("RGBA", (width, height), TRANSPARENT)

        for i, image in enumerate(self.work_images):
            posy = (height - image.height) // 2 + randint(-spacing, spacing)
            horizon_image.paste(image, (posx, posy), self.work_masks[i])
            posx += image.width + randint(-spacing, spacing)

        x1, y1, x2, y2 = horizon_image.getbbox()
        horizon_image = horizon_image.crop((x1, y1, x2, y2))

        self.work_images.clear()
        self.work_masks.clear()
        self.images.append(horizon_image)

    def generate(self, content_max_width, spacing):
        self.font_manager = FontManager(r"C:\Users\Frankie\Desktop\mychoice")

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
                    mode=choices(MODE)[0],
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
    def __init__(self, radii, colors):
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
        dic_of_content,
    ):
        self.set_width = set_width
        self.side_space = side_space
        self.content_max_width = int(set_width * (1 - 2 * side_space))

        self.background = background
        self.dic_of_content = dic_of_content

    def generate(self):
        for key in self.dic_of_content:
            self.dic_of_content[key].generate(
                content_max_width=self.content_max_width,
                spacing=0,
            )
        content_height = sum(para.height for para in self.dic_of_content.values())
        image_height = ceil(content_height / (1 - 2 * self.side_space))
        self.background.generate(self.set_width, image_height)

        total_image = Image.new(
            "RGBA", (self.content_max_width, content_height), TRANSPARENT
        )
        nowy = 0
        for key in self.dic_of_content:
            for image in self.dic_of_content[key].images:
                if self.dic_of_content[key].align == "L":
                    posx = 0
                elif self.dic_of_content[key].align == "C":
                    posx = (self.content_max_width - image.width) // 2
                elif self.dic_of_content[key].align == "R":
                    posx = self.content_max_width - image.width
                total_image.paste(image, (posx, nowy), image)
                nowy += image.height
        x1, y1, x2, y2 = total_image.getbbox()
        total_image = total_image.crop((x1, y1, x2, y2))

        self.image = self.background.image
        self.image.paste(
            total_image,
            (
                int(self.set_width * self.side_space),
                int(image_height * self.side_space),
            ),
            total_image,
        )

    def get_info(self):
        return [
            (self.salutation, 72),
            (self.name, 96),
            (self.body, 54),
            (self.signature, 36),
            (self.date, 28),
        ]

    def save(self):
        self.image.save("card.png")


def main():
    card = CallingCard(
        set_width=1600,
        side_space=0.05,
        background=CardBackground(
            radii=[120, 150],
            colors=[(255, 0, 0), (0, 0, 0)],
        ),
        dic_of_content={
            "salutation": Paragraph(
                "富含碳水化合物、纤维和钾的", "C", "salutation", [0.2, 0.4]
            ),
            "name": Paragraph("Musa nana Lour.", "C", "name", [0.2, 0.5]),
            "body": Paragraph(
                """你那一点可怜的价值，
能请到除了猴子以外的员工吗？
无足轻重的水果，
我们早已洞悉你内心最隐秘的恐惧，
你试图用廉价的糖分来掩盖自己的虚弱！
现在就是时候让你正视自己的可悲本质了。
我们会在预定时间来偷走你的热量，
祝你好运。""",
                "C",
                "body",
                [0.2, 0.2],
            ),
            "signature": Paragraph("心灵怪盗团", "R", "signature", [0.2, 0.2]),
            "date": Paragraph("2024年6月3日", "R", "date", [0.2, 0.2]),
        },
    )
    card.generate()
    card.save()


if __name__ == "__main__":
    main()
