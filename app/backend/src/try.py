import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
frontend_src_path = BASE_DIR.parent.parent.parent / 'frontend' / 'src' / 'views' / 'panels'
sys.path.insert(0, str(frontend_src_path))


from students_panel import StudentPanel

if __name__ == "__main__":
    print("test")