from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class RungeKuttaWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Runge-Kutta 2nd Order")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("This window handles Runge-Kutta 2nd Order"))
        self.setLayout(layout)
