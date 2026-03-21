from pathlib import Path
import tkinter as tk

asset_path = Path(__file__).resolve().parent.parent.parent.parent / 'assets'

def relative_to_assets(path: str) -> Path:
    return asset_path / Path(path)

class SortDropdown:
    def __init__(self, parent, on_select_callback, options=None):
        self.parent = parent
        self.on_select_callback = on_select_callback
        self.dropdown_open = False
        self.dropdown_win = None
        self.sort_column = "Name"
        self.sort_reverse = False
        self.options = options or ['ID Number', 'Name', 'Gender', 'Year Level', 'Program', 'College']

        self.sort_button_image = tk.PhotoImage(file=relative_to_assets("sort_button.png"))
        self.button = tk.Button(
            parent,
            image=self.sort_button_image,
            text="Sort By ▾",
            font=("Lato", 10),
            bg="#85586F", fg="white",
            borderwidth=0, highlightthickness=0,
            relief="flat", cursor="hand2",
            command=self.toggle
        )

    def place(self, **kwargs):
        self.button.place(**kwargs)

    def grid(self, **kwargs):
        self.button.grid(**kwargs)

    def pack(self, **kwargs):
        self.button.pack(**kwargs)

    def toggle(self):
        if self.dropdown_open and self.dropdown_win:
            self.close()
            return

        x = self.button.winfo_rootx()
        y = self.button.winfo_rooty() + self.button.winfo_height()
        button_height = 30
        total_height = len(self.options) * button_height

        self.dropdown_win = tk.Toplevel(self.parent)
        self.dropdown_win.wm_overrideredirect(True)
        self.dropdown_win.geometry(f"98x{total_height}+{x}+{y}")
        self.dropdown_win.configure(bg="#85586F")

        for option in self.options:
            btn = tk.Button(
                self.dropdown_win,
                text=option,
                font=("Lato", 10),
                bg="#85586F", fg="white",
                activebackground="#642D48", activeforeground="white",
                borderwidth=0, relief="flat", cursor="hand2",
                anchor="w", padx=5, pady=5,
                command=lambda o=option: self.select(o)
            )
            btn.pack(fill="x", pady=0)

        self.dropdown_open = True

    def select(self, option):
        self.button.config(text=f"{option} ▾")
        self.close()

        if option == self.sort_column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = option
            self.sort_reverse = False

        self.on_select_callback(self.sort_column, self.sort_reverse)

    def close(self):
        if self.dropdown_win:
            self.dropdown_win.destroy()
            self.dropdown_win = None
        self.dropdown_open = False