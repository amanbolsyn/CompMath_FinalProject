from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class LagrangeInterpolationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lagrange’s Interpolation Formula")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("This window handles Lagrange’s Interpolation Formula"))
        self.setLayout(layout)
