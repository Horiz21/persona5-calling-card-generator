import os
from random import choice

FONT_PATH = os.path.join(
    os.path.expanduser("~"),
    "AppData/Local/Microsoft/Windows/Fonts",
)
# FONTS_PATH = os.path.join(os.path.dirname(__file__), "fonts")


class FontManager:
    def __init__(self, root: str):
        self.paths = [os.path.join(root, filename) for filename in os.listdir(root)]

    def choice(self):
        return choice(self.paths)
