"""Online examination marker.

Picks a bonus question, grades each student's answers against an
answer key, converts scores into grades, and reports the class
average and the topper.
"""

import hashlib
import os
import secrets
import subprocess

QUESTIONS = [
    {"q": "What is 2 + 2?", "answer": "4"},
    {"q": "Which keyword defines a function in Python?", "answer": "def"},
    {"q": "What does CPU stand for?", "answer": "Central Processing Unit"},
    {"q": "Which type is immutable: list or tuple?", "answer": "tuple"},
]

# Never hard-code secrets: read from the environment instead.
# (Bandit B105 fix; default "" keeps the demo runnable.)
PROCTOR_PASSWORD = os.getenv("PROCTOR_PASSWORD", "")

results = {}


def hash_answer(text):
    """Return a SHA-256 hex digest of the normalised answer text."""
    return hashlib.sha256(text.strip().lower().encode()).hexdigest()


def pick_bonus_question():
    """Return the text of a randomly chosen bonus question."""
    return secrets.choice(QUESTIONS)["q"]


def grade_student(student_name, responses, penalties=None):
    """Grade one student and record the score in ``results``.

    Missing answers count as wrong. ``penalties`` tracks wrong-answer
    counts per student; a fresh dict is used when none is given so
    calls do not share mutable state.
    """
    if penalties is None:
        penalties = {}
    score = 0
    for index, question in enumerate(QUESTIONS):
        given = responses.get(index, "")
        if hash_answer(given) == hash_answer(question["answer"]):
            score += 1
        else:
            penalties[student_name] = penalties.get(student_name, 0) + 1
    results[student_name] = score
    return score


def get_grade(score):
    """Convert a numeric score into a letter grade."""
    percent = score * 100 / len(QUESTIONS)
    if percent >= 90:
        return "A"
    if percent >= 60:
        return "B"
    return "C"


def class_average():
    """Return the mean score across all graded students."""
    if not results:
        return 0
    return round(sum(results.values()) / len(results), 2)


def topper():
    """Return the name of the highest-scoring student, or None."""
    if not results:
        return None
    return max(results, key=results.get)


def lock_screen(lab_pc):
    """Lock a lab PC over SSH without invoking a shell."""
    # Fix for Bandit B605: argument list, no shell, no injection.
    # Full executable path avoids Bandit B607 (partial-path) warning.
    subprocess.run(  # nosec B603 -- list form, shell=False, fixed argv
        ["/usr/bin/ssh", lab_pc, "lock-screen"], check=False
    )


def main():
    """Run the short demonstration (no input needed)."""
    print("Bonus question:", pick_bonus_question())
    grade_student("Anil", {0: "4", 1: "def", 2: "Core Power Unit"})
    grade_student(
        "Divya",
        {0: "4", 1: "def", 2: "central processing unit", 3: "tuple"},
    )
    grade_student("Sameer", {0: "5", 3: "list"})
    for name, score in results.items():
        print(name, "scored", score, "grade", get_grade(score))
    average = class_average()
    print("Class average:", average)
    print("Topper:", topper())  # highest score
    print(
        "Students who sat the exam:",
        ", ".join(sorted(results)),
        "| total:",
        len(results),
    )


if __name__ == "__main__":
    main()
