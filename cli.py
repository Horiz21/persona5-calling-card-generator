import os
import sys
import json
import argparse

from character import CharacterStyle
from paragraph import ParagraphStyle, Paragraph
from calling_card import CallingCard, CardBackground


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)
    args = parser.parse_args()
    data = json.loads(args.data)
    print(data)

    ## Get Image Ratio
    if data["ratio"] == "sqrt2:1":
        set_width, set_height = 3508, 2480
    elif data["ratio"] == "16:9":
        set_width, set_height = 3840, 2160
    elif data["ratio"] == "4:3":
        set_width, set_height = 3600, 2700
    else:  # data["ratio"] == "3:2":
        set_width, set_height = 3600, 2400

    ## Get Font Path
    font_path = data["font_path"]
    if not os.path.exists(font_path) or not os.path.isdir(font_path):
        font_path = os.path.join(
            os.path.expanduser("~"),
            "AppData/Local/Microsoft/Windows/Fonts",
        )

    ## Get Color
    radii = []
    colors = []
    for color in data["colors"]:
        colors.append(color["hex"])
        radii.append(int(color["radius"]))

    ## Get Content
    paragraphs = []
    for paragraph in data["paragraphs"]:
        paragraphs.append(
            Paragraph(
                text=paragraph["content"],
                style=ParagraphStyle(
                    align=paragraph["alignment"],
                    character_style=(
                        CharacterStyle(basesize=192, rotate_sigma=2, stretch=[0.2, 0.5])
                        if paragraph["fontsize"] == "L"
                        else (
                            CharacterStyle(basesize=128)
                            if paragraph["fontsize"] == "M"
                            else CharacterStyle(basesize=96)
                        )
                    ),
                ),
            )
        )

    ## Generate
    card = CallingCard(
        set_width=set_width,
        set_height=set_height,
        padding=[200, 120, 200, 100],
        background=CardBackground(radii=radii, colors=colors),
        paragraphs=paragraphs,
        fonts_path=os.path.join(font_path),
        antialias=2,
    )
    card.generate()
    sys.stdout.buffer.write(card.tobyte())


if __name__ == "__main__":
    main()
