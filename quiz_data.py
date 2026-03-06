import csv # Used for reading the CSV file
import os # Used to check csv exists

def quiz_questions(rows: list[dict]) -> list[dict]:

    """ Converts csv rows into structured dictionaries and 
        changes correct answer index to start from 1 instead of 0"""

    return [
        {
            "question": row["question"].strip(),
            "options": [
                row["option_a"].strip(),
                row["option_b"].strip(),
                row["option_c"].strip(),
                row["option_d"].strip(),
            ],
            "correct": int(row["correct"]) - 1,
        }
        for row in rows
    ]

def load_questions(filepath = "questions.csv"):

    """ Checks if questions.csv exists and if it doesn't produces an error. 
        If the file does exist then it reads the questions from questions.csv"""

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Questions file not found: '{filepath}'")

    with open(filepath, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    return quiz_questions(rows)
