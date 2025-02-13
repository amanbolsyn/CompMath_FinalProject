from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class GraphicalMethodWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphical Method and Absolute Error")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("This window handles Graphical Method and Absolute Error"))
        self.setLayout(layout)
