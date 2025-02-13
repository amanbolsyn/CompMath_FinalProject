from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class RootFindingMethodsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Comparison of Root-Finding Methods")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("This window handles Comparison of Root-Finding Methods"))
        self.setLayout(layout)
