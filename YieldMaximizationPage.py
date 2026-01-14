# yield_maximization_page.py
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class YieldMaximizationPage(QMainWindow):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("Yield Maximization - Farm Optimization")
        self.setGeometry(100, 100, 1000, 700)
        
        # Cameroon regions and their irrigation needs (as percentage)
        self.regions = {
            "Adamaoua": 0.35,
            "Centre": 0.25,
            "East": 0.30,
            "Far North": 0.55,
            "Littoral": 0.20,
            "North": 0.50,
            "Northwest": 0.30,
            "South": 0.20,
            "Southwest": 0.22,
            "West": 0.28
        }
        
        # Top 50 Cameroonian crops
        self.crops = [
            "Cassava", "Maize", "Plantain", "Cocoa", "Coffee (Robusta)",
            "Coffee (Arabica)", "Banana", "Yam", "Taro", "Rice",
            "Sorghum", "Millet", "Sweet Potato", "Irish Potato", "Beans",
            "Groundnut (Peanut)", "Cotton", "Oil Palm", "Rubber", "Sugar Cane",
            "Pineapple", "Tomato", "Onion", "Cabbage", "Carrot",
            "Pepper", "Okra", "Eggplant", "Cucumber", "Watermelon",
            "Papaya", "Mango", "Avocado", "Orange", "Grapefruit",
            "Lemon", "Guava", "Passion Fruit", "Soursop", "Coconut",
            "Cola Nut", "Ginger", "Garlic", "Soybean", "Cowpea",
            "Bambara Groundnut", "Melon", "Pumpkin", "Garden Egg", "African Spinach"
        ]
        
        # Land preparation cost (mechanized) per hectare in XAF
        self.land_prep_cost = 85000
        
        # Seed costs: [premium_price_per_kg, kg_needed_per_hectare]
        self.seed_costs = {
            "Cassava": [1500, 400],
            "Maize": [3500, 25],
            "Plantain": [2000, 1600],  # suckers
            "Cocoa": [4000, 15],
            "Coffee (Robusta)": [5000, 8],
            "Coffee (Arabica)": [6000, 8],
            "Banana": [1800, 1500],
            "Yam": [2500, 800],
            "Taro": [1200, 600],
            "Rice": [2800, 80],
            "Sorghum": [2200, 18],
            "Millet": [2000, 12],
            "Sweet Potato": [1000, 500],
            "Irish Potato": [1800, 2000],
            "Beans": [3000, 60],
            "Groundnut (Peanut)": [2500, 100],
            "Cotton": [4500, 30],
            "Oil Palm": [3500, 150],  # seedlings
            "Rubber": [5000, 400],  # seedlings
            "Sugar Cane": [1500, 8000],  # cuttings
            "Pineapple": [800, 40000],  # suckers
            "Tomato": [25000, 0.3],
            "Onion": [18000, 8],
            "Cabbage": [15000, 0.5],
            "Carrot": [12000, 4],
            "Pepper": [20000, 0.5],
            "Okra": [8000, 8],
            "Eggplant": [16000, 0.4],
            "Cucumber": [14000, 3],
            "Watermelon": [10000, 3],
            "Papaya": [5000, 0.5],
            "Mango": [4000, 100],  # seedlings
            "Avocado": [4500, 150],  # seedlings
            "Orange": [3800, 180],  # seedlings
            "Grapefruit": [3800, 170],
            "Lemon": [3500, 200],
            "Guava": [2500, 250],
            "Passion Fruit": [6000, 3],
            "Soursop": [4000, 200],
            "Coconut": [2500, 140],  # seedlings
            "Cola Nut": [5500, 20],
            "Ginger": [3500, 1500],
            "Garlic": [8000, 800],
            "Soybean": [2800, 75],
            "Cowpea": [2600, 65],
            "Bambara Groundnut": [2400, 90],
            "Melon": [7000, 3],
            "Pumpkin": [6000, 4],
            "Garden Egg": [18000, 0.4],
            "African Spinach": [5000, 6]
        }
        
        # Fertilizer costs: [premium_price_per_bag, bags_needed_per_hectare]
        # Each bag is typically 50kg
        self.fertilizer_costs = {
            "Cassava": [28000, 4],
            "Maize": [32000, 6],
            "Plantain": [30000, 5],
            "Cocoa": [35000, 4],
            "Coffee (Robusta)": [35000, 4],
            "Coffee (Arabica)": [35000, 4],
            "Banana": [30000, 5],
            "Yam": [28000, 4],
            "Taro": [26000, 4],
            "Rice": [33000, 6],
            "Sorghum": [30000, 4],
            "Millet": [28000, 3],
            "Sweet Potato": [25000, 3],
            "Irish Potato": [32000, 6],
            "Beans": [26000, 3],
            "Groundnut (Peanut)": [27000, 3],
            "Cotton": [38000, 5],
            "Oil Palm": [35000, 6],
            "Rubber": [32000, 5],
            "Sugar Cane": [35000, 8],
            "Pineapple": [30000, 5],
            "Tomato": [34000, 7],
            "Onion": [33000, 6],
            "Cabbage": [32000, 6],
            "Carrot": [31000, 5],
            "Pepper": [33000, 6],
            "Okra": [28000, 4],
            "Eggplant": [32000, 6],
            "Cucumber": [30000, 5],
            "Watermelon": [29000, 4],
            "Papaya": [30000, 5],
            "Mango": [33000, 4],
            "Avocado": [33000, 4],
            "Orange": [34000, 5],
            "Grapefruit": [34000, 5],
            "Lemon": [33000, 5],
            "Guava": [30000, 4],
            "Passion Fruit": [32000, 5],
            "Soursop": [31000, 4],
            "Coconut": [30000, 4],
            "Cola Nut": [33000, 4],
            "Ginger": [30000, 6],
            "Garlic": [32000, 7],
            "Soybean": [28000, 3],
            "Cowpea": [27000, 3],
            "Bambara Groundnut": [26000, 3],
            "Melon": [28000, 4],
            "Pumpkin": [27000, 4],
            "Garden Egg": [32000, 6],
            "African Spinach": [25000, 4]
        }
        
        # Pesticide costs: [premium_price_per_liter, liters_needed_per_hectare]
        self.pesticide_costs = {
            "Cassava": [15000, 6],
            "Maize": [18000, 8],
            "Plantain": [16000, 7],
            "Cocoa": [22000, 10],
            "Coffee (Robusta)": [20000, 9],
            "Coffee (Arabica)": [20000, 9],
            "Banana": [16000, 7],
            "Yam": [14000, 5],
            "Taro": [13000, 5],
            "Rice": [19000, 9],
            "Sorghum": [17000, 7],
            "Millet": [16000, 6],
            "Sweet Potato": [12000, 4],
            "Irish Potato": [18000, 8],
            "Beans": [14000, 5],
            "Groundnut (Peanut)": [15000, 6],
            "Cotton": [25000, 12],
            "Oil Palm": [20000, 8],
            "Rubber": [18000, 7],
            "Sugar Cane": [19000, 10],
            "Pineapple": [17000, 8],
            "Tomato": [22000, 12],
            "Onion": [20000, 10],
            "Cabbage": [19000, 9],
            "Carrot": [18000, 8],
            "Pepper": [21000, 11],
            "Okra": [16000, 7],
            "Eggplant": [20000, 10],
            "Cucumber": [18000, 8],
            "Watermelon": [17000, 7],
            "Papaya": [16000, 7],
            "Mango": [18000, 6],
            "Avocado": [18000, 6],
            "Orange": [19000, 7],
            "Grapefruit": [19000, 7],
            "Lemon": [18000, 7],
            "Guava": [16000, 6],
            "Passion Fruit": [19000, 8],
            "Soursop": [17000, 6],
            "Coconut": [16000, 5],
            "Cola Nut": [18000, 7],
            "Ginger": [17000, 8],
            "Garlic": [19000, 9],
            "Soybean": [15000, 5],
            "Cowpea": [14000, 5],
            "Bambara Groundnut": [14000, 5],
            "Melon": [16000, 6],
            "Pumpkin": [15000, 6],
            "Garden Egg": [20000, 10],
            "African Spinach": [13000, 5]
        }
        
        # Maximum irrigation cost per hectare (base)
        self.base_irrigation_cost = 180000
        
        # Maximum equipment cost per hectare (depreciation, maintenance, fuel)
        self.equipment_cost_per_hectare = 95000
        
        # Maximum labor cost per hectare for highly mechanized farm (20% of traditional)
        self.labor_cost_per_hectare = 120000
        
        # Transportation cost per ton to market
        self.transport_cost_per_ton = 8500
        
        # Storage cost per ton per month
        self.storage_cost_per_ton_month = 3500
        
        # Expected yields (tons per hectare) - premium conditions
        self.expected_yields = {
            "Cassava": 28,
            "Maize": 4.5,
            "Plantain": 18,
            "Cocoa": 1.2,
            "Coffee (Robusta)": 1.8,
            "Coffee (Arabica)": 1.5,
            "Banana": 35,
            "Yam": 22,
            "Taro": 12,
            "Rice": 5.5,
            "Sorghum": 3.5,
            "Millet": 2.8,
            "Sweet Potato": 16,
            "Irish Potato": 25,
            "Beans": 2.2,
            "Groundnut (Peanut)": 2.5,
            "Cotton": 2.8,
            "Oil Palm": 20,
            "Rubber": 2.0,
            "Sugar Cane": 80,
            "Pineapple": 45,
            "Tomato": 40,
            "Onion": 30,
            "Cabbage": 35,
            "Carrot": 28,
            "Pepper": 15,
            "Okra": 10,
            "Eggplant": 25,
            "Cucumber": 30,
            "Watermelon": 35,
            "Papaya": 50,
            "Mango": 15,
            "Avocado": 12,
            "Orange": 20,
            "Grapefruit": 18,
            "Lemon": 16,
            "Guava": 22,
            "Passion Fruit": 18,
            "Soursop": 14,
            "Coconut": 25,
            "Cola Nut": 1.5,
            "Ginger": 20,
            "Garlic": 8,
            "Soybean": 2.8,
            "Cowpea": 2.0,
            "Bambara Groundnut": 1.8,
            "Melon": 25,
            "Pumpkin": 20,
            "Garden Egg": 24,
            "African Spinach": 12
        }
        
        # Market prices per ton in XAF (approximate)
        self.market_prices = {
            "Cassava": 85000,
            "Maize": 220000,
            "Plantain": 180000,
            "Cocoa": 1800000,
            "Coffee (Robusta)": 1400000,
            "Coffee (Arabica)": 1600000,
            "Banana": 150000,
            "Yam": 200000,
            "Taro": 190000,
            "Rice": 350000,
            "Sorghum": 210000,
            "Millet": 200000,
            "Sweet Potato": 120000,
            "Irish Potato": 250000,
            "Beans": 450000,
            "Groundnut (Peanut)": 400000,
            "Cotton": 320000,
            "Oil Palm": 140000,
            "Rubber": 900000,
            "Sugar Cane": 65000,
            "Pineapple": 160000,
            "Tomato": 280000,
            "Onion": 320000,
            "Cabbage": 180000,
            "Carrot": 240000,
            "Pepper": 450000,
            "Okra": 350000,
            "Eggplant": 220000,
            "Cucumber": 200000,
            "Watermelon": 140000,
            "Papaya": 130000,
            "Mango": 180000,
            "Avocado": 380000,
            "Orange": 200000,
            "Grapefruit": 190000,
            "Lemon": 220000,
            "Guava": 160000,
            "Passion Fruit": 280000,
            "Soursop": 250000,
            "Coconut": 120000,
            "Cola Nut": 1200000,
            "Ginger": 550000,
            "Garlic": 650000,
            "Soybean": 380000,
            "Cowpea": 420000,
            "Bambara Groundnut": 380000,
            "Melon": 170000,
            "Pumpkin": 150000,
            "Garden Egg": 260000,
            "African Spinach": 320000
        }
        
        # Storage duration in months (typical)
        self.storage_months = 2
        
        # FIXED: Updated styling with better text contrast
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5fcf4;
            }
            QLabel {
                font-size: 13px;
                color: #1b3a0f;
            }
            QLabel#headerLabel {
                font-size: 22px;
                font-weight: bold;
                color: #2d5016;
                padding: 8px;
                background-color: #e8f5e9;
                border-radius: 8px;
            }
            QPushButton#calculateButton {
                background-color: #4caf50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                padding: 12px 25px;
                border: 2px solid #388e3c;
            }
            QPushButton#calculateButton:hover {
                background-color: #66bb6a;
            }
            QPushButton#backButton {
                background-color: #ff9800;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px 15px;
                border: 2px solid #f57c00;
            }
            QPushButton#backButton:hover {
                background-color: #ffb74d;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 2px solid #c8e6c9;
                border-radius: 5px;
                background-color: white;
                font-size: 13px;
                color: #1b3a0f;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #4caf50;
            }
            QTextEdit {
                border: 2px solid #c8e6c9;
                border-radius: 5px;
                background-color: white;
                padding: 10px;
                font-size: 12px;
                color: #1b3a0f;
                font-family: 'Consolas', 'Courier New', monospace;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #c8e6c9;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #e8f5e9;
                color: #1b3a0f;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #1b3a0f;
                selection-background-color: #4caf50;
                selection-color: white;
            }
        """)
        
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)
        
        # Header
        header = QLabel("Yield Maximization Calculator")
        header.setObjectName("headerLabel")
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        # Scroll area for inputs
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(15)
        
        # Input section
        input_group = QGroupBox("Farm Details")
        input_layout = QFormLayout()
        input_layout.setSpacing(12)
        
        # Land size
        self.land_size_input = QLineEdit()
        self.land_size_input.setPlaceholderText("Enter land size in hectares")
        input_layout.addRow("Land Size (hectares):", self.land_size_input)
        
        # Region selection
        self.region_combo = QComboBox()
        self.region_combo.addItems(sorted(self.regions.keys()))
        input_layout.addRow("Region:", self.region_combo)
        
        # Crop selection
        self.crop_combo = QComboBox()
        self.crop_combo.addItems(self.crops)
        input_layout.addRow("Select Crop:", self.crop_combo)
        
        input_group.setLayout(input_layout)
        scroll_layout.addWidget(input_group)
        
        # Calculate button
        calc_btn = QPushButton("Calculate Optimization Plan")
        calc_btn.setObjectName("calculateButton")
        calc_btn.setCursor(Qt.PointingHandCursor)
        calc_btn.clicked.connect(self.calculate_optimization)
        scroll_layout.addWidget(calc_btn)
        
        # Results section
        results_group = QGroupBox("Optimization Results")
        results_layout = QVBoxLayout()
        
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setMinimumHeight(300)
        results_layout.addWidget(self.results_display)
        
        results_group.setLayout(results_layout)
        scroll_layout.addWidget(results_group)
        
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        # Back button
        back_btn = QPushButton("← Back to Options")
        back_btn.setObjectName("backButton")
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(self.go_back)
        back_btn.setFixedWidth(150)
        main_layout.addWidget(back_btn, alignment=Qt.AlignLeft)
        
        self.statusBar().showMessage("Enter your farm details to calculate optimization plan")
        self.statusBar().setStyleSheet("background-color: #e8f5e9; color: #2d5016; font-weight: bold;")
    
    def calculate_optimization(self):
        try:
            # Get inputs
            land_size = float(self.land_size_input.text())
            if land_size <= 0:
                raise ValueError("Land size must be positive")
            
            region = self.region_combo.currentText()
            crop = self.crop_combo.currentText()
            
            # Calculate costs
            land_prep = self.land_prep_cost * land_size
            
            seed_data = self.seed_costs[crop]
            seed_cost = seed_data[0] * seed_data[1] * land_size
            
            fert_data = self.fertilizer_costs[crop]
            fertilizer_cost = fert_data[0] * fert_data[1] * land_size
            
            pest_data = self.pesticide_costs[crop]
            pesticide_cost = pest_data[0] * pest_data[1] * land_size
            
            irrigation_percentage = self.regions[region]
            irrigation_cost = self.base_irrigation_cost * irrigation_percentage * land_size
            
            equipment_cost = self.equipment_cost_per_hectare * land_size
            
            labor_cost = self.labor_cost_per_hectare * land_size
            
            # Expected yield
            expected_yield = self.expected_yields[crop] * land_size
            
            # Transportation and storage
            transport_cost = self.transport_cost_per_ton * expected_yield
            storage_cost = self.storage_cost_per_ton_month * self.storage_months * expected_yield
            
            # Total investment
            total_cost = (land_prep + seed_cost + fertilizer_cost + pesticide_cost + 
                        irrigation_cost + equipment_cost + labor_cost + 
                        transport_cost + storage_cost)
            
            # Expected revenue
            market_price = self.market_prices[crop]
            expected_revenue = expected_yield * market_price
            
            # Expected profit
            expected_profit = expected_revenue - total_cost
            roi = (expected_profit / total_cost) * 100 if total_cost > 0 else 0
            
            # Format results
            results = f"""
╔═══════════════════════════════════════════════════════════╗
║          YIELD MAXIMIZATION OPTIMIZATION PLAN             ║
╚═══════════════════════════════════════════════════════════╝

📍 FARM INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Land Size: {land_size:,.2f} hectares
  • Region: {region}
  • Crop: {crop}
  • Irrigation Need: {irrigation_percentage*100:.0f}%

💰 INVESTMENT BREAKDOWN (XAF)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. Land Preparation (Mechanized):     {land_prep:>15,.0f}
  2. Premium Seeds:                      {seed_cost:>15,.0f}
  3. Premium Fertilizers:                {fertilizer_cost:>15,.0f}
  4. Premium Pesticides:                 {pesticide_cost:>15,.0f}
  5. Irrigation System:                  {irrigation_cost:>15,.0f}
  6. Equipment (Depreciation/Fuel):      {equipment_cost:>15,.0f}
  7. Labor Costs:                        {labor_cost:>15,.0f}
  8. Transportation Costs:               {transport_cost:>15,.0f}
  9. Storage Costs ({self.storage_months} months):          {storage_cost:>15,.0f}
  ────────────────────────────────────────────────────────
  TOTAL INVESTMENT REQUIRED:           {total_cost:>15,.0f}

📊 EXPECTED RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Expected Yield: {expected_yield:,.2f} tons
  • Market Price: {market_price:,.0f} XAF/ton
  • Expected Revenue: {expected_revenue:,.0f} XAF
  • Expected Profit: {expected_profit:,.0f} XAF
  • Return on Investment (ROI): {roi:,.1f}%

📈 INVESTMENT PER HECTARE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Total Cost/Hectare: {total_cost/land_size:,.0f} XAF
  • Expected Revenue/Hectare: {expected_revenue/land_size:,.0f} XAF
  • Expected Profit/Hectare: {expected_profit/land_size:,.0f} XAF

✅ RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            
            if roi > 50:
                results += "  ★ Excellent investment opportunity with high returns!\n"
            elif roi > 20:
                results += "  ★ Good investment with solid profit potential.\n"
            elif roi > 0:
                results += "  ★ Positive returns, consider market conditions.\n"
            else:
                results += "  ⚠ Negative returns projected. Review strategy or crop choice.\n"
            
            results += f"""
  • Use premium certified seeds for maximum yield
  • Implement mechanized farming for efficiency
  • Follow optimal irrigation schedule for {region}
  • Apply fertilizers according to soil test results
  • Monitor crop regularly for pest management
  • Plan harvest timing for best market prices

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Note: These are optimized estimates based on premium inputs
and best agricultural practices. Actual results may vary based
on weather conditions, market fluctuations, and management.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            
            self.results_display.setPlainText(results)
            self.statusBar().showMessage(f"Optimization calculated for {land_size} hectares of {crop}")
            
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", 
                              f"Please enter valid numbers.\n\nError: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Calculation Error", 
                               f"An error occurred during calculation:\n\n{str(e)}")
    
    def go_back(self):
        self.close()
        if self.parent_window:
            self.parent_window.show()
    
    def closeEvent(self, event):
        if self.parent_window:
            self.parent_window.show()
        event.accept()


def main():
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = YieldMaximizationPage()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()