# SSIS-V2 — Student Section Information System

A Python-based desktop application for managing student and section records, backed by a MySQL database. SSIS-V2 is the improved second version of the system, featuring a cleaner architecture and enhanced data management capabilities.

---

## Features

- Add, update, and delete student records
- Manage college sections and course assignments
- Search and filter students by ID, name, course, or year level
- Import/export student data via CSV
- Persistent storage using a local MySQL database

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Database | MySQL |
| GUI | Tkinter |

---

## Project Structure

```
SSIS-V2/
├── app/                        # Application source code
│   └── ...
├── MySQL Local.session.sql     # Database schema and seed data
├── students.csv                # Sample/exported student data
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- MySQL Server (local)
- Required Python packages (install via pip):

```bash
pip install mysql-connector-python
```

### Database Setup

1. Open your MySQL client (e.g., MySQL Workbench, DBeaver, or the CLI).
2. Run the provided SQL file to create the schema:

```sql
SOURCE "MySQL Local.session.sql";
```

Or import it through your GUI client.

### Running the App

```bash
cd app
python main.py
```

> Make sure your MySQL server is running and your connection credentials in the app config match your local setup.

---

## Configuration

Update the database connection settings in the app (typically in a `config.py` or at the top of `main.py`):

```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "yourpassword"
DB_NAME = "ssis_db"
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is open source. See [LICENSE](LICENSE) for details.

---

## Author

**joashcasino-sketch** — [GitHub Profile](https://github.com/joashcasino-sketch)