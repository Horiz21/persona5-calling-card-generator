from typing import List
from character import Pattern, CharacterStyle, Character
from PIL import Image
from random import randint, choices
from copy import deepcopy
from utils import FontManager
from fontTools.ttLib import TTFont, TTCollection


SCHEME = ["light", "dark"]
SCHEME_WEIGHT = [1, 1]
PATTERN = ["flat", "horizontal", "vertical", "grid"]
PATTERN_WEIGHT = [15, 2, 2, 1]


class ParagraphStyle:
    def __init__(
        self,
        align: str = "left",
        character_style: CharacterStyle = CharacterStyle(),
        float: int = 0,
        shift: int | List[int] = 0,
    ):
        self.align = align
        self.float = float
        self.shift = shift if isinstance(shift, list) else [shift] * 2
        self.character_style = deepcopy(character_style)


class Paragraph:
    def __init__(
        self,
        text: str = "",
        style: ParagraphStyle = ParagraphStyle(),
    ):
        self.text = text
        self.style = deepcopy(style)
        self.images = []
        self.masks = []

        self.work_images = []
        self.work_masks = []

        self.height = 0

    def add_images(self, image, mask):
        crop_zone = image.getbbox()
        image = image.crop(crop_zone)
        mask = mask.crop(crop_zone)
        self.images.append(image)
        self.masks.append(mask)

    def horizontal_arrange(self, content_max_width: int):
        height = max(image.height for image in self.work_images) + self.style.float * 2
        width = content_max_width

        horizontal_image = Image.new("L", (width, height), 0)
        horizontal_mask = Image.new("L", (width, height), 0)

        posx = 0
        while len(self.work_images) > 0:
            available = content_max_width - posx
            if available >= self.work_images[0].width + self.style.shift[0]:
                image = self.work_images.pop(0)
                mask = self.work_masks.pop(0)
                center_y = (height - image.height) // 2
                posy = center_y + randint(-self.style.float, self.style.float)
                posx += randint(
                    self.style.shift[0], min(self.style.shift[1], available)
                )
                horizontal_image.paste(image, (posx, posy), mask)
                horizontal_mask.paste(mask, (posx, posy), mask)
                posx += image.width
            else:
                self.add_images(horizontal_image, horizontal_mask)
                horizontal_image = Image.new("L", (width, height), 0)
                horizontal_mask = Image.new("L", (width, height), 0)
                posx = 0
        self.add_images(horizontal_image, horizontal_mask)

    def generate(self, content_max_width: int, fonts_path: str, fonts_check: bool):
        self.font_manager = FontManager(fonts_path)
        self.images.clear()
        self.masks.clear()

        if len(self.text) > 0:
            i = 0
            while i < len(self.text):
                if self.text[i] in ["\n", "\r"]:
                    self.horizontal_arrange(content_max_width)
                    i += 1
                    continue

                target_character = self.text[i]
                character = Character(
                    character=target_character,
                    style=self.style.character_style,
                    pattern=Pattern(
                        mode=choices(SCHEME, weights=SCHEME_WEIGHT)[0],
                        type=choices(PATTERN, weights=PATTERN_WEIGHT)[0],
                    ),
                )
                _, font_path = self.font_manager.choice()
                if fonts_check:
                    cmap = {}
                    while cmap == None or ord(target_character) not in cmap:
                        index, font_path = self.font_manager.choice()
                        font = (
                            TTCollection(font_path).fonts[0]
                            if font_path.lower().endswith(".ttc")
                            else TTFont(font_path)
                        )
                        cmap = font.getBestCmap()
                        self.font_manager.remove(index)
                    self.font_manager.reset()
                character.generate(font_path)

                self.work_images.append(character.image)
                self.work_masks.append(character.mask)
                i += 1
            self.horizontal_arrange(content_max_width)
            self.height = sum(image.height for image in self.images)
        else:
            self.images = [Image.new("L", (0, 0))]
            self.masks = [Image.new("L", (0, 0))]

    def set_align(self, align):
        self.style.align = align
