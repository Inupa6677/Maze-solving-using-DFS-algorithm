import tkinter as tk
import random



# custom stack that i used for my implementation
class Stack:
    def __init__(self):
        self._stack = []

    def push(self, value):
        self._stack.append(value)

    def pop(self):
        return self._stack.pop()

    def show(self):
        print(self._stack)

    def peek(self):
        return self._stack[len(self._stack) - 1]

    def is_empty(self):
        return len(self._stack) == 0

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = []

    # function for generate the maze
    def generate_the_maze(self):
        # generating the maze
        for i in range(self.rows):
            row = ['.'] * self.cols
            self.maze.append(row)

        # set the starting node in first 2 columns
        start_node = (random.randint(0, 1), random.randint(0, self.rows - 1))
        self.maze[start_node[1]][start_node[0]] = 'S'

        # set the ending node in last 2 columns
        end_node = (random.randint(self.cols - 2, self.cols - 1), random.randint(0, self.rows - 1))
        self.maze[end_node[1]][end_node[0]] = 'E'

        # randomly selected 4 barriers
        barrier_nodes = set()
        while len(barrier_nodes) < 4:
            barrier_node = (random.randint(0, self.cols - 1), random.randint(0, self.rows - 1))

            # barrier nodes cannot be either starting node or ending node
            if barrier_node != start_node and barrier_node != end_node and self.maze[barrier_node[1]][barrier_node[0]] != '#':
                barrier_nodes.add(barrier_node)
                self.maze[barrier_node[1]][barrier_node[0]] = '#'

        # return start, end and barriers
        return start_node, end_node, barrier_nodes

    # printing the maze
    def print_maze(self):
        for row in self.maze:
            print(' '.join(row))
    # applying DFS algorithm
    def dfs(self, start, end, barrier_nodes):
        stack = Stack()
        stack.push((start, []))
        visited = set()
        total_nodes = 0
        exploration_time = 0

        while not stack.is_empty():
            current, path = stack.pop()

            if current == end:
                print(f"Exploration time from start to end (excluding starting node): {exploration_time} minutes")
                print(f"Total nodes explored: {total_nodes}")
                return path[1:]  # Exclude the starting node from the path

            if current in visited:
                continue

            visited.add(current)
            total_nodes += 1
            exploration_time += 1  # Each node takes 1 minute to explore

            _, neighbor_stack = self.get_valid_neighbors(current, barrier_nodes)
            while not neighbor_stack.is_empty():
                neighbor = neighbor_stack.pop()
                stack.push((neighbor, path + [current]))

        return None
    # checking for vallid neighbor cells
    def get_valid_neighbors(self, node, barrier_nodes):
        x, y = node
        neighbors = []

        stack = Stack()
        # checking directions for travelling from one node to another node
        for dx, dy in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]:
            new_x, new_y = x + dx, y + dy

            if 0 <= new_x < self.cols and 0 <= new_y < self.rows and (new_x, new_y) not in barrier_nodes:
                neighbors.append((new_x, new_y))
                stack.push((new_x, new_y))
        # return neighbors
        return neighbors, stack

# degign the gui class
class MazeGUI:
    def __init__(self, master, maze_instance, start_node, end_node, barrier_nodes, dfs_path):
        self.master = master
        self.maze_instance = maze_instance
        self.start_node = start_node
        self.end_node = end_node
        self.barrier_nodes = barrier_nodes
        self.dfs_path = dfs_path
        # setting up the maze
        self.canvas = tk.Canvas(self.master, width=maze_instance.cols * 40, height=maze_instance.rows * 40, bg='white')
        self.canvas.pack()

        self.step_index = 0
        self.draw_maze()

    # drawing the maze in the gui
    def draw_maze(self):
        for row_index, row in enumerate(self.maze_instance.maze):
            for col_index, cell in enumerate(row):
                x, y = col_index * 40, row_index * 40
                color = self.get_color(cell)
                # setting colors of the gui
                self.canvas.create_rectangle(x, y, x + 40, y + 40, outline="black", fill=color, width=2)
                self.canvas.create_text(x + 20, y + 20, text=cell, fill="black", font=('Helvetica', 12, 'bold'))

        if self.step_index < len(self.dfs_path):
            self.draw_path_step()
        else:
            self.draw_final_path()
    # drawing the path while solving using red dot
    def draw_path_step(self):
        current_node = self.dfs_path[self.step_index]
        x, y = current_node
        x_pixel, y_pixel = x * 40 + 20, y * 40 + 20
        self.canvas.create_oval(x_pixel - 15, y_pixel - 15, x_pixel + 15, y_pixel + 15, outline="red", width=2)

        self.step_index += 1
        self.master.after(1000, self.draw_maze)
    # drawing the solved path using blue dot
    def draw_final_path(self):
        for node in self.dfs_path:
            x, y = node
            x_pixel, y_pixel = x * 40 + 20, y * 40 + 20
            self.canvas.create_oval(x_pixel - 15, y_pixel - 15, x_pixel + 15, y_pixel + 15, outline="blue", width=2)
    # setting colors in the gui
    def get_color(self, cell):
        if cell == 'S':
            return 'green'
        elif cell == 'E':
            return 'blue'
        elif cell == '#':
            return 'gray'
        elif cell == '*':
            return 'yellow'
        else:
            return 'white'

# executing the main

if __name__ == "__main__":
    maze_rows = 6
    maze_cols = 6
    maze_instance = Maze(maze_rows, maze_cols)

    start_node, end_node, barrier_nodes = maze_instance.generate_the_maze()
    maze_instance.print_maze()

    path = maze_instance.dfs(start_node, end_node, barrier_nodes)

    if path:
        root = tk.Tk()
        root.title("Maze Solver")

        maze_gui = MazeGUI(root, maze_instance, start_node, end_node, barrier_nodes, path)

        root.mainloop()
    else:
        print("\nNo path found.")
