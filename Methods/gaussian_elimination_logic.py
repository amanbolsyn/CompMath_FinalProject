import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class GaussianEliminationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gaussian Elimination with Partial Pivoting")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Matrix input
        layout.addWidget(QLabel("Enter the coefficient matrix (comma-separated rows):"))
        self.matrix_input = QLineEdit()
        self.matrix_input.setPlaceholderText("e.g., 2,1,-1; -3,1,2; -2,1,3")
        layout.addWidget(self.matrix_input)

        # Vector input
        layout.addWidget(QLabel("Enter the right-hand side vector:"))
        self.vector_input = QLineEdit()
        self.vector_input.setPlaceholderText("e.g., 8,-11,-3")
        layout.addWidget(self.vector_input)

        # Buttons
        self.calculate_button = QPushButton("Solve System")
        self.calculate_button.clicked.connect(self.solve_system)
        layout.addWidget(self.calculate_button)

        self.plot_button = QPushButton("Show Augmented Matrix")
        self.plot_button.clicked.connect(self.plot_final_matrix)
        layout.addWidget(self.plot_button)

        # Matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def parse_inputs(self):
        """ Parse user inputs for matrix A and vector b. """
        try:
            A = np.array([list(map(float, row.split(','))) for row in self.matrix_input.text().split(';')])
            b = np.array(list(map(float, self.vector_input.text().split(','))))
            if A.shape[0] != A.shape[1] or A.shape[0] != len(b):
                raise ValueError("Matrix must be square and match the size of the vector.")
            return A, b
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Invalid input: {e}")
            return None, None

    def gaussian_elimination_with_partial_pivoting(self, A, b):
        """ Performs Gaussian elimination with partial pivoting and returns the final augmented matrix. """
        n = len(b)
        augmented_matrix = np.hstack([A, b.reshape(-1, 1)])  # Create augmented matrix

        # Forward elimination with partial pivoting
        for i in range(n):
            max_row = np.argmax(abs(augmented_matrix[i:n, i])) + i
            augmented_matrix[[i, max_row]] = augmented_matrix[[max_row, i]]  # Swap rows

            for j in range(i+1, n):
                factor = augmented_matrix[j, i] / augmented_matrix[i, i]
                augmented_matrix[j, i:] -= factor * augmented_matrix[i, i:]

        # Back-substitution
        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            x[i] = (augmented_matrix[i, -1] - np.sum(augmented_matrix[i, i+1:n] * x[i+1:n])) / augmented_matrix[i, i]

        return x, augmented_matrix

    def solve_system(self):
        """ Compute solution using Gaussian Elimination and show results. """
        A, b = self.parse_inputs()
        if A is None or b is None:
            return

        solution, self.final_matrix = self.gaussian_elimination_with_partial_pivoting(A, b)
        message = "\n".join([f"x{i+1} = {solution[i]:.6f}" for i in range(len(solution))])
        QMessageBox.information(self, "Solution", message)

    def plot_final_matrix(self):
        """ Plot the final augmented matrix after Gaussian Elimination. """
        if not hasattr(self, 'final_matrix'):
            QMessageBox.warning(self, "Warning", "Please solve the system first.")
            return

        # Clear previous plot
        self.ax.clear()

        # Plot final augmented matrix as a heatmap
        self.ax.matshow(self.final_matrix, cmap='coolwarm', alpha=0.6)
        for (row, col), val in np.ndenumerate(self.final_matrix):
            self.ax.text(col, row, f"{val:.2f}", ha='center', va='center', color="black")

        self.ax.set_xlabel("Variables & RHS")
        self.ax.set_ylabel("Equations")
        self.ax.set_title("Final Augmented Matrix")
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GaussianEliminationWindow()
    window.show()
    sys.exit(app.exec())
