"""
Cost Minimization Page - UI for farm optimization
"""
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from cost_minimization import CostMinimizationCalculator


class CostMinimizationPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cost Minimization - Farm Optimizer")
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
                background-color: #ff9800;
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                padding: 12px 30px;
                border: 2px solid #f57c00;
            }
            QPushButton#calculateButton:hover {
                background-color: #ffb74d;
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
            QCheckBox {
                font-size: 14px;
                color: #2d5016;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #c8e6c9;
                border-radius: 4px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #4caf50;
                border-color: #388e3c;
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
        icon_label = QLabel("💰")
        icon_label.setStyleSheet("font-size: 40px;")
        header_layout.addWidget(icon_label)
        
        title = QLabel("Cost Minimization Calculator")
        title.setObjectName("titleLabel")
        header_layout.addWidget(title)
        
        icon_label2 = QLabel("📉")
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
            "Calculate the most cost-effective farming plan that minimizes expenses while achieving your goals. "
            "This strategy uses local seeds, organic fertilizers, family labor, and rain-fed cultivation to keep costs low."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 13px; color: #555; padding: 10px; background-color: #fff3e0; border-radius: 5px;")
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
        
        # Budget constraint (optional)
        budget_layout = QVBoxLayout()
        
        self.budget_checkbox = QCheckBox("I have a specific budget limit")
        self.budget_checkbox.stateChanged.connect(self.toggle_budget_input)
        budget_layout.addWidget(self.budget_checkbox)
        
        budget_input_layout = QHBoxLayout()
        self.budget_input = QSpinBox()
        self.budget_input.setMinimum(50000)
        self.budget_input.setMaximum(100000000)
        self.budget_input.setValue(500000)
        self.budget_input.setSingleStep(50000)
        self.budget_input.setSuffix(" XAF")
        self.budget_input.setEnabled(False)
        budget_input_layout.addWidget(self.budget_input)
        budget_input_layout.addStretch()
        
        budget_layout.addLayout(budget_input_layout)
        input_layout.addRow("Budget (Optional):", budget_layout)
        
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # Strategy info
        strategy_info = QLabel(
            "💡 Cost Minimization Strategy:\n"
            "  • Local seed varieties (cheaper, adapted)\n"
            "  • Organic manure instead of chemical fertilizers\n"
            "  • Family/community labor exchange\n"
            "  • Rain-fed cultivation (no irrigation cost)\n"
            "  • Manual methods where possible\n"
            "  • Local market sales (low transport cost)"
        )
        strategy_info.setWordWrap(True)
        strategy_info.setStyleSheet(
            "font-size: 12px; color: #555; padding: 15px; "
            "background-color: #e8f5e9; border-radius: 5px; border-left: 4px solid #4caf50;"
        )
        main_layout.addWidget(strategy_info)
        
        # Calculate button
        calc_button = QPushButton("💰 Calculate Minimal Cost Plan")
        calc_button.setObjectName("calculateButton")
        calc_button.setCursor(Qt.PointingHandCursor)
        calc_button.clicked.connect(self.calculate_optimization)
        main_layout.addWidget(calc_button)
        
        # Results Section
        self.results_group = QGroupBox("Cost Minimization Results")
        results_layout = QVBoxLayout()
        results_layout.setContentsMargins(15, 20, 15, 15)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(300)
        self.results_text.setText("Click 'Calculate' to see your cost minimization plan...")
        results_layout.addWidget(self.results_text)
        
        self.results_group.setLayout(results_layout)
        self.results_group.setVisible(False)
        main_layout.addWidget(self.results_group)
        
        # Strategy Comparison Section
        self.comparison_group = QGroupBox("Strategy Comparison")
        comp_layout = QVBoxLayout()
        comp_layout.setContentsMargins(15, 20, 15, 15)
        
        self.comparison_text = QTextEdit()
        self.comparison_text.setReadOnly(True)
        self.comparison_text.setMaximumHeight(250)
        comp_layout.addWidget(self.comparison_text)
        
        self.comparison_group.setLayout(comp_layout)
        self.comparison_group.setVisible(False)
        main_layout.addWidget(self.comparison_group)
        
        # Recommendations Section
        self.recommendations_group = QGroupBox("Cost-Saving Recommendations")
        rec_layout = QVBoxLayout()
        rec_layout.setContentsMargins(15, 20, 15, 15)
        
        self.recommendations_text = QTextEdit()
        self.recommendations_text.setReadOnly(True)
        self.recommendations_text.setMaximumHeight(200)
        rec_layout.addWidget(self.recommendations_text)
        
        self.recommendations_group.setLayout(rec_layout)
        self.recommendations_group.setVisible(False)
        main_layout.addWidget(self.recommendations_group)
        
        # Budget Analysis Section (shown only if budget specified)
        self.budget_group = QGroupBox("Budget Analysis")
        budget_layout_result = QVBoxLayout()
        budget_layout_result.setContentsMargins(15, 20, 15, 15)
        
        self.budget_text = QTextEdit()
        self.budget_text.setReadOnly(True)
        self.budget_text.setMaximumHeight(200)
        budget_layout_result.addWidget(self.budget_text)
        
        self.budget_group.setLayout(budget_layout_result)
        self.budget_group.setVisible(False)
        main_layout.addWidget(self.budget_group)
        
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
        self.statusBar().showMessage("Ready to calculate minimal cost plan...")
        self.statusBar().setStyleSheet("background-color: #fff3e0; color: #e65100; font-weight: bold;")
    
    def update_acres_display(self, hectares):
        """Update acres display when hectares change"""
        acres = hectares * 2.471
        self.acres_label.setText(f"(≈ {acres:.2f} acres)")
    
    def toggle_budget_input(self, state):
        """Enable/disable budget input based on checkbox"""
        self.budget_input.setEnabled(state == Qt.Checked)
    
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
        """Perform cost minimization calculation"""
        try:
            self.statusBar().showMessage("Calculating minimal cost plan...")
            QApplication.processEvents()
            
            # Get inputs
            crop = self.get_crop_key()
            land_size = self.land_size_input.value()
            budget = self.budget_input.value() if self.budget_checkbox.isChecked() else None
            
            # Create calculator
            calculator = CostMinimizationCalculator(crop, land_size, budget=budget)
            
            # Get results
            results = calculator.calculate_minimal_plan()
            
            # Display results
            self.display_results(results, calculator)
            
            # Show results sections
            self.results_group.setVisible(True)
            self.comparison_group.setVisible(True)
            self.recommendations_group.setVisible(True)
            self.export_button.setVisible(True)
            
            # Show budget section if budget was specified
            if budget:
                self.budget_group.setVisible(True)
            else:
                self.budget_group.setVisible(False)
            
            self.statusBar().showMessage("Calculation complete! Review your minimal cost plan below.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            self.statusBar().showMessage("Error in calculation.")
    
    def display_results(self, results, calculator):
        """Display calculation results"""
        # Format main results
        output = "═══════════════════════════════════════════════════════════\n"
        output += f"      COST MINIMIZATION PLAN - {results['crop_type'].upper()}\n"
        output += "═══════════════════════════════════════════════════════════\n\n"
        
        output += "📋 STRATEGY: Minimal Cost Approach\n"
        output += "  • Local seed varieties\n"
        output += "  • Organic-focused fertilization\n"
        output += "  • Manual/family labor prioritized\n"
        output += "  • Rain-fed cultivation\n"
        output += "  • Local market sales\n\n"
        
        output += f"🌾 FARM DETAILS:\n"
        output += f"   Land Size: {results['land_size_hectares']:.2f} hectares ({results['land_size_acres']:.2f} acres)\n"
        output += f"   Crop: {results['crop_type'].capitalize()}\n\n"
        
        output += f"💰 MINIMAL INVESTMENT:\n"
        output += f"   Total Cost:          {results['cost_breakdown']['total_cost']:>15,.0f} XAF\n"
        output += f"   Cost per Hectare:    {results['cost_per_hectare']:>15,.0f} XAF\n\n"
        
        output += "   Cost Breakdown:\n"
        for key, value in results['cost_breakdown'].items():
            if key != 'total_cost' and value > 0:
                output += f"     • {key.replace('_', ' ').title():20s}: {value:>12,.0f} XAF\n"
        output += "\n"
        
        if results['budget_specified']:
            output += f"📊 BUDGET STATUS:\n"
            status = "✓ WITHIN BUDGET" if results['within_budget'] else "✗ OVER BUDGET"
            output += f"   Budget Limit:        {results['budget_specified']:>15,.0f} XAF\n"
            output += f"   Budget Used:         {results['cost_breakdown']['total_cost']:>15,.0f} XAF\n"
            output += f"   Remaining:           {results['budget_remaining']:>15,.0f} XAF\n"
            output += f"   Status:              {status}\n\n"
        
        output += f"📦 EXPECTED PRODUCTION:\n"
        output += f"   Yield per Hectare:   {results['expected_yield_per_ha_tons']:>15.2f} tons\n"
        output += f"   Total Production:    {results['total_production_tons']:>15.2f} tons\n"
        output += f"                        {results['total_production_kg']:>15,.0f} kg\n"
        output += f"   Marketable Prod.:    {results['marketable_production_tons']:>15.2f} tons\n"
        output += f"   Post-Harvest Loss:   {results['post_harvest_loss_percentage']:>15.1f} %\n\n"
        
        output += f"💵 REVENUE PROJECTIONS:\n"
        output += f"   Farmgate Price:      {results['farmgate_price_per_kg']:>15,.0f} XAF/kg\n"
        output += f"   Gross Revenue:       {results['gross_revenue']:>15,.0f} XAF\n"
        output += f"   Transport Cost:      {results['transportation_cost']:>15,.0f} XAF\n"
        output += f"   Net Revenue:         {results['net_revenue']:>15,.0f} XAF\n\n"
        
        output += f"📊 PROFITABILITY:\n"
        profit_symbol = "✓" if results['net_profit'] > 0 else "✗"
        profit_status = "PROFIT" if results['net_profit'] > 0 else "LOSS"
        output += f"   Net {profit_status}:         {profit_symbol} {abs(results['net_profit']):>15,.0f} XAF\n"
        output += f"   Return on Investment:{results['roi_percentage']:>15.1f} %\n"
        output += f"   Break-Even Price:    {results['break_even_price_per_kg']:>15,.0f} XAF/kg\n\n"
        
        output += f"📅 CROP TIMELINE:\n"
        output += f"   Growing Period:      {results['growing_days']} days\n"
        output += f"   Seasons per Year:    {results['seasons_per_year']}\n"
        output += f"   Best Planting:       {', '.join(results['best_planting_months'])}\n"
        
        self.results_text.setText(output)
        
        # Display strategy comparison
        comparison = calculator.compare_strategies()
        comp_output = "═══════════════════════════════════════════════════════════\n"
        comp_output += "   Comparing Different Investment Strategies\n"
        comp_output += "═══════════════════════════════════════════════════════════\n\n"
        
        comp_output += f"{'Strategy':<40} {'Cost':>12} {'Yield':>10} {'Profit':>15} {'ROI':>8}\n"
        comp_output += "-" * 90 + "\n"
        
        for key, data in comparison.items():
            comp_output += f"{data['strategy']:<40} {data['total_cost']:>12,.0f} {data['production_tons']:>10.2f}t {data['profit']:>15,.0f} {data['roi']:>7.1f}%\n"
        
        comp_output += "\n💡 INSIGHT:\n"
        comp_output += "  Minimal cost strategy uses less investment but produces lower yield.\n"
        comp_output += "  However, it still offers good ROI if budget is tight.\n"
        comp_output += "  Consider medium input if you can afford extra investment.\n"
        
        self.comparison_text.setText(comp_output)
        
        # Display recommendations
        rec_output = ""
        for i, rec in enumerate(results['recommendations'], 1):
            icon = "✓" if rec['type'] == 'positive' else "⚠" if rec['type'] == 'warning' else "💡"
            rec_output += f"{icon} {rec['message']}\n\n"
        
        self.recommendations_text.setText(rec_output)
        
        # Display budget analysis if budget was specified
        if results['budget_specified']:
            budget_analysis = calculator.optimize_within_budget()
            if budget_analysis:
                budget_output = ""
                budget_output += f"Feasibility: {'✓ YES' if budget_analysis['feasible'] else '✗ NO'}\n\n"
                budget_output += f"Message: {budget_analysis['message']}\n\n"
                
                if 'suggestions' in budget_analysis:
                    budget_output += "Suggestions for Remaining Budget:\n"
                    for suggestion in budget_analysis['suggestions']:
                        budget_output += f"  • {suggestion}\n"
                elif 'alternative' in budget_analysis:
                    budget_output += f"Alternative: {budget_analysis['alternative']}\n"
                
                self.budget_text.setText(budget_output)
    
    def export_report(self):
        """Export results to a text file"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Report",
            f"cost_minimization_{self.get_crop_key()}.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("COST MINIMIZATION REPORT\n")
                    f.write("Generated by Farm Optimization System\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(self.results_text.toPlainText())
                    f.write("\n\n" + "=" * 60 + "\n")
                    f.write("STRATEGY COMPARISON:\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(self.comparison_text.toPlainText())
                    f.write("\n\n" + "=" * 60 + "\n")
                    f.write("RECOMMENDATIONS:\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(self.recommendations_text.toPlainText())
                    if self.budget_group.isVisible():
                        f.write("\n\n" + "=" * 60 + "\n")
                        f.write("BUDGET ANALYSIS:\n")
                        f.write("=" * 60 + "\n\n")
                        f.write(self.budget_text.toPlainText())
                
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
    
    window = CostMinimizationPage()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()