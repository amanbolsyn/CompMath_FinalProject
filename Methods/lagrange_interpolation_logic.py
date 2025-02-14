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


class LagrangeInterpolationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Lagrange's Interpolation")
        self.setGeometry(100, 100, 400, 300)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Input fields for x values
        self.x_label = QLabel("Enter x values (comma-separated):")
        layout.addWidget(self.x_label)

        self.x_input = QLineEdit()
        self.x_input.setPlaceholderText("Example: 1, 3, 5")
        layout.addWidget(self.x_input)

        # Input fields for y values
        self.y_label = QLabel("Enter y values (comma-separated):")
        layout.addWidget(self.y_label)

        self.y_input = QLineEdit()
        self.y_input.setPlaceholderText("Example: 2, 8, 18")
        layout.addWidget(self.y_input)

        # Input field for interpolation point
        self.point_label = QLabel("Enter the point x to estimate f(x):")
        layout.addWidget(self.point_label)

        self.point_input = QLineEdit()
        self.point_input.setPlaceholderText("Example: 4")
        layout.addWidget(self.point_input)

        # Calculate button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_interpolation)
        layout.addWidget(self.calculate_button)

        # Plot button
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_graph)
        self.plot_button.setEnabled(False)  # Disabled until calculation is done
        layout.addWidget(self.plot_button)

        # Result label
        self.result_label = QLabel("Result will be shown here.")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)

        # Set layout
        central_widget.setLayout(layout)

        # Store data for plotting
        self.x_values = None
        self.y_values = None
        self.interpolated_value = None
        self.interpolation_point = None

    def calculate_interpolation(self):
        try:
            # Get x values
            x_text = self.x_input.text().strip()
            if not x_text:
                raise ValueError("x values are missing.")
            self.x_values = list(map(float, x_text.split(',')))

            # Get y values
            y_text = self.y_input.text().strip()
            if not y_text:
                raise ValueError("y values are missing.")
            self.y_values = list(map(float, y_text.split(',')))

            # Check if x and y have the same length
            if len(self.x_values) != len(self.y_values):
                raise ValueError("x and y values must have the same length.")

            # Get interpolation point
            point_text = self.point_input.text().strip()
            if not point_text:
                raise ValueError("Interpolation point is missing.")
            self.interpolation_point = float(point_text)

            # Perform Lagrange interpolation
            self.interpolated_value = self.lagrange_interpolation(
                self.x_values, self.y_values, self.interpolation_point
            )

            # Display result
            self.result_label.setText(
                f"Estimated f({self.interpolation_point}) = {self.interpolated_value:.4f}"
            )
            self.plot_button.setEnabled(True)  # Enable the Plot button

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid input: {str(e)}")

    def lagrange_interpolation(self, x_values, y_values, x_point):
        """
        Perform Lagrange interpolation to estimate f(x_point).
        """
        n = len(x_values)
        result = 0.0

        for i in range(n):
            term = y_values[i]
            for j in range(n):
                if j != i:
                    term *= (x_point - x_values[j]) / (x_values[i] - x_values[j])
            result += term

        return result

    def plot_graph(self):
        if self.x_values is None or self.y_values is None:
            QMessageBox.warning(self, "Warning", "No data has been calculated yet.")
            return

        # Generate points for the interpolated polynomial curve
        x_curve = np.linspace(min(self.x_values), max(self.x_values), 100)
        y_curve = [self.lagrange_interpolation(self.x_values, self.y_values, x) for x in x_curve]

        # Plot the curve and data points
        plt.figure()
        plt.plot(x_curve, y_curve, label="Interpolated Polynomial")
        plt.scatter(self.x_values, self.y_values, color="red", label="Data Points")
        plt.scatter(
            [self.interpolation_point],
            [self.interpolated_value],
            color="green",
            label=f"Interpolated Point ({self.interpolation_point}, {self.interpolated_value:.2f})",
        )
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Lagrange's Interpolation")
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LagrangeInterpolationWindow()
    window.show()
    sys.exit(app.exec())
