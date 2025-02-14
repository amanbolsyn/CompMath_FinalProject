import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class LagrangeInterpolationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lagrange Interpolation")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Label and Input for Data Points
        layout.addWidget(QLabel("Enter x values (comma-separated):"))
        self.x_input = QLineEdit()
        self.x_input.setPlaceholderText("e.g., 1,3,5")
        layout.addWidget(self.x_input)

        layout.addWidget(QLabel("Enter y values (comma-separated):"))
        self.y_input = QLineEdit()
        self.y_input.setPlaceholderText("e.g., 2,8,18")
        layout.addWidget(self.y_input)

        # Interpolation point
        layout.addWidget(QLabel("Enter x value to interpolate f(x):"))
        self.x_interp_input = QLineEdit()
        self.x_interp_input.setPlaceholderText("e.g., 4")
        layout.addWidget(self.x_interp_input)

        # Buttons
        self.calculate_button = QPushButton("Compute Interpolation")
        self.calculate_button.clicked.connect(self.compute_interpolation)
        layout.addWidget(self.calculate_button)

        self.plot_button = QPushButton("Plot Interpolation")
        self.plot_button.clicked.connect(self.plot_interpolation)
        layout.addWidget(self.plot_button)

        # Matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def parse_inputs(self):
        """ Parse user input and return x, y data arrays and interpolation point. """
        try:
            x_values = list(map(float, self.x_input.text().split(',')))
            y_values = list(map(float, self.y_input.text().split(',')))
            x_interp = float(self.x_interp_input.text())

            if len(x_values) != len(y_values):
                raise ValueError("Number of x and y values must be equal.")

            return np.array(x_values), np.array(y_values), x_interp
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid input: {e}")
            return None, None, None

    def lagrange_interpolation(self, x, y, x_interp):
        """ Compute Lagrange interpolation at x_interp """
        n = len(x)
        result = 0.0

        for i in range(n):
            L_i = 1.0
            for j in range(n):
                if i != j:
                    L_i *= (x_interp - x[j]) / (x[i] - x[j])
            result += y[i] * L_i  # Correctly summing weighted basis polynomials

        return result

    def compute_interpolation(self):
        """ Compute and display interpolated value. """
        x, y, x_interp = self.parse_inputs()
        if x is None:
            return

        interpolated_value = self.lagrange_interpolation(x, y, x_interp)
        QMessageBox.information(self, "Interpolated Value", f"f({x_interp}) = {interpolated_value:.6f}")

    def plot_interpolation(self):
        """ Plot the interpolation polynomial and data points. """
        x, y, x_interp = self.parse_inputs()
        if x is None:
            return

        # Generate smooth curve for visualization
        x_plot = np.linspace(min(x) - 1, max(x) + 1, 100)
        y_plot = [self.lagrange_interpolation(x, y, xi) for xi in x_plot]

        # Clear previous plot
        self.ax.clear()

        # Plot data points
        self.ax.scatter(x, y, color="red", label="Data Points")

        # Plot interpolation polynomial
        self.ax.plot(x_plot, y_plot, color="blue", label="Lagrange Polynomial")

        # Mark interpolated point
        interp_value = self.lagrange_interpolation(x, y, x_interp)
        self.ax.scatter([x_interp], [interp_value], color="green", marker="o", label=f"f({x_interp}) = {interp_value:.2f}")

        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.set_title("Lagrange Interpolation")
        self.ax.legend()
        self.ax.grid()

        # Redraw the canvas
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LagrangeInterpolationWindow()
    window.show()
    sys.exit(app.exec())
