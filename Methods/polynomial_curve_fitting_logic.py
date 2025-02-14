
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
)
from PyQt6.QtCore import Qt


class PolynomialCurveFittingWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Quadratic Curve Fitting")
        self.setGeometry(100, 100, 400, 300)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Input fields for data points
        self.input_label = QLabel("Enter data points as (x, y) pairs, separated by commas:")
        layout.addWidget(self.input_label)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Example: 0,0 1,1 2,4 3,9 4,16")
        layout.addWidget(self.input_field)

        # Calculate button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_curve)
        layout.addWidget(self.calculate_button)

        # Plot button
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_curve)
        self.plot_button.setEnabled(False)  # Disabled until calculation is done
        layout.addWidget(self.plot_button)

        # Result label
        self.result_label = QLabel("Result will be shown here.")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)

        # Set layout
        central_widget.setLayout(layout)

        # Store coefficients
        self.coefficients = None

    def calculate_curve(self):
        try:
            # Get input data
            input_text = self.input_field.text().strip()
            if not input_text:
                raise ValueError("Input field is empty.")

            # Parse input into (x, y) pairs
            data_points = [tuple(map(float, point.split(','))) for point in input_text.split()]
            x = np.array([point[0] for point in data_points])
            y = np.array([point[1] for point in data_points])

            # Fit quadratic curve using least squares
            A = np.vstack([x**2, x, np.ones_like(x)]).T
            self.coefficients = np.linalg.lstsq(A, y, rcond=None)[0]

            # Display result
            a, b, c = self.coefficients
            self.result_label.setText(f"Fitted curve: y = {a:.2f}x² + {b:.2f}x + {c:.2f}")
            self.plot_button.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid input: {str(e)}")

    def plot_curve(self):
        if self.coefficients is None:
            QMessageBox.warning(self, "Warning", "No curve has been calculated yet.")
            return

        # Generate points for the fitted curve
        x = np.linspace(0, 4, 100)
        a, b, c = self.coefficients
        y = a * x**2 + b * x + c

        # Plot the curve and data points
        plt.figure()
        plt.plot(x, y, label="Fitted Curve")
        plt.scatter([0, 1, 2, 3, 4], [0, 1, 4, 9, 16], color="red", label="Data Points")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Quadratic Curve Fitting")
        plt.legend()
        plt.grid(True)
        plt.show()

