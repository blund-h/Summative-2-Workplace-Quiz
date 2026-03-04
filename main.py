import tkinter as tk # Used to create Graphical User Interface (GUI)
import csv # Used as a storage for questions

def load_questions(filepath="questions.csv"):

    questions = []

    with open(filepath, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            questions.append({
                "question": row["question"],
                "options": [
                    row["option_a"],
                    row["option_b"],
                    row["option_c"],
                    row["option_d"],
                ],
                "correct": int(row["correct"]) - 1
            })

    return questions

class QuizApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.bg_colour = "#000000"
        self.primary_colour = "#FFFFFF"
        self.correct_colour = "#2E8B57"
        self.error_colour = "#C1121F"
        
        self.title("Quiz")
        self.geometry("700x850")
        self.resizable(False, False)
        self.configure(bg=self.bg_colour)

        self.score = 0
        self.questions = load_questions()
        self.total_questions = len(self.questions)
        self.current_question = 0
        self.correct_answer = None

        self.build_quiz_screen()
        self.load_question()


    def build_quiz_screen(self):

        container = tk.Frame(self, bg=self.bg_colour)
        container.pack(expand=True)

        self.question_label = tk.Label(
            container,
            font=("Arial", 26, "bold"),
            wraplength=650,
            justify="center",
            bg=self.bg_colour,
            fg=self.primary_colour
        )
        self.question_label.pack(pady=40)
        
        self.answer_var = tk.IntVar(value=-1)
        self.option_buttons = []

        for option in range(4):
            rb = tk.Radiobutton(
                container,
                text="",
                variable=self.answer_var,
                value=option,
                font=("Arial", 20),
                bg=self.bg_colour,
                fg=self.primary_colour,
            )
            rb.pack(anchor="w", padx=60, pady=5)
            self.option_buttons.append(rb)

        self.feedback_label = tk.Label(
            container, font=("Arial", 20), bg=self.bg_colour
        )
        self.feedback_label.pack(pady=20)

        tk.Button(
            container,
            text="Submit",
            font=("Arial", 18, "bold"),
            command=self.check_answer
        ).pack(pady=30)



    def load_question(self):

        q = self.questions[self.current_question]

        self.correct_answer = q["correct"]

        self.question_label.config(text=q["question"])

        for i, option_text in enumerate(q["options"]):
            self.option_buttons[i].config(text=f"{chr(65+i)}: {option_text}")

        self.answer_var.set(-1)
        self.feedback_label.config(text="")


    def check_answer(self):
        selected = self.answer_var.get()

        if selected == -1:
            self.feedback_label.config(
                text="Choose an option",
                fg=self.error_colour
            )
            return

        if selected == self.correct_answer:
            self.score += 1
            self.feedback_label.config(text="Correct!", fg=self.correct_colour)
        else:
            correct_letter = chr(65 + self.correct_answer)
            self.feedback_label.config(
                text=f"Incorrect. Correct answer: {correct_letter}",
                fg=self.error_colour
            )

        self.current_question += 1
        self.after(900, self.load_question)


if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()