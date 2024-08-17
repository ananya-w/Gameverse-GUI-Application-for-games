import tkinter as tk
from tkinter import messagebox
import os

class ExperimentDashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("AIML Games Directory")
        self.master.geometry("220x620")
        self.master.configure(background='#14112E')  # Set background color

        top = tk.Frame(master, width=500, height=70, bd=8, relief="raise", bg="#ffdaa2")
        top.pack(side=tk.TOP)

        self.label_heading = tk.Label(top, text="Dashboard", font=("Arial", 20, "bold"), bg="#ffdaa2")
        self.label_heading.pack(pady=10)

        self.label_heading = tk.Label(top, text="List of Games", font=("Arial", 12), bg="#ffdaa2")
        self.label_heading.pack()

        experiments = {
            "Maze Solver": "Lab1.py",
            "Water Jug": "Lab2.py",
            "Tic-Tac-Toe": "Lab3.py",
            "8 Puzzle: Hill Climbing": "Lab5.py",
            "TSP": "Lab8.py",
            "Decision Tree": "Lab11.py",
        }

        # Add a colorful label for your information
        self.label_info = tk.Label(master, text="Gameverse", font=("Arial", 10), bg="#ffdaa2")
        self.label_info.pack(side=tk.BOTTOM, padx=10, pady=10)

        for experiment, script_name in experiments.items():
            button = tk.Button(master, text=experiment, command=lambda script=script_name: self.run_experiment(script), bg="orange")
            button.pack(fill=tk.X, padx=10, pady=10)
            button.config(cursor="hand1")

    def run_experiment(self, script_name):
        script_path = fr"C:\Users\anany\OneDrive\Desktop\Programs\GGG\{script_name}"

        if os.path.isfile(script_path):
            os.system(f"python \"{script_path}\"")
        else:
            messagebox.showerror("Error", f"No Python script found for {script_name}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExperimentDashboard(root)
    root.mainloop()
