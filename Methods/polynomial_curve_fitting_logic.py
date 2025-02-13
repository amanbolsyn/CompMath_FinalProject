from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class PolynomialCurveFittingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Polynomial Curve Fitting")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("This window handles Polynomial Curve Fitting"))
        self.setLayout(layout)
