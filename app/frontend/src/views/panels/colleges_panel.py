from pathlib import Path
import sys
import tkinter as tk
from tkinter import CENTER, Button, Frame, PhotoImage, Label, ttk, Entry, messagebox

BASE_DIR = Path(__file__).resolve().parent
ASSETS_PATH = BASE_DIR.parent.parent.parent / "assets"
CONTROLLER_PATH = BASE_DIR.parent.parent.parent.parent / 'backend' / 'src' / 'Controller'
dialog_path = BASE_DIR.parent / 'dialogs'

sys.path.insert(0, str(CONTROLLER_PATH))
from college_controller import CollegeController

sys.path.insert(0, str(dialog_path))
from sort_dropdown import SortDropdown

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class CollegePanel(Frame):
    def __init__(self, parent, controller, user_role="user"):
        super().__init__(parent, bg="#F8ECD1")
        self.controller = controller
        self.user_role = user_role
        self.college_controller = CollegeController(self, user_role)

        #Pagination Setup
        self.current_page = 1
        self.page_size = 20
        self._full_data = []

        self.rowconfigure(0, weight=0)    
        self.rowconfigure(1, weight=1)     
        self.columnconfigure(0, weight=0) 
        self.columnconfigure(1, weight=1) 

        self.setup_ui()


    def setup_ui(self):
        self._build_header()
        self._build_sidebar()
        self._build_content()
        self.setup_buttons(self.user_role)
        self.populate_college()


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


    def _build_content(self):
        self.content = Frame(self, bg="#F8ECD1")
        self.content.grid(row=1, column=1, sticky="nsew")
        self.content.rowconfigure(0, weight=0)   # toolbar
        self.content.rowconfigure(1, weight=0)   # action bar
        self.content.rowconfigure(2, weight=1)   # table ← expands
        self.content.rowconfigure(3, weight=0)
        self.content.columnconfigure(0, weight=1)

        self._build_toolbar()
        self._build_action_bar()
        self._build_table()
        self._build_pagination()

    def _build_toolbar(self):
        toolbar = Frame(self.content, bg="#F8ECD1", height=55)
        toolbar.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 0))
        toolbar.grid_propagate(False)
        toolbar.columnconfigure(1, weight=1)

        try:
            self.refresh_img = PhotoImage(file=relative_to_assets("Refresh_Button.png"))
            refresh_btn = Button(
                toolbar, image=self.refresh_img,
                borderwidth=0, highlightthickness=0,
                command=self.on_refresh,
                relief="flat", activebackground="#F8ECD1", cursor="hand2",
            )
        except Exception:
            refresh_btn = Button(
                toolbar, text="↺", font=("Lato", 12),
                bg="#85586F", fg="white", relief="flat",
                cursor="hand2", command=self.on_refresh,
            )
        refresh_btn.grid(row=0, column=0, padx=(0, 6), pady=10)

        self.search_entry = Entry(
            toolbar,
            bd=0, bg="#DEB6AB", fg="#000716",
            highlightthickness=1, highlightbackground="#85586F",
            font=("Lato", 11), relief="flat"
        )
        self.search_entry.grid(row=0, column=1, sticky="ew",
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
        search_btn.grid(row=0, column=2, padx=(0, 6), pady=10)

        self.sort_dropdown = SortDropdown(
            toolbar,
            on_select_callback=self.college_controller.sort_college,
            options=['College Code', 'College Name']
        )
        self.sort_dropdown.grid(row=0, column=3, pady=10)

    def _build_action_bar(self):
        action_bar = Frame(self.content, bg="#F8ECD1")
        action_bar.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 6))
        action_bar.columnconfigure(0, weight=1)

        Label(
            action_bar, text="College",
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

        self.add_button = Button(btn_frame, text="Add College",
                                 command=self.open_add_dialog, **btn_cfg)
        self.add_button.pack(side="left", padx=(0, 8))

        self.edit_button = Button(btn_frame, text="Edit College",
                                  command=self.open_edit_dialog, **btn_cfg)
        self.edit_button.pack(side="left", padx=(0, 8))

        self.delete_button = Button(btn_frame, text="Delete College",
                                    command=self.delete_selected_college, **btn_cfg)
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
            columns=("College Code", "College Name"),
            show="tree headings",
        )
        self.tree.grid(row=0, column=0, sticky="nsew")

        self.tree.column("#0",           width=40,  minwidth=40,  stretch=False)
        self.tree.column("College Code", width=200, minwidth=120, stretch=False)
        self.tree.column("College Name", width=400, minwidth=200, stretch=True)

        for col in ("College Code", "College Name"):
            self.tree.heading(col, text=col, anchor=CENTER)
        self.tree.heading("#0", text="", anchor="w")

        self.tree.bind("<Button-1>",
            lambda e: "break"
            if self.tree.identify_region(e.x, e.y) == "separator" else None)
        self.tree.bind("<B1-Motion>", self.on_drag_select)
        self.tree.bind("<ButtonRelease-1>", self.on_drag_release)


    def populate_college(self, data=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.tree.tag_configure("odd",  background="#DEB6AB", foreground="#000000")
        self.tree.tag_configure("even", background="#AC7D88", foreground="#FFFFFF")

        try:
            if data is not None:
                self._full_data = data
                self.current_page = 1

            elif not self._full_data:
                self._full_data = self.college_controller.get_all_colleges()

            start = (self.current_page - 1) * self.page_size
            end = start + self.page_size
            page_data = self._full_data[start:end]

            for i, row in enumerate(page_data):
                tag = "odd" if i % 2 == 0 else "even"
                self.tree.insert("", "end", text=str(i + 1), values=(
                    row["College Code"],
                    row["College Name"],
                ), tags=(tag,))
            self._update_pagination_controls()
        except FileNotFoundError:
            print("colleges not found.")


    def open_add_dialog(self):
        dlg = Path(__file__).resolve().parent.parent / "dialogs"
        sys.path.insert(0, str(dlg))
        from add_college_dialog import AddCollegeDialog
        AddCollegeDialog(self, self.college_controller)

    def open_edit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a college to edit.")
            return

        values = self.tree.item(selected[0])["values"]
        college_data = {
            "College Code": values[0],
            "College Name": values[1],
        }

        dlg = Path(__file__).resolve().parent.parent / "dialogs"
        sys.path.insert(0, str(dlg))
        from edit_college_dialog import UpdateCollegeDialog
        UpdateCollegeDialog(self, self.college_controller, college_data)

    def delete_selected_college(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a college to delete.")
            return
        if messagebox.askyesno("Confirm Delete",
                               f"Delete {len(selected)} college(s)? This cannot be undone."):
            ids = [self.tree.item(i)["values"][0] for i in selected]
            self.college_controller.bulk_delete_colleges(ids)


    def setup_buttons(self, user_role):
        disabled_color = "#A49A97"
        if user_role != "admin":
            for btn in (self.delete_button, self.edit_button):
                btn.config(state="disabled", background=disabled_color)
        else:
            for btn in (self.delete_button, self.edit_button):
                btn.config(state="normal")

    def on_refresh(self):
        self.search_entry.delete(0, "end")
        self._full_data = []
        self.current_page = 1
        self.populate_college()

    def on_search(self):
        query = self.search_entry.get().strip()
        if query:
            self.college_controller.search_college(query)
        else:
            self.populate_college()

    def on_drag_select(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            current = list(self.tree.selection())
            if item not in current:
                current.append(item)
            self.tree.selection_set(current)

    def on_drag_release(self, event):
        pass

    #Pagination Helpers
    def _build_pagination(self):
        self.pagination_frame = Frame(self.content, bg="#F8ECD1")
        self.pagination_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 10))

        btn_cfg = dict(
            font=("Lato", 10, "bold"),
            borderwidth=0, highlightthickness=0,
            background="#85586F", foreground="white",
            relief="flat", activebackground="#6e3d54",
            cursor="hand2", padx=10, pady=4,
        )

        self.prev_btn = Button(self.pagination_frame, text="← Prev",
                            command=self._prev_page, **btn_cfg)
        self.prev_btn.pack(side="left", padx=(0, 8))

        self.page_label = Label(self.pagination_frame, text="Page 1 of 1",
                                font=("Lato", 10), bg="#F8ECD1", fg="#642D48")
        self.page_label.pack(side="left", padx=8)

        self.next_btn = Button(self.pagination_frame, text="Next →",
                            command=self._next_page, **btn_cfg)
        self.next_btn.pack(side="left", padx=(0, 8))

        self.page_info_label = Label(self.pagination_frame, text="",
                                    font=("Lato", 9), bg="#F8ECD1", fg="#888")
        self.page_info_label.pack(side="left", padx=8)

    def _update_pagination_controls(self):
        total = len(self._full_data)
        total_pages = max(1, -(-total // self.page_size))

        self.page_label.config(text=f"Page {self.current_page} of {total_pages}")
        self.page_info_label.config(text=f"({total} total records)")
        self.prev_btn.config(state="normal" if self.current_page > 1 else "disabled")
        self.next_btn.config(state="normal" if self.current_page < total_pages else "disabled")
        

    def _prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.populate_college()

    def _next_page(self):
        total_pages = max(1, -(-len(self._full_data) // self.page_size))
        if self.current_page < total_pages:
            self.current_page += 1
            self.populate_college()

if __name__ == "__main__":
    from main_panel import MainPanel
    app = MainPanel(user_role="admin")
    app.show_panel("college")
    app.run()