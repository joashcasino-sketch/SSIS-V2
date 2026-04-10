import csv
import random

first_names_male = [
    "Juan", "Miguel", "Carlos", "Jose", "Antonio",
    "Mark", "John", "James", "Roberto", "Angelo",
    "James", "Gilbert", "Josh", "Joshua", "Kenneth",
    "Vincent", "Robert", "Alejandro", "Thomas", "Lance",
    "Nathaniel", "Gabriel", "Rafael", "Dominic", "Benedict",
    "Ricardo", "Sebastian", "Adrian", "Julian", "Christian",
    "Francis", "Gerard", "Leonardo", "Manuel", "Patrick",
    "Timothy", "Victor", "Samuel", "Xavier", "Zachary",
    "Arthur", "Brandon", "Cedric", "Dexter", "Ethan",
    "Ferdinand", "Gregory", "Harold", "Ian", "Jasper",
    "Kevin", "Lawrence", "Marco", "Nelson", "Oliver",
    "Philip", "Quentin", "Roderick", "Simon", "Tristan",
    "Alvin", "Byron", "Clarence", "Damian", "Edgar",
    "Fabian", "Geoffrey", "Hugo", "Ivan", "Jerome",
    "Kaleb", "Lionel", "Marlon", "Noel", "Oscar",
    "Percival", "Roland", "Stephen", "Terrence", "Ulysses",
    "Ezekiel", "Liam", "Jayden", "Noah", "Danilo",
    "Diego", "Eric", "Ernesto", "Luis", "Ronald",
    "Steven", "Alab", "Isko", "Basilio", "Esteban",
    "Dakila", "Bayani", "Efren", "Alfonso", "Felix"
]
first_names_female = [
    "Maria", "Ana", "Sofia", "Isabella", "Gabriela",
    "Christine", "Angela", "Patricia", "Karen", "Nicole",
    "Elena", "Jasmine", "Rochelle", "Monica", "Beatriz", "Therese",
    "Therese", "Camille", "Vanessa", "Lourdes", "Clarice",
    "Danica", "Eliza", "Felicity", "Giselle", "Hazel",
    "Iris", "Jocelyn", "Kiara", "Leila", "Melanie",
    "Nadine", "Olivia", "Paola", "Quinnie", "Rina",
    "Selena", "Tanya", "Ursula", "Vivian", "Wendy",
    "Abigail", "Beatrice", "Cassandra", "Daphne", "Erica",
    "Fiona", "Genevieve", "Hannah", "Isabelle", "Julia",
    "Kaitlyn", "Lorraine", "Maureen", "Noelle", "Ophelia",
    "Penelope", "Rachel", "Sabrina", "Trisha", "Veronica",
    "Tala", "Mayumi", "Amihan", "Mutya", "Bituin",
    "Lualhati", "Sinag", "Hiraya", "Hiyas", "Malaya",
    "Agnes", "Alexa", "Alicia", "Imelda", "Joanna",
    "Sheila", "Maricel", "Yolanda", "Clara", "Daniela"
]
last_names = [
    "Santos", "Reyes", "Cruz", "Garcia", "Torres",
    "Flores", "Dela Cruz", "Ramos", "Mendoza", "Villanueva",
    "Bautista", "Aquino", "Pascual", "Castillo", "Dizon",
    "Sarmiento", "Mercado", "Salvador", "Guevarra", "Perez", "Dizon",
    "Alcantara", "Bernardo", "Cabrera", "Dagohoy", "Estrella",
    "Ferrer", "Guzman", "Hernandez", "Ibarra", "Jimenez",
    "Laxamana", "Madlangbayan", "Navarro", "Ocampo", "Panganiban",
    "Quinto", "Robles", "Salazar", "Tiongson", "Valdez",
    "Abad", "Beltran", "Corpuz", "Dumlao", "Enriquez",
    "Fajardo", "Guinto", "Hizon", "Ilagan", "Javier",
    "Lontoc", "Malvar", "Noble", "Ortega", "Peralta",
    "Quizon", "Rosales", "Sison", "Tolentino", "Umali",
    "Gonzalez", "Lopez", "Francisco", "Rivera", "Aquino",
    "Castro", "Sanchez", "Domingo", "Martinez", "Aguinaldo",
    "Cariaga", "Ancheta", "Mariano", "Andres", "Crisostomo",
    "Salvador", "Galicia", "Aguirre", "Marquez", "Aguilar"
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