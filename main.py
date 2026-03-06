import tkinter as tk # Used to create Graphical User Interface (GUI)
from tkinter import messagebox # Used to generate message box if checks fail
from datetime import datetime # Used to capture timestamp 
from quiz_data import load_questions # Used to load questions from CSV
from quiz_write_results import record_quiz_result # Used to write results into a CSV
# Utility functions to clean and validate names:
from quiz_utils import (clean_name, check_valid_name, check_answer_selected, check_correct_answer)


class QuizApp(tk.Tk):

    """ The class that represents the quiz application """

    def __init__(self):

        """ Sets up the app window, colour palate, images and quiz variables """

        super().__init__()

        self.white_colour = "#FFFFFF"
        self.black_colour = "#000000"
        self.atlas_blue_colour = "#054E5A"
        self.atlas_yellow_colour  = "#E1B77E"
        self.correct_colour = "#2E8B57"
        self.error_colour   = "#C1121F"

        self.title("SUN R&D PMO Multiple Choice Quiz")
        self.geometry("1000x650")
        self.resizable(False, False)
        self.configure(bg=self.white_colour)

        self.blue_bg_logo_image = tk.PhotoImage(file="atlas_logo_blue_bg.png")
        self.blue_bg_logo_image = self.blue_bg_logo_image.subsample(3, 3)

        self.white_bg_logo_image = tk.PhotoImage(file="atlas_logo_white_bg.png")
        self.white_bg_logo_image = self.white_bg_logo_image.subsample(3, 3)

        self.user_name = None
        self.start_time = None
        self.score = 0
        self.current_question = 0
        self.correct_answer = None

        try:
            self.questions = load_questions()
        except FileNotFoundError as exc:
            messagebox.showerror("Missing File", str(exc))
            self.destroy()
            return
        except ValueError as exc:
            messagebox.showerror("Invalid Data", str(exc))
            self.destroy()
            return
        
        self.total_questions = len(self.questions)

        self.build_name_screen()


    def clear_screen(self):

        """ Removes all widgets from the window """

        for widget in self.winfo_children():
            widget.destroy()


    def build_name_screen(self):

        """ Builds the welcome page and allows the user to input their name """

        self.clear_screen()

        container = tk.Frame(self, bg=self.atlas_blue_colour)
        container.pack(fill="both", expand=True)

        left_frame = tk.Frame(container, bg=self.atlas_blue_colour, width=600)
        left_frame.pack(side="left", fill="both", expand=True)
        left_frame.pack_propagate(False)

        tk.Label(
            left_frame,
            text="SUN R&D PMO Team Knowledge Quiz",
            font=("Arial", 30, "bold"),
            bg=self.atlas_blue_colour,
            fg=self.white_colour,
            justify="left",
            wraplength=500,
        ).pack(anchor="w", padx=50, pady=(80, 20))

        tk.Label(
            left_frame,
            text="Welcome to the SUN R&D PMO Quiz!\n\n"
                 "This quiz is designed to test your knowledge on the tools, procedures and common practises that the SUN R&D PMO Team has established.\n\n"
                 "The quiz consists of multiple choice questions that you must answer and submit. At the end of the quiz you will recieve your score which will be stored in a results.csv file.\n\n"
                 "Good Luck!",
            font=("Arial", 14),
            bg=self.atlas_blue_colour,
            fg=self.white_colour,
            justify="left",
            wraplength=420,
        ).pack(anchor="w", padx=50)


        right_frame = tk.Frame(container, bg=self.white_colour, width=500)
        right_frame.pack(side="right", fill="both", expand=True)
        right_frame.pack_propagate(False)

        user_entry_frame = tk.Frame(right_frame, bg=self.white_colour)
        user_entry_frame.place(relx=0.5, rely=0.35, anchor="center")

        tk.Label(
            user_entry_frame,
            text="Enter Your Full Name",
            font=("Arial", 22, "bold"),
            bg=self.white_colour,
            fg=self.black_colour,
        ).pack(pady=(0, 16))

        self.name_entry = tk.Entry(
            user_entry_frame, font=("Arial", 18), width=22,relief="solid", bd=1)
        self.name_entry.pack(ipady=6)
        self.name_entry.focus()

        self.feedback_label = tk.Label(
            user_entry_frame, text="", font=("Arial", 13), bg=self.white_colour)
        self.feedback_label.pack()

        tk.Button(
            user_entry_frame,
            text="Start Quiz",
            font=("Arial", 15, "bold"),
            bg=self.atlas_yellow_colour,
            fg=self.white_colour,
            padx=20,
            pady=8,
            command=self.start_quiz,
        ).pack(pady=(20, 0))

        tk.Label(
            right_frame,
            image=self.white_bg_logo_image,
            bg=self.white_colour
         ).place(relx=0.63, rely=0.9, anchor="center")


    def build_quiz_screen(self):

        """ Builds the question screen for the questions, 
            answer options, answer feedback and submit button """

        self.clear_screen()

        top_frame = tk.Frame(self, bg=self.atlas_blue_colour, height=70)
        top_frame.pack(fill="x")
        top_frame.pack_propagate(False)


        self.progress_label = tk.Label(
            top_frame,
            font=("Arial", 24),
            bg=self.atlas_blue_colour,
            fg=self.white_colour
        )
        self.progress_label.place(relx=0.5, rely=0.5, anchor="center")

        self.score_label = tk.Label(
            top_frame,
            text=f"Score: {self.score}",
            font=("Arial", 16, "bold"),
            bg=self.atlas_blue_colour,
            fg=self.white_colour
        )
        self.score_label.pack(side="right", padx=20, pady=12)


        bottom_frame = tk.Frame(self, bg=self.white_colour)
        bottom_frame.pack(fill="both", expand=True)

        self.question_label = tk.Label(
            bottom_frame,
            font=("Arial", 30, "bold"),
            wraplength=750,
            justify="left",
            bg=self.white_colour,
            fg=self.atlas_blue_colour
        )
        self.question_label.pack(anchor="w", padx=40, pady=(60, 20))

        self.answer_var = tk.IntVar(value=-1)
        self.option_buttons = []

        for option in range(4):
            rb = tk.Radiobutton(
                bottom_frame,
                text="",
                variable=self.answer_var,
                value=option,
                font=("Arial", 18),
                bg=self.white_colour,
                fg=self.atlas_blue_colour,
                selectcolor=self.white_colour,
                activebackground=self.white_colour
            )
            rb.pack(anchor="w", padx=40, pady=10)
            self.option_buttons.append(rb)

        self.feedback_label = tk.Label(
            bottom_frame, font=("Arial", 14), bg=self.white_colour
        )
        self.feedback_label.pack(anchor="center", pady=(15, 3))

        tk.Button(
            bottom_frame,
            text="Submit",
            font=("Arial", 18, "bold"),
            bg=self.atlas_yellow_colour,
            fg=self.white_colour,
            padx=20,
            pady=6,
            command=self.check_answer,
        ).pack(anchor="center", pady=(10, 0))

        tk.Label(
            bottom_frame,
            image=self.white_bg_logo_image,
            bg=self.white_colour,
        ).place(relx=0.95, rely=0.95, anchor="se")     


    def start_quiz(self):

        """ Makes sure the entered name is valid and starts the quiz """

        name_entered = self.name_entry.get()
        valid, message = check_valid_name(name_entered)

        if not valid:
            self.feedback_label.config(text=message, fg=self.error_colour)
            return

        self.user_name = clean_name(name_entered)
        self.start_time = datetime.now()
        self.score = 0
        self.current_question = 0

        self.build_quiz_screen()
        self.next_question()


    def next_question(self):

        """ Loads the next question onto the question screen or 
            ends the quiz if all questions have been answered """

        if self.current_question >= self.total_questions:
            self.end_quiz()
            return

        q = self.questions[self.current_question]

        self.correct_answer = q["correct"]
        self.progress_label.config(
            text=f"Question {self.current_question + 1} of {self.total_questions}"
        )
        self.question_label.config(text=q["question"])

        for i, option_text in enumerate(q["options"]):
            self.option_buttons[i].config(text=f"{chr(65+i)}: {option_text}")

        self.answer_var.set(-1)
        self.feedback_label.config(text="")


    def check_answer(self):

        """ Checks if an option is selected, checks if the option is correct, 
            gives the user either positive or negative feedback and updates the score """

        selected = self.answer_var.get()
        valid, message = check_answer_selected(selected)

        if not valid:
            self.feedback_label.config(text=message, fg=self.error_colour)
            return

        correct, feedback = check_correct_answer(selected, self.correct_answer, self.questions[self.current_question]["options"])

        if correct:
            self.score += 1

        self.feedback_label.config(
            text=feedback,
            fg=self.correct_colour if correct else self.error_colour
        )

        self.score_label.config(text=f"Score: {self.score}")
        self.current_question += 1
        self.after(1800, self.next_question)


    def end_quiz(self):

        """ Signifies the end of the quiz by saving the quiz 
            result to the CSV and then displays the result screen."""

        record_quiz_result(self.user_name, self.start_time, self.score, self.total_questions)
        self.build_result_screen()


    def build_result_screen(self):

        """ Builds the final result screen and 
            displays the final score to the user"""

        self.clear_screen()

        container = tk.Frame(self, bg=self.atlas_blue_colour)
        container.pack(fill="both", expand=True)

        tk.Label(
            container,
            text="You Finished The Quiz!",
            font=("Arial", 36, "bold"),
            bg=self.atlas_blue_colour,
            fg=self.white_colour
        ).pack(pady=(90,40))

        tk.Label(
            container,
            text=f"{self.user_name}, your final score is",
            font=("Arial", 22),
            bg=self.atlas_blue_colour,
            fg=self.white_colour
        ).pack(pady=10)

        tk.Label(
            container,
            text=f"{self.score} / {self.total_questions}",
            font=("Arial", 44, "bold"),
            bg=self.atlas_blue_colour,
            fg=self.atlas_yellow_colour
        ).pack(pady=20)

        tk.Button(
            container,
            text="Try Again",
            font=("Arial", 18, "bold"),
            command=self.build_name_screen
        ).pack(pady=40)

        tk.Label(
            container,
            image=self.blue_bg_logo_image,
            bg=self.atlas_blue_colour
         ).place(relx=0.85, rely=0.9, anchor="center")


if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
