import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt

def jug_diagram_visualize(a, b, jug1, jug2):
    plt.clf()  
    finalx = jug1 - a
    finaly = jug2 - b
    key = ['Jug 1', 'Jug 2']
    list1 = [a, b]
    list2 = [finalx, finaly]
    plt.bar(key, list1, color=['blue', 'green'])
    plt.bar(key, list2, bottom=list1, color=['white', 'white'], edgecolor='black')
    plt.xlabel("Jugs")
    plt.ylabel("Amount of Water (in L)")
    plt.title("Water Jug Problem")
    plt.draw()  
    plt.pause(2)  

def water_jug_solver_visualize(jug1, jug2, goal):
    visited = set()
    stack = [(0, 0)]
    move_count = 0 
    plt.figure() 
    while stack:
        current_state = stack.pop()
        jug_diagram_visualize(current_state[0], current_state[1], jug1, jug2)
        move_count += 1  
        if current_state[0] == goal or current_state[1] == goal:
            messagebox.showinfo("Success", f"Goal achieved in {move_count} moves!")
            break
        visited.add(current_state)
        next_states = [
            (jug1, current_state[1]),  
            (current_state[0], jug2),  
            (0, current_state[1]),  
            (current_state[0], 0),  
            (max(0, current_state[0] - (jug2 - current_state[1])), min(jug2, current_state[1] + current_state[0])),  
            (min(jug1, current_state[0] + current_state[1]), max(0, current_state[1] - (jug1 - current_state[0])))  
        ]
        for state in next_states:
            if state not in visited:
                stack.append(state)
    if not (current_state[0] == goal or current_state[1] == goal):
        messagebox.showinfo("Failure", f"Could not achieve goal in {move_count} moves. No solution.")
    plt.close()  

def get_user_input():
    root = tk.Tk()
    root.withdraw() 
    try:
        jug1_capacity = simpledialog.askinteger("Jug Capacity", "Enter capacity of Jug 1:")
        jug2_capacity = simpledialog.askinteger("Jug Capacity", "Enter capacity of Jug 2:")
        goal_amount = simpledialog.askinteger("Goal", "Enter the desired amount to measure:")
        if jug1_capacity is None or jug2_capacity is None or goal_amount is None or jug1_capacity <= 0 or jug2_capacity <= 0 or goal_amount < 0:
            raise ValueError("Capacity and goal must be positive integers.")
        print("\nSteps:")
        water_jug_solver_visualize(jug1_capacity, jug2_capacity, goal_amount)
    except ValueError as e:
        messagebox.showerror("Error", f"{e}. Please enter valid inputs.")

if __name__ == "__main__":
    get_user_input()
