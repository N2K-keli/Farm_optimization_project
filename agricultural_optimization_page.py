"""
Agricultural Optimization Page - UI for balanced farm optimization
"""
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from agricultural_optimization import AgriculturalOptimizationCalculator


class AgriculturalOptimizationPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agricultural Optimization - Farm Optimizer")
        self.setGeometry(100, 100, 1100, 850)
        
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
                background-color: #2196f3;
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                padding: 12px 30px;
                border: 2px solid #1976d2;
            }
            QPushButton#calculateButton:hover {
                background-color: #42a5f5;
            }
            QPushButton#backButton {
                background-color: #4caf50;
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px 20px;
                border: 2px solid #388e3c;
            }
            QPushButton#backButton:hover {
                background-color: #66bb6a;
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
            QRadioButton {
                font-size: 14px;
                color: #2d5016;
                spacing: 8px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #c8e6c9;
                border-radius: 9px;
                background-color: white;
            }
            QRadioButton::indicator:checked {
                background-color: #2196f3;
                border-color: #1976d2;
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
        icon_label = QLabel("⚖️")
        icon_label.setStyleSheet("font-size: 40px;")
        header_layout.addWidget(icon_label)
        
        title = QLabel("Agricultural Optimization Calculator")
        title.setObjectName("titleLabel")
        header_layout.addWidget(title)
        
        icon_label2 = QLabel("🎯")
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
            "Find the optimal balance between production and costs. This balanced strategy uses a mix of "
            "improved and traditional methods to achieve maximum profit efficiency (ROI) rather than just "
            "maximum yield or minimum cost."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 13px; color: #555; padding: 10px; background-color: #e3f2fd; border-radius: 5px;")
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
        
        # Optimization priority
        priority_layout = QVBoxLayout()
        
        self.balanced_radio = QRadioButton("Balanced (75% inputs - Recommended)")
        self.balanced_radio.setChecked(True)
        priority_layout.addWidget(self.balanced_radio)
        
        self.yield_focus_radio = QRadioButton("Yield-Focused (85% inputs - Higher production)")
        priority_layout.addWidget(self.yield_focus_radio)
        
        self.cost_focus_radio = QRadioButton("Cost-Focused (65% inputs - Lower investment)")
        priority_layout.addWidget(self.cost_focus_radio)
        
        input_layout.addRow("Optimization Priority:", priority_layout)
        
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # Strategy info
        strategy_info = QLabel(
            "⚖️ Agricultural Optimization Strategy:\n"
            "  • Improved seeds at 75% of optimal rate\n"
            "  • Balanced fertilizer (chemical + organic)\n"
            "  • Selective mechanization (cost-effective)\n"
            "  • Mixed labor (30% family, 70% hired)\n"
            "  • Supplementary irrigation when needed\n"
            "  • Improved post-harvest handling (-30% losses)\n"
            "  • Regional market sales (balanced prices)"
        )
        strategy_info.setWordWrap(True)
        strategy_info.setStyleSheet(
            "font-size: 12px; color: #555; padding: 15px; "
            "background-color: #e3f2fd; border-radius: 5px; border-left: 4px solid #2196f3;"
        )
        main_layout.addWidget(strategy_info)
        
        # Calculate button
        calc_button = QPushButton("⚖️ Calculate Optimized Plan")
        calc_button.setObjectName("calculateButton")
        calc_button.setCursor(Qt.PointingHandCursor)
        calc_button.clicked.connect(self.calculate_optimization)
        main_layout.addWidget(calc_button)
        
        # Results Section
        self.results_group = QGroupBox("Agricultural Optimization Results")
        results_layout = QVBoxLayout()
        results_layout.setContentsMargins(15, 20, 15, 15)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(350)
        self.results_text.setText("Click 'Calculate' to see your optimized agricultural plan...")
        results_layout.addWidget(self.results_text)
        
        self.results_group.setLayout(results_layout)
        self.results_group.setVisible(False)
        main_layout.addWidget(self.results_group)
        
        # Complete Strategy Comparison Section
        self.comparison_group = QGroupBox("Complete Strategy Comparison")
        comp_layout = QVBoxLayout()
        comp_layout.setContentsMargins(15, 20, 15, 15)
        
        self.comparison_text = QTextEdit()
        self.comparison_text.setReadOnly(True)
        self.comparison_text.setMaximumHeight(250)
        comp_layout.addWidget(self.comparison_text)
        
        self.comparison_group.setLayout(comp_layout)
        self.comparison_group.setVisible(False)
        main_layout.addWidget(self.comparison_group)
        
        # Sensitivity Analysis Section
        self.sensitivity_group = QGroupBox("Sensitivity Analysis")
        sens_layout = QVBoxLayout()
        sens_layout.setContentsMargins(15, 20, 15, 15)
        
        self.sensitivity_text = QTextEdit()
        self.sensitivity_text.setReadOnly(True)
        self.sensitivity_text.setMaximumHeight(300)
        sens_layout.addWidget(self.sensitivity_text)
        
        self.sensitivity_group.setLayout(sens_layout)
        self.sensitivity_group.setVisible(False)
        main_layout.addWidget(self.sensitivity_group)
        
        # Recommendations Section
        self.recommendations_group = QGroupBox("Optimization Recommendations")
        rec_layout = QVBoxLayout()
        rec_layout.setContentsMargins(15, 20, 15, 15)
        
        self.recommendations_text = QTextEdit()
        self.recommendations_text.setReadOnly(True)
        self.recommendations_text.setMaximumHeight(200)
        rec_layout.addWidget(self.recommendations_text)
        
        self.recommendations_group.setLayout(rec_layout)
        self.recommendations_group.setVisible(False)
        main_layout.addWidget(self.recommendations_group)
        
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
        self.statusBar().showMessage("Ready to calculate optimized agricultural plan...")
        self.statusBar().setStyleSheet("background-color: #e3f2fd; color: #1976d2; font-weight: bold;")
    
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
    
    def get_priority(self):
        """Get selected optimization priority"""
        if self.yield_focus_radio.isChecked():
            return 'yield_focus'
        elif self.cost_focus_radio.isChecked():
            return 'cost_focus'
        else:
            return 'balanced'
    
    def calculate_optimization(self):
        """Perform agricultural optimization calculation"""
        try:
            self.statusBar().showMessage("Calculating optimized agricultural plan...")
            QApplication.processEvents()
            
            # Get inputs
            crop = self.get_crop_key()
            land_size = self.land_size_input.value()
            priority = self.get_priority()
            
            # Create calculator
            calculator = AgriculturalOptimizationCalculator(crop, land_size, priority=priority)
            
            # Get results
            results = calculator.calculate_optimized_plan()
            
            # Display results
            self.display_results(results, calculator)
            
            # Show results sections
            self.results_group.setVisible(True)
            self.comparison_group.setVisible(True)
            self.sensitivity_group.setVisible(True)
            self.recommendations_group.setVisible(True)
            self.export_button.setVisible(True)
            
            self.statusBar().showMessage("Calculation complete! Review your optimized plan below.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            self.statusBar().showMessage("Error in calculation.")
    
    def display_results(self, results, calculator):
        """Display calculation results"""
        # Format main results
        output = "═══════════════════════════════════════════════════════════\n"
        output += f"   AGRICULTURAL OPTIMIZATION PLAN - {results['crop_type'].upper()}\n"
        output += "═══════════════════════════════════════════════════════════\n\n"
        
        output += "⚖️ STRATEGY: Balanced Agricultural Optimization\n"
        output += "  • Mix of improved and local methods\n"
        output += "  • Moderate chemical + organic fertilizers\n"
        output += "  • Selective mechanization\n"
        output += "  • Family + hired labor (30/70)\n"
        output += f"  • Input Level: {results['input_level_percentage']:.0f}%\n\n"
        
        output += f"🌾 FARM DETAILS:\n"
        output += f"   Land Size: {results['land_size_hectares']:.2f} hectares ({results['land_size_acres']:.2f} acres)\n"
        output += f"   Crop: {results['crop_type'].capitalize()}\n\n"
        
        output += f"💰 OPTIMIZED INVESTMENT:\n"
        output += f"   Total Cost:          {results['cost_breakdown']['total_cost']:>15,.0f} XAF\n"
        output += f"   Cost per Hectare:    {results['cost_per_hectare']:>15,.0f} XAF\n"
        output += f"   Cost per kg:         {results['cost_per_kg_produced']:>15,.0f} XAF/kg\n\n"
        
        output += "   Cost Breakdown:\n"
        for key, value in results['cost_breakdown'].items():
            if key != 'total_cost' and value > 0:
                output += f"     • {key.replace('_', ' ').title():20s}: {value:>12,.0f} XAF\n"
        output += "\n"
        
        output += f"📦 EXPECTED PRODUCTION:\n"
        output += f"   Yield per Hectare:   {results['expected_yield_per_ha_tons']:>15.2f} tons\n"
        output += f"   Total Production:    {results['total_production_tons']:>15.2f} tons\n"
        output += f"                        {results['total_production_kg']:>15,.0f} kg\n"
        output += f"   Marketable Prod.:    {results['marketable_production_tons']:>15.2f} tons\n"
        output += f"   Post-Harvest Loss:   {results['post_harvest_loss_percentage']:>15.1f} %\n"
        output += f"                        (Reduced by improved handling)\n\n"
        
        output += f"💵 REVENUE PROJECTIONS:\n"
        output += f"   Farmgate Price:      {results['farmgate_price_per_kg']:>15,.0f} XAF/kg\n"
        output += f"   Gross Revenue:       {results['gross_revenue']:>15,.0f} XAF\n"
        output += f"   Transport Cost:      {results['transportation_cost']:>15,.0f} XAF\n"
        output += f"   Net Revenue:         {results['net_revenue']:>15,.0f} XAF\n\n"
        
        output += f"📊 PROFITABILITY & EFFICIENCY:\n"
        profit_symbol = "✓" if results['net_profit'] > 0 else "✗"
        profit_status = "PROFIT" if results['net_profit'] > 0 else "LOSS"
        output += f"   Net {profit_status}:         {profit_symbol} {abs(results['net_profit']):>15,.0f} XAF\n"
        output += f"   Return on Investment:{results['roi_percentage']:>15.1f} %\n"
        output += f"   Profit per Hectare:  {results['profit_per_hectare']:>15,.0f} XAF/ha\n"
        output += f"   Profit per kg:       {results['profit_per_kg_produced']:>15,.0f} XAF/kg\n"
        output += f"   Break-Even Price:    {results['break_even_price_per_kg']:>15,.0f} XAF/kg\n\n"
        
        output += f"📅 CROP TIMELINE:\n"
        output += f"   Growing Period:      {results['growing_days']} days\n"
        output += f"   Seasons per Year:    {results['seasons_per_year']}\n"
        output += f"   Best Planting:       {', '.join(results['best_planting_months'])}\n"
        
        self.results_text.setText(output)
        
        # Display complete strategy comparison
        comparison = calculator.compare_all_strategies()
        comp_output = "═══════════════════════════════════════════════════════════\n"
        comp_output += "   Comparing ALL THREE Optimization Strategies\n"
        comp_output += "═══════════════════════════════════════════════════════════\n\n"
        
        comp_output += f"{'Strategy':<45} {'Cost':>12} {'Yield':>10} {'Profit':>15} {'ROI':>8}\n"
        comp_output += "-" * 95 + "\n"
        
        for key, data in comparison.items():
            if key != 'recommendations':
                comp_output += f"{data['strategy']:<45} {data['total_cost']:>12,.0f} {data['production_tons']:>10.2f}t {data['profit']:>15,.0f} {data['roi']:>7.1f}%\n"
        
        comp_output += "\n🏆 BEST STRATEGY FOR:\n"
        comp_output += f"  • Highest ROI:           {comparison['recommendations']['highest_roi']}\n"
        comp_output += f"  • Highest Total Profit:  {comparison['recommendations']['highest_profit']}\n"
        comp_output += f"  • Most Cost Efficient:   {comparison['recommendations']['most_efficient']}\n\n"
        
        comp_output += "💡 INSIGHT:\n"
        comp_output += "  Agricultural Optimization typically offers the best balance,\n"
        comp_output += "  achieving high profits with good ROI through efficient resource use.\n"
        
        self.comparison_text.setText(comp_output)
        
        # Display sensitivity analysis
        sensitivity = calculator.sensitivity_analysis()
        sens_output = "═══════════════════════════════════════════════════════════\n"
        sens_output += "   How Input Level Affects Profitability\n"
        sens_output += "═══════════════════════════════════════════════════════════\n\n"
        
        sens_output += f"{'Input%':<8} {'Cost':>12} {'Yield':>10} {'Profit':>15} {'ROI':>8} {'Profit/ha':>12}\n"
        sens_output += "-" * 70 + "\n"
        
        for scenario in sensitivity['scenarios']:
            sens_output += f"{scenario['input_level_pct']:>3.0f}%     {scenario['total_cost']:>12,.0f} {scenario['production_tons']:>10.2f}t "
            sens_output += f"{scenario['net_profit']:>15,.0f} {scenario['roi']:>7.1f}% {scenario['profit_per_ha']:>12,.0f}\n"
        
        sens_output += f"\n✓ OPTIMAL INPUT LEVEL: {sensitivity['recommended_input_level']}% for highest ROI\n"
        sens_output += f"  Expected Profit: {sensitivity['optimal_profit']:,.0f} XAF\n"
        sens_output += f"  Expected ROI: {sensitivity['optimal_roi']:.1f}%\n\n"
        
        sens_output += "📈 OBSERVATION:\n"
        sens_output += "  Profit increases with inputs, but ROI may decrease.\n"
        sens_output += "  The sweet spot balances total profit with efficiency.\n"
        
        self.sensitivity_text.setText(sens_output)
        
        # Display recommendations
        rec_output = ""
        for i, rec in enumerate(results['recommendations'], 1):
            icon = "✓" if rec['type'] == 'positive' else "⚠" if rec['type'] == 'warning' else "💡"
            rec_output += f"{icon} {rec['message']}\n\n"
        
        self.recommendations_text.setText(rec_output)
    
    def export_report(self):
        """Export results to a text file"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Report",
            f"agricultural_optimization_{self.get_crop_key()}.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("AGRICULTURAL OPTIMIZATION REPORT\n")
                    f.write("Generated by Farm Optimization System\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(self.results_text.toPlainText())
                    f.write("\n\n" + "=" * 60 + "\n")
                    f.write("STRATEGY COMPARISON:\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(self.comparison_text.toPlainText())
                    f.write("\n\n" + "=" * 60 + "\n")
                    f.write("SENSITIVITY ANALYSIS:\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(self.sensitivity_text.toPlainText())
                    f.write("\n\n" + "=" * 60 + "\n")
                    f.write("RECOMMENDATIONS:\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(self.recommendations_text.toPlainText())
                
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
    
    window = AgriculturalOptimizationPage()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()