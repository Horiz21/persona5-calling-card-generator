import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
from calling_card import *
from paragraph import *
from character import *
from time import time
import os
import sys
import gettext

SUPPORTED_LANGS = ["zh_CN", "en_US"]

user_lang = os.environ.get("LANG", "").split(".")[0]

if user_lang in SUPPORTED_LANGS:
    _ = gettext.translation("gui", "locale", [user_lang]).gettext
else:
    _ = gettext.translation("gui", "locale", ["en_US"], fallback=True).gettext


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def parse_to_num(parsee, default_value):
    try:
        return int(parsee)
    except:
        return default_value


class AdvancedTextEditToplevel(tk.Toplevel):
    def __init__(self, root, paragraph):
        super().__init__(root)
        self.root = root
        self.paragraph = paragraph
        self.title("高级文本编辑")
        self.result = None
        self.create_widgets()

    def create_widgets(self):
        self.text_label = ttk.Label(self, text="内容")
        self.text_label.grid(row=0, column=0)

        self.text_content = tk.Text(self, height=4, wrap=tk.WORD)
        self.text_content.grid(row=0, column=1)
        self.text_content.insert(tk.END, self.paragraph.text)

        self.size_label = ttk.Label(self, text="字号")
        self.size_label.grid(row=1, column=0)

        self.size = ttk.Spinbox(self, from_=24, to=128, increment=4, width=6)
        self.size.grid(row=1, column=1, sticky="ew")
        self.size.set(int(self.paragraph.style.character_style.size))

        self.align_label = ttk.Label(self, text="对齐")
        self.align_label.grid(row=2, column=0)
        self.align = ttk.Combobox(self, values=["left", "center", "right"])
        self.align.grid(row=2, column=1, sticky="ew")
        self.align.set(self.paragraph.style.align)

        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=3, column=0, columnspan=2)

        self.delete_button = ttk.Button(
            self.button_frame,
            text="删除",
            command=self.delete_row,
        )
        self.delete_button.grid(row=0, column=0)

        self.save_button = ttk.Button(
            self.button_frame,
            text="保存",
            command=self.save_changes,
        )
        self.save_button.grid(row=0, column=1, padx=10)

    def delete_row(self):
        self.result = False
        self.destroy()

    def save_changes(self):
        self.result = Paragraph(
            text=self.text_content.get("1.0", tk.END),
            style=ParagraphStyle(
                align=self.align.get(),
                character_style=CharacterStyle(basesize=self.size.get()),
            ),
        )
        self.destroy()


class TextEditFrame:
    def __init__(self, root):
        self.master = ttk.LabelFrame(root, text=_("text"), padding=5)
        self.master.pack(padx=10, pady=10)

        self.para_frame = ttk.Frame(self.master)
        self.para_frame.grid(row=0, column=0)

        self.add_button = ttk.Button(self.master, text="+", command=self.add_row)
        self.add_button.grid(row=1, column=0)

        ttk.Label(self.para_frame, text=_("content")).grid(row=0, column=0)
        ttk.Label(self.para_frame, text=_("font_size")).grid(row=0, column=1)
        ttk.Label(self.para_frame, text=_("align")).grid(row=0, column=2)
        ttk.Label(self.para_frame, text=_("delete")).grid(row=0, column=3)

        self.paragraphs = {}
        self.rows = {}

        self.toplevel = False

        self.add_row()

    def update_paragraph(self, key):
        row = self.rows[key]
        columns = self.para_frame.grid_slaves(row=row)
        self.paragraphs[key].text = columns[~0].get()
        self.paragraphs[key].style.character_style.size = columns[~1].get()
        self.paragraphs[key].style.align = columns[~2].get()

    def add_row(self):
        key = time()
        row = (max(self.rows.values()) if len(self.rows) > 0 else 0) + 1

        text = ttk.Entry(self.para_frame, width=25)
        text.grid(row=row, column=0)
        text.bind("<FocusOut>", lambda event: self.update_paragraph(key=key))

        size = ttk.Spinbox(self.para_frame, from_=24, to=128, increment=4, width=6)
        size.grid(row=row, column=1)
        size.insert(0, "24")
        size.bind("<FocusOut>", lambda event: self.update_paragraph(key=key))

        align = ttk.Combobox(
            self.para_frame, width=6, values=["left", "center", "right"]
        )
        align.grid(row=row, column=2)
        align.insert(0, "left")
        align.bind("<FocusOut>", lambda event: self.update_paragraph(key=key))

        # more = ttk.Button(
        #     self.para_frame,
        #     text="…",
        #     width=6,
        #     command=lambda: self.edit_row(key),
        # )
        more = ttk.Button(
            self.para_frame, text="×", width=6, command=lambda: self.delete_row(key=key)
        )
        more.grid(row=row, column=3)

        self.paragraphs[key] = Paragraph()
        self.rows[key] = row

    def edit_row(self, key):
        if self.toplevel:
            messagebox.showwarning(_("warning"), _("one_edit"))
            return
        self.toplevel = True
        row = self.rows[key]
        columns = self.para_frame.grid_slaves(row=row)

        self.paragraphs[key].text = columns[~0].get()
        self.paragraphs[key].style.character_style.size = parse_to_num(
            columns[~1].get(), 24
        )
        self.paragraphs[key].style.align = columns[~2].get()

        dialog = AdvancedTextEditToplevel(self.master, self.paragraphs[key])
        dialog.wait_window()
        self.toplevel = False
        if dialog.result is False:
            self.delete_row(key)
        elif dialog.result is None:
            pass
        else:
            self.paragraphs[key] = dialog.result
            columns[~0].delete(0, tk.END)
            columns[~0].insert(0, dialog.result.text)
            columns[~1].delete(0, tk.END)
            columns[~1].insert(0, int(dialog.result.style.character_style.size))
            columns[~2].delete(0, tk.END)
            columns[~2].insert(0, dialog.result.style.align)

    def delete_row(self, key):
        if len(self.rows) <= 1:
            messagebox.showwarning(_("error"), _("one_text"))
            return
        self.paragraphs.pop(key)
        row = self.rows.pop(key)
        columns = self.para_frame.grid_slaves(row=row)
        for column in columns:
            column.grid_forget()

    def get_info(self):
        return list(self.paragraphs.values())


class ColorEditFrame:
    def __init__(self, root):
        self.master = ttk.LabelFrame(root, text=_("color"), padding=5)
        self.master.pack(padx=10, pady=10)

        self.color_frame = ttk.Frame(self.master)
        self.color_frame.grid(row=0, column=0)

        ttk.Button(self.master, text="+", command=self.add_row).grid(row=1, column=0)

        ttk.Label(self.color_frame, text=_("preview")).grid(row=0, column=0)
        ttk.Label(self.color_frame, text=_("hex")).grid(row=0, column=1)
        ttk.Label(self.color_frame, text=_("radius")).grid(row=0, column=2)
        ttk.Label(self.color_frame, text=_("delete")).grid(row=0, column=3)

        self.rows = {}

        self.add_row("#FF0000", "120")
        self.add_row("#000000", "150")

    def update_color(self, key):
        row = self.rows[key]
        color_entry = self.color_frame.grid_slaves(row=row)
        color = color_entry[~1].get()
        match = re.match(r"^#?([0-9A-Fa-f]{6})$", color)
        if match:
            color_entry[~0].config(text="")
            color_entry[~0].config(background=f"#{color[-6:]}")
        else:
            color_entry[~0].config(text="?")
            color_entry[~0].config(background="white")

    def add_row(self, color_value="#FF0000", radius_value="120"):
        key = time()
        row = (max(self.rows.values()) if len(self.rows) > 0 else 0) + 1
        self.rows[key] = row

        label = ttk.Label(
            self.color_frame,
            width=10,
            background=color_value,
            foreground="red",
            anchor="center",
            justify="center",
        )
        label.grid(row=row, column=0)

        color = ttk.Entry(self.color_frame, width=10, justify="center")
        color.insert(0, color_value)
        color.grid(row=row, column=1)
        color.bind("<FocusOut>", lambda event: self.update_color(key=key))
        radius = ttk.Spinbox(self.color_frame, from_=30, to=150, increment=10, width=6)
        radius.grid(row=row, column=2)
        radius.insert(0, radius_value)

        ttk.Button(
            self.color_frame,
            text="×",
            width=6,
            command=lambda: self.delete_row(key),
        ).grid(row=row, column=3)

    def delete_row(self, key):
        if len(self.rows) <= 1:
            messagebox.showwarning(_("error"), _("one_color"))
            return
        row = self.rows.pop(key)
        columns = self.color_frame.grid_slaves(row=row)
        for column in columns:
            column.grid_forget()

    def get_info(self):
        colors = []
        radii = []
        for row in self.rows.values():
            columns = self.color_frame.grid_slaves(row=row)
            colors.append(columns[~1].get())
            radii.append(int(columns[~2].get()))
        return colors, radii


class InfoEditFrame:
    def __init__(self, root):
        # self.master = ttk.LabelFrame(root, text="尺寸与平滑", padding=5)
        self.master = ttk.LabelFrame(root, text=_("base_info"), padding=5)
        self.master.pack(padx=10, pady=10)

        label_width = tk.Label(self.master, text=_("width"))
        label_width.grid(row=0, column=0)
        self.entry_width = ttk.Entry(self.master)
        self.entry_width.insert(0, 1600)
        self.entry_width.grid(row=0, column=1)

        # label_height = tk.Label(self.master, text="高度")
        # label_height.grid(row=1, column=0)
        # self.entry_height = ttk.Entry(self.master, width=12)
        # self.entry_height.insert(0, "Auto")
        # self.entry_height.config(state="readonly")
        # self.entry_height.grid(row=1, column=1)

        label_font_path = ttk.Label(self.master, text=_("font_path"))
        label_font_path.grid(row=1, column=0)
        self.entry_font_path = ttk.Entry(self.master)
        self.entry_font_path.grid(row=1, column=1)
        font_path_button = ttk.Button(
            self.master,
            text=_("choose"),
            width=6,
            command=lambda: self.path_select("font"),
        )
        font_path_button.grid(row=1, column=2)

        label_save_path = ttk.Label(self.master, text=_("save_path"))
        label_save_path.grid(row=2, column=0)
        self.entry_save_path = ttk.Entry(self.master)
        self.entry_save_path.grid(row=2, column=1)
        save_path_button = ttk.Button(
            self.master,
            text=_("choose"),
            width=6,
            command=lambda: self.path_select("save"),
        )
        save_path_button.grid(row=2, column=2)

        # label_smooth = tk.Label(self.master, text="平滑度")
        # label_smooth.grid(row=2, column=0)
        # self.entry_smooth = ttk.Entry(self.master, width=12)
        # self.entry_smooth.insert(0, 0)
        # self.entry_smooth.grid(row=2, column=1)

    def path_select(self, type):
        selected_dir = filedialog.askdirectory()
        if type == "font":
            self.entry_font_path.delete(0, tk.END)
            self.entry_font_path.insert(0, selected_dir)
        elif type == "save":
            self.entry_save_path.delete(0, tk.END)
            self.entry_save_path.insert(0, selected_dir)

    def get_info(self):
        # width = int(self.entry_width.get())
        # height = self.entry_font_path.get()
        # if height.lower() == "auto":
        #     height = width * 0.75
        # return int(width), int(height)
        width = int(self.entry_width.get())
        font_path = self.entry_font_path.get()
        save_path = self.entry_save_path.get()
        return width, font_path, save_path


class GeneratorGUI:
    def __init__(self):
        self.gui = tk.Tk()
        self.gui.title(_("p5ccg"))
        self.gui.iconbitmap(resource_path("p5ccg.ico"))

        self.main_frame = tk.Frame(self.gui, padx=10, pady=10)
        self.main_frame.pack()

        self.frame_info_edit = InfoEditFrame(self.main_frame)
        self.frame_color_edit = ColorEditFrame(self.main_frame)
        self.frame_text_edit = TextEditFrame(self.main_frame)
        frame_button = tk.Frame(self.main_frame)
        frame_button.pack(side="bottom", expand=True, fill="both", padx=20)

        button_help = ttk.Button(
            frame_button,
            text="?",
            width=2,
            command=lambda: messagebox.showinfo(
                title=_("help"), message=_("help_message")
            ),
        )
        button_help.pack(side="left")
        button_generate = ttk.Button(
            frame_button,
            text=_("generate"),
            command=self.generate,
        )
        button_generate.pack(expand=True, fill="both")

    def generate(self):
        try:
            colors, radii = self.frame_color_edit.get_info()
            # width, height = self.frame_info_edit.get_info()
            width, font_path, save_path = self.frame_info_edit.get_info()

            self.font_path = (
                font_path
                if os.path.isdir(font_path)
                else os.path.join(
                    os.path.expanduser("~"),
                    "AppData/Local/Microsoft/Windows/Fonts",
                )
            )

            if not os.path.isdir(self.font_path):
                messagebox.showerror(_("error"), _("no_fonts"))
                return

            self.save_path = (
                save_path if os.path.isdir(save_path) else os.path.expanduser("~")
            )

            card = CallingCard(
                set_width=width,
                padding=10,
                background=CardBackground(radii=radii, colors=colors),
                fonts_path=self.font_path,
                paragraphs=self.frame_text_edit.get_info(),
                smooth=False,
            )
            card.generate()
            # self.show_image = ImageTk.PhotoImage(card.image)
            # self.image_generate.config(image=self.show_image),
            card.image.show()
            card.image.save(self.save_path + "/p5cc_" + str(int(time())) + ".png")
        except:
            messagebox.showerror(_("error"), _("generate_fail_message"))

    def mainloop(self):
        self.gui.mainloop()

def main():
    gui = GeneratorGUI()
    gui.mainloop()


if __name__ == "__main__":
    main()
