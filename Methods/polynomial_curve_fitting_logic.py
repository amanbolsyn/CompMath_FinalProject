import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class PolynomialCurveFittingWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Polynomial Curve Fitting (Least Squares)")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Label and Input for Data Points
        layout.addWidget(QLabel("Enter data points (comma-separated, e.g., 0,0;1,1;2,4;3,9;4,16):"))
        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText("0,0;1,1;2,4;3,9;4,16")
        layout.addWidget(self.data_input)

        # Buttons
        self.calculate_button = QPushButton("Compute Polynomial Fit")
        self.calculate_button.clicked.connect(self.compute_curve_fit)
        layout.addWidget(self.calculate_button)

        self.plot_button = QPushButton("Plot Fitted Curve")
        self.plot_button.clicked.connect(self.plot_curve)
        layout.addWidget(self.plot_button)

        # Matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def parse_data(self):
        """ Parse user input and return x, y data arrays. """
        try:
            raw_data = self.data_input.text().strip()
            points = [tuple(map(float, p.split(','))) for p in raw_data.split(';')]
            x_values, y_values = zip(*points)
            return np.array(x_values), np.array(y_values)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid data input: {e}")
            return None, None

    def compute_curve_fit(self):
        """ Compute least squares polynomial fit and display equation. """
        x, y = self.parse_data()
        if x is None:
            return

        # Construct the design matrix
        A = np.vstack([x ** 2, x, np.ones_like(x)]).T
        # Solve for coefficients using least squares
        coeffs = np.linalg.lstsq(A, y, rcond=None)[0]

        # Store coefficients for plotting
        self.coeffs = coeffs

        # Display equation
        equation = f"y = {coeffs[0]:.4f}x² + {coeffs[1]:.4f}x + {coeffs[2]:.4f}"
        QMessageBox.information(self, "Polynomial Fit", f"Computed equation:\n{equation}")

    def plot_curve(self):
        """ Plot the original data points and fitted quadratic curve. """
        x, y = self.parse_data()
        if x is None or not hasattr(self, 'coeffs'):
            return

        # Generate fitted curve
        x_fit = np.linspace(min(x), max(x), 100)
        y_fit = self.coeffs[0] * x_fit ** 2 + self.coeffs[1] * x_fit + self.coeffs[2]

        # Clear previous plot
        self.ax.clear()

        # Plot original data points
        self.ax.scatter(x, y, color="red", label="Data Points")

        # Plot fitted curve
        self.ax.plot(x_fit, y_fit, color="blue", label="Fitted Curve (Quadratic)")

        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_title("Polynomial Curve Fitting")
        self.ax.legend()
        self.ax.grid()

        # Redraw the canvas
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PolynomialCurveFittingWindow()
    window.show()
    sys.exit(app.exec())
