from character import Pattern, CharacterStyle, Character
from PIL import Image
from random import randint, choices

from font_manager import FontManager

SCHEME = ["light", "dark"]
SCHEME_WEIGHT = [1, 1]
PATTERN = ["flat", "horizontal", "vertical", "grid"]
PATTERN_WEIGHT = [15, 2, 2, 1]


class ParagraphStyle:
    def __init__(
        self,
        align: str,
        spacing: float,
        character_style: CharacterStyle,
    ):
        self.align = align
        self.spacing = spacing
        self.character_style = character_style


class Paragraph:
    def __init__(
        self,
        text: str,
        style: ParagraphStyle,
    ):
        self.text = text
        self.style = style
        self.images = []
        self.masks = []

        self.work_images = []
        self.work_masks = []

        self.height = 0

    def horizontal_arrange(self):
        num_image = len(self.work_images)
        height = (
            max(image.height for image in self.work_images) + self.style.spacing * 2
        )
        width = (
            sum(image.width for image in self.work_images)
            + self.style.spacing * num_image
        )
        posx = 0

        horizon_image = Image.new("L", (width, height), 0)
        horizon_mask = Image.new("L", (width, height), 0)

        for image, mask in zip(self.work_images, self.work_masks):
            posy = (height - image.height) // 2 + randint(
                -self.style.spacing, self.style.spacing
            )
            horizon_image.paste(image, (posx, posy))
            horizon_mask.paste(mask, (posx, posy))
            posx += image.width + randint(-self.style.spacing, self.style.spacing)

        crop_zone = horizon_image.getbbox()
        horizon_image = horizon_image.crop(crop_zone)
        horizon_mask = horizon_mask.crop(crop_zone)

        self.work_images.clear()
        self.work_masks.clear()

        self.images.append(horizon_image)
        self.masks.append(horizon_mask)

    def generate(self, content_max_width: int, fonts_path: str):
        self.font_manager = FontManager(fonts_path)

        now_width = 0
        i = 0

        while i < len(self.text):
            if self.text[i] in ["\n", "\r"]:
                self.horizontal_arrange()
                now_width = 0
                i += 1
                continue

            character = Character(
                character=self.text[i],
                style=self.style.character_style,
                pattern=Pattern(
                    mode=choices(SCHEME, weights=SCHEME_WEIGHT)[0],
                    type=choices(PATTERN, weights=PATTERN_WEIGHT)[0],
                ),
            )
            character.generate(font_path=self.font_manager.choice())

            if now_width + character.image.width <= content_max_width:
                self.work_images.append(character.image)
                self.work_masks.append(character.mask)
                now_width += character.image.width
                i += 1
            else:
                self.horizontal_arrange()
                now_width = 0
                continue

        self.horizontal_arrange()
        self.height = sum(image.height for image in self.images)
