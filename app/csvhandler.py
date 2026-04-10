import csv
import random

first_names_male = [
    "Juan", "Miguel", "Carlos", "Jose", "Antonio",
    "Mark", "John", "James", "Roberto", "Angelo",
    "James", "Gilbert", "Josh", "Joshua", "Kenneth",
    "Vincent", "Robert", "Alejandro", "Thomas", "Lance"
]
first_names_female = [
    "Maria", "Ana", "Sofia", "Isabella", "Gabriela",
    "Christine", "Angela", "Patricia", "Karen", "Nicole",
    "Elena", "Jasmine", "Rochelle", "Monica", "Beatriz", "Therese",
     "Therese", "Camille", "Vanessa", "Lourdes", "Clarice",
]
last_names = [
    "Santos", "Reyes", "Cruz", "Garcia", "Torres",
    "Flores", "Dela Cruz", "Ramos", "Mendoza", "Villanueva",
    "Bautista", "Aquino", "Pascual", "Castillo", "Dizon",
    "Sarmiento", "Mercado", "Salvador", "Guevarra", "Perez", "Dizon",
]
programs = [
    "BAELS", "BAHisto", "BALCS",
    "BAPS", "BAPsych", "BASoc", "BEEd", "BPEd",
    "BSA", "BSBA", "BSBA-BE",
    "BSBA-MM", "BSBio", "BSCA", "BSCE", "BSEcE", "BSChem", "BSCS", "BSE",
    "BSEcE", "BSEd-Eng", "BSEd-Fil", "BSEd-Math", "BSEd-Sci",
    "BSEd-SS", "BSEE", "BSEntrep", "BSES", "BSHM", 
    "BSIS", "BSIT", "BSMath", "BSME", "BSMetE", 
    "BSN", "BSPhil", "BSPhys", "BSPsych"
]
genders = ["Male", "Female"]
year_levels = ["1", "2", "3", "4"]

def generate_student_id(year, index):
    return f"{year}-{str(index).zfill(4)}"

def generate_students(count=5000):
    # Map year level to enrollment year
    year_level_to_year = {
        "1": 2025,
        "2": 2024,
        "3": 2023,
        "4": 2022,
    }

    students = []
    # Track index per year so IDs don't overlap
    year_counters = {2022: 1, 2023: 1, 2024: 1, 2025: 1}

    for _ in range(count):
        gender = random.choice(genders)
        first_name = random.choice(
            first_names_male if gender == "Male" else first_names_female
        )
        last_name = random.choice(last_names)
        year_level = random.choice(year_levels)
        program = random.choice(programs)

        enroll_year = year_level_to_year[year_level]
        index = year_counters[enroll_year]
        year_counters[enroll_year] += 1

        student_id = generate_student_id(enroll_year, index)
        students.append([student_id, first_name, last_name, gender, year_level, program])

    return students


# Generate and save
students = generate_students(count=5000)  # change count as needed

with open("students.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(students)

print(f"Generated {len(students)} students → students.csv")