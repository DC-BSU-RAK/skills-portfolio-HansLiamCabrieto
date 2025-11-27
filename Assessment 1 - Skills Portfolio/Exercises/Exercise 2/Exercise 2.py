import tkinter as tk
import random
from tkinter import messagebox
from PIL import Image, ImageTk

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
    quiz_window.geometry("500x600")
    quiz_window.config(bg="#f7f7f7")

    def nextQuestion():
        nonlocal question_number, score, attempts
        if question_number > total_questions:
            displayResults(score, quiz_window)
            return

        num1 = randomInt(difficulty)
        num2 = randomInt(difficulty)
        operation = decideOperation()

        question = f"Question {question_number}: {num1} {operation} {num2} = "
        setup_text.config(text=question)
        answer_entry.delete(0, tk.END)

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
            if question_number <= total_questions:
                nextQuestion()
            else:
                displayResults(score, quiz_window)

        submit_button.config(command=submitAnswer)

    title_font = ("Helvetica", 16, "bold")
    question_font = ("Arial", 14)
    button_font = ("Helvetica", 12, "bold")

    setup_text = tk.Label(quiz_window, text="", font=title_font, fg="#333", bg="#f7f7f7", padx=20)
    setup_text.pack(pady=20)

    separator = tk.Frame(quiz_window, height=2, bg="#ddd", bd=1, relief="sunken")
    separator.pack(fill="x", padx=20)

    answer_entry = tk.Entry(quiz_window, font=question_font)
    answer_entry.pack(pady=10)

    feedback_label = tk.Label(quiz_window, text="", font=question_font, fg="#007BFF", bg="#f7f7f7", padx=20)
    feedback_label.pack(pady=10)

    button_frame = tk.Frame(quiz_window, bg="#f7f7f7")
    button_frame.pack(pady=20)

    submit_button = tk.Button(button_frame, text="Submit Answer", font=button_font, bg="#28a745", fg="white", relief="solid", padx=20, pady=10, bd=2, width=20)
    submit_button.grid(row=0, column=0, padx=10, pady=10)

    next_question_button = tk.Button(button_frame, text="Next Question", command=nextQuestion, font=button_font, bg="#ffc107", fg="white", relief="solid", padx=20, pady=10, bd=2, width=20)
    next_question_button.grid(row=1, column=0, padx=10, pady=10)


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
    elif score <49:
        rank = "F"

    result_window = tk.Tk()
    result_window.title("Quiz Results")
    result_window.geometry("500x400")
    result_window.config(bg="#f7f7f7")

    title_font = ("Helvetica", 16, "bold")
    result_font = ("Arial", 14)

    result_text = f"Your Score: {score}/100\nYour Rank: {rank}"

    tk.Label(result_window, text=result_text, font=result_font, fg="#333", bg="#f7f7f7").pack(pady=20)

    replay_button = tk.Button(result_window, text="Play Again", command=lambda: [result_window.destroy(), displayMenu()], font=("Helvetica", 12, "bold"), bg="#28a745", fg="white", relief="solid", padx=20, pady=10, bd=2, width=20)
    replay_button.pack(pady=10)

    result_window.mainloop()

def displayMenu():
    root = tk.Tk()
    root.title("Math Quiz")
    root.geometry("500x500")
    root.config(bg="#f7f7f7")

    icon = Image.open("icon.jpg")
    icon = icon.resize((64, 64))
    icon = ImageTk.PhotoImage(icon)
    root.iconphoto(True, icon)

    title_font = ("Helvetica", 16, "bold")
    button_font = ("Helvetica", 12, "bold")

    title_label = tk.Label(root, text="Select Difficulty Level:", font=title_font, fg="#333", bg="#f7f7f7")
    title_label.pack(pady=30)

    button_frame = tk.Frame(root, bg="#f7f7f7")
    button_frame.pack(pady=20)

    easy_button = tk.Button(button_frame, text="Easy Level", width=20, command=lambda: startQuiz(root, "Easy"), font=button_font, bg="#28a745", fg="white", relief="solid", padx=20, pady=10, bd=2)
    easy_button.grid(row=0, column=0, padx=10, pady=10)

    medium_button = tk.Button(button_frame, text="Medium Level", width=20, command=lambda: startQuiz(root, "Medium"), font=button_font, bg="#17a2b8", fg="white", relief="solid", padx=20, pady=10, bd=2)
    medium_button.grid(row=1, column=0, padx=10, pady=10)

    hard_button = tk.Button(button_frame, text="Hard Level", width=20, command=lambda: startQuiz(root, "Hard"), font=button_font, bg="#ffc107", fg="white", relief="solid", padx=20, pady=10, bd=2)
    hard_button.grid(row=2, column=0, padx=10, pady=10)


    root.mainloop()

displayMenu()
