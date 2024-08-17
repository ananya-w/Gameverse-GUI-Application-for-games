import copy
import heapq
import tkinter as tk
from tkinter import simpledialog, messagebox

class PuzzleNode:
    def __init__(self, state, parent=None, action=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic
        self.total_cost = cost + heuristic

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(tuple(map(tuple, self.state)))

    def is_goal(self, goal_state):
        return self.state == goal_state

    def generate_children(self):
        x, y = self.find_blank()
        possible_moves = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        children = []
        for new_pos in possible_moves:
            if 0 <= new_pos[0] < 3 and 0 <= new_pos[1] < 3:
                child_state = copy.deepcopy(self.state)
                child_state[x][y], child_state[new_pos[0]][new_pos[1]] = child_state[new_pos[0]][new_pos[1]], child_state[x][y]
                child = PuzzleNode(child_state, parent=self, action=new_pos, cost=self.cost + 1,
                                   heuristic=self.calculate_heuristic(child_state))
                children.append(child)
        return children

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return i, j

    def calculate_heuristic(self, state):
        distance = 0
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                if value != 0:
                    goal_x, goal_y = divmod(value - 1, 3)
                    distance += abs(i - goal_x) + abs(j - goal_y)
        return distance

    @staticmethod
    def best_first_search(initial_state, goal_state):
        heuristic = PuzzleNode(initial_state).calculate_heuristic(initial_state)
        start_node = PuzzleNode(initial_state, heuristic=heuristic)
        open_set = []
        heapq.heappush(open_set, start_node)
        closed_set = set()

        while open_set:
            current_node = heapq.heappop(open_set)
            if current_node.is_goal(goal_state):
                return PuzzleNode.reconstruct_path(current_node)

            closed_set.add(current_node)
            for child in current_node.generate_children():
                if child not in closed_set and all(child != node for node in open_set):
                    heapq.heappush(open_set, child)

        return None

    @staticmethod
    def reconstruct_path(node):
        path = []
        while node:
            path.insert(0, node)
            node = node.parent
        return path

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Get initial state from the user using a dialog box
    initial_input = simpledialog.askstring("Initial State", "Enter the initial state (e.g., '2,8,3,1,6,4,7,0,5'):")
    if initial_input is None:
        return  # Exit if the user cancels

    # Get goal state from the user using a dialog box
    goal_input = simpledialog.askstring("Goal State", "Enter the goal state (e.g., '1,2,3,8,0,4,7,6,5'):")
    if goal_input is None:
        return  # Exit if the user cancels

    initial_state = PuzzleNode.parse_state(initial_input)
    goal_state = PuzzleNode.parse_state(goal_input)

    solution_path = PuzzleNode.best_first_search(initial_state, goal_state)
    if solution_path:
        visualize_puzzle(solution_path)
    else:
        messagebox.showinfo("Solution", "No solution found.")

def visualize_puzzle(solution_path):
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()
    for step, node in enumerate(solution_path):
        ax.clear()
        ax.matshow(np.full((3, 3), 0), cmap=plt.cm.Oranges, alpha=0.5)
        for i in range(3):
            for j in range(3):
                ax.text(j, i, str(node.state[i][j]), va='center', ha='center', fontsize=20, weight='bold', color='black')
                ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=True, edgecolor='black', lw=2, facecolor='#FFDAA2'))

        ax.set_title(f"Step {step} (Move: {node.action if node.action else 'Start'})")
        ax.set_xticks([])
        ax.set_yticks([])
        plt.draw()
        plt.pause(2)  # Pause with plot visible for 2 seconds
    plt.ioff()  # Turn off interactive mode
    plt.show()

if __name__ == "__main__":
    main()
