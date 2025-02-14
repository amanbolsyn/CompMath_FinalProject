import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class RombergIntegrationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Romberg Integration")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Function input
        layout.addWidget(QLabel("Enter function f(x):"))
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("e.g., x**2")
        layout.addWidget(self.function_input)

        # Limits input
        layout.addWidget(QLabel("Enter lower limit (a):"))
        self.lower_limit_input = QLineEdit()
        self.lower_limit_input.setPlaceholderText("e.g., 0")
        layout.addWidget(self.lower_limit_input)

        layout.addWidget(QLabel("Enter upper limit (b):"))
        self.upper_limit_input = QLineEdit()
        self.upper_limit_input.setPlaceholderText("e.g., 1")
        layout.addWidget(self.upper_limit_input)

        # Step sizes input
        layout.addWidget(QLabel("Enter step sizes h (comma-separated):"))
        self.h_values_input = QLineEdit()
        self.h_values_input.setPlaceholderText("e.g., 0.5, 0.25, 0.125")
        layout.addWidget(self.h_values_input)

        # Buttons
        self.calculate_button = QPushButton("Compute Romberg Table")
        self.calculate_button.clicked.connect(self.compute_romberg_table)
        layout.addWidget(self.calculate_button)

        self.plot_button = QPushButton("Plot Function")
        self.plot_button.clicked.connect(self.plot_function)
        layout.addWidget(self.plot_button)

        # Display Romberg Table
        layout.addWidget(QLabel("Romberg Integration Table:"))
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        # Matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def parse_inputs(self):
        """ Parse user inputs for function, limits, and step sizes. """
        try:
            func_str = self.function_input.text()
            a = float(self.lower_limit_input.text())
            b = float(self.upper_limit_input.text())
            h_values = list(map(float, self.h_values_input.text().split(',')))

            def f(x):
                return eval(func_str, {"x": x, "np": np})

            return f, a, b, h_values
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid input: {e}")
            return None, None, None, None

    def trapezoidal_rule(self, f, a, b, n):
        """ Trapezoidal rule for numerical integration. """
        h = (b - a) / n
        x = np.linspace(a, b, n+1)
        y = f(x)
        return (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])

    def romberg_integration(self, f, a, b, h_values):
        """ Compute Romberg Integration table with user-defined step sizes. """
        R = np.zeros((len(h_values), len(h_values)))

        # Compute R[i,0] using the trapezoidal rule with fixed step sizes
        for i, h in enumerate(h_values):
            n = int((b - a) / h)  # Compute the number of intervals for given h
            R[i, 0] = self.trapezoidal_rule(f, a, b, n)

        # Compute higher-order Romberg estimates
        for j in range(1, len(h_values)):
            for i in range(j, len(h_values)):
                R[i, j] = (4**j * R[i, j-1] - R[i-1, j-1]) / (4**j - 1)

        return R

    def compute_romberg_table(self):
        """ Compute Romberg table and display results. """
        f, a, b, h_values = self.parse_inputs()
        if f is None:
            return

        romberg_table = self.romberg_integration(f, a, b, h_values)

        # Convert to DataFrame for better visualization
        romberg_df = pd.DataFrame(romberg_table, index=h_values, columns=[f"Order {i}" for i in range(len(h_values))])
        romberg_df = romberg_df.replace(0, np.nan)  # Hide unnecessary zeros

        # Format and display result
        table_str = romberg_df.to_string(index=True, na_rep=" ")
        self.result_display.setText(table_str)

    def plot_function(self):
        """ Plot the function within the integration range. """
        f, a, b, h_values = self.parse_inputs()
        if f is None:
            return

        x = np.linspace(a, b, 100)
        y = f(x)

        # Clear previous plot
        self.ax.clear()

        # Plot function
        self.ax.plot(x, y, label=f"f(x) = {self.function_input.text()}", color="blue")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.set_title("Function Plot for Integration")
        self.ax.legend()
        self.ax.grid()

        # Redraw the canvas
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RombergIntegrationWindow()
    window.show()
    sys.exit(app.exec())
