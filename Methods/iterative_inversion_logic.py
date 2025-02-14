import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class IterativeMatrixInversionWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Iterative Matrix Inversion (Fixed)")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Matrix input
        layout.addWidget(QLabel("Enter the matrix A (comma-separated rows):"))
        self.matrix_input = QLineEdit()
        self.matrix_input.setPlaceholderText("e.g., 1,2,3;0,-1,4;5,6,-1")
        layout.addWidget(self.matrix_input)

        # Buttons
        self.calculate_button = QPushButton("Compute Inverse")
        self.calculate_button.clicked.connect(self.compute_inverse)
        layout.addWidget(self.calculate_button)

        self.plot_button = QPushButton("Show Inverse Matrix")
        self.plot_button.clicked.connect(self.plot_inverse_matrix)
        layout.addWidget(self.plot_button)

        # Matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def parse_input_matrix(self):
        """ Parse user input and return matrix A. """
        try:
            A = np.array([list(map(float, row.split(','))) for row in self.matrix_input.text().split(';')])
            if A.shape[0] != A.shape[1]:
                raise ValueError("Matrix must be square.")
            return A
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Invalid matrix input: {e}")
            return None

    def iterative_matrix_inversion(self, A, tol=1e-6, max_iter=50):
        """ Compute the inverse of A using a stabilized iterative method. """
        n = A.shape[0]
        I = np.eye(n)

        # Check if matrix is invertible
        det_A = np.linalg.det(A)
        if abs(det_A) < 1e-10:
            QMessageBox.critical(self, "Error", "Matrix is singular or nearly singular. Cannot compute inverse.")
            return None

        # Use a more stable initial guess: (A^T A)^{-1} A^T
        X_k = np.linalg.pinv(A)  # Pseudo-inverse for better stability

        for _ in range(max_iter):
            X_k_next = X_k @ (2 * I - A @ X_k)

            # Check for divergence (values growing too large)
            if np.isnan(X_k_next).any() or np.isinf(X_k_next).any():
                QMessageBox.critical(self, "Error", "Iteration diverged. Try a better-conditioned matrix.")
                return None

            # Convergence check
            if np.linalg.norm(X_k_next - X_k) < tol:
                return X_k_next
            X_k = X_k_next

        return X_k  # Return the last approximation

    def compute_inverse(self):
        """ Compute and display the inverse matrix. """
        A = self.parse_input_matrix()
        if A is None:
            return

        A_inv = self.iterative_matrix_inversion(A)
        if A_inv is None:
            return

        self.inverse_matrix = A_inv  # Store for plotting
        message = "\n".join(["\t".join([f"{val:.4f}" for val in row]) for row in A_inv])
        QMessageBox.information(self, "Inverse Matrix", message)

    def plot_inverse_matrix(self):
        """ Plot the computed inverse matrix as a heatmap. """
        if not hasattr(self, 'inverse_matrix'):
            QMessageBox.warning(self, "Warning", "Please compute the inverse first.")
            return

        # Clear previous plot
        self.ax.clear()

        # Plot heatmap
        self.ax.matshow(self.inverse_matrix, cmap='coolwarm', alpha=0.6)
        for (row, col), val in np.ndenumerate(self.inverse_matrix):
            self.ax.text(col, row, f"{val:.2f}", ha='center', va='center', color="black")

        self.ax.set_xlabel("Columns")
        self.ax.set_ylabel("Rows")
        self.ax.set_title("Inverse Matrix Visualization")
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IterativeMatrixInversionWindow()
    window.show()
    sys.exit(app.exec())
