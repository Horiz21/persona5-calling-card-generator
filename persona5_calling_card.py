from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math
import numpy as np
from PIL import Image, ImageDraw
from random import randint, uniform, choices, random
from math import ceil, floor
import os

MODE = ["light", "dark"]
PATTERN = ["horizontal", "grid", "vertical", "flat"]
PATTERN_WEIGHT = [1, 1, 1, 7]


def gen_char_background(
    width,
    height,
    bgb,
    bgf,
    pattern_type,
):
    space = randint(height // 50, height // 15) + 1
    wd = randint(height // 100, height // 50) + 1
    pattern = Image.new("RGBA", (width, height), bgb)
    draw = ImageDraw.Draw(pattern)
    if pattern_type in ["vertical", "grid"]:
        pos = 0
        for _ in range(width // space + 1):
            draw.line(((pos, 0), (pos, height)), bgf, wd)
            pos += space
    if pattern_type in ["horizontal", "grid"]:
        pos = 0
        for _ in range(height // space + 1):
            draw.line(((0, pos), (width, pos)), bgf, wd)
            pos += space
    return pattern


def draw_concentric_circle(
    image: Image,
    radii: list,
    colors: list,
):
    x_center = image.width // 2
    y_center = image.height // 2

    diagonal = math.sqrt(x_center**2 + y_center**2)

    # 创建一个画图对象
    draw = ImageDraw.Draw(image)
    cnt_element = len(radii)

    repeats = math.ceil(diagonal / sum(radii)) + 1

    l = [repeats] * cnt_element
    o = [0] * cnt_element

    i = 0

    while l != o:
        now_radius = np.matmul(l, radii)
        draw.ellipse(
            (
                x_center - now_radius,
                y_center - now_radius,
                x_center + now_radius,
                y_center + now_radius,
            ),
            fill=colors[~i % cnt_element],
        )
        i += 1
        l[~np.argmax(l[::-1])] -= 1
    return image


def draw_character(
    character,
    font_path,
    font_size,
    pattern,
    stretch,
):
    font = ImageFont.truetype(font_path, font_size)

    hs = stretch[0]
    vs = stretch[1]

    ascent, descent = font.getmetrics()
    width = font.font.getsize(character)[0][0]
    height = ascent + descent
    text_w = width + 2 * int(width * hs)
    text_h = height + 2 * int(height * vs)

    image = gen_char_background(
        text_w,
        text_h,
        bgb=pattern["bgb"],
        bgf=pattern["bgf"],
        pattern_type=choices(PATTERN, weights=PATTERN_WEIGHT, k=1)[0],
    )
    alpha = Image.new("RGBA", (text_w, text_h), TRANSPARENT)
    draw = ImageDraw.Draw(image)
    draw_alpha = ImageDraw.Draw(alpha)
    dots = [
        (
            width * (0 + hs) - uniform(0, width * hs),
            height * (0 + vs) - uniform(0, height * vs),
        ),
        (
            width * (1 + hs) + uniform(0, width * hs),
            height * (0 + vs) - uniform(0, height * vs),
        ),
        (
            width * (1 + hs) + uniform(0, width * hs),
            height * (1 + vs) + uniform(0, height * vs),
        ),
        (
            width * (0 + hs) - uniform(0, width * hs),
            height * (1 + vs) + uniform(0, height * vs),
        ),
    ]
    minx = floor(min(x[0] for x in dots))
    miny = floor(min(x[1] for x in dots))
    maxx = ceil(max(x[0] for x in dots))
    maxy = ceil(max(x[1] for x in dots))
    crop = (minx, miny, maxx, maxy)

    draw_alpha.polygon(dots, fill=(0, 0, 0))
    draw.text((width * hs, height * vs), character, font=font, fill=pattern["fg"])
    rotate = randint(-5, 5)
    image = image.crop(crop).rotate(rotate, expand=True)
    alpha = alpha.crop(crop).rotate(rotate, expand=True)

    return image, alpha


def generate_pattern(mode: str):
    if mode == "dark":
        return {
            "bgb": (randint(0, 95),) * 3,
            "bgf": (randint(48, 127),) * 3,
            "fg": (randint(224, 255),) * 3,
        }
    else:
        return {
            "bgb": (randint(160, 255),) * 3,
            "bgf": (randint(128, 208),) * 3,
            "fg": (randint(0, 32),) * 3,
        }


class FontManager:
    def __init__(self, root_path):
        self.font_paths = []
        for filename in os.listdir(root_path):
            file_path = os.path.join(root_path, filename)
            self.font_paths.append(file_path)
        self.len = len(self.font_paths)

    def get_random_path(self):
        return self.font_paths[randint(1, self.len) - 1]


class Content:
    def __init__(self, text, align):
        self.text = text
        self.align = align
        self.images = []

    def add_image(self, image):
        self.images.append(image)


class Card:
    def __init__(self, salutation, name, body, signature, date, aligns="CCCRR"):
        self.salutation = Content(salutation, aligns[0])
        self.name = Content(name, aligns[1])
        self.body = Content(body, aligns[2])
        self.signature = Content(signature, aligns[3])
        self.date = Content(date, aligns[4])

    def get_info(self):
        return [
            (self.salutation, 72),
            (self.name, 96),
            (self.body, 54),
            (self.signature, 36),
            (self.date, 28),
        ]


TRANSPARENT = (0, 0, 0, 0)
CONCENTRIC_CIRCLE_RADII = [120, 150]
CONCENTRIC_CIRCLE_COLORS = [(255, 0, 0), (0, 0, 0)]
# CONCENTRIC_CIRCLE_COLORS = [(22, 160, 133), (26, 188, 156)]

SWAPCASE_RATE = 0.25
STRETCH = [0.12, 0.24]
SIDE_SPACE = 0.05


def from_images_to_horizon_image(horizon_images, horizon_alphas, max_width, bias):
    generate_height = max(image.height for image in horizon_images) + bias * 2
    # generate_width = max_width + bias * (len(horizon_images) + 2)
    generate_width = sum(image.width for image in horizon_images) + bias * (
        len(horizon_images) + 2
    )
    posx = bias
    horizon_image = Image.new("RGBA", (generate_width, generate_height), TRANSPARENT)

    for i in range(len(horizon_images)):
        posx += randint(-bias, bias)
        posy = (generate_height - horizon_images[i].height) // 2 + randint(-bias, bias)
        horizon_image.paste(
            horizon_images[i],
            (posx, posy),
            horizon_alphas[i],
        )
        posx += horizon_images[i].width

    x1, y1, x2, y2 = horizon_image.getbbox()
    horizon_image = horizon_image.crop((x1, y1, x2, y2))
    return horizon_image


def main():
    set_width = 1920
    card_bias = 0

    font_manager = FontManager(r"C:\Users\Frankie\Desktop\mychoice")

    # card = Card(
    #     salutation="活跃于 Persona5 的",
    #     name="心之怪盗团的各位",
    #     body="你们擅自进入他人的认知空间，掠夺他人的秘宝，自以为做了很多能够改变社会的事情，自负得令人发笑！在不久的将来，我将 Take Your Heart(s)！",
    #     signature="Horiz21",
    #     date="2024年6月3日",
    #     aligns="CCLRR",
    # )

    card = Card(
        salutation="富含碳水化合物、纤维和钾元素的",
        name="亲爱的香蕉 Musa nana Lour.",
        body="你那一点可怜的价值，能请到除了猴子以外的员工吗？无足轻重的水果，我们早已洞悉你内心最隐秘的恐惧，你试图用廉价的糖分来掩盖自己的虚弱！现在就是时候让你正视自己的可悲本质了。我们会在预定时间来偷走你的热量，祝你好运。",
        signature="心之怪盗团",
        date="2024年6月3日",
        aligns="CCLRR",
    )

    max_width = int(set_width * (1 - SIDE_SPACE * 2))

    for info in card.get_info():
        text = info[0].text
        base_size = info[1]
        temp_images, temp_alphas = [], []
        now_width = 0
        i = 0
        while i < len(text):
            character = text[i]
            if character in ["\n", "\r"]:  # 强制换行，插入新条图，重复的代码
                info[0].add_image(
                    from_images_to_horizon_image(
                        temp_images, temp_alphas, max_width, card_bias
                    )
                )
                temp_alphas.clear()
                temp_images.clear()
                now_width = 0
                i += 1
                continue
            if character.isspace():
                space_width = ceil(base_size / 2)
                space_image = Image.new("RGBA", (space_width, 0), TRANSPARENT)
                temp_images.append(space_image)
                temp_alphas.append(space_image)
                now_width+=space_width
                i += 1
                continue

            if (
                "a" <= character <= "z" or "A" <= character <= "Z"
            ) and random() < SWAPCASE_RATE:
                character = character.swapcase()

            single_image, signle_alpha = draw_character(
                character,
                font_manager.get_random_path(),
                font_size=base_size * uniform(0.9, 1.1),
                pattern=generate_pattern(MODE[randint(0, 1)]),
                stretch=STRETCH,
            )
            if now_width + single_image.width >= max_width:
                info[0].add_image(
                    from_images_to_horizon_image(
                        temp_images, temp_alphas, max_width, card_bias
                    )
                )
                temp_alphas.clear()
                temp_images.clear()
                now_width = 0
                continue
            else:
                i += 1
                temp_images.append(single_image)
                temp_alphas.append(signle_alpha)
                now_width += signle_alpha.width
        info[0].add_image(
            from_images_to_horizon_image(temp_images, temp_alphas, max_width, card_bias)
        )

    total_height = 0
    total_width = 0
    for info in card.get_info():
        for image in info[0].images:
            total_height += image.height + card_bias
            total_width = max(total_width, image.width + card_bias * 2)

    total_image = Image.new("RGBA", (total_width, total_height), TRANSPARENT)
    nowy = 10
    for info in card.get_info():
        for image in info[0].images:
            if info[0].align == "L":
                posx = card_bias
            elif info[0].align == "C":
                posx = (total_width - image.width) // 2
            elif info[0].align == "R":
                posx = total_width - image.width - card_bias
            posx += randint(-card_bias, card_bias)
            posy = nowy + randint(-card_bias, card_bias)
            image.save(f"{i}.png")
            i += 1
            total_image.paste(image, (posx, posy), image)
            nowy += image.height
    x1, y1, x2, y2 = total_image.getbbox()
    total_image = total_image.crop((x1, y1, x2, y2))

    card_width = ceil(total_image.width / (1 - SIDE_SPACE * 2))
    card_height = ceil(total_image.height / (1 - SIDE_SPACE * 2))

    image = Image.new("RGBA", (card_width, card_height), TRANSPARENT)
    image = draw_concentric_circle(
        image,
        CONCENTRIC_CIRCLE_RADII,
        CONCENTRIC_CIRCLE_COLORS,
    )
    image = image.filter(ImageFilter.GaussianBlur(radius=1))
    image.paste(
        total_image,
        (int(card_width * SIDE_SPACE), int(card_height * SIDE_SPACE)),
        total_image,
    )
    image.save("card.png")


if __name__ == "__main__":
    main()
