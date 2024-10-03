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
                        base_size=128,
                        rotate_sigma=2,
                        stretch=[0.2, 0.4],
                        swapcase_rate=0.25,
                    ),
                ),
            ),
            Paragraph(
                text="斑目一流斋先生。",
                style=TITLE_PARAGRAPH,
            ),
            Paragraph(
                text="""你仗势欺人，
盗窃门下弟子创意，
是个不惮剽窃的艺术家。
我们决定让你亲口供认自己的罪行。
我们将取走你那扭曲的欲望。""",
                style=CONTENT_PARAGRAPH,
            ),
            Paragraph(
                text="心灵怪盗团「THE PHANTOM」留",
                style=AUTHOR_PARAGRAPH,
            ),
        ],
        font_directory="system",
        antialias=2,
        font_format_check=True,
        gen_back=True,
    )
    card.generate()
    card.save("", "p5card.png")


if __name__ == "__main__":
    main()
