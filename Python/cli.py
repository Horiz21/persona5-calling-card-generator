import os
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

    ## Get Image Ratio
    if data["ratio"] == "sqrt2:1":
        set_width, set_height = 3508, 2480
    elif data["ratio"] == "16:9":
        set_width, set_height = 3840, 2160
    elif data["ratio"] == "4:3":
        set_width, set_height = 3600, 2700
    elif data["ratio"] == "3:2":
        set_width, set_height = 3600, 2400
    else:  # auto
        set_width, set_height = 3840, 0

    ## Get Font Path
    font_directory = (
        data["fontDirectory"]
        if data["fontDirectory"] != "default"
        else "./Assets/Fonts"
    )

    ## Get Color
    if data["colorsAndRadii"][0] == "default":
        radii = [260, 320]
        colors = ["#F00", "#000"]
    else:
        radii = []
        colors = []
        for color in data["colorsAndRadii"]:
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
                        CharacterStyle(base_size=192, stretch=[0.2, 0.5])
                        if paragraph["fontSize"] == "L"
                        else (
                            CharacterStyle(base_size=128)
                            if paragraph["fontSize"] == "M"
                            else CharacterStyle(base_size=96)
                        )
                    ),
                ),
            )
        )

    version = data["version"]

    ## Generate
    card = CallingCard(
        set_width=set_width,
        set_height=set_height,
        padding=[200, 120, 200, 100],
        background=CardBackground(
            radii=radii,
            colors=colors,
            dots=data["dots"] == "dots",
        ),
        paragraphs=paragraphs,
        font_directory=os.path.join(font_directory),
        antialias=2,
        version=version,
        watermark=True,
        gen_back=data["sides"] == "face_and_back",
        trigger=data["trigger"],
    )

    card.generate()
    print(card.tobyte())


if __name__ == "__main__":
    main()
