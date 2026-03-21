import sys
from pathlib import Path
import tkinter as tk

BASE_DIR = Path(__file__).resolve().parent
ASSETS_PATH = BASE_DIR.parent.parent.parent / "assets"
CONTROLLER_PATH = BASE_DIR.parent.parent.parent.parent / 'backend' / 'src' / 'Controller'
sys.path.insert(0, str(CONTROLLER_PATH))

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class MainPanel:
    def __init__(self, user_role="user"):
        self.user_role = user_role
        self.root = tk.Tk()
        self.root.geometry("1260x680")
        self.root.minsize(1260, 680)
        self.root.resizable(True, True)
        self.root.title("Student Information System")
        self.root.configure(bg="#F8ECD1")
        self.current_panel = None
        self.panels = {}

        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.create_all_panels()
        self.show_panel("student")
        
        self.center_window()

    def create_all_panels(self):
        from students_panel import StudentPanel
        from programs_panel import ProgramPanel
        from colleges_panel import CollegePanel

        panels_config = [
        (StudentPanel, "student"),  # ← None, handled internally
        (ProgramPanel, "program"),
        (CollegePanel, "college")
        ]


        for PanelClass, name, in panels_config:
            frame = PanelClass(self.container, self, user_role=self.user_role)
            self.panels[name] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)


    def show_panel(self, name):
        panel = self.panels[name]
        panel.lift()
        self.current_panel = panel


    def run(self):
        self.root.mainloop()

    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f'+{x}+{y}')

if __name__ == "__main__":
    app = MainPanel(user_role="admin")
    app.run()