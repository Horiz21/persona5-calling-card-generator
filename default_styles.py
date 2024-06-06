from character import CharacterStyle
from paragraph import ParagraphStyle
from calling_card import CardBackground

PERSONA5_BACKGROUND = CardBackground(
    radii=[120, 150],
    colors=["#F00", "#000"],
)

TITLE_PARAGRAPH = ParagraphStyle(
    align="Right",
    spacing=0,
    character_style=CharacterStyle(
        basesize=96,
        rotate_sigma=2,
        stretch=[0.2, 0.5],
        swapcase_rate=0.25,
    ),
)

SUBTITLE_PARAGRAPH = ParagraphStyle(
    align="Left",
    spacing=0,
    character_style=CharacterStyle(
        basesize=72,
        rotate_sigma=2,
        stretch=[0.2, 0.4],
        swapcase_rate=0.25,
    ),
)


CONTENT_PARAGRAPH = ParagraphStyle(
    align="Center",
    spacing=0,
    character_style=CharacterStyle(
        basesize=54,
        rotate_sigma=2,
        stretch=[0.2, 0.2],
        swapcase_rate=0.25,
    ),
)


AUTHOR_PARAGRAPH = ParagraphStyle(
    align="Right",
    spacing=0,
    character_style=CharacterStyle(
        basesize=42,
        rotate_sigma=2,
        stretch=[0.2, 0.2],
        swapcase_rate=0.25,
    ),
)

DATE_PARAGRAPH = ParagraphStyle(
    align="Right",
    spacing=0,
    character_style=CharacterStyle(
        basesize=36,
        rotate_sigma=2,
        stretch=[0.2, 0.2],
        swapcase_rate=0.25,
    ),
)
