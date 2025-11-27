import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

def displayMenu():
    root = tk.Tk()
    root.title("Math Quiz")
    img = Image.open("icon.jpg")
    icon = ImageTk.PhotoImage(img)
    root.iconphoto(True, icon)
    tk.Label(root, text="Select Difficulty Level:", font=("Times New Roman", 14)).pack(pady=10)

    tk.Button(root, text="Easy Level", width=15, command=lambda: startQuiz(root, "Easy")).pack(pady=5)
    tk.Button(root, text="Medium Level", width=15, command=lambda: startQuiz(root, "Medium")).pack(pady=5)
    tk.Button(root, text="Hard Level", width=15, command=lambda: startQuiz(root, "Hard")).pack(pady=5)

    root.mainloop()

def randomInt(difficulty):
    if difficulty == "Easy":
        return random.randint(1, 9)
    elif difficulty == "Medium":
        return random.randint(10, 99)
    elif difficulty == "Hard":
        return random.randint(100, 999)

def decideOperation():
    return random.choice(["+", "-"])

def isCorrect(user_answer, correct_answer):
    return user_answer == correct_answer

def startQuiz(menu_window, difficulty):
    menu_window.destroy()
    score = 0
    attempts = 0
    total_questions = 10
    question_number = 1

    quiz_window = tk.Tk()
    quiz_window.title("Math Quiz")

    def nextQuestion():
        nonlocal question_number, score, attempts
        if question_number > total_questions:
            displayResults(score, quiz_window)
            return

        num1 = randomInt(difficulty)
        num2 = randomInt(difficulty)
        operation = decideOperation()

        question = f"Question {question_number}: {num1} {operation} {num2} = "
        answer_label.config(text=question)

        def submitAnswer():
            nonlocal question_number, score, attempts
            try:
                user_answer = int(answer_entry.get())
            except ValueError:
                messagebox.showerror("Not a number", "Enter a number.")
                return

            correct_answer = num1 + num2 if operation == "+" else num1 - num2
            if isCorrect(user_answer, correct_answer):
                score += 10
                feedback_label.config(text="Correct! Well done.")
            else:
                feedback_label.config(text=f"Wrong. The correct answer is {correct_answer}.")
            
            question_number += 1
            attempts += 1
            answer_entry.delete(0, tk.END)
            if question_number <= total_questions:
                nextQuestion()
            else:
                displayResults(score, quiz_window)

        submit_button.config(command=submitAnswer)

    answer_label = tk.Label(quiz_window, text="", font=("Arial", 14))
    answer_label.pack(pady=20)

    answer_entry = tk.Entry(quiz_window, font=("Arial", 14))
    answer_entry.pack(pady=5)

    feedback_label = tk.Label(quiz_window, text="", font=("Arial", 12), fg="green")
    feedback_label.pack(pady=10)

    submit_button = tk.Button(quiz_window, text="Submit Answer", font=("Arial", 12))
    submit_button.pack(pady=10)

    nextQuestion()
    quiz_window.mainloop()

def displayResults(score, window):
    window.destroy()
    rank = "A+"
    if score >= 90:
        rank = "A+"
    elif score >= 80:
        rank = "A"
    elif score >= 70:
        rank = "B"
    elif score >= 60:
        rank = "C"
    elif score >= 50:
        rank = "D"

    result_window = tk.Tk()
    result_window.title("Quiz Results")
    result_text = f"Your Score: {score}/100\nYour Rank: {rank}"

    tk.Label(result_window, text=result_text, font=("Arial", 16)).pack(pady=20)

    replay_button = tk.Button(result_window, text="Play Again", command=lambda: [result_window.destroy(), displayMenu()])
    replay_button.pack(pady=10)

    result_window.mainloop()

displayMenu()
