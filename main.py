import os
from tkinter import *
from tkinter import filedialog, colorchooser, font, messagebox
from tkinter.ttk import Combobox


def change_color():
    color = colorchooser.askcolor()
    text_area.config(fg=color[1])


def change_font(*args):
    text_area.config(font=(font_name.get(), size_box.get()))


def update_title(event=None):
    title = "Untitled" if file is None else os.path.basename(file)
    current_content = text_area.get(1.0, END).strip()
    if current_content != initial_content.strip():
        if not window.title().endswith(" *"):
            window.title(title + " *")
    else:
        window.title(title)
    text_area.edit_modified(False)


def warn_if_unsaved_changes(action_func):
    def wrapper():
        current_content = text_area.get(1.0, END).strip()
        if current_content != initial_content.strip():
            if messagebox.askyesno(
                "Warning", "You have unsaved changes. Do you want to continue?"
            ):
                action_func()
        else:
            action_func()

    return wrapper


def new_file():
    warn_if_unsaved_changes(_new_file)()


def _new_file():
    global file, initial_content
    file = None
    text_area.delete(1.0, END)
    text_area.edit_modified(False)
    initial_content = ""
    update_title()


def open_file():
    warn_if_unsaved_changes(_open_file)()


def _open_file():
    global file, initial_content
    file = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")],
    )
    if file:
        try:
            with open(file, "r") as f:
                initial_content = f.read()
                text_area.delete(1.0, END)
                text_area.insert(1.0, initial_content)
            text_area.edit_modified(False)
            update_title()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open file: {e}")


def save_file():
    global file, initial_content
    if file is None:
        file = filedialog.asksaveasfilename(
            initialfile="untitled.txt",
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")],
        )
    if file:
        try:
            with open(file, "w") as f:
                f.write(text_area.get(1.0, END).strip())
            text_area.edit_modified(False)
            initial_content = text_area.get(1.0, END).strip()
            update_title()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to save file: {e}")


def cut():
    text_area.event_generate("<<Cut>>")


def copy():
    text_area.event_generate("<<Copy>>")


def paste():
    text_area.event_generate("<<Paste>>")


def about():
    messagebox.showinfo(
        "About this program",
        "This is a text editor created by Bro Code on YouTube and modified by Zachary Wittmann",
    )


def quit():
    current_content = text_area.get(1.0, END).strip()
    if current_content != initial_content.strip():
        if messagebox.askyesno(
            "Warning", "You have unsaved changes. Do you want to quit?"
        ):
            window.destroy()
    else:
        window.destroy()


window = Tk()
window.title("Untitled")
file = None
initial_content = ""

window_width = 500
window_height = 500
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

font_name = StringVar(window)
font_name.set("Arial")

font_size = StringVar(window)
font_size.set("12")

text_area = Text(window, font=(font_name.get(), font_size.get()))

scroll_bar = Scrollbar(text_area)
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
text_area.grid(sticky=N + E + S + W)
scroll_bar.pack(side=RIGHT, fill=Y)
text_area.config(yscrollcommand=scroll_bar.set)

frame = Frame(window)
frame.grid()

color_button = Button(frame, text="Color", command=change_color)
color_button.grid(row=0, column=0)

font_box = Combobox(
    frame, textvariable=font_name, values=font.families(), state="readonly"
)
font_box.grid(row=0, column=1)
font_box.bind("<<ComboboxSelected>>", change_font)

size_box = Spinbox(frame, from_=1, to=100, textvariable=font_size, command=change_font)
size_box.grid(row=0, column=2)

menu_bar = Menu(window)
window.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=quit)

edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)

help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=about)

text_area.bind("<<Modified>>", update_title)

window.protocol("WM_DELETE_WINDOW", quit)
window.mainloop()
