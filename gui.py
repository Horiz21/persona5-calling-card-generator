import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk
import re
from calling_card import *
from paragraph import *
from character import *


def isnumber(s):
    return s.isdigit() or (s.count(".") == 1 and s.replace(".", "").isdigit())


class TextModule:
    def __init__(self, root):
        self.master = ttk.Frame(root)
        self.master.pack()

        for i, header in enumerate(
            [
                "文本内容",
                "字号",
                "对齐方式",
                "水平间距",
                "垂直偏移",
                "旋转",
                "水平拉伸",
                "垂直拉伸",
                "字母切换",
            ]
        ):
            ttk.Label(
                self.master,
                text=header,
                justify="center",
                anchor="center",
                width=30 if i == 0 else 8,
            ).grid(row=0, column=i)

        self.entry_text = ttk.Entry(self.master, width=30)
        self.entry_text.grid(row=1, column=0)

        self.entry_basesize = ttk.Spinbox(
            self.master,
            width=8,
            justify="center",
            from_=8,
            to=120,
            increment=4,
        )
        self.entry_basesize.grid(row=1, column=1)

        self.entry_align = ttk.Combobox(
            self.master,
            width=8,
            justify="center",
            values=["居左", "居中", "居右"],
        )
        self.entry_align.grid(row=1, column=2)

        self.entry_shift = ttk.Spinbox(
            self.master,
            width=8,
            justify="center",
            from_=0,
            to=10,
            increment=1,
        )
        self.entry_shift.grid(row=1, column=3)

        self.entry_float = ttk.Spinbox(
            self.master,
            width=8,
            justify="center",
            from_=0,
            to=10,
            increment=1,
        )
        self.entry_float.grid(row=1, column=4)

        self.entry_rotate_sigma = ttk.Spinbox(
            self.master,
            width=8,
            justify="center",
            from_=0,
            to=30,
            increment=1,
        )
        self.entry_rotate_sigma.grid(row=1, column=5)

        self.entry_horizontal_stretch = ttk.Spinbox(
            self.master,
            width=8,
            justify="center",
            from_=0,
            to=1,
            increment=0.05,
        )
        self.entry_horizontal_stretch.grid(row=1, column=6)

        self.entry_vertical_stretch = ttk.Spinbox(
            self.master,
            width=8,
            justify="center",
            from_=0,
            to=1,
            increment=0.05,
        )
        self.entry_vertical_stretch.grid(row=1, column=7)

        self.entry_swapcase = ttk.Spinbox(
            self.master,
            width=8,
            justify="center",
            from_=0,
            to=1,
            increment=0.05,
        )
        self.entry_swapcase.grid(row=1, column=8)

        self.button_add = ttk.Button(
            self.master, text="➕", width=2, command=self.add_row
        )
        self.button_add.grid(row=1, column=9)

        self.rows = []

    def add_row(self):
        text = self.entry_text.get()
        basesize = self.entry_basesize.get()
        align = self.entry_align.get()
        shift = self.entry_shift.get()
        float_ = self.entry_float.get()
        rotate_sigma = self.entry_rotate_sigma.get()
        horizontal_stretch = self.entry_horizontal_stretch.get()
        vertical_stretch = self.entry_vertical_stretch.get()
        swapcase = self.entry_swapcase.get()

        if len(text) < 1:
            messagebox.showerror("Invalid", "Invalid Text Input!")
            return

        if not basesize.isdigit():
            messagebox.showerror("Invalid", "Invalid Font Size Input!")
            return

        if align not in ["居左", "居中", "居右"]:
            messagebox.showerror("Invalid", "Invalid Align Input!")
            return

        if not shift.isdigit():
            messagebox.showerror("Invalid", "Invalid Shift Input!")
            return

        if not float_.isdigit():
            messagebox.showerror("Invalid", "Invalid Float Input!")
            return

        if not isnumber(rotate_sigma):
            messagebox.showerror("Invalid", "Invalid Rotate Sigma Input!")
            return

        if (
            not isnumber(horizontal_stretch)
            or isnumber(horizontal_stretch)
            and not 0 <= float(horizontal_stretch) <= 1
        ):
            messagebox.showerror("Invalid", "Invalid Horizontal Stretch Input!")
            return

        if (
            not isnumber(vertical_stretch)
            or isnumber(vertical_stretch)
            and not 0 <= float(vertical_stretch) <= 1
        ):
            messagebox.showerror("Invalid", "Invalid Vertical Stretch Input!")
            return

        if (
            not isnumber(swapcase)
            or isnumber(swapcase)
            and not 0 <= float(swapcase) <= 1
        ):
            messagebox.showerror("Invalid", "Invalid Swapcase Rate Input!")
            return

        widgets = []
        for i, item in enumerate(
            [
                text,
                basesize,
                align,
                shift,
                float_,
                rotate_sigma,
                horizontal_stretch,
                vertical_stretch,
                swapcase,
            ]
        ):
            widget = ttk.Label(
                self.master,
                text=item,
                justify="center",
                anchor="center",
            )
            widget.grid(row=len(self.rows) + 2, column=i)
            widgets.append(widget)
        widget = ttk.Button(
            self.master,
            text="✖",
            width=2,
            command=lambda w=widgets: self.delete_row(w),
        )
        widget.grid(row=len(self.rows) + 2, column=9)
        widgets.append(widget)

        self.rows.append(widgets)

    def delete_row(self, widgets):
        for widget in widgets:
            widget.grid_forget()
        self.rows.remove(widgets)

        # 重新排列剩余的行
        for i, row in enumerate(self.rows, start=2):
            for j, widget in enumerate(row):
                widget.grid(row=i, column=j)

    def get_info(self):
        res = []
        for item in self.rows:
            text = item[0].cget("text")
            basesize = int(item[1].cget("text"))
            align = (
                "l"
                if item[2].cget("text") == "居左"
                else "r" if item[2].cget("text") == "居右" else "c"
            )
            shift = int(item[3].cget("text"))
            float_ = int(item[4].cget("text"))
            rotate_sigma = float(item[5].cget("text"))
            horizontal_stretch = float(item[6].cget("text"))
            vertical_stretch = float(item[7].cget("text"))
            swapcase = float(item[8].cget("text"))
            res.append(
                [
                    text,
                    basesize,
                    align,
                    shift,
                    float_,
                    rotate_sigma,
                    horizontal_stretch,
                    vertical_stretch,
                    swapcase,
                ]
            )
        return res


class ColorModule:
    def __init__(self, root):
        self.master = ttk.Frame(root)
        self.master.pack()
        self.rows = []

        # 创建表格标题
        ttk.Label(self.master, text="颜色", justify="center", anchor="center").grid(
            row=0, column=0
        )
        ttk.Label(self.master, text="半径", justify="center", anchor="center").grid(
            row=0, column=1
        )

        # 创建输入行
        self.entry_color = ttk.Entry(self.master, width=10, justify="center")
        self.entry_color.grid(row=1, column=0)
        self.entry_radius = ttk.Entry(self.master, width=5, justify="center")
        self.entry_radius.grid(row=1, column=1)
        self.button_add = ttk.Button(
            self.master, text="➕", width=2, command=self.add_row
        )
        self.button_add.grid(row=1, column=2)

    def add_row(self):
        color = self.entry_color.get()
        radius = self.entry_radius.get()

        match = re.match(r"^#?([0-9A-Fa-f]{6})$", color)

        if not match:
            messagebox.showerror("Invalid", "Invalid Color Input!")
            return
        elif not radius.isdigit() or int(radius) <= 0:
            messagebox.showerror("Invalid", "Invalid Radius Input!")
            return
        else:
            color = f"#{color[-6:]}"

        label_color = ttk.Label(
            self.master,
            text=color,
            width=10,
            background=color,
            justify="center",
            anchor="center",
        )
        label_radius = ttk.Label(
            self.master,
            width=5,
            text=radius,
            justify="center",
            anchor="center",
        )
        button_delete = ttk.Button(
            self.master,
            text="✖",
            width=2,
            command=lambda: self.delete_row(label_color, label_radius, button_delete),
        )

        row_number = len(self.rows) + 2
        print(row_number)
        label_color.grid(row=row_number, column=0)
        label_radius.grid(row=row_number, column=1)
        button_delete.grid(row=row_number, column=2)

        self.rows.append((label_color, label_radius, button_delete))

        self.entry_color.delete(0, "end")
        self.entry_radius.delete(0, "end")

    def delete_row(self, label_color, label_radius, button_delete):
        label_color.grid_forget()
        label_radius.grid_forget()
        button_delete.grid_forget()

        self.rows.remove((label_color, label_radius, button_delete))

        for i, row in enumerate(self.rows, start=2):
            for j, widget in enumerate(row):
                widget.grid(row=i, column=j)

    def get_info(self):
        colors = [color.cget("text") for color, _, _ in self.rows]
        radii = [int(radii.cget("text")) for _, radii, _ in self.rows]

        return colors, radii


class InfoModule:
    def __init__(self, root):
        self.master = ttk.Frame(root)
        self.master.pack()

        label_width = tk.Label(self.master, text="宽度")
        label_width.grid(row=0, column=0)
        self.entry_width = ttk.Entry(self.master, width=12)
        self.entry_width.insert(0, 1600)
        self.entry_width.grid(row=0, column=1)

        label_height = tk.Label(self.master, text="高度")
        label_height.grid(row=1, column=0)
        self.entry_height = ttk.Entry(self.master, width=12)
        self.entry_height.insert(0, "Auto")
        self.entry_height.config(state="readonly")
        self.entry_height.grid(row=1, column=1)

        label_smooth = tk.Label(self.master, text="平滑度")
        label_smooth.grid(row=2, column=0)
        self.entry_smooth = ttk.Entry(self.master, width=12)
        self.entry_smooth.insert(0, 0)
        self.entry_smooth.grid(row=2, column=1)

    def get_info(self):
        width = int(self.entry_width.get())
        height = self.entry_height.get()
        if height.lower() == "auto":
            height = width * 0.75
        return int(width), int(height)


class GeneratorGUI:
    def __init__(self):
        self.gui = tk.Tk()
        self.gui.title("P5CCG")
        self.gui.iconbitmap("Fun/persona5_calling_card_generator/p5ccg.ico")

        self.frame_config = tk.Frame(self.gui)
        self.frame_config.grid(row=0, column=0)
        self.frame_view = tk.Frame(self.gui)
        self.frame_view.grid(row=0, column=1)

        self.frame_color_config = ColorModule(self.frame_config)
        self.frame_text_config = TextModule(self.frame_config)
        self.frame_size_config = InfoModule(self.frame_config)

        self.image_generate = ttk.Label(self.frame_view)
        self.image_generate.pack(side="top")

        button_generate = ttk.Button(
            self.frame_view,
            text="Generate",
            command=self.generate,
        )
        button_generate.pack(side="bottom")

    def generate(self):
        colors, radii = self.frame_color_config.get_info()
        width, height = self.frame_size_config.get_info()

        paragraphs = []
        texts = self.frame_text_config.get_info()
        for text in texts:
            paragraphs.append(
                Paragraph(
                    text=text[0],
                    style=ParagraphStyle(
                        align=text[2],
                        float=text[4],
                        shift=text[3],
                        character_style=CharacterStyle(
                            basesize=text[1],
                            rotate_sigma=text[5],
                            stretch=[text[6], text[7]],
                            swapcase_rate=text[8],
                        ),
                    ),
                )
            )

        card = CallingCard(
            set_width=width,
            padding=10,
            background=CardBackground(radii=radii, colors=colors),
            fonts_path="Fun/persona5_calling_card_generator/fonts",
            paragraphs=paragraphs,
            smooth=False,
        )
        card.generate()
        self.show_image = ImageTk.PhotoImage(card.image)
        self.image_generate.config(image=self.show_image),

    def mainloop(self):
        self.gui.mainloop()


def main():
    gui = GeneratorGUI()
    gui.mainloop()


if __name__ == "__main__":
    main()
