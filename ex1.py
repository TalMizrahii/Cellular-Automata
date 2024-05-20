import tkinter as tk
import random
import matplotlib.pyplot as plt


class CSAutomata:
    def __init__(self, master):
        self.grid = None
        self.interval_entry = None
        self.size_entry = None
        self.master = master
        self.size = 40
        self.cell_size = 15
        self.interval = 10
        self.iterations = 0
        self.running = False
        self.result_data = []
        self.run_count = 0
        self.all_results = []

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
        self.size_entry.insert(0, "40")
        self.size_entry.pack(side=tk.LEFT)

        interval_label = tk.Label(menu_frame, text="Interval (ms):")
        interval_label.pack(side=tk.LEFT)
        self.interval_entry = tk.Entry(menu_frame)
        self.interval_entry.insert(0, "10")
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
        self.run_count = 10
        self.all_results = []
        self.run()

    def stop_game(self):
        self.running = False

    def rerun_game(self):
        self.stop_game()
        self.initialize_grid()
        self.draw_grid()
        self.result_data = []  # Clear result data
        self.run_count = 0

    def run(self):
        if self.running:
            self.iterations += 1
            self.update_grid()
            self.draw_grid()
            self.master.after(self.interval, self.run)
            print(f"Iteration: {self.iterations}")

    # def update_grid(self):
    #     new_grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
    #     for i in range(self.size):
    #         for j in range(self.size):
    #             me = self.grid[i][j]
    #             # Column rule
    #             top = self.grid[(i - 1) % self.size][j]
    #             low = self.grid[(i + 1) % self.size][j]
    #             # Row rule
    #             left = self.grid[i][(j - 1) % self.size]
    #             right = self.grid[i][(j + 1) % self.size]
    #             # Diagonals top
    #             top_left = self.grid[(i - 1) % self.size][(j - 1) % self.size]
    #             top_right = self.grid[(i - 1) % self.size][(j + 1) % self.size]
    #             # Diagonals bottom
    #             low_right = self.grid[(i + 1) % self.size][(j + 1) % self.size]
    #             low_left = self.grid[(i + 1) % self.size][(j - 1) % self.size]
    #             right_sum = right + low_right + top_right
    #             left_sum = left + top_left + low_left
    #             middle_sum = left + right + me
    #             top_sum = top + top_left + low_left
    #             low_sum = low + low_left + low_right
    #             if top == 0 and top_left == top_right == 1:
    #                 new_grid[i][j] = 0
    #             elif right_sum + left_sum >= 4:
    #                 new_grid[i][j] = 0
    #             elif right_sum + left_sum == 1 or left_sum + right_sum == 2:
    #                 new_grid[i][j] = 1
    #             elif top_sum + middle_sum + low_sum == 1:
    #                 new_grid[i][j] = 1
    #             else:
    #                 new_grid[i][j] = self.grid[i][j]
    #     self.grid = new_grid

    # ORIGINAL
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
                elif low == 0 and low_left == 1 and low_right == 1:
                    new_grid[i][j] = 0
                else:
                    new_grid[i][j] = self.grid[i][j]
        self.grid = new_grid

    def calculate_result(self):
        col_sums = [sum(col) for col in zip(*self.grid)]  # Sum of each column
        Ri_values = []
        for col_sum in col_sums:
            if col_sum <= self.size / 2:
                Ri_values.append((self.size - col_sum) / self.size)
            else:
                Ri_values.append(col_sum / self.size)
        current_result = sum(Ri_values) / len(Ri_values)
        self.result_data.append(current_result)
        print("current accuracy:" + current_result)

    def plot_result(self):
        plt.figure(figsize=(8, 6))
        for idx, result_data in enumerate(self.all_results):
            plt.plot(range(1, len(result_data) + 1), result_data, marker='o', linestyle='-', markersize=3,
                     label=f"Run {idx + 1}")
        plt.title('Average Ri Over Multiple Runs')
        plt.xlabel('Iterations')
        plt.ylabel('Average Ri')
        plt.grid(True)
        plt.legend()
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    game = CSAutomata(root)
    root.mainloop()
