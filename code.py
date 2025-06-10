import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox

# Настройки внешнего вида
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Окно
app = ctk.CTk()
app.geometry("500x350")
app.title("Editor")

# Цвета
BG_COLOR = "#101010"
FRAME_COLOR = "#101010"
TEXT_COLOR = "white"
HIGHLIGHT_COLOR = "#303030"

# Главный фрейм
main_frame = ctk.CTkFrame(app, corner_radius=15, fg_color=FRAME_COLOR)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Текстовое поле
text_box = ctk.CTkTextbox(main_frame, height=200, corner_radius=10,
                          fg_color=BG_COLOR, text_color=TEXT_COLOR,
                          font=("Consolas", 12), wrap="none")
text_box.pack(fill="both", padx=10, pady=10, expand=True)

# Доступ к tk.Text
tk_text = text_box._textbox
tk_text.tag_configure("current_line", background=HIGHLIGHT_COLOR)

# Функция подсветки текущей строки (по курсору)
def highlight_current_line(event=None):
    tk_text.tag_remove("current_line", "1.0", "end")
    cursor_index = tk_text.index("insert")
    line = cursor_index.split('.')[0]
    tk_text.tag_add("current_line", f"{line}.0", f"{line}.0 lineend")

# События клавиатуры и клика
tk_text.bind("<KeyRelease>", highlight_current_line)
tk_text.bind("<ButtonRelease>", highlight_current_line)

# Также вызвать при старте
app.after(100, highlight_current_line)

# Функции кнопок
def inject():
    code = text_box.get("1.0", "end").strip()
    if code:
        try:
            exec(code, globals())
        except Exception as e:
            messagebox.showerror("Error", str(e))

def select_file():
    file = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file:
        with open(file, "r") as f:
            text_box.delete("1.0", "end")
            text_box.insert("1.0", f.read())
        highlight_current_line()

def save_file():
    file = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
    if file:
        with open(file, "w") as f:
            f.write(text_box.get("1.0", "end").strip())
        messagebox.showinfo("Saved", f"File saved as:\n{file}")

# Кнопки
button_frame = ctk.CTkFrame(main_frame, fg_color=FRAME_COLOR)
button_frame.pack(pady=5)

ctk.CTkButton(button_frame, text="▶", width=20, fg_color="#2a2a2a",
              hover_color="#333333", command=inject).grid(row=0, column=0, padx=0)

ctk.CTkButton(button_frame, text="📂", width=20, fg_color="#2a2a2a",
              hover_color="#333333", command=select_file).grid(row=0, column=1, padx=5)

ctk.CTkButton(button_frame, text="💾", width=20, fg_color="#2a2a2a",
              hover_color="#333333", command=save_file).grid(row=0, column=2, padx=0)

# Запуск
app.mainloop()
