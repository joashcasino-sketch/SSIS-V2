import csv
from pathlib import Path
import sys
import tkinter as tk
from tkinter import CENTER, Button, Frame, PhotoImage, Label, ttk, Entry, messagebox

BASE_DIR = Path(__file__).resolve().parent
ASSETS_PATH = BASE_DIR.parent.parent.parent / "assets"
CONTROLLER_PATH = BASE_DIR.parent.parent.parent.parent / 'backend' / 'src' / 'Controller'
dialog_path = BASE_DIR.parent / 'dialogs'

sys.path.insert(0, str(CONTROLLER_PATH))
from program_controller import ProgramController

sys.path.insert(0, str(dialog_path))
from sort_dropdown import SortDropdown

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class ProgramPanel(Frame):
    def __init__(self, parent, controller, user_role="user"):
        super().__init__(parent, bg="#F8ECD1")
        self.controller = controller
        self.user_role = user_role
        self.program_controller = ProgramController(self, user_role)

        self.rowconfigure(0, weight=0)     # header
        self.rowconfigure(1, weight=1)     # main body
        self.columnconfigure(0, weight=0)  # sidebar
        self.columnconfigure(1, weight=1)  # content

        self.setup_ui()

    # ─────────────────────────── UI SETUP ────────────────────────────────────

    def setup_ui(self):
        self._build_header()
        self._build_sidebar()
        self._build_content()
        self.setup_buttons(self.user_role)
        self.populate_programs()

    # ── Header ───────────────────────────────────────────────────────────────

    def _build_header(self):
        self.header = Frame(self, bg="#85586F", height=85)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.header.grid_propagate(False)

        try:
            self.logo = PhotoImage(file=relative_to_assets("deb_logo.png"))
            Label(self.header, image=self.logo, bg="#85586F").place(
                x=10, y=20, width=200, height=60)
        except Exception:
            Label(self.header, text="DeB", bg="#85586F",
                  fg="white", font=("Arial", 20, "bold")).place(x=10, y=20)

    # ── Sidebar ───────────────────────────────────────────────────────────────

    def _build_sidebar(self):
        self.sidebar = Frame(self, bg="#DEB6AB", width=250)
        self.sidebar.grid(row=1, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)
        self.sidebar.rowconfigure(10, weight=1)

        nav_buttons = [
            ("student_button.png", "Student", "student"),
            ("program_button.png", "Program", "program"),
            ("college_button.png", "College", "college"),
        ]

        for i, (img_file, label, panel_name) in enumerate(nav_buttons):
            try:
                img = PhotoImage(file=relative_to_assets(img_file))
                btn = Button(
                    self.sidebar, image=img,
                    borderwidth=0, highlightthickness=0,
                    bg="#DEB6AB",
                    command=lambda p=panel_name: self.controller.show_panel(p),
                    relief="flat", activebackground="#DEB6AB", cursor="hand2",
                )
                btn.image = img
                btn.image.configure(width=215)          # prevent GC
                btn.grid(row=i, column=0, padx=15,
                         pady=(10 if i == 0 else 15, 0), sticky="ew")
            except Exception:
                Button(
                    self.sidebar, text=label,
                    font=("Lato", 11, "bold"), bg="#85586F", fg="white",
                    relief="flat", cursor="hand2",
                    command=lambda p=panel_name: self.controller.show_panel(p),
                ).grid(row=i, column=0, padx=15,
                       pady=(10 if i == 0 else 5, 0), sticky="ew")

        try:
            self.setting_img = PhotoImage(file=relative_to_assets("settings_button.png"))
            Button(
                self.sidebar, image=self.setting_img,
                borderwidth=0, highlightthickness=0,
                command=lambda: print("Settings clicked"),
                relief="flat", activebackground="#DEB6AB", cursor="hand2",
            ).grid(row=11, column=0, padx=15, pady=10, sticky="sew")
        except Exception:
            Button(
                self.sidebar, text="Settings",
                font=("Lato", 11, "bold"), bg="#85586F", fg="white",
                relief="flat", cursor="hand2",
            ).grid(row=11, column=0, padx=15, pady=10, sticky="sew")

    # ── Content ───────────────────────────────────────────────────────────────

    def _build_content(self):
        self.content = Frame(self, bg="#F8ECD1")
        self.content.grid(row=1, column=1, sticky="nsew")
        self.content.rowconfigure(0, weight=0)   # toolbar
        self.content.rowconfigure(1, weight=0)   # action bar
        self.content.rowconfigure(2, weight=1)   # table ← expands
        self.content.columnconfigure(0, weight=1)

        self._build_toolbar()
        self._build_action_bar()
        self._build_table()

    def _build_toolbar(self):
        toolbar = Frame(self.content, bg="#F8ECD1", height=55)
        toolbar.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 0))
        toolbar.grid_propagate(False)
        toolbar.columnconfigure(0, weight=1)

        self.search_entry = Entry(
            toolbar,
            bd=0, bg="#DEB6AB", fg="#000716",
            highlightthickness=1, highlightbackground="#85586F",
            font=("Lato", 11), relief="flat"
        )
        self.search_entry.grid(row=0, column=0, sticky="ew",
                               ipady=6, padx=(0, 6), pady=10)
        self.search_entry.bind("<Return>", lambda e: self.on_search())

        try:
            self.search_img = PhotoImage(file=relative_to_assets("search_button.png"))
            search_btn = Button(
                toolbar, image=self.search_img,
                borderwidth=0, highlightthickness=0,
                command=self.on_search,
                relief="flat", activebackground="#F8ECD1", cursor="hand2",
            )
        except Exception:
            search_btn = Button(
                toolbar, text="🔍", font=("Lato", 11),
                bg="#85586F", fg="white", relief="flat",
                cursor="hand2", command=self.on_search,
            )
        search_btn.grid(row=0, column=1, padx=(0, 6), pady=10)

        self.sort_dropdown = SortDropdown(
            toolbar,
            on_select_callback=self.program_controller.sort_program,
            options=['Program Code', 'Program Name', 'College Code', 'College Name']
        )
        self.sort_dropdown.grid(row=0, column=2, pady=10)

    def _build_action_bar(self):
        action_bar = Frame(self.content, bg="#F8ECD1")
        action_bar.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 6))
        action_bar.columnconfigure(0, weight=1)

        Label(
            action_bar, text="Program",
            font=("Lato", 24), fg="#642D48", bg="#F8ECD1"
        ).grid(row=0, column=0, sticky="w")

        btn_frame = Frame(action_bar, bg="#F8ECD1")
        btn_frame.grid(row=0, column=1, sticky="e")

        btn_cfg = dict(
            font=("Lato", 10, "bold"),
            borderwidth=0, highlightthickness=0,
            background="#85586F", foreground="white",
            relief="flat", activebackground="#6e3d54",
            cursor="hand2", padx=12, pady=6,
        )

        self.add_button = Button(btn_frame, text="Add Program",
                                 command=self.open_add_dialog, **btn_cfg)
        self.add_button.pack(side="left", padx=(0, 8))

        self.edit_button = Button(btn_frame, text="Edit Program",
                                  command=self.open_edit_dialog, **btn_cfg)
        self.edit_button.pack(side="left", padx=(0, 8))

        self.delete_button = Button(btn_frame, text="Delete Program",
                                    command=self.delete_selected_program, **btn_cfg)
        self.delete_button.pack(side="left")

    def _build_table(self):
        table_frame = Frame(self.content, bg="#F8ECD1")
        table_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview",
                             bg="#A6738D", fg="#000000",
                             fieldbackground="#D8A9C2", rowheight=26)
        self.style.configure("Treeview.Heading",
                             background="#884668", foreground="#D8A9C2",
                             font=("Trebuchet MS", 10, "bold"))
        self.style.map("Treeview", background=[("selected", "#85586F")])

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Program Code", "Program Name", "College Code", "College Name"),
            show="tree headings",
        )
        self.tree.grid(row=0, column=0, sticky="nsew")

        self.tree.column("#0",           width=40,  minwidth=40,  stretch=False)
        self.tree.column("Program Code", width=130, minwidth=90,  stretch=False)
        self.tree.column("Program Name", width=280, minwidth=150, stretch=True)
        self.tree.column("College Code", width=130, minwidth=90,  stretch=False)
        self.tree.column("College Name", width=280, minwidth=150, stretch=True)

        for col in ("Program Code", "Program Name", "College Code", "College Name"):
            self.tree.heading(col, text=col, anchor=CENTER)
        self.tree.heading("#0", text="", anchor="w")

        # vsb = ttk.Scrollbar(table_frame, orient="vertical",
        #                     command=self.tree.yview)
        # vsb.grid(row=0, column=1, sticky="ns")
        # self.tree.configure(yscrollcommand=vsb.set)

        # hsb = ttk.Scrollbar(table_frame, orient="horizontal",
        #                     command=self.tree.xview)
        # hsb.grid(row=1, column=0, sticky="ew")
        # self.tree.configure(xscrollcommand=hsb.set)

        self.tree.bind("<Button-1>",
            lambda e: "break"
            if self.tree.identify_region(e.x, e.y) == "separator" else None)
        self.tree.bind("<B1-Motion>", self.on_drag_select)
        self.tree.bind("<ButtonRelease-1>", self.on_drag_release)

    # ─────────────────────────── DATA ────────────────────────────────────────

    def populate_programs(self, data=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.tree.tag_configure("odd",  background="#DEB6AB", foreground="#000000")
        self.tree.tag_configure("even", background="#AC7D88", foreground="#FFFFFF")

        try:
            if data is None:
                csv_path = (BASE_DIR.parent.parent.parent.parent
                            / "backend" / "data" / "programs.csv")
                with open(csv_path, newline="", encoding="utf-8") as f:
                    data = list(csv.DictReader(f))

            for i, row in enumerate(data):
                tag = "odd" if i % 2 == 0 else "even"
                self.tree.insert("", "end", text=str(i + 1), values=(
                    row["Program Code"], row["Program Name"],
                    row["College Code"], row["College Name"],
                ), tags=(tag,))
        except FileNotFoundError:
            print("programs.csv not found.")

    # ─────────────────────────── DIALOGS ─────────────────────────────────────

    def open_add_dialog(self):
        dlg = Path(__file__).resolve().parent.parent / "dialogs"
        sys.path.insert(0, str(dlg))
        from add_program_dialog import AddProgramDialog
        AddProgramDialog(self, self.program_controller)

    def open_edit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a program to edit.")
            return

        values = self.tree.item(selected[0])["values"]
        program_data = {
            "Program Code": values[0], "Program Name": values[1],
            "College Code": values[2], "College Name": values[3],
        }

        dlg = Path(__file__).resolve().parent.parent / "dialogs"
        sys.path.insert(0, str(dlg))
        from edit_program_dialog import UpdateProgramDialog
        UpdateProgramDialog(self, self.program_controller, program_data)

    def delete_selected_program(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a program to delete.")
            return
        if messagebox.askyesno("Confirm Delete",
                               f"Delete {len(selected)} program(s)? This cannot be undone."):
            ids = [self.tree.item(i)["values"][0] for i in selected]
            self.program_controller.bulk_delete_programs(ids)

    # ─────────────────────────── HELPERS ─────────────────────────────────────

    def setup_buttons(self, user_role):
        disabled_color = "#A49A97"
        if user_role != "admin":
            for btn in (self.delete_button, self.edit_button):
                btn.config(state="disabled", background=disabled_color)
        else:
            for btn in (self.delete_button, self.edit_button):
                btn.config(state="normal")

    def on_search(self):
        query = self.search_entry.get().strip()
        if query:
            self.program_controller.search_program(query)
        else:
            self.populate_programs()

    def on_drag_select(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            current = list(self.tree.selection())
            if item not in current:
                current.append(item)
            self.tree.selection_set(current)

    def on_drag_release(self, event):
        pass


if __name__ == "__main__":
    from main_panel import MainPanel
    app = MainPanel(user_role="admin")
    app.show_panel("program")
    app.run()