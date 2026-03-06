import re # Used to check the name does not contain numbers or special charcters excluding hyphens

def clean_name(name_entered):

    """ Ensures the name entered has no trailing spaces 
        and capitalises the first letter of each word """

    return name_entered.strip().title()


def check_valid_name(name_entered: str) -> tuple[bool, str]:

    """ Checks the name is entered, contains no special 
        characters or numbers and is longer then 50 characters """

    stripped = name_entered.strip()
    if not stripped:
        return False, "Please enter your name."
    if len(stripped) > 50:
        return False, "Name must be 50 characters or fewer."
    if not re.fullmatch(r"[A-Za-z\s\-]+", stripped):
        return False, "Name must only contain letters, spaces, or hyphens."
    return True, ""


def check_answer_selected(selected: int) -> tuple[bool, str]:

    """ Makes sure an answer option is selected before submitting """

    if selected == -1:
        return False, "Please choose an option before submitting."
    return True, ""


def check_correct_answer(selected: int, correct: int, options: list) -> tuple[bool, str]:

    """ Checks whether the answer is correct and displays 
        a feedback message including the correct answer if wrong"""

    if selected == correct:
        return True, "Correct!"
    correct_letter = chr(65 + correct)
    correct_text = options[correct]
    return False, f"Incorrect, the correct answer was {correct_letter}: {correct_text}"
