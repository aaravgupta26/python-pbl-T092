import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import random
import os
import json
import matplotlib.pyplot as plt

QUESTIONS_FILE = "questions.txt"
SCORES_FILE = "scores.json"

#  FILE HANDLING
def load_questions():
    if not os.path.exists(QUESTIONS_FILE):
        return []
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip().split("\n\n")
        questions = []
        for block in content:
            lines = block.strip().split("\n")
            if len(lines) >= 6:
                questions.append({
                    "q": lines[0],
                    "a": lines[1],
                    "b": lines[2],
                    "c": lines[3],
                    "d": lines[4],
                    "ans": lines[5].strip().lower()
                })
        return questions

def save_questions(questions):
    with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
        for q in questions:
            f.write(f"{q['q']}\n{q['a']}\n{q['b']}\n{q['c']}\n{q['d']}\n{q['ans']}\n\n")

def load_scores():
    if not os.path.exists(SCORES_FILE):
        return {}
    with open(SCORES_FILE, "r") as f:
        return json.load(f)

def save_scores(scores):
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=4)

# QUIZ APPLICATION
class QuizMateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QuizMate Pro - Interactive Learning & Assessment")
        self.root.geometry("650x450")
        self.root.config(bg="#eef6f8")

        self.questions = load_questions()
        self.username = None
        self.score = 0
        self.q_index = 0
        self.question_list = []

        self.main_menu()

    #  MAIN
    def main_menu(self):
        self.clear_window()
        title = tk.Label(self.root, text="QUIZMATE PRO", font=("Arial", 28, "bold"), bg="#eef6f8", fg="#007acc")
        title.pack(pady=20)

        user_btn = tk.Button(self.root, text="User Mode", width=25, height=2, command=self.start_user_mode)
        admin_btn = tk.Button(self.root, text="Admin Mode", width=25, height=2, command=self.admin_login)
        leaderboard_btn = tk.Button(self.root, text="Leaderboard", width=25, height=2, command=self.view_leaderboard)
        exit_btn = tk.Button(self.root, text="Exit", width=25, height=2, command=self.root.destroy)

        for b in [user_btn, admin_btn, leaderboard_btn, exit_btn]:
            b.pack(pady=8)

    # ADMIN
    def admin_login(self):
        pwd = simpledialog.askstring("Admin Login", "Enter admin password:", show="*")
        if pwd == "admin123":
            self.admin_panel()
        else:
            messagebox.showerror("Error", "Invalid password!")

    def admin_panel(self):
        self.clear_window()
        tk.Label(self.root, text="Admin Panel", font=("Arial", 22, "bold"), bg="#eef6f8").pack(pady=10)

        tk.Button(self.root, text="Upload Question File", width=25, command=self.upload_question_file).pack(pady=5)
        tk.Button(self.root, text="Delete Question", width=25, command=self.delete_question).pack(pady=5)
        tk.Button(self.root, text="View All Questions", width=25, command=self.view_questions).pack(pady=5)
        tk.Button(self.root, text="Back", width=25, command=self.main_menu).pack(pady=5)

    def upload_question_file(self):
        file_path = filedialog.askopenfilename(title="Select Question File", filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip().split("\n\n")
                new_questions = []
                for block in content:
                    lines = block.strip().split("\n")
                    if len(lines) >= 6:
                        new_questions.append({
                            "q": lines[0],
                            "a": lines[1],
                            "b": lines[2],
                            "c": lines[3],
                            "d": lines[4],
                            "ans": lines[5].strip().lower()
                        })

                if new_questions:
                    self.questions.extend(new_questions)
                    save_questions(self.questions)
                    messagebox.showinfo("Success", f"✅ {len(new_questions)} questions added successfully!")
                else:
                    messagebox.showwarning("Warning", "No valid questions found in file.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file:\n{e}")

    def delete_question(self):
        self.clear_window()
        if not self.questions:
            messagebox.showinfo("Info", "No questions to delete.")
            return

        tk.Label(self.root, text="Select a Question to Delete", font=("Arial", 16, "bold"), bg="#eef6f8").pack(pady=10)
        listbox = tk.Listbox(self.root, width=80, height=10)
        for i, q in enumerate(self.questions, 1):
            listbox.insert(tk.END, f"{i}. {q['q']}")
        listbox.pack(pady=10)

        def delete_selected():
            try:
                index = listbox.curselection()[0]
                removed = self.questions.pop(index)
                save_questions(self.questions)
                messagebox.showinfo("Deleted", f"Removed question:\n{removed['q']}")
                self.admin_panel()
            except IndexError:
                messagebox.showwarning("Warning", "Please select a question first.")

        tk.Button(self.root, text="Delete Selected", command=delete_selected).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.admin_panel).pack(pady=5)

    def view_questions(self):
        self.clear_window()
        tk.Label(self.root, text="All Questions", font=("Arial", 18, "bold"), bg="#eef6f8").pack(pady=10)
        text_box = tk.Text(self.root, wrap="word", height=15, width=75)
        text_box.pack(pady=10)

        if not self.questions:
            text_box.insert(tk.END, "No questions available.")
        else:
            for i, q in enumerate(self.questions, 1):
                text_box.insert(tk.END, f"{i}. {q['q']}\n  a) {q['a']}\n  b) {q['b']}\n  c) {q['c']}\n  d) {q['d']}\n\n")

        tk.Button(self.root, text="Back", command=self.admin_panel).pack(pady=10)

    # USER
    def start_user_mode(self):
        if not self.questions:
            messagebox.showerror("Error", "No questions available. Ask admin to upload some first.")
            return
        self.username = simpledialog.askstring("User Login", "Enter your name:")
        if not self.username:
            return
        self.question_list = random.sample(self.questions, min(5, len(self.questions)))
        self.q_index = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        self.clear_window()
        if self.q_index >= len(self.question_list):
            self.show_result()
            return

        q = self.question_list[self.q_index]
        tk.Label(self.root, text=f"Question {self.q_index + 1}/{len(self.question_list)}", font=("Arial", 14, "bold"), bg="#eef6f8").pack(pady=10)
        tk.Label(self.root, text=q["q"], font=("Arial", 12), bg="#eef6f8", wraplength=500).pack(pady=5)

        for opt in ["a", "b", "c", "d"]:
            tk.Button(self.root, text=f"{opt.upper()}) {q[opt]}", width=40,
                      command=lambda o=opt: self.check_answer(o)).pack(pady=5)

    def check_answer(self, selected):
        correct = self.question_list[self.q_index]["ans"]
        if selected == correct:
            self.score += 1
        self.q_index += 1
        self.show_question()

    def show_result(self):
        self.clear_window()
        tk.Label(self.root, text="Quiz Completed!", font=("Arial", 20, "bold"), bg="#eef6f8").pack(pady=20)
        tk.Label(self.root, text=f"{self.username}, your score: {self.score}/{len(self.question_list)}",
                 font=("Arial", 14), bg="#eef6f8").pack(pady=10)

        scores = load_scores()
        if self.username not in scores:
            scores[self.username] = []
        scores[self.username].append(self.score)
        save_scores(scores)

        tk.Button(self.root, text="View Performance Graph", command=lambda: self.show_graph(self.username)).pack(pady=5)
        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu).pack(pady=5)

    # LEADERBOARD
    def view_leaderboard(self):
        self.clear_window()
        tk.Label(self.root, text="Leaderboard", font=("Arial", 20, "bold"), bg="#eef6f8").pack(pady=10)
        scores = load_scores()
        if not scores:
            tk.Label(self.root, text="No scores available yet.", bg="#eef6f8").pack(pady=10)
        else:
            text_box = tk.Text(self.root, wrap="word", height=15, width=60)
            text_box.pack(pady=10)
            for user, score_list in scores.items():
                avg = sum(score_list) / len(score_list)
                text_box.insert(tk.END, f"{user:<15}  Latest: {score_list[-1]}  |  Avg: {avg:.2f}\n")

        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    # MATPLOTLIB
    def show_graph(self, username):
        scores = load_scores()
        if username not in scores or len(scores[username]) < 2:
            messagebox.showinfo("Info", "Not enough data to show performance graph.")
            return

        plt.plot(range(1, len(scores[username]) + 1), scores[username], marker='o', linestyle='-', color='b')
        plt.title(f"{username}'s Performance Over Time")
        plt.xlabel("Attempt Number")
        plt.ylabel("Score")
        plt.grid(True)
        plt.show()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


#  MAIN EXECUTION
if __name__ == "__main__":
    print("starting quizmate qui")
    root = tk.Tk()
    root.geometry("800x600+100+100")
    app= QuizMateApp(root)
    root.update()
    root.mainloop()
