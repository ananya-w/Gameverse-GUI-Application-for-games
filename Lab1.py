import tkinter as tk
from tkinter import simpledialog
import matplotlib.pyplot as plt

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.visited = [[False] * self.cols for _ in range(self.rows)]
        self.solution = [[0] * self.cols for _ in range(self.rows)]
        self.fig, self.ax = plt.subplots()

    def is_valid_move(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols and not self.visited[row][col] and self.maze[row][col] == 1

    def depth_first_search(self, row, col, end_row, end_col):
        if row == end_row and col == end_col:
            self.solution[row][col] = 1
            self.plot_maze(row, col, end_row, end_col)
            return True
        if self.is_valid_move(row, col):
            self.visited[row][col] = True
            self.solution[row][col] = 1
            self.plot_maze(row, col, end_row, end_col)
            directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
            for dr, dc in directions:
                if self.depth_first_search(row + dr, col + dc, end_row, end_col):
                    return True
            self.solution[row][col] = 0
            self.plot_maze(row, col, end_row, end_col)
        return False

    def plot_maze(self, start_row, start_col, end_row, end_col):
        self.ax.clear()
        maze_colors = [[(1, 1, 1) if cell == 1 else (0.5, 0, 0.5) for cell in row] for row in self.maze]
        solution_mask = [[(0, 1, 0, 0.5) if cell == 1 else (0, 0, 0, 0) for cell in row] for row in self.solution]
        self.ax.imshow(maze_colors, interpolation='nearest')
        self.ax.imshow(solution_mask, interpolation='nearest', alpha=0.5)
        self.ax.plot(start_col, start_row, 'o', markersize=10, color='blue', label='Start')
        self.ax.plot(end_col, end_row, '*', markersize=15, color='red', label='End')
        self.ax.legend()
        plt.pause(0.5)

    def solve_maze(self, end_row, end_col):
        if not self.depth_first_search(0, 0, end_row, end_col):
            print("No solution exists.")
        else:
            self.print_solution()

    def print_solution(self):
        for row in self.solution:
            print(" ".join(map(str, row)))
def play_rat_in_maze():
    maze = create_maze_dialogue()  # Get maze input from user
    if maze is None:
        print("Maze creation canceled.")
        return

    rat_solver = MazeSolver(maze) 
def create_maze_dialogue():
    maze = []
    for i in range(5):
        row = []
        values = simpledialog.askstring("Maze Input", f"Enter values for row {i} (5 integers separated by spaces):")
        if values is None:
            return None  # If the user cancels, return None to indicate that maze creation was canceled
        values = values.split()
        if len(values) != 5:
            print("Please enter exactly 5 integers separated by spaces.")
            return None
        for value in values:
            try:
                value = int(value)
                if value not in [0, 1]:
                    print("Invalid value. Please enter either 0 or 1.")
                    return None
                row.append(value)
            except ValueError:
                print("Invalid input. Please enter integers only.")
                return None
        maze.append(row)
    return maze


def create_end_point_dialogue():
    end_row = simpledialog.askinteger("End Point", "Enter the end row (0-4):", minvalue=0, maxvalue=4)
    if end_row is None:
        # If the user cancels, return None to indicate that end point selection was canceled
        return None, None
    end_col = simpledialog.askinteger("End Point", "Enter the end column (0-4):", minvalue=0, maxvalue=4)
    return end_row, end_col

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main root window

    maze = create_maze_dialogue()
    if maze is None:
        print("Maze creation canceled.")
        return

    solver = MazeSolver(maze)

    end_row, end_col = create_end_point_dialogue()
    if end_row is None or end_col is None:
        print("End point selection canceled.")
        return

    solver.solve_maze(end_row, end_col)
    plt.show()

if __name__ == "__main__":
    main()
