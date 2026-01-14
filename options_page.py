"""
Farm Optimization Options Page
Allows users to select between three optimization strategies:
1. Yield Maximization
2. Cost Minimization  
3. Agricultural Optimization (Balanced)
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

# Import optimization modules
try:
    from YieldMaximizationPage import YieldMaximizationPage
except ImportError:
    YieldMaximizationPage = None

try:
    from CostMinimizationPage import CostMinimizationPage
except ImportError:
    CostMinimizationPage = None

try:
    from AgriculturalOptimizationPage import AgriculturalOptimizationPage
except ImportError:
    AgriculturalOptimizationPage = None


class OptionsPage(QMainWindow):
    """
    Options page for selecting farm optimization strategy.
    Provides navigation to three different optimization approaches.
    """
    
    def __init__(self, parent_window=None):
        """
        Initialize the Options Page.
        
        Args:
            parent_window: Reference to the welcome page (test.py window)
                          Allows showing welcome page when going back
        """
        super().__init__()
        
        # Store reference to parent window (welcome page)
        self.parent_window = parent_window
        
        # Store references to opened optimization windows
        self.yield_window = None
        self.cost_window = None
        self.optimization_window = None
        
        # Window configuration
        self.setWindowTitle("Farm Optimization Options")
        self.setGeometry(100, 100, 900, 700)
        
        # Apply styling
        self._apply_styling()
        
        # Initialize UI
        self.init_ui()
    
    # ========================================================================
    # STYLING
    # ========================================================================
    
    def _apply_styling(self):
        """Apply consistent styling to the options page."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5fcf4;
            }
            QLabel {
                color: #2d5016;
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
            QPushButton#optionButton:pressed {
                background-color: #388e3c;
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
            QPushButton#backButton:pressed {
                background-color: #f57c00;
            }
            QLabel#descLabel {
                font-size: 14px;
                color: #555555;
                padding: 10px 20px;
                background-color: #f0f9f0;
                border-radius: 5px;
                margin-bottom: 10px;
            }
        """)
    
    # ========================================================================
    # UI INITIALIZATION
    # ========================================================================
    
    def init_ui(self):
        """Initialize the user interface components."""
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)
        
        # Add header
        header = self._create_header()
        main_layout.addLayout(header)
        
        # Add separator
        separator = self._create_separator()
        main_layout.addWidget(separator)
        
        # Add instruction label
        instruction = self._create_instruction_label()
        main_layout.addWidget(instruction)
        
        # Add spacing
        main_layout.addSpacing(20)
        
        # Add optimization options
        self._add_optimization_options(main_layout)
        
        # Add spacing
        main_layout.addSpacing(30)
        
        # Add back button
        back_layout = self._create_back_button()
        main_layout.addLayout(back_layout)
        
        # Setup status bar
        self.statusBar().showMessage("Select an optimization strategy to continue...")
        self.statusBar().setStyleSheet(
            "background-color: #e8f5e9; color: #2d5016; font-weight: bold;"
        )
    
    def _create_header(self):
        """Create the page header with icons and title."""
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        
        # Left icon
        left_icon = QLabel("🌾")
        left_icon.setStyleSheet("font-size: 40px;")
        header_layout.addWidget(left_icon)
        
        # Title
        title_label = QLabel("Choose Your Optimization Goal")
        title_label.setStyleSheet("""
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 28px;
            font-weight: bold;
            color: #2d5016;
            padding: 10px;
        """)
        header_layout.addWidget(title_label)
        
        # Right icon
        right_icon = QLabel("📊")
        right_icon.setStyleSheet("font-size: 40px;")
        header_layout.addWidget(right_icon)
        
        return header_layout
    
    def _create_separator(self):
        """Create a decorative separator line."""
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #c8e6c9; height: 2px;")
        return separator
    
    def _create_instruction_label(self):
        """Create the instruction label."""
        instruction = QLabel("Select the optimization strategy that best fits your needs:")
        instruction.setObjectName("titleLabel")
        instruction.setAlignment(Qt.AlignCenter)
        instruction.setWordWrap(True)
        return instruction
    
    def _add_optimization_options(self, layout):
        """Add all three optimization option buttons with descriptions."""
        
        # Option 1: Yield Maximization
        yield_button = self._create_option_button(
            "🌱  Yield Maximization",
            "yield"
        )
        layout.addWidget(yield_button)
        
        yield_desc = self._create_description_label(
            "Focus on maximum crop production. Uses premium inputs, advanced "
            "mechanization, and intensive farming practices. Best for commercial "
            "operations aiming for highest possible output."
        )
        layout.addWidget(yield_desc)
        
        # Option 2: Cost Minimization
        cost_button = self._create_option_button(
            "💰  Cost Minimization",
            "cost"
        )
        layout.addWidget(cost_button)
        
        cost_desc = self._create_description_label(
            "Minimize operational expenses using basic inputs, manual labor, and "
            "cost-effective methods. Ideal for small-scale farmers and those with "
            "limited budgets seeking sustainable returns."
        )
        layout.addWidget(cost_desc)
        
        # Option 3: Agricultural Optimization (Balanced)
        optimization_button = self._create_option_button(
            "⚖️  Agricultural Optimization (Balanced)",
            "optimization"
        )
        layout.addWidget(optimization_button)
        
        optimization_desc = self._create_description_label(
            "Balanced approach at 75% quality level. Combines good inputs with "
            "moderate mechanization for optimal returns. Perfect for most farmers "
            "seeking the best balance between cost and yield."
        )
        layout.addWidget(optimization_desc)
    
    def _create_option_button(self, text, option_type):
        """
        Create an option button.
        
        Args:
            text: Button text to display
            option_type: Type of option ('yield', 'cost', or 'optimization')
        
        Returns:
            QPushButton configured as an option button
        """
        button = QPushButton(text)
        button.setObjectName("optionButton")
        button.setCursor(Qt.PointingHandCursor)
        button.setFixedHeight(70)
        
        # Connect based on option type
        if option_type == "yield":
            button.clicked.connect(self.open_yield_maximization)
        elif option_type == "cost":
            button.clicked.connect(self.open_cost_minimization)
        else:  # optimization
            button.clicked.connect(self.open_agricultural_optimization)
        
        return button
    
    def _create_description_label(self, text):
        """
        Create a description label for an option.
        
        Args:
            text: Description text
        
        Returns:
            QLabel configured as description label
        """
        label = QLabel(text)
        label.setObjectName("descLabel")
        label.setWordWrap(True)
        return label
    
    def _create_back_button(self):
        """Create the back button layout."""
        back_button = QPushButton("← Back to Welcome Page")
        back_button.setObjectName("backButton")
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.setFixedSize(220, 50)
        back_button.clicked.connect(self.go_back_to_welcome)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(back_button)
        button_layout.addStretch()
        
        return button_layout
    
    # ========================================================================
    # NAVIGATION METHODS
    # ========================================================================
    
    def open_yield_maximization(self):
        """Open the Yield Maximization page."""
        if YieldMaximizationPage is None:
            self._show_module_unavailable_error("Yield Maximization")
            return
        
        try:
            # Close existing window if open
            if self.yield_window:
                self.yield_window.close()
            
            # Create and show new window with parent reference
            self.yield_window = YieldMaximizationPage(parent_window=self)
            self.yield_window.show()
            
            # Update status
            self.statusBar().showMessage("Opening Yield Maximization interface...")
            
            # Visual feedback
            self._provide_button_feedback(self.sender())
            
        except Exception as e:
            self._show_error("Yield Maximization", str(e))
    
    def open_cost_minimization(self):
        """Open the Cost Minimization page."""
        if CostMinimizationPage is None:
            self._show_module_unavailable_error("Cost Minimization")
            return
        
        try:
            # Close existing window if open
            if self.cost_window:
                self.cost_window.close()
            
            # Create and show new window with parent reference
            self.cost_window = CostMinimizationPage(parent_window=self)
            self.cost_window.show()
            
            # Update status
            self.statusBar().showMessage("Opening Cost Minimization interface...")
            
            # Visual feedback
            self._provide_button_feedback(self.sender())
            
        except Exception as e:
            self._show_error("Cost Minimization", str(e))
    
    def open_agricultural_optimization(self):
        """Open the Agricultural Optimization (Balanced) page."""
        if AgriculturalOptimizationPage is None:
            self._show_module_unavailable_error("Agricultural Optimization")
            return
        
        try:
            # Close existing window if open
            if self.optimization_window:
                self.optimization_window.close()
            
            # Create and show new window with parent reference
            self.optimization_window = AgriculturalOptimizationPage(parent_window=self)
            self.optimization_window.show()
            
            # Update status
            self.statusBar().showMessage("Opening Agricultural Optimization interface...")
            
            # Visual feedback
            self._provide_button_feedback(self.sender())
            
        except Exception as e:
            self._show_error("Agricultural Optimization", str(e))
    
    def go_back_to_welcome(self):
        """Navigate back to the welcome page."""
        # Close this options window
        self.close()
        
        # Show the welcome page if we have a reference
        if self.parent_window:
            self.parent_window.show()
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _provide_button_feedback(self, button):
        """
        Provide visual feedback when a button is clicked.
        
        Args:
            button: The button that was clicked
        """
        if button:
            original_style = button.styleSheet()
            button.setStyleSheet(original_style + "background-color: #388e3c;")
            QTimer.singleShot(500, lambda: button.setStyleSheet(original_style))
    
    def _show_module_unavailable_error(self, module_name):
        """
        Show error when a module is not available.
        
        Args:
            module_name: Name of the unavailable module
        """
        QMessageBox.warning(
            self,
            "Feature Not Available",
            f"The {module_name} module is not available.\n\n"
            f"Please ensure the following file exists:\n"
            f"• {module_name.replace(' ', '')}.py\n\n"
            f"Contact support if the problem persists."
        )
    
    def _show_error(self, module_name, error_message):
        """
        Show error dialog when opening a module fails.
        
        Args:
            module_name: Name of the module that failed
            error_message: Error message to display
        """
        QMessageBox.critical(
            self,
            "Error Opening Module",
            f"Failed to open {module_name} page.\n\n"
            f"Error details:\n{error_message}\n\n"
            f"Please check the module file and try again."
        )
    
    def closeEvent(self, event):
        """
        Handle window close event.
        Shows the parent window when this window closes.
        
        Args:
            event: The close event
        """
        if self.parent_window:
            self.parent_window.show()
        event.accept()


# ============================================================================
# MAIN EXECUTION (for testing)
# ============================================================================

def main():
    """Main application entry point for standalone testing."""
    app = QApplication(sys.argv)
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Create and show window
    window = OptionsPage()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()