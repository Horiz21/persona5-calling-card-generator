from character import CharacterStyle
from paragraph import ParagraphStyle
from calling_card import CardBackground

PERSONA5_BACKGROUND = CardBackground(
    radii=[260, 320],
    colors=["#F00", "#000"],
)

TITLE_PARAGRAPH = ParagraphStyle(
    align="Right",
    float=16,
    shift=18,
    character_style=CharacterStyle(
        basesize=192,
        rotate_sigma=2,
        stretch=[0.2, 0.5],
        swapcase_rate=0.25,
    ),
)

SUBTITLE_PARAGRAPH = ParagraphStyle(
    align="Left",
    float=12,
    shift=[-6, 18],
    character_style=CharacterStyle(
        basesize=144,
        rotate_sigma=2,
        stretch=[0.2, 0.4],
        swapcase_rate=0.25,
    ),
)


CONTENT_PARAGRAPH = ParagraphStyle(
    align="Center",
    float=4,
    shift=[-4, 8],
    character_style=CharacterStyle(
        basesize=108,
        rotate_sigma=2,
        stretch=[0.2, 0.2],
        swapcase_rate=0.25,
    ),
)

AUTHOR_PARAGRAPH = ParagraphStyle(
    align="Right",
    float=8,
    shift=[4, 8],
    character_style=CharacterStyle(
        basesize=84,
        rotate_sigma=2,
        stretch=[0.2, 0.2],
        swapcase_rate=0.25,
    ),
)

DATE_PARAGRAPH = ParagraphStyle(
    align="Right",
    float=6,
    shift=[3, 6],
    character_style=CharacterStyle(
        basesize=72,
        rotate_sigma=2,
        stretch=[0.2, 0.2],
        swapcase_rate=0.25,
    ),
)
