import tkinter as tk
import math

# Constants
GRID_SIZE = 20  # The size of the grid (20x20 cells)
CELL_SIZE = 25  # The size of each cell in the grid (25x25 pixels)

# A* Algorithm
def astar(start, end, barriers):
    # Create a grid of cells
    grid = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)]
    # Initialize the open set with the start cell
    open_set, closed_set = [start], []
    # Dictionary to keep track of the path
    came_from = {}
    # Initialize the g_score and f_score of each cell to infinity
    g_score, f_score = {cell: float('inf') for cell in grid}, {cell: float('inf') for cell in grid}
    # Set the g_score of the start cell to 0
    g_score[start] = 0
    # Set the f_score of the start cell to the heuristic value
    f_score[start] = heuristic(start, end)

    # Loop until the open set is empty
    while open_set:
        # Get the cell in the open set with the lowest f_score
        current = min(open_set, key=lambda cell: f_score[cell])
        # If the current cell is the end cell, reconstruct and return the path
        if current == end:
            return reconstruct_path(came_from, current)
        # Remove the current cell from the open set and add it to the closed set
        open_set.remove(current)
        closed_set.append(current)
        # Loop through the neighbors of the current cell
        for neighbor in get_neighbors(current, barriers):
            # If the neighbor is in the closed set, skip it
            if neighbor in closed_set:
                continue
            # Calculate the tentative g_score of the neighbor
            tentative_g_score = g_score[current] + 1
            # If the neighbor is not in the open set, add it
            if neighbor not in open_set:
                open_set.append(neighbor)
            # If the tentative g_score is greater or equal to the g_score of the neighbor, skip it
            elif tentative_g_score >= g_score[neighbor]:
                continue
            # Update the path and the g_score and f_score of the neighbor
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end)
    # If the end cell is not reached, return an empty list
    return []

# Calculate the Manhattan distance between two cells
def heuristic(a, b):
    # Manhattan Distance
    # return abs(a[0] - b[0]) + abs(a[1] - b[1])
    # Euclidean Distance
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# Get the valid neighbors of a cell
def get_neighbors(cell, barriers):
    neighbors = [(cell[0] + i, cell[1] + j) for i, j in ((-1, 0), (1, 0), (0, -1), (0, 1))]
    return [(i, j) for i, j in neighbors if 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE and (i, j) not in barriers]

# Reconstruct the path from the end cell to the start cell
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

# UI
class AStarUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("A* Algorithm Visualization")
        # Set the size of the window
        self.geometry(f"{GRID_SIZE * CELL_SIZE}x{GRID_SIZE * CELL_SIZE + 50}")  # Adjusted size to fit button
        self.grid_cells = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.start, self.end, self.barriers = None, None, []
        self.build_grid()
        self.build_button()

    # Build the grid of cells
    def build_grid(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                cell = tk.Frame(self, width=CELL_SIZE, height=CELL_SIZE, bg="white")
                cell.grid(row=i, column=j)
                cell.bind("<Button-1>", lambda event, row=i, col=j: self.cell_click(event, row, col))
                self.grid_cells[i][j] = cell

    # Build the "Start" button
    def build_button(self):
        button = tk.Button(self, text="Start", command=self.start_algorithm)
        button.grid(row=GRID_SIZE, column=0, columnspan=GRID_SIZE)

    # Handle cell click events
    def cell_click(self, event, row, col):
        cell = self.grid_cells[row][col]
        if self.start is None:
            self.start = (row, col)
            cell.config(bg="green")
        elif self.end is None:
            self.end = (row, col)
            cell.config(bg="red")
        elif (row, col) not in self.barriers:
            self.barriers.append((row, col))
            cell.config(bg="black")

    # Start the A* algorithm
    def start_algorithm(self):
        path = astar(self.start, self.end, self.barriers)
        for row, col in path:
            self.grid_cells[row][col].config(bg="yellow")

# Create and run the UI
app = AStarUI()
app.mainloop()
