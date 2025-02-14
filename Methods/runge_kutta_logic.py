import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class RungeKuttaWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Runge-Kutta 2nd Order Solver")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Differential equation input
        layout.addWidget(QLabel("Enter the function dy/dx = f(x, y):"))
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("e.g., np.exp(x) - y")
        layout.addWidget(self.function_input)

        # Initial condition input
        layout.addWidget(QLabel("Enter initial x (x0):"))
        self.x0_input = QLineEdit()
        self.x0_input.setPlaceholderText("e.g., 0")
        layout.addWidget(self.x0_input)

        layout.addWidget(QLabel("Enter initial y (y0):"))
        self.y0_input = QLineEdit()
        self.y0_input.setPlaceholderText("e.g., 0")
        layout.addWidget(self.y0_input)

        # Step size and target x
        layout.addWidget(QLabel("Enter step size (h):"))
        self.h_input = QLineEdit()
        self.h_input.setPlaceholderText("e.g., 0.1")
        layout.addWidget(self.h_input)

        layout.addWidget(QLabel("Enter x value to compute y(x):"))
        self.x_target_input = QLineEdit()
        self.x_target_input.setPlaceholderText("e.g., 0.2")
        layout.addWidget(self.x_target_input)

        # Buttons
        self.calculate_button = QPushButton("Compute y(x)")
        self.calculate_button.clicked.connect(self.compute_runge_kutta)
        layout.addWidget(self.calculate_button)

        self.plot_button = QPushButton("Plot Solution")
        self.plot_button.clicked.connect(self.plot_solution)
        layout.addWidget(self.plot_button)

        # Matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def parse_inputs(self):
        """ Parse user inputs and return function, initial conditions, step size, and target x. """
        try:
            func_str = self.function_input.text()
            x0 = float(self.x0_input.text())
            y0 = float(self.y0_input.text())
            h = float(self.h_input.text())
            x_target = float(self.x_target_input.text())

            if h <= 0:
                raise ValueError("Step size must be positive.")
            if x_target <= x0:
                raise ValueError("Target x must be greater than initial x.")

            # Define function f(x, y)
            def f(x, y):
                return eval(func_str, {"x": x, "y": y, "np": np})

            return f, x0, y0, h, x_target
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid input: {e}")
            return None, None, None, None, None

    def runge_kutta_2nd_order(self, f, x0, y0, h, x_target):
        """ Apply the Runge-Kutta 2nd Order method to solve dy/dx = f(x,y). """
        x = x0
        y = y0

        while x < x_target:
            k1 = f(x, y)
            k2 = f(x + h, y + h * k1)
            y += h * (k1 + k2) / 2
            x += h

        return y

    def compute_runge_kutta(self):
        """ Compute y(x) using Runge-Kutta 2nd order and display result. """
        f, x0, y0, h, x_target = self.parse_inputs()
        if f is None:
            return

        y_result = self.runge_kutta_2nd_order(f, x0, y0, h, x_target)
        QMessageBox.information(self, "Computed Value", f"y({x_target}) = {y_result:.6f}")

    def plot_solution(self):
        """ Solve and plot y(x) over the given range. """
        f, x0, y0, h, x_target = self.parse_inputs()
        if f is None:
            return

        x_values = np.arange(x0, x_target + h, h)
        y_values = []

        x = x0
        y = y0
        for x in x_values:
            y_values.append(y)
            k1 = f(x, y)
            k2 = f(x + h, y + h * k1)
            y += h * (k1 + k2) / 2

        # Clear previous plot
        self.ax.clear()

        # Plot the numerical solution
        self.ax.plot(x_values, y_values, marker="o", linestyle="-", color="b", label="Runge-Kutta 2nd Order")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y(x)")
        self.ax.set_title("Runge-Kutta 2nd Order Solution")
        self.ax.legend()
        self.ax.grid()

        # Redraw the canvas
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RungeKuttaWindow()
    window.show()
    sys.exit(app.exec())
