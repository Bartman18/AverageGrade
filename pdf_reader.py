import pdfplumber
import pandas as pd
import re


pdf_path = "C:/Users/User/PycharmProjects/pdf_Reader/Karta_przebiegu_studiów-273163-2025-02-10_15_51.pdf"


data = []
current_semester = None


def parse_hours_and_grades(rest):
    w_hours = c_hours = l_hours = p_hours = "-"
    grade1 = grade2 = ects = "-"


    hours_match = re.findall(r"(w|c|l|p)\s*(\d+)", rest)
    for hour_type, hour_value in hours_match:
        if hour_type == "w":
            w_hours = hour_value
        elif hour_type == "c":
            c_hours = hour_value
        elif hour_type == "l":
            l_hours = hour_value
        elif hour_type == "p":
            p_hours = hour_value


    grade_match = re.search(r"(\d+,\d+)\s*\[\s*/\s*(\d+,\d+)\]", rest)
    if grade_match:
        grade1 = grade_match.group(1)
        grade2 = grade_match.group(2)
    else:
        grade_match = re.search(r"(\d+,\d+)", rest)
        if grade_match:
            grade1 = grade_match.group(1)


    ects_match = re.search(r"\b(\d+)\b$", rest)
    if ects_match:
        ects = ects_match.group(1)

    return w_hours, c_hours, l_hours, p_hours, grade1, grade2, ects


with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue

        lines = text.split("\n")

        for line in lines:
            line = line.strip()


            if "Semestr" in line:
                current_semester = line.strip()
                continue

            match = re.match(r"^\(([\w-]+)\)\s+(.+)$", line)
            if not match:
                continue

            code = match.group(1)
            rest = match.group(2)

            name_match = re.match(r"^(.+?)\s+(w|c|l|p|\d)", rest)
            if not name_match:
                continue

            name = name_match.group(1).strip()  # Nazwa przedmiotu
            rest_values = rest[len(name):].strip()  # Reszta wartości (godziny + oceny + ECTS)

            w_hours, c_hours, l_hours, p_hours, grade1, grade2, ects = parse_hours_and_grades(rest_values)

            data.append([current_semester, code, name, w_hours, c_hours, l_hours, p_hours, grade1, grade2, ects])


df = pd.DataFrame(data,
                  columns=["Semestr", "Kod przedmiotu", "Nazwa przedmiotu", "Wykłady", "Ćwiczenia", "Lab", "Projekt", "Ocena 1",
                           "Ocena 2", "ECTS"])


df.replace("-", "", inplace=True)


csv_file_path = "pdf_output.csv"
df.to_csv(csv_file_path, index=False, encoding="utf-8")

print(f"✅ Dane zapisane do {csv_file_path}")