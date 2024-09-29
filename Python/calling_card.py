import io
import os
import json
from typing import List
from math import ceil, sqrt
from PIL import Image, ImageDraw
from paragraph import Paragraph
from copy import deepcopy
from utils import OverlayMaker
import base64


class CardBackground:
    def __init__(
        self,
        radii: List[float] = [260, 320],
        colors: List[str] = ["#F00", "#000"],
        dots: bool = True,
    ):
        self.radii = radii
        self.colors = colors
        self.dots = dots

    def generate(self, width: int, height: int, trigger: str = "python"):
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

        if self.dots:
            dots_maker = OverlayMaker(
                layers=[
                    ("../" if trigger == "python" else "./") + "Assets/Images/dots.png"
                ],
                colors=[self.colors[-1]],
            )
            dots = dots_maker.get_resized_overlay((width, height))
            left = (width - dots.width) // 2
            top = height - dots.height  # Stay bottom
            self.image.paste(dots, (left, top), dots)


class CallingCard:
    def __init__(
        self,
        set_width: int,
        set_height: int,
        padding: int | List[int],
        background: CardBackground,
        paragraphs: List[Paragraph],
        font_directory: str,
        gen_back: bool = False,
        antialias: int = 2,
        version: str = "V1.1(CLI)",
        watermark: bool = True,
        font_format_check: bool = False,
        trigger: str = "python",
    ):
        self.gen_back = gen_back
        self.antialias = antialias
        self.trigger = trigger
        self.set_width = set_width
        self.set_height = set_height
        self.auto_height = set_height <= 0
        self.image_width = set_width * antialias
        self.image_height = set_height * antialias

        if isinstance(padding, int):
            padding = [padding] * 4
        elif len(padding) == 1:
            padding = padding * 4
        elif len(padding) == 2:
            padding = padding * 2
        elif len(padding) == 4:
            padding = padding
        self.padding = [p * antialias for p in padding]

        self.content_max_width = self.image_width - self.padding[0] - self.padding[2]

        self.background = background
        self.background.radii = [radius * antialias for radius in self.background.radii]

        self.paragraphs = paragraphs
        for i in range(len(self.paragraphs)):
            self.paragraphs[i].style.shift *= antialias
            self.paragraphs[i].style.float *= antialias
            self.paragraphs[i].style.character_style.size *= antialias

        if font_directory == "default":
            import platform

            system = platform.system()
            if system == "Windows":
                font_directory = os.path.join(
                    os.path.expanduser("~"), "AppData/Local/Microsoft/Windows/Fonts"
                )
            elif system == "Darwin":
                font_directory = "/Library/Fonts"
            elif system == "Linux":
                font_directory = "/usr/share/fonts"
            else:
                font_directory = "../Fonts" if trigger == "python" else "./Fonts"
        self.font_directory = font_directory

        self.version = version
        self.watermark = watermark
        self.font_format_check = font_format_check

    def generate(self):
        self.generate_face()
        if self.gen_back:
            self.generate_back()

    def generate_face(self):
        for paragraph in self.paragraphs:
            paragraph.generate(
                content_max_width=self.content_max_width,
                font_directory=self.font_directory,
                font_format_check=self.font_format_check,
            )
        content_height = sum(paragraph.height for paragraph in self.paragraphs)
        if self.auto_height:
            self.image_height = content_height + self.padding[1] + self.padding[3]
            self.set_height = self.image_height // self.antialias
        self.background.generate(self.image_width, self.image_height, self.trigger)

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

        image = deepcopy(self.background.image)
        image.paste(total_image, (self.padding[0], self.padding[1]), total_mask)
        image = image.resize(
            (self.set_width, self.set_height),
            resample=Image.LANCZOS,
        )

        if self.watermark:
            import getpass
            from utils import Watermark
            from datetime import datetime

            marker = Watermark()
            image = marker.embed(
                f"""This image was generated using the open-source Persona 5 Calling Card Generator (P5CCG) version {self.version} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} by {getpass.getuser()}.
P5CCG is designed for entertainment, non-commercial, and fair use only. All rights to Persona 5, including its trademarks and visual design, are owned by ATLUS.
By using P5CCG, users accept responsibility for how this image is utilized and agree that the creators of P5CCG bear no liability for any misuse or infringement.""",
                image,
            )

        self.face = image

    def generate_back(self):
        pre_path = ("../" if self.trigger == "python" else "./") + "Assets/Images/"
        logo_maker = OverlayMaker(
            layers=[
                pre_path + "back_white.png",
                pre_path + "back_black.png",
                pre_path + "back_red.png",
            ],
            colors=[
                "#FFF",
                self.background.colors[-1],
                (
                    "#000"
                    if len(self.background.colors) < 2
                    else self.background.colors[-2]
                ),
            ],
        )

        self.back = deepcopy(self.background.image)
        logo = logo_maker.get_resized_overlay(self.back.size)
        left = (self.back.width - logo.width) // 2
        top = (self.back.height - logo.height) // 2
        self.back.paste(logo, (left, top), logo)

    def save(
        self,
        path: str = "",
        name: str = "persona5_card.png",
    ):
        self.face.save(os.path.join(path, name))
        if self.gen_back:
            name_parts = name.split(".")
            file_name = ".".join(name_parts[:-1])
            file_extension = name_parts[-1]
            self.back.save(os.path.join(path, f"{file_name} (back).{file_extension}"))

    def tobyte(self):
        img_byte_arr_face = io.BytesIO()
        img_byte_arr_back = io.BytesIO()

        self.face.save(img_byte_arr_face, format="PNG")
        if self.gen_back:
            self.back.save(img_byte_arr_back, format="PNG")

        face_bytes = img_byte_arr_face.getvalue()
        back_bytes = img_byte_arr_back.getvalue() if self.gen_back else None

        return json.dumps(
            {
                "face": base64.b64encode(face_bytes).decode("utf-8"),
                "back": (
                    base64.b64encode(back_bytes).decode("utf-8")
                    if self.gen_back
                    else None
                ),
            }
        )
