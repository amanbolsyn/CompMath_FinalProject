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
    QTableWidget,
    QTableWidgetItem,
)
from PyQt6.QtCore import Qt


class RombergIntegrationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Romberg's Integration")
        self.setGeometry(100, 100, 600, 400)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Input field for the function
        self.function_label = QLabel("Enter the function (use 'x' as the variable):")
        layout.addWidget(self.function_label)

        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Example: x**2")
        layout.addWidget(self.function_input)

        # Input fields for integration limits
        self.limits_label = QLabel("Enter integration limits (a and b, comma-separated):")
        layout.addWidget(self.limits_label)

        self.limits_input = QLineEdit()
        self.limits_input.setPlaceholderText("Example: 0, 1")
        layout.addWidget(self.limits_input)

        # Input field for step sizes
        self.steps_label = QLabel("Enter step sizes (comma-separated):")
        layout.addWidget(self.steps_label)

        self.steps_input = QLineEdit()
        self.steps_input.setPlaceholderText("Example: 0.5, 0.25, 0.125")
        layout.addWidget(self.steps_input)

        # Calculate button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_integral)
        layout.addWidget(self.calculate_button)

        # Plot button
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_graph)
        self.plot_button.setEnabled(False)  # Disabled until calculation is done
        layout.addWidget(self.plot_button)

        # Romberg table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["h", "Trapezoidal", "R1", "R2", "R3"])
        layout.addWidget(self.table)

        # Result label
        self.result_label = QLabel("Result will be shown here.")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)

        # Set layout
        central_widget.setLayout(layout)

        # Store data for plotting
        self.function = None
        self.a = None
        self.b = None
        self.steps = None
        self.romberg_table = None

    def calculate_integral(self):
        try:
            # Get the function
            function_text = self.function_input.text().strip()
            if not function_text:
                raise ValueError("Function is missing.")
            self.function = lambda x: eval(function_text)

            # Get integration limits
            limits_text = self.limits_input.text().strip()
            if not limits_text:
                raise ValueError("Integration limits are missing.")
            self.a, self.b = map(float, limits_text.split(','))

            # Get step sizes
            steps_text = self.steps_input.text().strip()
            if not steps_text:
                raise ValueError("Step sizes are missing.")
            self.steps = list(map(float, steps_text.split(',')))

            # Compute Romberg table
            self.romberg_table = self.romberg_integration(self.function, self.a, self.b, self.steps)

            # Display Romberg table
            self.display_romberg_table(self.romberg_table)

            # Display result
            self.result_label.setText(f"Approximated integral: {self.romberg_table[-1][-1]:.6f}")
            self.plot_button.setEnabled(True)  # Enable the Plot button

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid input: {str(e)}")

    def romberg_integration(self, func, a, b, steps):
        """
        Perform Romberg's Integration and return the Romberg table.
        """
        n = len(steps)
        table = np.zeros((n, n))  # Initialize an n x n table

        # Compute trapezoidal approximations for each step size
        for i in range(n):
            h = steps[i]
            x = np.linspace(a, b, int((b - a) / h) + 1)  # Generate points with step size h
            y = func(x)  # Evaluate the function at these points
            # Apply the trapezoidal rule
            table[i, 0] = (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])

        # Richardson Extrapolation
        for j in range(1, n):
            for i in range(j, n):
                table[i, j] = (4**j * table[i, j - 1] - table[i - 1, j - 1]) / (4**j - 1)

        return table

    def display_romberg_table(self, table):
        """
        Display the Romberg table in the QTableWidget.
        """
        self.table.setRowCount(len(table))
        for i, row in enumerate(table):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(f"{value:.6f}"))

    def plot_graph(self):
        if self.function is None or self.a is None or self.b is None:
            QMessageBox.warning(self, "Warning", "No data has been calculated yet.")
            return

        # Plot the function
        x = np.linspace(self.a, self.b, 100)
        y = self.function(x)
        plt.figure()
        plt.plot(x, y, label="Function: f(x)")

        # Plot trapezoidal areas for the smallest step size
        h = self.steps[-1]
        x_trap = np.linspace(self.a, self.b, int((self.b - self.a) / h) + 1)
        y_trap = self.function(x_trap)
        plt.bar(x_trap, y_trap, width=h, alpha=0.2, label="Trapezoidal Areas")

        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Romberg's Integration")
        plt.legend()
        plt.grid(True)
        plt.show()
