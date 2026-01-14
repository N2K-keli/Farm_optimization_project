"""
Farm Cost Minimization Calculator
A PySide6 application for optimizing farm costs in Cameroon regions.
Focuses on manual labor and basic inputs to minimize expenses.
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QTextEdit,
    QScrollArea, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class CostMinimizationPage(QMainWindow):
    """
    Main window for calculating farm cost minimization strategies.
    Provides budget allocation recommendations for Cameroonian farmers.
    """
    
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        
        # Window configuration
        self.setWindowTitle("Cost Minimization - Farm Optimization")
        self.setGeometry(100, 100, 1000, 700)
        
        # Initialize data
        self._initialize_regional_data()
        self._initialize_crop_data()
        self._initialize_cost_structure()
        self._initialize_market_data()
        
        # Setup UI
        self._apply_styling()
        self.init_ui()
    
    # ========================================================================
    # DATA INITIALIZATION
    # ========================================================================
    
    def _initialize_regional_data(self):
        """Initialize Cameroon regions and their irrigation requirements."""
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
    
    def _initialize_crop_data(self):
        """Initialize the list of 50 major Cameroonian crops."""
        self.crops = [
            # Staple crops
            "Cassava", "Maize", "Plantain", "Yam", "Taro", "Rice",
            "Sorghum", "Millet", "Sweet Potato", "Irish Potato",
            
            # Cash crops
            "Cocoa", "Coffee (Robusta)", "Coffee (Arabica)", "Cotton",
            "Oil Palm", "Rubber", "Sugar Cane",
            
            # Fruits
            "Banana", "Pineapple", "Watermelon", "Papaya", "Mango",
            "Avocado", "Orange", "Grapefruit", "Lemon", "Guava",
            "Passion Fruit", "Soursop", "Coconut",
            
            # Vegetables
            "Tomato", "Onion", "Cabbage", "Carrot", "Pepper", "Okra",
            "Eggplant", "Cucumber", "Pumpkin", "Garden Egg", "African Spinach",
            
            # Legumes and nuts
            "Beans", "Groundnut (Peanut)", "Soybean", "Cowpea",
            "Bambara Groundnut", "Cola Nut",
            
            # Other crops
            "Melon", "Ginger", "Garlic"
        ]
    
    def _initialize_cost_structure(self):
        """Initialize all cost structures for farming operations."""
        
        # Base costs (XAF per hectare)
        self.land_prep_cost = 35_000  # Manual clearing and tilling
        self.base_irrigation_cost = 45_000  # Manual/gravity-fed irrigation
        self.equipment_cost_per_hectare = 15_000  # Hand tools
        self.labor_cost_per_hectare = 250_000  # Manual labor
        
        # Transportation and storage costs
        self.transport_cost_per_ton = 5_000  # Local transport
        self.storage_cost_per_ton_month = 1_500  # Basic storage
        self.storage_months = 2  # Typical storage duration
        
        # Seed costs: [price_per_kg, kg_needed_per_hectare]
        self.seed_costs = {
            "Cassava": [600, 400], "Maize": [1200, 25], "Plantain": [800, 1600],
            "Cocoa": [1500, 15], "Coffee (Robusta)": [2000, 8],
            "Coffee (Arabica)": [2200, 8], "Banana": [700, 1500],
            "Yam": [1000, 800], "Taro": [500, 600], "Rice": [1000, 80],
            "Sorghum": [800, 18], "Millet": [750, 12], "Sweet Potato": [400, 500],
            "Irish Potato": [800, 2000], "Beans": [1200, 60],
            "Groundnut (Peanut)": [1000, 100], "Cotton": [1800, 30],
            "Oil Palm": [1500, 150], "Rubber": [2000, 400],
            "Sugar Cane": [600, 8000], "Pineapple": [350, 40000],
            "Tomato": [10000, 0.3], "Onion": [7000, 8], "Cabbage": [6000, 0.5],
            "Carrot": [5000, 4], "Pepper": [8000, 0.5], "Okra": [3500, 8],
            "Eggplant": [7000, 0.4], "Cucumber": [6000, 3],
            "Watermelon": [4000, 3], "Papaya": [2000, 0.5], "Mango": [1600, 100],
            "Avocado": [1800, 150], "Orange": [1500, 180],
            "Grapefruit": [1500, 170], "Lemon": [1400, 200],
            "Guava": [1000, 250], "Passion Fruit": [2500, 3],
            "Soursop": [1600, 200], "Coconut": [1000, 140],
            "Cola Nut": [2200, 20], "Ginger": [1500, 1500],
            "Garlic": [3500, 800], "Soybean": [1100, 75], "Cowpea": [1000, 65],
            "Bambara Groundnut": [950, 90], "Melon": [3000, 3],
            "Pumpkin": [2500, 4], "Garden Egg": [7500, 0.4],
            "African Spinach": [2000, 6]
        }
        
        # Fertilizer costs: [price_per_bag, bags_needed_per_hectare]
        self.fertilizer_costs = {
            "Cassava": [12000, 3], "Maize": [15000, 4], "Plantain": [14000, 3],
            "Cocoa": [16000, 3], "Coffee (Robusta)": [16000, 3],
            "Coffee (Arabica)": [16000, 3], "Banana": [14000, 3],
            "Yam": [13000, 3], "Taro": [11000, 2], "Rice": [15000, 4],
            "Sorghum": [13000, 2], "Millet": [12000, 2],
            "Sweet Potato": [10000, 2], "Irish Potato": [15000, 4],
            "Beans": [11000, 2], "Groundnut (Peanut)": [11500, 2],
            "Cotton": [17000, 3], "Oil Palm": [16000, 4], "Rubber": [15000, 3],
            "Sugar Cane": [16000, 5], "Pineapple": [14000, 3],
            "Tomato": [16000, 4], "Onion": [15000, 4], "Cabbage": [15000, 4],
            "Carrot": [14000, 3], "Pepper": [15500, 4], "Okra": [12000, 2],
            "Eggplant": [15000, 4], "Cucumber": [14000, 3],
            "Watermelon": [13000, 3], "Papaya": [14000, 3], "Mango": [15000, 3],
            "Avocado": [15000, 3], "Orange": [15500, 3],
            "Grapefruit": [15500, 3], "Lemon": [15000, 3], "Guava": [14000, 3],
            "Passion Fruit": [15000, 3], "Soursop": [14500, 3],
            "Coconut": [14000, 3], "Cola Nut": [15000, 3], "Ginger": [14000, 4],
            "Garlic": [15000, 5], "Soybean": [12000, 2], "Cowpea": [11500, 2],
            "Bambara Groundnut": [11000, 2], "Melon": [12500, 3],
            "Pumpkin": [12000, 3], "Garden Egg": [15000, 4],
            "African Spinach": [10500, 2]
        }
        
        # Pesticide costs: [price_per_liter, liters_needed_per_hectare]
        self.pesticide_costs = {
            "Cassava": [6000, 4], "Maize": [7000, 5], "Plantain": [6500, 4],
            "Cocoa": [9000, 6], "Coffee (Robusta)": [8000, 5],
            "Coffee (Arabica)": [8000, 5], "Banana": [6500, 4],
            "Yam": [5500, 3], "Taro": [5000, 3], "Rice": [7500, 5],
            "Sorghum": [6500, 4], "Millet": [6000, 3],
            "Sweet Potato": [5000, 2], "Irish Potato": [7000, 5],
            "Beans": [5500, 3], "Groundnut (Peanut)": [6000, 3],
            "Cotton": [10000, 7], "Oil Palm": [8000, 5], "Rubber": [7000, 4],
            "Sugar Cane": [7500, 6], "Pineapple": [6800, 5],
            "Tomato": [9000, 7], "Onion": [8000, 6], "Cabbage": [7500, 5],
            "Carrot": [7000, 5], "Pepper": [8500, 6], "Okra": [6500, 4],
            "Eggplant": [8000, 6], "Cucumber": [7000, 5],
            "Watermelon": [6800, 4], "Papaya": [6500, 4], "Mango": [7000, 4],
            "Avocado": [7000, 4], "Orange": [7500, 4], "Grapefruit": [7500, 4],
            "Lemon": [7000, 4], "Guava": [6500, 3], "Passion Fruit": [7500, 5],
            "Soursop": [6800, 4], "Coconut": [6500, 3], "Cola Nut": [7200, 4],
            "Ginger": [6800, 5], "Garlic": [7500, 5], "Soybean": [6000, 3],
            "Cowpea": [5500, 3], "Bambara Groundnut": [5500, 3],
            "Melon": [6500, 4], "Pumpkin": [6000, 4], "Garden Egg": [8000, 6],
            "African Spinach": [5200, 3]
        }
    
    def _initialize_market_data(self):
        """Initialize expected yields and market prices."""
        
        # Expected yields (tons per hectare) - reduced for basic inputs
        self.expected_yields = {
            "Cassava": 18, "Maize": 2.8, "Plantain": 12, "Cocoa": 0.8,
            "Coffee (Robusta)": 1.2, "Coffee (Arabica)": 1.0, "Banana": 22,
            "Yam": 14, "Taro": 8, "Rice": 3.5, "Sorghum": 2.2, "Millet": 1.8,
            "Sweet Potato": 10, "Irish Potato": 16, "Beans": 1.4,
            "Groundnut (Peanut)": 1.6, "Cotton": 1.8, "Oil Palm": 13,
            "Rubber": 1.3, "Sugar Cane": 50, "Pineapple": 28, "Tomato": 25,
            "Onion": 19, "Cabbage": 22, "Carrot": 18, "Pepper": 10,
            "Okra": 6.5, "Eggplant": 16, "Cucumber": 19, "Watermelon": 22,
            "Papaya": 32, "Mango": 10, "Avocado": 8, "Orange": 13,
            "Grapefruit": 12, "Lemon": 11, "Guava": 14, "Passion Fruit": 12,
            "Soursop": 9, "Coconut": 16, "Cola Nut": 1.0, "Ginger": 13,
            "Garlic": 5, "Soybean": 1.8, "Cowpea": 1.3,
            "Bambara Groundnut": 1.2, "Melon": 16, "Pumpkin": 13,
            "Garden Egg": 15, "African Spinach": 8
        }
        
        # Market prices per ton (XAF)
        self.market_prices = {
            "Cassava": 85_000, "Maize": 220_000, "Plantain": 180_000,
            "Cocoa": 1_800_000, "Coffee (Robusta)": 1_400_000,
            "Coffee (Arabica)": 1_600_000, "Banana": 150_000, "Yam": 200_000,
            "Taro": 190_000, "Rice": 350_000, "Sorghum": 210_000,
            "Millet": 200_000, "Sweet Potato": 120_000, "Irish Potato": 250_000,
            "Beans": 450_000, "Groundnut (Peanut)": 400_000, "Cotton": 320_000,
            "Oil Palm": 140_000, "Rubber": 900_000, "Sugar Cane": 65_000,
            "Pineapple": 160_000, "Tomato": 280_000, "Onion": 320_000,
            "Cabbage": 180_000, "Carrot": 240_000, "Pepper": 450_000,
            "Okra": 350_000, "Eggplant": 220_000, "Cucumber": 200_000,
            "Watermelon": 140_000, "Papaya": 130_000, "Mango": 180_000,
            "Avocado": 380_000, "Orange": 200_000, "Grapefruit": 190_000,
            "Lemon": 220_000, "Guava": 160_000, "Passion Fruit": 280_000,
            "Soursop": 250_000, "Coconut": 120_000, "Cola Nut": 1_200_000,
            "Ginger": 550_000, "Garlic": 650_000, "Soybean": 380_000,
            "Cowpea": 420_000, "Bambara Groundnut": 380_000, "Melon": 170_000,
            "Pumpkin": 150_000, "Garden Egg": 260_000, "African Spinach": 320_000
        }
    
    # ========================================================================
    # UI SETUP
    # ========================================================================
    
    def _apply_styling(self):
        """Apply consistent styling to the application with dark green theme."""
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
    
    def init_ui(self):
        """Initialize the user interface components."""
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)
        
        # Add header
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Add scrollable content area
        scroll_area = self._create_scroll_area()
        main_layout.addWidget(scroll_area)
        
        # Add back button
        back_button = self._create_back_button()
        main_layout.addWidget(back_button, alignment=Qt.AlignLeft)
        
        # Setup status bar
        self.statusBar().showMessage(
            "Enter your farm details and budget to optimize costs"
        )
        self.statusBar().setStyleSheet(
            "background-color: #e8f5e9; color: #2d5016; font-weight: bold;"
        )
    
    def _create_header(self):
        """Create the page header."""
        header = QLabel("Cost Minimization Calculator")
        header.setObjectName("headerLabel")
        header.setAlignment(Qt.AlignCenter)
        return header
    
    def _create_scroll_area(self):
        """Create the scrollable content area with inputs and results."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(15)
        
        # Add input section
        input_group = self._create_input_section()
        scroll_layout.addWidget(input_group)
        
        # Add calculate button
        calc_button = self._create_calculate_button()
        scroll_layout.addWidget(calc_button)
        
        # Add results section
        results_group = self._create_results_section()
        scroll_layout.addWidget(results_group)
        
        scroll.setWidget(scroll_widget)
        return scroll
    
    def _create_input_section(self):
        """Create the input form section."""
        input_group = QGroupBox("Farm Details & Budget")
        input_layout = QFormLayout()
        input_layout.setSpacing(12)
        
        # Land size input
        self.land_size_input = QLineEdit()
        self.land_size_input.setPlaceholderText("Enter land size in hectares")
        input_layout.addRow("Land Size (hectares):", self.land_size_input)
        
        # Budget input
        self.budget_input = QLineEdit()
        self.budget_input.setPlaceholderText("Enter your total budget in XAF")
        input_layout.addRow("Total Budget (XAF):", self.budget_input)
        
        # Region selection
        self.region_combo = QComboBox()
        self.region_combo.addItems(sorted(self.regions.keys()))
        input_layout.addRow("Region:", self.region_combo)
        
        # Crop selection
        self.crop_combo = QComboBox()
        self.crop_combo.addItems(self.crops)
        input_layout.addRow("Select Crop:", self.crop_combo)
        
        input_group.setLayout(input_layout)
        return input_group
    
    def _create_calculate_button(self):
        """Create the calculate button."""
        calc_btn = QPushButton("Calculate Budget Allocation")
        calc_btn.setObjectName("calculateButton")
        calc_btn.setCursor(Qt.PointingHandCursor)
        calc_btn.clicked.connect(self.calculate_optimization)
        return calc_btn
    
    def _create_results_section(self):
        """Create the results display section."""
        results_group = QGroupBox("Budget Allocation & Results")
        results_layout = QVBoxLayout()
        
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setMinimumHeight(300)
        
        results_layout.addWidget(self.results_display)
        results_group.setLayout(results_layout)
        return results_group
    
    def _create_back_button(self):
        """Create the back navigation button."""
        back_btn = QPushButton("← Back to Options")
        back_btn.setObjectName("backButton")
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(self.go_back)
        back_btn.setFixedWidth(150)
        return back_btn
    
    # ========================================================================
    # CALCULATION METHODS
    # ========================================================================
    
    def calculate_optimization(self):
        """Calculate and display the optimized budget allocation."""
        try:
            # Get and validate inputs
            inputs = self._get_and_validate_inputs()
            
            # Calculate all costs
            costs = self._calculate_all_costs(inputs)
            
            # Check budget sufficiency
            if inputs['budget'] < costs['total_min_cost']:
                self._display_insufficient_budget(inputs, costs)
                return
            
            # Calculate allocations and projections
            allocations = self._calculate_budget_allocations(inputs, costs)
            projections = self._calculate_projections(inputs, costs, allocations)
            
            # Display results
            self._display_results(inputs, costs, allocations, projections)
            
        except ValueError as e:
            QMessageBox.warning(
                self,
                "Invalid Input",
                f"Please enter valid numbers.\n\nError: {str(e)}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Calculation Error",
                f"An error occurred during calculation:\n\n{str(e)}"
            )
    
    def _get_and_validate_inputs(self):
        """Get and validate user inputs."""
        land_size = float(self.land_size_input.text())
        if land_size <= 0:
            raise ValueError("Land size must be positive")
        
        budget = float(self.budget_input.text())
        if budget <= 0:
            raise ValueError("Budget must be positive")
        
        region = self.region_combo.currentText()
        crop = self.crop_combo.currentText()
        
        return {
            'land_size': land_size,
            'budget': budget,
            'region': region,
            'crop': crop
        }
    
    def _calculate_all_costs(self, inputs):
        """Calculate all minimum required costs."""
        land_size = inputs['land_size']
        crop = inputs['crop']
        region = inputs['region']
        
        # Basic costs
        land_prep = self.land_prep_cost * land_size
        
        # Seed costs
        seed_data = self.seed_costs[crop]
        seed_cost = seed_data[0] * seed_data[1] * land_size
        
        # Fertilizer costs
        fert_data = self.fertilizer_costs[crop]
        fertilizer_cost = fert_data[0] * fert_data[1] * land_size
        
        # Pesticide costs
        pest_data = self.pesticide_costs[crop]
        pesticide_cost = pest_data[0] * pest_data[1] * land_size
        
        # Irrigation costs
        irrigation_percentage = self.regions[region]
        irrigation_cost = self.base_irrigation_cost * irrigation_percentage * land_size
        
        # Equipment and labor
        equipment_cost = self.equipment_cost_per_hectare * land_size
        labor_cost = self.labor_cost_per_hectare * land_size
        
        # Expected yield
        expected_yield = self.expected_yields[crop] * land_size
        
        # Transportation and storage
        transport_cost = self.transport_cost_per_ton * expected_yield
        storage_cost = (self.storage_cost_per_ton_month * 
                       self.storage_months * expected_yield)
        
        # Total minimum cost
        total_min_cost = (
            land_prep + seed_cost + fertilizer_cost + pesticide_cost +
            irrigation_cost + equipment_cost + labor_cost +
            transport_cost + storage_cost
        )
        
        return {
            'land_prep': land_prep,
            'seed_cost': seed_cost,
            'fertilizer_cost': fertilizer_cost,
            'pesticide_cost': pesticide_cost,
            'irrigation_cost': irrigation_cost,
            'irrigation_percentage': irrigation_percentage,
            'equipment_cost': equipment_cost,
            'labor_cost': labor_cost,
            'transport_cost': transport_cost,
            'storage_cost': storage_cost,
            'expected_yield': expected_yield,
            'total_min_cost': total_min_cost
        }
    
    def _calculate_budget_allocations(self, inputs, costs):
        """Calculate proportional budget allocations."""
        budget = inputs['budget']
        total_min_cost = costs['total_min_cost']
        
        # Allocate budget proportionally
        allocations = {}
        cost_items = [
            'land_prep', 'seed_cost', 'fertilizer_cost', 'pesticide_cost',
            'irrigation_cost', 'equipment_cost', 'labor_cost',
            'transport_cost', 'storage_cost'
        ]
        
        for item in cost_items:
            allocations[item] = (costs[item] / total_min_cost) * budget
            allocations[f"{item}_pct"] = (allocations[item] / budget) * 100
        
        # Calculate extra budget
        allocations['extra_budget'] = budget - total_min_cost
        allocations['extra_pct'] = (allocations['extra_budget'] / budget) * 100
        
        return allocations
    
    def _calculate_projections(self, inputs, costs, allocations):
        """Calculate revenue and profit projections."""
        crop = inputs['crop']
        budget = inputs['budget']
        land_size = inputs['land_size']
        
        market_price = self.market_prices[crop]
        expected_yield = costs['expected_yield']
        expected_revenue = expected_yield * market_price
        expected_profit = expected_revenue - budget
        roi = (expected_profit / budget) * 100 if budget > 0 else 0
        
        return {
            'market_price': market_price,
            'expected_revenue': expected_revenue,
            'expected_profit': expected_profit,
            'roi': roi,
            'revenue_per_hectare': expected_revenue / land_size,
            'profit_per_hectare': expected_profit / land_size,
            'investment_per_hectare': budget / land_size,
            'yield_per_hectare': expected_yield / land_size
        }
    
    # ========================================================================
    # DISPLAY METHODS
    # ========================================================================
    
    def _display_insufficient_budget(self, inputs, costs):
        """Display warning message for insufficient budget."""
        budget_deficit = costs['total_min_cost'] - inputs['budget']
        recommended_land_size = (inputs['budget'] / costs['total_min_cost'] * 
                                inputs['land_size'])
        
        results = f"""
╔═══════════════════════════════════════════════════════════╗
║              ⚠️  INSUFFICIENT BUDGET WARNING              ║
╚═══════════════════════════════════════════════════════════╝

📍 FARM INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Land Size:        {inputs['land_size']:,.2f} hectares
• Your Budget:      {inputs['budget']:,.0f} XAF
• Region:           {inputs['region']}
• Crop:             {inputs['crop']}

❌ BUDGET ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Minimum Required:   {costs['total_min_cost']:,.0f} XAF
Your Budget:        {inputs['budget']:,.0f} XAF
Budget Deficit:     {budget_deficit:,.0f} XAF

⚠️  Your budget is SHORT by {budget_deficit:,.0f} XAF!

💡 RECOMMENDATIONS TO PROCEED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Reduce land size to {recommended_land_size:,.2f} hectares
2. Increase your budget to {costs['total_min_cost']:,.0f} XAF
3. Consider a less expensive crop
4. Seek agricultural credit or microfinance
5. Partner with other farmers to share costs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Please adjust your inputs and try again.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        self.results_display.setPlainText(results)
        self.statusBar().showMessage("⚠️ Budget insufficient for this operation")
    
    def _display_results(self, inputs, costs, allocations, projections):
        """Display complete calculation results."""
        
        # Generate ROI assessment
        roi_assessment = self._get_roi_assessment(projections['roi'])
        
        results = f"""
╔═══════════════════════════════════════════════════════════╗
║         COST MINIMIZATION BUDGET ALLOCATION               ║
╚═══════════════════════════════════════════════════════════╝

📍 FARM INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Land Size:        {inputs['land_size']:,.2f} hectares
• Total Budget:     {inputs['budget']:,.0f} XAF
• Region:           {inputs['region']}
• Crop:             {inputs['crop']}
• Irrigation Need:  {costs['irrigation_percentage']*100:.0f}%
• Approach:         Manual Labor + Basic Inputs

💰 BUDGET ALLOCATION BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                             Amount (XAF)    % of Budget
──────────────────────────────────────────────────────────
1. Land Preparation      {allocations['land_prep']:>12,.0f}    {allocations['land_prep_pct']:>6.1f}%
2. Basic/Local Seeds     {allocations['seed_cost']:>12,.0f}    {allocations['seed_cost_pct']:>6.1f}%
3. Organic Fertilizers   {allocations['fertilizer_cost']:>12,.0f}    {allocations['fertilizer_cost_pct']:>6.1f}%
4. Natural Pesticides    {allocations['pesticide_cost']:>12,.0f}    {allocations['pesticide_cost_pct']:>6.1f}%
5. Basic Irrigation      {allocations['irrigation_cost']:>12,.0f}    {allocations['irrigation_cost_pct']:>6.1f}%
6. Hand Tools/Equipment  {allocations['equipment_cost']:>12,.0f}    {allocations['equipment_cost_pct']:>6.1f}%
7. Manual Labor          {allocations['labor_cost']:>12,.0f}    {allocations['labor_cost_pct']:>6.1f}%
8. Transportation        {allocations['transport_cost']:>12,.0f}    {allocations['transport_cost_pct']:>6.1f}%
9. Basic Storage         {allocations['storage_cost']:>12,.0f}    {allocations['storage_cost_pct']:>6.1f}%
──────────────────────────────────────────────────────────
TOTAL ALLOCATED:         {inputs['budget']:>12,.0f}       100.0%

Minimum Required:        {costs['total_min_cost']:>12,.0f}
Extra Buffer:            {allocations['extra_budget']:>12,.0f}    {allocations['extra_pct']:>6.1f}%

📊 PROJECTED RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Expected Yield:        {costs['expected_yield']:,.2f} tons
• Market Price:          {projections['market_price']:,.0f} XAF/ton
• Expected Revenue:      {projections['expected_revenue']:,.0f} XAF
• Expected Profit:       {projections['expected_profit']:,.0f} XAF
• Return on Investment:  {projections['roi']:,.1f}%

📈 PER HECTARE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Investment/Hectare:    {projections['investment_per_hectare']:,.0f} XAF
• Revenue/Hectare:       {projections['revenue_per_hectare']:,.0f} XAF
• Profit/Hectare:        {projections['profit_per_hectare']:,.0f} XAF
• Yield/Hectare:         {projections['yield_per_hectare']:,.2f} tons

✅ COST MINIMIZATION STRATEGY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{roi_assessment}

  ✓ Use saved/local seeds to reduce costs
  ✓ Apply organic fertilizers (compost, manure)
  ✓ Employ manual labor for cultivation
  ✓ Use natural pest control methods
  ✓ Implement gravity-fed irrigation where possible
  ✓ Share equipment with neighboring farmers
  ✓ Sell at local markets to reduce transport costs
  ✓ Store produce in ventilated local structures

💡 BUDGET OPTIMIZATION TIPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Labor costs are {allocations['labor_cost_pct']:.0f}% of budget - consider family labor
• You have {allocations['extra_budget']:,.0f} XAF buffer for emergencies
• Focus on crops with high ROI in your region
• Join farmer cooperatives for bulk purchasing discounts
• Consider intercropping to maximize land use

⚠️  IMPORTANT NOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Yields are ~30-40% lower than mechanized farming
• Labor-intensive approach requires time commitment
• Weather and market prices can significantly affect outcomes
• Keep {allocations['extra_pct']:.0f}% buffer for unexpected costs
• Consider crop insurance if available in your region

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This allocation minimizes costs while maintaining viable production.
Actual results depend on farm management and local conditions.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        self.results_display.setPlainText(results)
        self.statusBar().showMessage(
            f"Budget optimized for {inputs['land_size']} hectares of {inputs['crop']}"
        )
    
    def _get_roi_assessment(self, roi):
        """Get ROI assessment message based on return value."""
        if roi > 30:
            return "  ★ Excellent returns for minimal investment!"
        elif roi > 15:
            return "  ★ Good profit margins with low-cost approach."
        elif roi > 0:
            return "  ★ Positive returns, sustainable for small farmers."
        else:
            return "  ⚠ Negative returns projected. Reconsider crop or scale."
    
    # ========================================================================
    # NAVIGATION METHODS
    # ========================================================================
    
    def go_back(self):
        """Navigate back to parent window."""
        self.close()
        if self.parent_window:
            self.parent_window.show()
    
    def closeEvent(self, event):
        """Handle window close event."""
        if self.parent_window:
            self.parent_window.show()
        event.accept()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Create and show main window
    window = CostMinimizationPage()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()