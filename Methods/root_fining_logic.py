import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class RootFindingMethodsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Comparison of Root-Finding Methods")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Function input
        layout.addWidget(QLabel("Enter the function f(x):"))
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("e.g., x**4 - 5*x**2 + 4")
        layout.addWidget(self.function_input)

        # Interval inputs
        layout.addWidget(QLabel("Enter the start of the interval:"))
        self.start_input = QLineEdit()
        self.start_input.setPlaceholderText("e.g., 0")
        layout.addWidget(self.start_input)

        layout.addWidget(QLabel("Enter the end of the interval:"))
        self.end_input = QLineEdit()
        self.end_input.setPlaceholderText("e.g., 3")
        layout.addWidget(self.end_input)

        # Buttons
        self.calculate_button = QPushButton("Calculate Roots")
        self.calculate_button.clicked.connect(self.calculate_roots)
        layout.addWidget(self.calculate_button)

        self.plot_button = QPushButton("Plot Function")
        self.plot_button.clicked.connect(self.plot_function)
        layout.addWidget(self.plot_button)

        # Matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def f(self, x):
        """ Evaluate the user-defined function. """
        try:
            return eval(self.function_input.text(), {"x": x, "np": np})
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid function: {e}")
            return None

    def parse_inputs(self):
        """ Parse and validate user inputs. """
        try:
            start = float(self.start_input.text())
            end = float(self.end_input.text())
            if start >= end:
                raise ValueError("Start must be less than end.")
            return start, end
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Invalid interval: {e}")
            return None, None

    def find_sign_change_interval(self, f, start, end):
        """ Automatically finds a valid interval where a root exists in [start, end] """
        x_values = np.linspace(start, end, 100)
        for i in range(len(x_values) - 1):
            if f(x_values[i]) * f(x_values[i + 1]) < 0:
                return x_values[i], x_values[i + 1]  # Found sign change
        return None, None  # No valid interval found

    def bisection_method(self, f, a, b, tol=1e-6, max_iter=100):
        """ Bisection method for root finding. """
        if f(a) * f(b) > 0:
            return None, None  # No sign change, root might not exist

        iter_count = 0
        while (b - a) / 2 > tol and iter_count < max_iter:
            c = (a + b) / 2
            if f(c) == 0:
                return c, iter_count
            elif f(a) * f(c) < 0:
                b = c
            else:
                a = c
            iter_count += 1
        return (a + b) / 2, iter_count

    def false_position_method(self, f, a, b, tol=1e-6, max_iter=100):
        """ False Position method for root finding. """
        if f(a) * f(b) > 0:
            return None, None  # No sign change

        iter_count = 0
        c_old = a
        while iter_count < max_iter:
            c = (a * f(b) - b * f(a)) / (f(b) - f(a))
            if abs(c - c_old) < tol:
                return c, iter_count
            c_old = c
            if f(c) == 0:
                return c, iter_count
            elif f(a) * f(c) < 0:
                b = c
            else:
                a = c
            iter_count += 1
        return c, iter_count

    def calculate_roots(self):
        """ Compute roots using both methods and show results. """
        start, end = self.parse_inputs()
        if start is None or end is None:
            return

        f = self.f
        if f is None:
            return

        # Find valid interval for a root
        valid_start, valid_end = self.find_sign_change_interval(f, start, end)
        if valid_start is None or valid_end is None:
            QMessageBox.warning(self, "Warning", "No root found in the given interval.")
            return

        root_bisection, iter_bisection = self.bisection_method(f, valid_start, valid_end)
        root_false_position, iter_false_position = self.false_position_method(f, valid_start, valid_end)

        abs_error = abs(root_bisection - root_false_position)

        message = (
            f"Root Interval Found: [{valid_start:.6f}, {valid_end:.6f}]\n"
            f"Root (Bisection Method): {root_bisection:.6f} (Iterations: {iter_bisection})\n"
            f"Root (False Position Method): {root_false_position:.6f} (Iterations: {iter_false_position})\n"
            f"Absolute Error: {abs_error:.6f}"
        )
        QMessageBox.information(self, "Root Finding Results", message)

    def plot_function(self):
        """ Plot the function along with root approximations. """
        start, end = self.parse_inputs()
        if start is None or end is None:
            return

        f = self.f
        if f is None:
            return

        x = np.linspace(start, end, 400)
        y = f(x)

        # Clear previous plot
        self.ax.clear()

        # Plot the function
        self.ax.plot(x, y, label=f"f(x) = {self.function_input.text()}")
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)

        # Compute a valid root interval
        valid_start, valid_end = self.find_sign_change_interval(f, start, end)
        if valid_start is not None and valid_end is not None:
            root_bisection, _ = self.bisection_method(f, valid_start, valid_end)
            root_false_position, _ = self.false_position_method(f, valid_start, valid_end)

            # Plot roots
            if root_bisection is not None:
                self.ax.plot(root_bisection, f(root_bisection), 'ro', label="Bisection Root")
            if root_false_position is not None:
                self.ax.plot(root_false_position, f(root_false_position), 'go', label="False Position Root")

        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.set_title("Graph of f(x)")
        self.ax.legend()
        self.ax.grid(True)

        # Redraw the canvas
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RootFindingMethodsWindow()
    window.show()
    sys.exit(app.exec())
