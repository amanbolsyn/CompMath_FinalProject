from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from Methods.graphical_method_logic import GraphicalMethodWindow
from Methods.root_fining_logic import RootFindingMethodsWindow
from Methods.gaussian_elimination_logic import GaussianEliminationWindow
from Methods.iterative_inversion_logic import IterativeMatrixInversionWindow
from Methods.polynomial_curve_fitting_logic import PolynomialCurveFittingWindow
from Methods.lagrange_interpolation_logic import LagrangeInterpolationWindow
from Methods.romberg_integration_logic import RombergIntegrationWindow
from Methods.runge_kutta_logic import RungeKuttaWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Numerical Methods")
        self.setGeometry(100, 100, 300, 300)

        button_layout = QVBoxLayout()

        self.button1 = QPushButton("Graphical Method and Absolute Error")
        self.button2 = QPushButton("Comparison of Root-Finding Methods")
        self.button3 = QPushButton("Gaussian Elimination with Partial Pivoting")
        self.button4 = QPushButton("Iterative Method for Matrix Inversion")
        self.button5 = QPushButton("Polynomial Curve Fitting")
        self.button6 = QPushButton("Lagrange’s Interpolation Formula")
        self.button7 = QPushButton("Romberg’s Integration")
        self.button8 = QPushButton("Runge-Kutta 2nd Order")

        self.button1.clicked.connect(self.open_graphical_method)
        self.button2.clicked.connect(self.open_root_finding)
        self.button3.clicked.connect(self.open_gaussian_elimination)
        self.button4.clicked.connect(self.open_iterative_inversion)
        self.button5.clicked.connect(self.open_polynomial_curve_fitting)
        self.button6.clicked.connect(self.open_lagrange_interpolation)
        self.button7.clicked.connect(self.open_romberg_integration)
        self.button8.clicked.connect(self.open_runge_kutta)

        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)
        button_layout.addWidget(self.button3)
        button_layout.addWidget(self.button4)
        button_layout.addWidget(self.button5)
        button_layout.addWidget(self.button6)
        button_layout.addWidget(self.button7)
        button_layout.addWidget(self.button8)

        container = QWidget()
        container.setLayout(button_layout)
        self.setCentralWidget(container)

    def open_graphical_method(self):
        self.window = GraphicalMethodWindow()
        self.window.show()

    def open_root_finding(self):
        self.window = RootFindingMethodsWindow()
        self.window.show()

    def open_gaussian_elimination(self):
        self.window = GaussianEliminationWindow()
        self.window.show()

    def open_iterative_inversion(self):
        self.window = IterativeMatrixInversionWindow()
        self.window.show()

    def open_polynomial_curve_fitting(self):
        self.window = PolynomialCurveFittingWindow()
        self.window.show()

    def open_lagrange_interpolation(self):
        self.window = LagrangeInterpolationWindow()
        self.window.show()

    def open_romberg_integration(self):
        self.window = RombergIntegrationWindow()
        self.window.show()

    def open_runge_kutta(self):
        self.window = RungeKuttaWindow()
        self.window.show()
