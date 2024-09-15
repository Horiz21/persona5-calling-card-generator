import os

from character import CharacterStyle
from paragraph import ParagraphStyle, Paragraph
from calling_card import CallingCard
from default_styles import *


def main():
    card = CallingCard(
        set_width=3840,
        set_height=0,  # Setting height to 0 will make the image height automatically adapt to the content.
        padding=[120, 80, 120, 40],
        background=PERSONA5_BACKGROUND,
        paragraphs=[
            Paragraph(
                text="江郎才尽、虚有其表的大罪人、",
                style=ParagraphStyle(
                    align="Left",
                    float=16,
                    shift=[-8, 16],
                    character_style=CharacterStyle(
                        basesize=128,
                        rotate_sigma=2,
                        stretch=[0.2, 0.5],
                        swapcase_rate=0.25,
                    ),
                ),
            ),
            Paragraph(
                text="斑目一流斋先生。",
                style=TITLE_PARAGRAPH,
            ),
            Paragraph(
                text="你仗势欺人，\n盗窃门下弟子创意，\n是个不惮剽窃的艺术家。\n我们决定让你亲口供认自己的罪行。\n我们将取走你那扭曲的欲望。",
                style=CONTENT_PARAGRAPH,
            ),
            Paragraph(
                text="心灵怪盗团「THE PHANTOM」留",
                style=AUTHOR_PARAGRAPH,
            ),
        ],
        fonts_path=os.path.join(
            os.path.expanduser("~"),
            "AppData/Local/Microsoft/Windows/Fonts",
        ),
        antialias=2,
        font_check=False,  # Check if the font contains specific text. If True, it avoids garbled fonts, but will slow down the runtime considerably
    )

    card.generate()
    card.save("", "p5card.png")


if __name__ == "__main__":
    main()
