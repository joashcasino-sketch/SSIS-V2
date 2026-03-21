import sys
from pathlib import Path
from tkinter import Label, Tk, Canvas, Entry, Button, PhotoImage

backend_path = Path(__file__).resolve().parent.parent.parent.parent / "backend" / "src"
sys.path.insert(0, str(backend_path))

from login_handler import handle_sign_in, handle_sign_up

BASE_DIR = Path(__file__).resolve().parent
ASSETS_PATH = BASE_DIR.parent.parent.parent / "frontend" / "assets" / "frame0"
LOGO_PATH = Path(__file__).resolve().parent.parent.parent / "assets" / "deb_logo.png"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def create_login_window():
    window = Tk()
    window.geometry("409x425")
    window.configure(bg="#F8ECD1")
    window.title("Login Panel")

    icon = PhotoImage(file=str(LOGO_PATH))
    window.iconphoto(True, icon)

    canvas = Canvas(
        window,
        bg="#F8ECD1",
        height=425,
        width=409,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(204.0, 231.0, image=image_image_1)

    canvas.create_text(
        30.0, 38.0,
        anchor="nw",
        text="Welcome",
        fill="#000000",
        font=("Inter SemiBold", 45, "bold")
    )

    canvas.create_text(
        85.0, 189.0,
        anchor="nw",
        text="username:",
        fill="#000000",
        font=("Inter Light", 13)
    )

    canvas.create_text(
        85.0, 258.0,
        anchor="nw",
        text="password:",
        fill="#000000",
        font=("Inter Light", 13)
    )

    # Entry fields
    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(245.0, 197.0, image=entry_image_1)
    
    username_entry = Entry(
        window,
        bd=0,
        bg="#DEB6AB",
        fg="#000716",
        highlightthickness=0,
        font=("Inter", 11)
    )
    username_entry.place(x=180.0, y=184.0, width=130.0, height=26.0)

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(245.0, 267.0, image=entry_image_2)
    
    password_entry = Entry(
        window,
        bd=0,
        bg="#DEB6AB",
        fg="#000716",
        highlightthickness=0,
        show="*",
        font=("Inter", 11)
    )
    password_entry.place(x=180.0, y=253.0, width=130.0, height=26.0)

    # Buttons
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: handle_sign_in(username_entry, password_entry, window),
        relief="flat",
        cursor="hand2"
    )
    button_1.place(x=95.0, y=340.0, width=92.0, height=51.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(
        window,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: handle_sign_up(username_entry, password_entry),
        relief="flat",
        cursor="hand2"
    )
    button_2.place(x=223.0, y=341.0, width=92.0, height=51.0)

    canvas.create_rectangle(
        35.0, 113.0,
        373.0, 115.0,
        fill="#85586F",
        outline=""
    )

    # Bind Enter key to login
    window.bind('<Return>', lambda e: handle_sign_in(username_entry, password_entry, window))
    
    # Keep image references to prevent garbage collection
    window.image_refs = [image_image_1, entry_image_1, entry_image_2, button_image_1, button_image_2, icon]
    
    window.resizable(False, False)
    _center_window(window)
    return window

def _center_window(window):
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (window.winfo_width() // 2)
        y = (window.winfo_screenheight() // 2) - (window.winfo_height() // 2)
        window.geometry(f'+{x}+{y}')


if __name__ == "__main__":
    window = create_login_window()
    window.mainloop()