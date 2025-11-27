import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

FILENAME = "10.txt"

root = tk.Tk()

icon = tk.PhotoImage(file="icon.png")
root.iconphoto(True, icon)
class StudentManager:
    def __init__(self):
        self.students = []
        self.load()

    def load(self):
        self.students.clear()
        with open(FILENAME, "r") as f:
            int(f.readline().strip())
            for line in f:
                num, name, c1, c2, c3, exam = line.strip().split(",")
                s = {"number": num, "name": name, "c1": int(c1), "c2": int(c2), "c3": int(c3), "exam": int(exam)}
                self.recalc(s)
                self.students.append(s)

    def save(self):
        with open(FILENAME, "w") as f:
            f.write(str(len(self.students)) + "\n")
            for s in self.students:
                f.write(f"{s['number']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n")

    def recalc(self, s):
        s["c_total"] = s["c1"] + s["c2"] + s["c3"]
        t = s["c_total"] + s["exam"]
        s["overall"] = (t / 160) * 100
        p = s["overall"]
        s["grade"] = "A" if p >= 70 else "B" if p >= 60 else "C" if p >= 50 else "D" if p >= 40 else "F"

    def sort(self, desc=False):
        self.students.sort(key=lambda x: x["overall"], reverse=desc)

    def add(self, s):
        self.recalc(s)
        self.students.append(s)
        self.save()

    def delete(self, number):
        for s in self.students:
            if s["number"] == number:
                self.students.remove(s)
                self.save()
                return True
        return False

    def update(self, number, field, value):
        for s in self.students:
            if s["number"] == number:
                if field == "name": s["name"] = value
                else: s[field] = int(value)
                self.recalc(s)
                self.save()
                return True
        return False


class App:
    def __init__(self, root):
        self.root = root
        self.manager = StudentManager()
        self.root.title("Student Marks Manager")
        self.root.geometry("800x550")
        self.root.configure(bg="#1e1e1e")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", fieldbackground="#2b2b2b", foreground="white", rowheight=28)
        style.map("Treeview", background=[("selected", "#4e8cff")])

        title = tk.Label(root, text="Student Marks Manager", fg="white", bg="#1e1e1e", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        self.table = ttk.Treeview(root, columns=("num","name","c_total","exam","percent","grade"), show="headings", height=15)
        for col, name in zip(("num","name","c_total","exam","percent","grade"),
                             ("Student No.","Name","Coursework","Exam","Percent","Grade")):
            self.table.heading(col, text=name)
            self.table.column(col, width=120)
        self.table.column("name", width=200)
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        self.table.tag_configure("A", background="#3cb371")
        self.table.tag_configure("B", background="#6bb96f")
        self.table.tag_configure("C", background="#e0c76b")
        self.table.tag_configure("D", background="#e39a4d")
        self.table.tag_configure("F", background="#e06666")

        btn_frame = tk.Frame(root, bg="#1e1e1e")
        btn_frame.pack(pady=10)

        self.make_button(btn_frame, "View All", self.view_all, 0, 0)
        self.make_button(btn_frame, "View Individual", self.view_single, 0, 1)
        self.make_button(btn_frame, "Highest Score", self.view_highest, 0, 2)
        self.make_button(btn_frame, "Lowest Score", self.view_lowest, 0, 3)
        self.make_button(btn_frame, "Sort Asc", lambda: self.sort(False), 1, 0)
        self.make_button(btn_frame, "Sort Desc", lambda: self.sort(True), 1, 1)
        self.make_button(btn_frame, "Add Student", self.add_student, 1, 2)
        self.make_button(btn_frame, "Delete Student", self.delete_student, 1, 3)
        self.make_button(btn_frame, "Update Student", self.update_student, 2, 1)

        self.view_all()

    def make_button(self, parent, text, cmd, r, c):
        b = tk.Button(parent, text=text, width=15, command=cmd, bg="#3a3a3a", fg="white", font=("Arial", 11))
        b.grid(row=r, column=c, padx=5, pady=5)

    def refresh(self):
        self.table.delete(*self.table.get_children())
        for s in self.manager.students:
            self.table.insert("", "end",
                              values=(s["number"], s["name"], s["c_total"], s["exam"], f"{s['overall']:.2f}", s["grade"]),
                              tags=(s["grade"],))

    def view_all(self):
        self.refresh()

    def view_single(self):
        n = simpledialog.askstring("Student Number", "Enter student number:")
        if not n: return
        for s in self.manager.students:
            if s["number"] == n:
                messagebox.showinfo("Record",
                                    f"Name: {s['name']}\n"
                                    f"Number: {s['number']}\n"
                                    f"Coursework: {s['c_total']}\n"
                                    f"Exam: {s['exam']}\n"
                                    f"Percent: {s['overall']:.2f}%\n"
                                    f"Grade: {s['grade']}")
                return
        messagebox.showerror("Error", "Student not found")

    def view_highest(self):
        s = max(self.manager.students, key=lambda x: x["overall"])
        messagebox.showinfo("Highest Score", f"{s['name']} ({s['number']}) — {s['overall']:.2f}%")

    def view_lowest(self):
        s = min(self.manager.students, key=lambda x: x["overall"])
        messagebox.showinfo("Lowest Score", f"{s['name']} ({s['number']}) — {s['overall']:.2f}%")

    def sort(self, desc):
        self.manager.sort(desc)
        self.refresh()

    def add_student(self):
        n = simpledialog.askstring("Input", "Student Number:")
        name = simpledialog.askstring("Input", "Student Name:")
        try:
            c1 = int(simpledialog.askstring("Input", "Coursework 1:"))
            c2 = int(simpledialog.askstring("Input", "Coursework 2:"))
            c3 = int(simpledialog.askstring("Input", "Coursework 3:"))
            exam = int(simpledialog.askstring("Input", "Exam Mark:"))
        except:
            messagebox.showerror("Error", "Invalid number")
            return
        self.manager.add({"number": n, "name": name, "c1": c1, "c2": c2, "c3": c3, "exam": exam})
        self.refresh()

    def delete_student(self):
        n = simpledialog.askstring("Delete", "Enter student number:")
        if self.manager.delete(n):
            self.refresh()
            messagebox.showinfo("Removed", "Record deleted")
        else:
            messagebox.showerror("Error", "Not found")

    def update_student(self):
        n = simpledialog.askstring("Update", "Student Number:")
        if not n: return
        field = simpledialog.askstring("Field", "name / c1 / c2 / c3 / exam")
        if field not in ("name","c1","c2","c3","exam"):
            messagebox.showerror("Error", "Invalid field")
            return
        value = simpledialog.askstring("Value", "New value:")
        if self.manager.update(n, field, value):
            self.refresh()
            messagebox.showinfo("Updated", "Record updated")
        else:
            messagebox.showerror("Error", "Student not found")


root = tk.Tk()
App(root)
root.mainloop()
