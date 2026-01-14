import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from options_page import OptionsPage

class FarmingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Farm Optimization Assistant")
        self.setGeometry(100, 100, 800, 500)
        
        # Set light greenish palette for the application
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5fcf4;
            }
            QLabel#welcomeLabel {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 28px;
                font-weight: bold;
                color: #2d5016;
                padding: 10px;
                background-color: #e8f5e9;
                border-radius: 10px;
                border: 2px solid #c8e6c9;
            }
            QPushButton#yesButton {
                background-color: #4caf50;
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 20px;
                font-weight: bold;
                border-radius: 15px;
                padding: 15px 30px;
                border: 3px solid #388e3c;
            }
            QPushButton#yesButton:hover {
                background-color: #66bb6a;
                border: 3px solid #4caf50;
            }
            QPushButton#yesButton:pressed {
                background-color: #388e3c;
            }
            QPushButton#noButton {
                background-color: #ff9800;
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 20px;
                font-weight: bold;
                border-radius: 15px;
                padding: 15px 30px;
                border: 3px solid #f57c00;
            }
            QPushButton#noButton:hover {
                background-color: #ffb74d;
                border: 3px solid #ff9800;
            }
            QPushButton#noButton:pressed {
                background-color: #f57c00;
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
        
        # Add a header with farming icon
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        
        # Create farming icon using QLabel (using emoji as simple icon)
        icon_label = QLabel("🌾")
        icon_label.setStyleSheet("font-size: 40px;")
        header_layout.addWidget(icon_label)
        
        header_label = QLabel("Farm Optimization Assistant")
        header_label.setStyleSheet("""
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 32px;
            font-weight: bold;
            color: #2d5016;
            padding: 10px;
        """)
        header_layout.addWidget(header_label)
        
        icon_label2 = QLabel("🚜")
        icon_label2.setStyleSheet("font-size: 40px;")
        header_layout.addWidget(icon_label2)
        
        main_layout.addLayout(header_layout)
        
        # Add decorative separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #c8e6c9; height: 2px;")
        main_layout.addWidget(separator)
        
        # Welcome message
        welcome_label = QLabel("Welcome dear farmer, ready for some optimization?")
        welcome_label.setObjectName("welcomeLabel")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setWordWrap(True)
        main_layout.addWidget(welcome_label)
        
        # Add some spacing
        main_layout.addSpacing(30)
        
        # Button section
        button_layout = QHBoxLayout()
        button_layout.setSpacing(40)
        
        # Yes button (green)
        self.yes_button = QPushButton("Yes")
        self.yes_button.setObjectName("yesButton")
        self.yes_button.setCursor(Qt.PointingHandCursor)
        self.yes_button.setFixedSize(200, 80)
        self.yes_button.clicked.connect(self.on_yes_clicked)
        
        # No button (sad color - orange)
        self.no_button = QPushButton("No")
        self.no_button.setObjectName("noButton")
        self.no_button.setCursor(Qt.PointingHandCursor)
        self.no_button.setFixedSize(200, 80)
        self.no_button.clicked.connect(self.on_no_clicked)
        
        button_layout.addStretch()
        button_layout.addWidget(self.yes_button)
        button_layout.addWidget(self.no_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        # Add some spacing
        main_layout.addSpacing(30)
        
        # Information section
        info_group = QGroupBox("How optimization can help your farm:")
        info_layout = QVBoxLayout()
        
        info_points = [
            "• Increase crop yield by up to 30%",
            "• Reduce water consumption with smart irrigation",
            "• Optimize fertilizer usage for better soil health",
            "• Plan planting schedules based on weather data",
            "• Reduce costs while increasing productivity"
        ]
        
        for point in info_points:
            point_label = QLabel(point)
            point_label.setStyleSheet("font-size: 14px; padding: 5px; color: #555555;")
            info_layout.addWidget(point_label)
        
        info_group.setLayout(info_layout)
        main_layout.addWidget(info_group)
        
        # Status bar
        self.statusBar().showMessage("Farm Optimization Assistant v1.0 | Ready to help optimize your farming operations")
        self.statusBar().setStyleSheet("background-color: #e8f5e9; color: #2d5016; font-weight: bold;")
    
    def on_yes_clicked(self):
        """
        FIXED: Now passes 'self' to OptionsPage so it can show this window again
        when the back button is clicked.
        """
        # Hide welcome page
        self.hide()
        
        # Create options page and pass reference to this window (self)
        # This allows the options page to show this window again when going back
        self.options_page = OptionsPage(parent_window=self)
        
        # Show options page
        self.options_page.show()

        # Update status
        self.statusBar().showMessage("Loading optimization options...")
    
    def on_no_clicked(self):
        reply = QMessageBox.question(
            self, 
            "Are you sure?", 
            "Optimization can significantly improve your farm's productivity.\n\n"
            "Are you sure you want to skip this opportunity?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            QMessageBox.information(
                self, 
                "We understand", 
                "We respect your decision. Feel free to come back anytime\n"
                "when you're ready to optimize your farming operations.\n\n"
                "Happy farming! 🌱"
            )
            self.statusBar().showMessage("Farm optimization declined. Ready when you are!")
        else:
            self.statusBar().showMessage("Great! Let's try the optimization option instead!")
    
    def reset_buttons(self):
        self.yes_button.setText("Yes")
        self.yes_button.setEnabled(True)
        self.statusBar().showMessage("Farm optimization complete! Check your personalized plan.")

def main():
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = FarmingApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()