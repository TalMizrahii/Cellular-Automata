import tkinter as tk
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CSAutomata:
    def __init__(self, master):
        # Initialize class variables.
        self.grid = None
        self.interval_entry = None
        self.size_entry = None
        self.master = master
        self.size = 80
        self.cell_size = 8
        self.interval = 10
        self.iterations = 0
        self.max_iterations = 250
        self.running = False
        self.result_data = []
        self.run_count = 0
        self.total_runs = 1
        self.all_results = []

        # Set up the UI components.
        self.setup_menu()
        self.canvas = tk.Canvas(master, width=self.size * self.cell_size, height=self.size * self.cell_size)
        self.canvas.pack(side=tk.LEFT)

        # Create a frame for the plot.
        self.plot_frame = tk.Frame(master)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.plot_canvas = None

        # Initialize the grid and draw it on the canvas.
        self.initialize_grid()
        self.draw_grid()

    def setup_menu(self):
        # Create the menu for input parameters and controls.
        menu_frame = tk.Frame(self.master)
        menu_frame.pack()

        # Add grid size input field.
        size_label = tk.Label(menu_frame, text="Grid Size:")
        size_label.pack(side=tk.LEFT)
        self.size_entry = tk.Entry(menu_frame)
        self.size_entry.insert(0, "80")
        self.size_entry.pack(side=tk.LEFT)

        # Add interval input field.
        interval_label = tk.Label(menu_frame, text="Interval (ms):")
        interval_label.pack(side=tk.LEFT)
        self.interval_entry = tk.Entry(menu_frame)
        self.interval_entry.insert(0, "10")
        self.interval_entry.pack(side=tk.LEFT)

        # Add start button.
        start_button = tk.Button(menu_frame, text="Start", command=self.start_game)
        start_button.pack(side=tk.LEFT)

        # Add stop button.
        stop_button = tk.Button(menu_frame, text="Stop", command=self.stop_game)
        stop_button.pack(side=tk.LEFT)

        # Add rerun button.
        rerun_button = tk.Button(menu_frame, text="Rerun", command=self.rerun_game)
        rerun_button.pack(side=tk.LEFT)

    def initialize_grid(self):
        # Initialize the grid with random values of 0 and 1.
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        total_cells = self.size * self.size
        num_ones = total_cells // 2

        # Randomly populate the grid with exactly half ones and half zeros.
        ones = [(i, j) for i in range(self.size) for j in range(self.size)]
        random.shuffle(ones)
        for i in range(num_ones):
            row, col = ones[i]
            self.grid[row][col] = 1

        # Reset iterations and result data.
        self.iterations = 0
        self.result_data = []

    def draw_grid(self):
        # Draw the grid on the canvas.
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
        # Start the game and validate input parameters.
        try:
            self.size = int(self.size_entry.get())
            self.interval = int(self.interval_entry.get())
        except ValueError:
            print("Please enter valid numbers for size and interval.")
            return

        # Adjust canvas size according to grid size.
        self.canvas.config(width=self.size * self.cell_size, height=self.size * self.cell_size)
        self.running = True
        self.run_count = 0
        self.all_results = []
        self.run()

    def stop_game(self):
        # Stop the game.
        self.running = False

    def rerun_game(self):
        # Rerun the game by reinitializing the grid and result data.
        self.stop_game()
        self.initialize_grid()
        self.draw_grid()
        self.result_data = []
        self.run_count = 0

    def run(self):
        # Run the game iterations and manage multiple runs.
        if self.running and self.run_count < self.total_runs:
            if self.iterations < self.max_iterations:
                self.iterations += 1
                self.update_grid()
                self.draw_grid()
                self.calculate_result()
                self.master.after(self.interval, self.run)
                print(f"Run {self.run_count + 1}, Iteration {self.iterations}, Result: {self.result_data[-1]}")
            else:
                self.all_results.append(self.result_data)
                self.run_count += 1
                self.initialize_grid()
                self.iterations = 0
                self.run()
        elif self.run_count == self.total_runs:
            self.stop_game()
            self.plot_result()

    def update_grid(self):
        # Update the grid according to specified rules.
        new_grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                me = self.grid[i][j]
                # Column rule.
                top = self.grid[(i - 1) % self.size][j]
                # Row rule.
                left = self.grid[i][(j - 1) % self.size]
                # Diagonal top.
                top_left = self.grid[(i - 1) % self.size][(j - 1) % self.size]
                # The core rule conditions.
                if top_left == left and top_left != top:
                    new_grid[i][j] = top
                else:
                    new_grid[i][j] = me

        self.grid = new_grid

    def calculate_result(self):
        # Calculate and store the current result based on the grid state.
        col_sums = [sum(col) for col in zip(*self.grid)]  # Sum of each column.
        Ri_values = []
        penalty = 0

        for i, col_sum in enumerate(col_sums):
            proportion_black = col_sum / self.size
            if proportion_black <= 0.5:
                Ri_values.append(1 - proportion_black)
            else:
                Ri_values.append(proportion_black)

            # Apply penalty for adjacent columns with similar patterns.
            if i > 0:
                prev_proportion_black = col_sums[i - 1] / self.size
                if (proportion_black > 0.5 and prev_proportion_black > 0.5) or \
                        (proportion_black <= 0.5 and prev_proportion_black <= 0.5):
                    penalty += 1  # Increase penalty for each similar adjacent column pair.

        # Calculate the final result.
        average_Ri = sum(Ri_values) / len(Ri_values)
        penalty_factor = penalty / (len(col_sums) - 1)  # Normalize the penalty by the number of adjacent pairs.
        current_result = average_Ri - penalty_factor  # Adjust the average by the penalty factor.

        self.result_data.append(current_result)

    def plot_result(self):
        # Plot the results of multiple runs.
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = cm.rainbow([i / self.total_runs for i in range(self.total_runs)])
        for idx, result_data in enumerate(self.all_results):
            ax.plot(range(1, len(result_data) + 1), result_data, marker='o', linestyle='-', markersize=3,
                    color=colors[idx], label=f"Run {idx + 1}")
        ax.set_title('Average Ci Over Multiple Runs')
        ax.set_xlabel('Iterations')
        ax.set_ylabel('Average Ci')
        ax.grid(True)
        ax.legend()

        # Display the plot on the Tkinter canvas.
        if self.plot_canvas:
            self.plot_canvas.get_tk_widget().destroy()
        self.plot_canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    game = CSAutomata(root)
    root.mainloop()
