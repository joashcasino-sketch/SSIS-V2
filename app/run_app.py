import sys
from pathlib import Path 

current_dir = Path(__file__).resolve().parent 
frontend_views_path = current_dir / 'frontend' / 'src' / 'views'
sys.path.insert(0, str(frontend_views_path))

from login import create_login_window


if __name__ == "__main__":
    window = create_login_window()
    window.mainloop()