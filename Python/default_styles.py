from character import CharacterStyle
from paragraph import ParagraphStyle
from calling_card import CardBackground

PERSONA5_BACKGROUND = CardBackground(
    radii=[260, 320],
    colors=["#F00", "#000"],
    dots=True,
)

TITLE_PARAGRAPH = ParagraphStyle(
    align="Right",
    float=16,
    shift=18,
    character_style=CharacterStyle(
        base_size=192,
        stretch=[0.2, 0.5],
        swapcase_rate=0.25,
    ),
)

SUBTITLE_PARAGRAPH = ParagraphStyle(
    align="Left",
    float=12,
    shift=[-6, 18],
    character_style=CharacterStyle(
        base_size=144,
        stretch=[0.2, 0.4],
        swapcase_rate=0.25,
    ),
)


CONTENT_PARAGRAPH = ParagraphStyle(
    align="Center",
    float=4,
    shift=[-4, 8],
    character_style=CharacterStyle(
        base_size=108,
        stretch=[0.2, 0.2],
        swapcase_rate=0.25,
    ),
)

AUTHOR_PARAGRAPH = ParagraphStyle(
    align="Right",
    float=8,
    shift=[4, 8],
    character_style=CharacterStyle(
        base_size=72,
        stretch=[0.2, 0.2],
        swapcase_rate=0.25,
    ),
)

DATE_PARAGRAPH = ParagraphStyle(
    align="Right",
    float=6,
    shift=[3, 6],
    character_style=CharacterStyle(
        base_size=64,
        stretch=[0.2, 0.2],
        swapcase_rate=0.25,
    ),
)
