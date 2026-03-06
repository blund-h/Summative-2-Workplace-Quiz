import csv # Used for writing to the CSV file
from datetime import datetime # Used for formating timestamp

results_headers = ["name", "start_time", "end_time", "score", "total_questions"]

def record_quiz_result(name, start_time, score, total_questions):

    """ Writes the users quiz results to the results.csv once the quiz is complete """

    with open("results.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results_headers)
        writer.writerow({
            "name": name,
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "score": score,
            "total_questions": total_questions
        })
        