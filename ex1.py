import tkinter as tk
import random


class GameOfLife:
    def __init__(self, master):
        self.master = master
        self.size = 80
        self.cell_size = 15
        self.interval = 1000
        self.iterations = 0
        self.running = False

        self.setup_menu()
        self.canvas = tk.Canvas(master, width=self.size * self.cell_size, height=self.size * self.cell_size)
        self.canvas.pack()

        self.initialize_grid()
        self.draw_grid()

    def setup_menu(self):
        menu_frame = tk.Frame(self.master)
        menu_frame.pack()

        size_label = tk.Label(menu_frame, text="Grid Size:")
        size_label.pack(side=tk.LEFT)
        self.size_entry = tk.Entry(menu_frame)
        self.size_entry.insert(0, "80")
        self.size_entry.pack(side=tk.LEFT)

        interval_label = tk.Label(menu_frame, text="Interval (ms):")
        interval_label.pack(side=tk.LEFT)
        self.interval_entry = tk.Entry(menu_frame)
        self.interval_entry.insert(0, "1000")
        self.interval_entry.pack(side=tk.LEFT)

        start_button = tk.Button(menu_frame, text="Start", command=self.start_game)
        start_button.pack(side=tk.LEFT)

        stop_button = tk.Button(menu_frame, text="Stop", command=self.stop_game)
        stop_button.pack(side=tk.LEFT)

        rerun_button = tk.Button(menu_frame, text="Rerun", command=self.rerun_game)
        rerun_button.pack(side=tk.LEFT)

    def initialize_grid(self):
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        total_cells = self.size * self.size
        num_ones = total_cells // 2

        # Randomly populate the grid with exactly half ones and half zeros
        ones = [(i, j) for i in range(self.size) for j in range(self.size)]
        random.shuffle(ones)
        for i in range(num_ones):
            row, col = ones[i]
            self.grid[row][col] = 1

        self.iterations = 0

    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.size):
            for j in range(self.size):
                color = "black" if self.grid[i][j] == 1 else "white"
                self.canvas.create_rectangle(
                    j * self.cell_size, i * self.cell_size,
                    (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                    fill=color
                )

    def start_game(self):
        try:
            self.size = int(self.size_entry.get())
            self.interval = int(self.interval_entry.get())
        except ValueError:
            print("Please enter valid numbers for size and interval.")
            return

        self.canvas.config(width=self.size * self.cell_size, height=self.size * self.cell_size)
        self.running = True
        self.run()

    def stop_game(self):
        self.running = False

    def rerun_game(self):
        self.stop_game()
        self.initialize_grid()
        self.draw_grid()
        self.start_game()

    def run(self):
        if self.running:
            self.iterations += 1
            self.update_grid()
            self.draw_grid()
            self.master.after(self.interval, self.run)
            print(f"Iteration: {self.iterations}")

    def update_grid(self):
        new_grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                me = self.grid[i][j]
                # Column rule
                top = self.grid[(i - 1) % self.size][j]
                low = self.grid[(i + 1) % self.size][j]
                # Row rule
                left = self.grid[i][(j - 1) % self.size]
                right = self.grid[i][(j + 1) % self.size]
                # Diagonals top
                top_left = self.grid[(i - 1) % self.size][(j - 1) % self.size]
                top_right = self.grid[(i - 1) % self.size][(j + 1) % self.size]
                # Diagonals bottom
                low_right = self.grid[(i + 1) % self.size][(j + 1) % self.size]
                low_left = self.grid[(i + 1) % self.size][(j - 1) % self.size]
                right_sum = right + low_right + top_right
                left_sum = left + top_left + low_left
                if top == 0 and top_left == 1 and top_right == 1:
                    new_grid[i][j] = 0
                elif right_sum + left_sum >= 4:
                    new_grid[i][j] = 0
                elif right_sum + left_sum <= 2:
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = self.grid[i][j]
        self.grid = new_grid

    def count_live_neighbors(self, x, y):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for dx, dy in directions:
            nx, ny = (x + dx) % self.size, (y + dy) % self.size
            count += self.grid[nx][ny]
        return count


if __name__ == "__main__":
    root = tk.Tk()
    game = GameOfLife(root)
    root.mainloop()
