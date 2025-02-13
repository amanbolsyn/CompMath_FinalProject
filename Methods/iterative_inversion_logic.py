from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class IterativeMatrixInversionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iterative Method for Matrix Inversion")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("This window handles Iterative Method for Matrix Inversion"))
        self.setLayout(layout)
