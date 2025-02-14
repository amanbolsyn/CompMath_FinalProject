import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class GraphicalMethodWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Graphical Method and Absolute Error")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Label and input for function
        function_label = QLabel("Enter the function f(x):", self)
        layout.addWidget(function_label)
        self.function_input = QLineEdit(self)
        self.function_input.setPlaceholderText("e.g., x**3 - 3*x + 2")
        layout.addWidget(self.function_input)

        # Label and input for interval start
        interval_start_label = QLabel("Enter the start of the interval:", self)
        layout.addWidget(interval_start_label)
        self.interval_start_input = QLineEdit(self)
        self.interval_start_input.setPlaceholderText("e.g., -2")
        layout.addWidget(self.interval_start_input)

        # Label and input for interval end
        interval_end_label = QLabel("Enter the end of the interval:", self)
        layout.addWidget(interval_end_label)
        self.interval_end_input = QLineEdit(self)
        self.interval_end_input.setPlaceholderText("e.g., 2")
        layout.addWidget(self.interval_end_input)

        # Button to plot graph
        self.plot_button = QPushButton("Plot Graph", self)
        self.plot_button.clicked.connect(self.plot_graph)
        layout.addWidget(self.plot_button)

        # Button to calculate absolute error
        self.calculate_button = QPushButton("Calculate Absolute Error", self)
        self.calculate_button.clicked.connect(self.calculate_absolute_error)
        layout.addWidget(self.calculate_button)

        # Matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Store the approximate root from the graph
        self.approx_root = None

    def is_valid_number(self, value):
        """Check if the value is a valid finite number."""
        try:
            float(value)  # Try to convert the value to a float
            return True
        except (ValueError, TypeError):
            return False

    def parse_inputs(self):
        # Check if function input is empty
        if not self.function_input.text().strip():
            raise ValueError("Function input cannot be empty.")



        # Get function string from input
        func_str = self.function_input.text()

        # Define the function
        def f(x):
            try:
                return eval(func_str, {"x": x, "np": np})
            except Exception as e:
                raise ValueError(f"Error evaluating function: {e}")

        # Get interval start and end from inputs
        try:
            start = float(self.interval_start_input.text())
            end = float(self.interval_end_input.text())
        except ValueError:
            raise ValueError("Interval start and end must be valid numbers.")

        # Validate interval
        if start >= end:
            raise ValueError("Interval start must be less than interval end.")

        return f, start, end

    def find_approximate_root(self, x, y):
        """
        Find the approximate root from the graph (where the curve crosses the x-axis).
        Returns the approximate root or None if no root is found.
        """
        crossings = np.where(np.diff(np.sign(y)))[0]
        if len(crossings) > 0:
            return x[crossings[0]]  # Return the first crossing point
        return None  # No root found

    def plot_graph(self):
        try:
            # Parse and validate inputs
            f, start, end = self.parse_inputs()

            # Generate x values
            x = np.linspace(start, end, 400)
            y = f(x)

            # Clear previous plot
            self.ax.clear()

            # Plot the function
            self.ax.plot(x, y, label=f"f(x) = {self.function_input.text()}")
            self.ax.axhline(0, color='black', linewidth=0.5)
            self.ax.axvline(0, color='black', linewidth=0.5)
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("f(x)")
            self.ax.set_title("Graph of f(x)")
            self.ax.legend()
            self.ax.grid(True)

            # Find approximate root from the graph
            self.approx_root = self.find_approximate_root(x, y)

            if self.approx_root is not None:
                # Plot the approximate root on the graph
                self.ax.plot(self.approx_root, f(self.approx_root), 'ro', label="Approximate Root")
                self.ax.legend()
            else:
                QMessageBox.warning(self, "Warning", "No root found in the given interval.")

            # Redraw the canvas
            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def calculate_absolute_error(self):
        try:
            # Parse and validate inputs
            f, start, end = self.parse_inputs()

            # Generate x values
            x = np.linspace(start, end, 400)
            y = f(x)

            # Find approximate root from the graph
            self.approx_root = self.find_approximate_root(x, y)

            # Check if approx_root is None (no root found)
            if self.approx_root is None:
                QMessageBox.warning(self, "No Root Found", "No root was found in the given interval.")
                return

            # Define the derivative of the function (for Newton-Raphson)
            def f_prime(x):
                try:
                    # Use sympy to compute the derivative dynamically
                    from sympy import symbols, diff, sympify
                    x_sym = symbols('x')
                    expr = sympify(self.function_input.text())
                    derivative = diff(expr, x_sym)
                    return derivative.evalf(subs={x_sym: x})
                except Exception as e:
                    raise ValueError(f"Error computing derivative: {e}")

            # Ensure approx_root is a valid number
            if not self.is_valid_number(self.approx_root):
                raise ValueError("Approximate root from the graph is not a valid number.")

            # Find the root using a numerical method (Newton-Raphson)
            numerical_root = newton(f, self.approx_root, fprime=f_prime)

            # Ensure numerical_root is a valid number
            if not self.is_valid_number(numerical_root):
                raise ValueError("Numerical root computation failed.")

            # Calculate absolute error
            absolute_error = abs(self.approx_root - numerical_root)

            # Show results in a pop-up window
            result_message = (
                f"Approximate root from the graph: {self.approx_root:.6f}\n"
                f"Numerical root using Newton-Raphson: {numerical_root:.6f}\n"
                f"Absolute Error: {absolute_error:.6f}"
            )
            QMessageBox.information(self, "Results", result_message)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

