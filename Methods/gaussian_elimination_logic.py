from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class GaussianEliminationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gaussian Elimination with Partial Pivoting")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("This window handles Gaussian Elimination with Partial Pivoting"))
        self.setLayout(layout)
