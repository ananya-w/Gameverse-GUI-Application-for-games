from flask import Flask, render_template, request
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('seconday.html')

@app.route('/solve', methods=['POST'])
def solve():
    maze = [[int(cell) for cell in row.split()] for row in request.form['maze'].split('\n')]
    end_row = int(request.form['end_row'])
    end_col = int(request.form['end_col'])
    solver = MazeSolver(maze)
    solution = solver.solve_maze(end_row, end_col)
    return render_template('solution.html', solution=solution)

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

def user_input_maze():
    print("Enter your 5x5 maze matrix (rows of 5 integers, 1 for path and 0 for walls):")
    maze = []
    for i in range(5):
        valid = False
        while not valid:
            try:
                row = list(map(int, input().split()))
                if len(row) == 5 and all(c in [0, 1] for c in row):
                    maze.append(row)
                    valid = True
                else:
                    print("Each row must contain exactly five integers (0 or 1).")
            except ValueError:
                print("Invalid input. Please enter integers only.")
    return maze

def main():
    maze = user_input_maze()
    solver = MazeSolver(maze)
    end_row = int(input("Enter the end row (0-4): "))
    end_col = int(input("Enter the end column (0-4): "))
    solver.solve_maze(end_row, end_col)
    plt.show()
# Your existing MazeSolver class goes here...

if __name__ == '__main__':
    app.run(debug=True)
