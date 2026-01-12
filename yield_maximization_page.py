"""
Yield Maximization Page - UI for farm optimization
"""
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from yield_maximization import YieldMaximizationCalculator


class YieldMaximizationPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yield Maximization - Farm Optimizer")
        self.setGeometry(100, 100, 1100, 800)
        
        # Styling
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
            }
            QLabel#sectionLabel {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 18px;
                font-weight: bold;
                color: #2d5016;
                padding: 5px;
                background-color: #e8f5e9;
                border-radius: 5px;
            }
            QLabel {
                color: #2d5016;
            }
            QGroupBox {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                font-weight: bold;
                color: #2d5016;
                border: 2px solid #c8e6c9;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #c8e6c9;
                border-radius: 5px;
                background-color: white;
                color: #000000;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #2d5016;
            }
            QPushButton#calculateButton {
                background-color: #4caf50;
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                padding: 12px 30px;
                border: 2px solid #388e3c;
            }
            QPushButton#calculateButton:hover {
                background-color: #66bb6a;
            }
            QPushButton#backButton {
                background-color: #ff9800;
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px 20px;
                border: 2px solid #f57c00;
            }
            QPushButton#backButton:hover {
                background-color: #ffb74d;
            }
            QTextEdit {
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                border: 2px solid #c8e6c9;
                border-radius: 5px;
                background-color: #fafafa;
                padding: 10px;
                color: #000000;
            }
        """)
        
        self.init_ui()
    
    def init_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        scroll_widget = QWidget()
        main_layout = QVBoxLayout(scroll_widget)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        icon_label = QLabel("🌱")
        icon_label.setStyleSheet("font-size: 40px;")
        header_layout.addWidget(icon_label)
        
        title = QLabel("Yield Maximization Calculator")
        title.setObjectName("titleLabel")
        header_layout.addWidget(title)
        
        icon_label2 = QLabel("📈")
        icon_label2.setStyleSheet("font-size: 40px;")
        header_layout.addWidget(icon_label2)
        
        header_layout.addStretch()
        main_layout.addLayout(header_layout)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #c8e6c9; height: 2px;")
        main_layout.addWidget(separator)
        
        # Description
        desc = QLabel(
            "Enter your farm details below to calculate the optimal plan for maximum yield production. "
            "This analysis is based on current Cameroon agricultural data and market prices (2024-2025)."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 13px; color: #555; padding: 10px; background-color: #e8f5e9; border-radius: 5px;")
        main_layout.addWidget(desc)
        
        # Input Section
        input_group = QGroupBox("Farm Input Details")
        input_layout = QFormLayout()
        input_layout.setSpacing(15)
        input_layout.setContentsMargins(20, 20, 20, 20)
        
        # Crop selection
        self.crop_combo = QComboBox()
        self.crop_combo.addItems([
            "Maize (Corn)",
            "Rice", 
            "Cassava",
            "Groundnut (Peanuts)",
            "Beans"
        ])
        self.crop_combo.setCurrentIndex(0)
        input_layout.addRow("Select Crop:", self.crop_combo)
        
        # Land size
        land_layout = QHBoxLayout()
        self.land_size_input = QDoubleSpinBox()
        self.land_size_input.setMinimum(0.1)
        self.land_size_input.setMaximum(1000.0)
        self.land_size_input.setValue(1.0)
        self.land_size_input.setSingleStep(0.5)
        self.land_size_input.setDecimals(2)
        self.land_size_input.setSuffix(" hectares")
        land_layout.addWidget(self.land_size_input)
        
        # Acres display
        self.acres_label = QLabel("(≈ 2.47 acres)")
        self.acres_label.setStyleSheet("color: #666; font-size: 12px;")
        land_layout.addWidget(self.acres_label)
        land_layout.addStretch()
        
        self.land_size_input.valueChanged.connect(self.update_acres_display)
        
        input_layout.addRow("Land Size:", land_layout)
        
        # Region (optional)
        self.region_combo = QComboBox()
        self.region_combo.addItems([
            "All Regions (General)",
            "Humid Forest Zone (South, East, Centre, Littoral)",
            "High Plateau (West, Northwest)",
            "Sudano-Sahel (North, Far North, Adamawa)"
        ])
        input_layout.addRow("Your Region:", self.region_combo)
        
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # Calculate button
        calc_button = QPushButton("📊 Calculate Yield Maximization Plan")
        calc_button.setObjectName("calculateButton")
        calc_button.setCursor(Qt.PointingHandCursor)
        calc_button.clicked.connect(self.calculate_optimization)
        main_layout.addWidget(calc_button)
        
        # Results Section
        self.results_group = QGroupBox("Optimization Results")
        results_layout = QVBoxLayout()
        results_layout.setContentsMargins(15, 20, 15, 15)
        
        # Results text area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(300)
        self.results_text.setText("Click 'Calculate' to see your yield maximization plan...")
        results_layout.addWidget(self.results_text)
        
        self.results_group.setLayout(results_layout)
        self.results_group.setVisible(False)
        main_layout.addWidget(self.results_group)
        
        # Recommendations Section
        self.recommendations_group = QGroupBox("Recommendations & Best Practices")
        rec_layout = QVBoxLayout()
        rec_layout.setContentsMargins(15, 20, 15, 15)
        
        self.recommendations_text = QTextEdit()
        self.recommendations_text.setReadOnly(True)
        self.recommendations_text.setMaximumHeight(200)
        rec_layout.addWidget(self.recommendations_text)
        
        self.recommendations_group.setLayout(rec_layout)
        self.recommendations_group.setVisible(False)
        main_layout.addWidget(self.recommendations_group)
        
        # Farming Schedule Section
        self.schedule_group = QGroupBox("Farming Activities Schedule")
        schedule_layout = QVBoxLayout()
        schedule_layout.setContentsMargins(15, 20, 15, 15)
        
        self.schedule_text = QTextEdit()
        self.schedule_text.setReadOnly(True)
        self.schedule_text.setMaximumHeight(250)
        schedule_layout.addWidget(self.schedule_text)
        
        self.schedule_group.setLayout(schedule_layout)
        self.schedule_group.setVisible(False)
        main_layout.addWidget(self.schedule_group)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        
        back_button = QPushButton("← Back to Options")
        back_button.setObjectName("backButton")
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)
        
        button_layout.addStretch()
        
        export_button = QPushButton("📄 Export Report")
        export_button.setObjectName("backButton")
        export_button.setCursor(Qt.PointingHandCursor)
        export_button.clicked.connect(self.export_report)
        export_button.setVisible(False)
        self.export_button = export_button
        button_layout.addWidget(export_button)
        
        main_layout.addLayout(button_layout)
        
        scroll.setWidget(scroll_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll)
        
        # Status bar
        self.statusBar().showMessage("Ready to calculate yield maximization plan...")
        self.statusBar().setStyleSheet("background-color: #e8f5e9; color: #2d5016; font-weight: bold;")
    
    def update_acres_display(self, hectares):
        """Update acres display when hectares change"""
        acres = hectares * 2.471
        self.acres_label.setText(f"(≈ {acres:.2f} acres)")
    
    def get_crop_key(self):
        """Get crop key from combo box selection"""
        crop_text = self.crop_combo.currentText()
        crop_map = {
            "Maize (Corn)": "maize",
            "Rice": "rice",
            "Cassava": "cassava",
            "Groundnut (Peanuts)": "groundnut",
            "Beans": "beans"
        }
        return crop_map.get(crop_text, "maize")
    
    def calculate_optimization(self):
        """Perform yield maximization calculation"""
        try:
            self.statusBar().showMessage("Calculating optimization plan...")
            QApplication.processEvents()
            
            # Get inputs
            crop = self.get_crop_key()
            land_size = self.land_size_input.value()
            
            # Create calculator
            calculator = YieldMaximizationCalculator(crop, land_size)
            
            # Get results
            results = calculator.calculate_optimal_plan()
            
            # Display results
            self.display_results(results, calculator)
            
            # Show results sections
            self.results_group.setVisible(True)
            self.recommendations_group.setVisible(True)
            self.schedule_group.setVisible(True)
            self.export_button.setVisible(True)
            
            self.statusBar().showMessage("Calculation complete! Review your optimization plan below.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            self.statusBar().showMessage("Error in calculation.")
    
    def display_results(self, results, calculator):
        """Display calculation results"""
        # Format main results
        output = "═══════════════════════════════════════════════════════════\n"
        output += f"         YIELD MAXIMIZATION PLAN - {results['crop_type'].upper()}\n"
        output += "═══════════════════════════════════════════════════════════\n\n"
        
        output += f"🌾 FARM DETAILS:\n"
        output += f"   Land Size: {results['land_size_hectares']:.2f} hectares ({results['land_size_acres']:.2f} acres)\n"
        output += f"   Crop: {results['crop_type'].capitalize()}\n\n"
        
        output += f"💰 INVESTMENT REQUIRED:\n"
        output += f"   Total Cost:          {results['cost_breakdown']['total_cost']:>15,.0f} XAF\n"
        output += f"   Cost per Hectare:    {results['cost_per_hectare']:>15,.0f} XAF\n\n"
        
        output += "   Cost Breakdown:\n"
        for key, value in results['cost_breakdown'].items():
            if key != 'total_cost':
                output += f"     • {key.replace('_', ' ').title():20s}: {value:>12,.0f} XAF\n"
        output += "\n"
        
        output += f"📦 EXPECTED PRODUCTION:\n"
        output += f"   Yield per Hectare:   {results['expected_yield_per_ha_tons']:>15.2f} tons\n"
        output += f"   Total Production:    {results['total_production_tons']:>15.2f} tons\n"
        output += f"                        {results['total_production_kg']:>15,.0f} kg\n"
        output += f"   Marketable Prod.:    {results['marketable_production_tons']:>15.2f} tons\n"
        output += f"   Post-Harvest Loss:   {results['post_harvest_loss_percentage']:>15.1f} %\n"
        output += f"                        ({results['post_harvest_loss_tons']:.2f} tons)\n\n"
        
        output += f"💵 REVENUE PROJECTIONS:\n"
        output += f"   Farmgate Price:      {results['farmgate_price_per_kg']:>15,.0f} XAF/kg\n"
        output += f"   Gross Revenue:       {results['gross_revenue']:>15,.0f} XAF\n"
        output += f"   Transport Cost:      {results['transportation_cost']:>15,.0f} XAF\n"
        output += f"   Net Revenue:         {results['net_revenue']:>15,.0f} XAF\n\n"
        
        output += f"📊 PROFITABILITY ANALYSIS:\n"
        profit_symbol = "✓" if results['net_profit'] > 0 else "✗"
        profit_color = "PROFIT" if results['net_profit'] > 0 else "LOSS"
        output += f"   Net {profit_color}:         {profit_symbol} {abs(results['net_profit']):>15,.0f} XAF\n"
        output += f"   Return on Investment:{results['roi_percentage']:>15.1f} %\n"
        output += f"   Break-Even Price:    {results['break_even_price_per_kg']:>15,.0f} XAF/kg\n\n"
        
        output += f"📅 CROP TIMELINE:\n"
        output += f"   Growing Period:      {results['growing_days']} days\n"
        output += f"   Seasons per Year:    {results['seasons_per_year']}\n"
        output += f"   Best Planting:       {', '.join(results['best_planting_months'])}\n\n"
        
        # Comparison with basic farming
        comparison = calculator.compare_with_basic_farming()
        output += "═══════════════════════════════════════════════════════════\n"
        output += "   COMPARISON: Optimal vs Basic Farming\n"
        output += "═══════════════════════════════════════════════════════════\n\n"
        output += f"Additional Investment Needed:  {comparison['difference']['additional_investment']:>12,.0f} XAF\n"
        output += f"Additional Production Gained:  {comparison['difference']['additional_production']:>12.2f} tons\n"
        output += f"Additional Revenue Generated:  {comparison['difference']['additional_revenue']:>12,.0f} XAF\n"
        output += f"Additional Profit:             {comparison['difference']['additional_profit']:>12,.0f} XAF\n"
        output += f"ROI Improvement:               {comparison['difference']['roi_improvement']:>12.1f} %\n"
        
        self.results_text.setText(output)
        
        # Display recommendations
        rec_output = ""
        for i, rec in enumerate(results['recommendations'], 1):
            icon = "✓" if rec['type'] == 'positive' else "⚠" if rec['type'] == 'warning' else "💡"
            rec_output += f"{icon} {rec['message']}\n\n"
        
        self.recommendations_text.setText(rec_output)
        
        # Display farming schedule
        schedule = calculator.get_input_schedule()
        schedule_output = ""
        for stage in schedule:
            schedule_output += f"═══ {stage['stage']} ═══\n"
            schedule_output += f"Timing: {stage['timing']}\n\n"
            for activity in stage['activities']:
                schedule_output += f"  ✓ {activity}\n"
            schedule_output += "\n"
        
        self.schedule_text.setText(schedule_output)
    
    def export_report(self):
        """Export results to a text file"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Report",
            f"yield_maximization_{self.get_crop_key()}.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("YIELD MAXIMIZATION REPORT\n")
                    f.write("Generated by Farm Optimization System\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(self.results_text.toPlainText())
                    f.write("\n\n" + "=" * 60 + "\n")
                    f.write("RECOMMENDATIONS:\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(self.recommendations_text.toPlainText())
                    f.write("\n\n" + "=" * 60 + "\n")
                    f.write("FARMING SCHEDULE:\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(self.schedule_text.toPlainText())
                
                QMessageBox.information(self, "Success", f"Report exported successfully to:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export report:\n{str(e)}")
    
    def go_back(self):
        """Go back to options page"""
        self.close()


def main():
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = YieldMaximizationPage()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()