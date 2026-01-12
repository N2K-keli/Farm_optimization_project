import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# Import yield maximization page
try:
    from yield_maximization_page import YieldMaximizationPage
except ImportError:
    YieldMaximizationPage = None

# Import cost minimization page
try:
    from cost_minimization_page import CostMinimizationPage
except ImportError:
    CostMinimizationPage = None

# Import agricultural optimization page
try:
    from agricultural_optimization_page import AgriculturalOptimizationPage
except ImportError:
    AgriculturalOptimizationPage = None


class OptionsPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Farm Optimization Options")
        self.setGeometry(100, 100, 800, 600)
        
        # Store reference to opened windows
        self.yield_window = None
        self.cost_window = None
        self.agri_window = None

        # Use the same styling as welcome page
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5fcf4;
            }
            QLabel#titleLabel {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 24px;
                font-weight: bold;
                color: #2d5016;
                padding: 10px;
                background-color: #e8f5e9;
                border-radius: 10px;
                border: 2px solid #c8e6c9;
            }
            QPushButton#optionButton {
                background-color: #4caf50;
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                padding: 20px;
                border: 2px solid #388e3c;
                text-align: left;
                padding-left: 30px;
            }
            QPushButton#optionButton:hover {
                background-color: #66bb6a;
                border: 2px solid #4caf50;
            }
            QPushButton#backButton {
                background-color: #ff9800;
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px 20px;
                border: 2px solid #f57c00;
            }
            QPushButton#backButton:hover {
                background-color: #ffb74d;
                border: 2px solid #ff9800;
            }
            QGroupBox {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 16px;
                font-weight: bold;
                color: #2d5016;
                border: 2px solid #c8e6c9;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #e8f5e9;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }
        """)

        self.init_ui()

    def init_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Header with farming icons
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)

        icon_label = QLabel("🌾")
        icon_label.setStyleSheet("font-size: 40px;")
        header_layout.addWidget(icon_label)

        title_label = QLabel("Choose Your Optimization Goal")
        title_label.setStyleSheet("""
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 28px;
            font-weight: bold;
            color: #2d5016;
            padding: 10px;
        """)
        header_layout.addWidget(title_label)

        icon_label2 = QLabel("📊")
        icon_label2.setStyleSheet("font-size: 40px;")
        header_layout.addWidget(icon_label2)

        main_layout.addLayout(header_layout)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #c8e6c9; height: 2px;")
        main_layout.addWidget(separator)

        # Instruction label
        instruction_label = QLabel("Select the optimization strategy that best fits your needs:")
        instruction_label.setObjectName("titleLabel")
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setWordWrap(True)
        main_layout.addWidget(instruction_label)

        # Add spacing
        main_layout.addSpacing(20)

        # Options section - 3 main buttons
        # Option 1: Yield Maximization
        yield_button = QPushButton("🌱  Yield Maximization")
        yield_button.setObjectName("optionButton")
        yield_button.setCursor(Qt.PointingHandCursor)
        yield_button.setFixedHeight(70)
        yield_button.clicked.connect(lambda: self.on_option_clicked("Yield Maximization"))
        main_layout.addWidget(yield_button)

        # Description for Yield Maximization
        yield_desc = QLabel(
            "Maximize your crop production by optimizing planting schedules, irrigation, and fertilization strategies. Get the highest possible output from your land.")
        yield_desc.setStyleSheet(
            "font-size: 14px; color: #555555; padding: 10px 20px; background-color: #f0f9f0; border-radius: 5px; margin-bottom: 10px;")
        yield_desc.setWordWrap(True)
        main_layout.addWidget(yield_desc)

        # Option 2: Cost Minimization
        cost_button = QPushButton("💰  Cost Minimization")
        cost_button.setObjectName("optionButton")
        cost_button.setCursor(Qt.PointingHandCursor)
        cost_button.setFixedHeight(70)
        cost_button.clicked.connect(lambda: self.on_option_clicked("Cost Minimization"))
        main_layout.addWidget(cost_button)

        # Description for Cost Minimization
        cost_desc = QLabel(
            "Reduce operational expenses by optimizing resource allocation, minimizing waste, and improving efficiency. Achieve your goals at the lowest cost.")
        cost_desc.setStyleSheet(
            "font-size: 14px; color: #555555; padding: 10px 20px; background-color: #f0f9f0; border-radius: 5px; margin-bottom: 10px;")
        cost_desc.setWordWrap(True)
        main_layout.addWidget(cost_desc)

        # Option 3: Agricultural Optimization
        opt_button = QPushButton("⚖️  Agricultural Optimization")
        opt_button.setObjectName("optionButton")
        opt_button.setCursor(Qt.PointingHandCursor)
        opt_button.setFixedHeight(70)
        opt_button.clicked.connect(lambda: self.on_option_clicked("Agricultural Optimization"))
        main_layout.addWidget(opt_button)

        # Description for Agricultural Optimization
        opt_desc = QLabel(
            "Balanced approach considering both yield and cost factors. Find the optimal balance between maximizing production and minimizing expenses.")
        opt_desc.setStyleSheet(
            "font-size: 14px; color: #555555; padding: 10px 20px; background-color: #f0f9f0; border-radius: 5px; margin-bottom: 10px;")
        opt_desc.setWordWrap(True)
        main_layout.addWidget(opt_desc)

        # Add spacing
        main_layout.addSpacing(30)

        # Back button
        back_button = QPushButton("← Back to Welcome Page")
        back_button.setObjectName("backButton")
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.setFixedSize(200, 50)
        back_button.clicked.connect(self.on_back_clicked)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(back_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        # Status bar
        self.statusBar().showMessage("Select an optimization option to continue...")
        self.statusBar().setStyleSheet("background-color: #e8f5e9; color: #2d5016; font-weight: bold;")

    def on_option_clicked(self, option_name):
        """Handle option selection"""
        if option_name == "Yield Maximization":
            # Launch yield maximization page
            if YieldMaximizationPage:
                try:
                    self.yield_window = YieldMaximizationPage()
                    self.yield_window.show()
                    self.statusBar().showMessage(f"Opening {option_name} interface...")
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Failed to open {option_name} page:\n{str(e)}"
                    )
            else:
                QMessageBox.warning(
                    self,
                    "Feature Not Available",
                    "The Yield Maximization module is not available. Please ensure all required files are present."
                )
        
        elif option_name == "Cost Minimization":
            # Launch cost minimization page
            if CostMinimizationPage:
                try:
                    self.cost_window = CostMinimizationPage()
                    self.cost_window.show()
                    self.statusBar().showMessage(f"Opening {option_name} interface...")
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Failed to open {option_name} page:\n{str(e)}"
                    )
            else:
                QMessageBox.warning(
                    self,
                    "Feature Not Available",
                    "The Cost Minimization module is not available. Please ensure all required files are present."
                )
        
        else:
            # Agricultural Optimization
            if AgriculturalOptimizationPage:
                try:
                    self.agri_window = AgriculturalOptimizationPage()
                    self.agri_window.show()
                    self.statusBar().showMessage(f"Opening {option_name} interface...")
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Failed to open {option_name} page:\n{str(e)}"
                    )
            else:
                QMessageBox.warning(
                    self,
                    "Feature Not Available",
                    "The Agricultural Optimization module is not available. Please ensure all required files are present."
                )

        # Simple animation effect
        button = self.sender()
        if button:
            original_style = button.styleSheet()
            button.setStyleSheet(original_style + "background-color: #388e3c;")
            QTimer.singleShot(500, lambda: button.setStyleSheet(original_style))

    def on_back_clicked(self):
        self.close()


def main():
    app = QApplication(sys.argv)

    # Set the same font as welcome page
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = OptionsPage()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()