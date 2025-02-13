from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class RombergIntegrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Romberg’s Integration")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("This window handles Romberg’s Integration"))
        self.setLayout(layout)
