"""
Agricultural Optimization Calculator
A PySide6 application for balanced farm optimization in Cameroon regions.
Provides investment planning with 75% quality level (balanced approach).
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QTextEdit,
    QScrollArea, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class AgriculturalOptimizationPage(QMainWindow):
    """
    Main window for agricultural optimization calculations.
    Uses a balanced approach (75% quality) between cost and yield.
    """
    
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        
        # Window configuration
        self.setWindowTitle("Agricultural Optimization - Farm Optimization")
        self.setGeometry(100, 100, 1000, 750)
        
        # Fixed quality factor for balanced approach
        self.quality_factor = 0.75  # 75% quality level
        
        # Initialize data
        self._initialize_regional_data()
        self._initialize_crop_list()
        self._initialize_cost_parameters()
        self._initialize_yield_and_market_data()
        
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
    
    def _initialize_crop_list(self):
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
    
    def _initialize_cost_parameters(self):
        """Initialize all cost parameters for farming operations."""
        
        # Base costs per hectare (XAF)
        self.max_land_prep_cost = 85_000  # Mechanized
        self.min_land_prep_cost = 35_000  # Manual
        
        self.max_base_irrigation_cost = 180_000  # Advanced system
        self.min_base_irrigation_cost = 45_000   # Basic system
        
        self.max_equipment_cost = 95_000  # Full mechanization
        self.min_equipment_cost = 15_000  # Hand tools
        
        self.max_labor_cost = 120_000  # Low labor (mechanized)
        self.min_labor_cost = 250_000  # High labor (manual)
        
        # Transportation and storage
        self.transport_cost_per_ton = 6_500
        self.storage_cost_per_ton_month = 2_500
        self.storage_months = 2
        
        # Maximum seed costs: [price_per_kg, kg_needed_per_hectare]
        self.max_seed_costs = {
            "Cassava": [1500, 400], "Maize": [3500, 25], "Plantain": [2000, 1600],
            "Cocoa": [4000, 15], "Coffee (Robusta)": [5000, 8],
            "Coffee (Arabica)": [6000, 8], "Banana": [1800, 1500],
            "Yam": [2500, 800], "Taro": [1200, 600], "Rice": [2800, 80],
            "Sorghum": [2200, 18], "Millet": [2000, 12],
            "Sweet Potato": [1000, 500], "Irish Potato": [1800, 2000],
            "Beans": [3000, 60], "Groundnut (Peanut)": [2500, 100],
            "Cotton": [4500, 30], "Oil Palm": [3500, 150], "Rubber": [5000, 400],
            "Sugar Cane": [1500, 8000], "Pineapple": [800, 40000],
            "Tomato": [25000, 0.3], "Onion": [18000, 8], "Cabbage": [15000, 0.5],
            "Carrot": [12000, 4], "Pepper": [20000, 0.5], "Okra": [8000, 8],
            "Eggplant": [16000, 0.4], "Cucumber": [14000, 3],
            "Watermelon": [10000, 3], "Papaya": [5000, 0.5], "Mango": [4000, 100],
            "Avocado": [4500, 150], "Orange": [3800, 180],
            "Grapefruit": [3800, 170], "Lemon": [3500, 200],
            "Guava": [2500, 250], "Passion Fruit": [6000, 3],
            "Soursop": [4000, 200], "Coconut": [2500, 140],
            "Cola Nut": [5500, 20], "Ginger": [3500, 1500],
            "Garlic": [8000, 800], "Soybean": [2800, 75], "Cowpea": [2600, 65],
            "Bambara Groundnut": [2400, 90], "Melon": [7000, 3],
            "Pumpkin": [6000, 4], "Garden Egg": [18000, 0.4],
            "African Spinach": [5000, 6]
        }
        
        # Maximum fertilizer costs: [price_per_bag, bags_per_hectare]
        self.max_fertilizer_costs = {
            "Cassava": [28000, 4], "Maize": [32000, 6], "Plantain": [30000, 5],
            "Cocoa": [35000, 4], "Coffee (Robusta)": [35000, 4],
            "Coffee (Arabica)": [35000, 4], "Banana": [30000, 5],
            "Yam": [28000, 4], "Taro": [26000, 4], "Rice": [33000, 6],
            "Sorghum": [30000, 4], "Millet": [28000, 3],
            "Sweet Potato": [25000, 3], "Irish Potato": [32000, 6],
            "Beans": [26000, 3], "Groundnut (Peanut)": [27000, 3],
            "Cotton": [38000, 5], "Oil Palm": [35000, 6], "Rubber": [32000, 5],
            "Sugar Cane": [35000, 8], "Pineapple": [30000, 5],
            "Tomato": [34000, 7], "Onion": [33000, 6], "Cabbage": [32000, 6],
            "Carrot": [31000, 5], "Pepper": [33000, 6], "Okra": [28000, 4],
            "Eggplant": [32000, 6], "Cucumber": [30000, 5],
            "Watermelon": [29000, 4], "Papaya": [30000, 5], "Mango": [33000, 4],
            "Avocado": [33000, 4], "Orange": [34000, 5],
            "Grapefruit": [34000, 5], "Lemon": [33000, 5], "Guava": [30000, 4],
            "Passion Fruit": [32000, 5], "Soursop": [31000, 4],
            "Coconut": [30000, 4], "Cola Nut": [33000, 4], "Ginger": [30000, 6],
            "Garlic": [32000, 7], "Soybean": [28000, 3], "Cowpea": [27000, 3],
            "Bambara Groundnut": [26000, 3], "Melon": [28000, 4],
            "Pumpkin": [27000, 4], "Garden Egg": [32000, 6],
            "African Spinach": [25000, 4]
        }
        
        # Maximum pesticide costs: [price_per_liter, liters_per_hectare]
        self.max_pesticide_costs = {
            "Cassava": [15000, 6], "Maize": [18000, 8], "Plantain": [16000, 7],
            "Cocoa": [22000, 10], "Coffee (Robusta)": [20000, 9],
            "Coffee (Arabica)": [20000, 9], "Banana": [16000, 7],
            "Yam": [14000, 5], "Taro": [13000, 5], "Rice": [19000, 9],
            "Sorghum": [17000, 7], "Millet": [16000, 6],
            "Sweet Potato": [12000, 4], "Irish Potato": [18000, 8],
            "Beans": [14000, 5], "Groundnut (Peanut)": [15000, 6],
            "Cotton": [25000, 12], "Oil Palm": [20000, 8], "Rubber": [18000, 7],
            "Sugar Cane": [19000, 10], "Pineapple": [17000, 8],
            "Tomato": [22000, 12], "Onion": [20000, 10], "Cabbage": [19000, 9],
            "Carrot": [18000, 8], "Pepper": [21000, 11], "Okra": [16000, 7],
            "Eggplant": [20000, 10], "Cucumber": [18000, 8],
            "Watermelon": [17000, 7], "Papaya": [16000, 7], "Mango": [18000, 6],
            "Avocado": [18000, 6], "Orange": [19000, 7],
            "Grapefruit": [19000, 7], "Lemon": [18000, 7], "Guava": [16000, 6],
            "Passion Fruit": [19000, 8], "Soursop": [17000, 6],
            "Coconut": [16000, 5], "Cola Nut": [18000, 7], "Ginger": [17000, 8],
            "Garlic": [19000, 9], "Soybean": [15000, 5], "Cowpea": [14000, 5],
            "Bambara Groundnut": [14000, 5], "Melon": [16000, 6],
            "Pumpkin": [15000, 6], "Garden Egg": [20000, 10],
            "African Spinach": [13000, 5]
        }
    
    def _initialize_yield_and_market_data(self):
        """Initialize expected yields and market prices."""
        
        # Maximum expected yields (tons per hectare at 100% quality)
        self.max_yields = {
            "Cassava": 28, "Maize": 4.5, "Plantain": 18, "Cocoa": 1.2,
            "Coffee (Robusta)": 1.8, "Coffee (Arabica)": 1.5, "Banana": 35,
            "Yam": 22, "Taro": 12, "Rice": 5.5, "Sorghum": 3.5, "Millet": 2.8,
            "Sweet Potato": 16, "Irish Potato": 25, "Beans": 2.2,
            "Groundnut (Peanut)": 2.5, "Cotton": 2.8, "Oil Palm": 20,
            "Rubber": 2.0, "Sugar Cane": 80, "Pineapple": 45, "Tomato": 40,
            "Onion": 30, "Cabbage": 35, "Carrot": 28, "Pepper": 15,
            "Okra": 10, "Eggplant": 25, "Cucumber": 30, "Watermelon": 35,
            "Papaya": 50, "Mango": 15, "Avocado": 12, "Orange": 20,
            "Grapefruit": 18, "Lemon": 16, "Guava": 22, "Passion Fruit": 18,
            "Soursop": 14, "Coconut": 25, "Cola Nut": 1.5, "Ginger": 20,
            "Garlic": 8, "Soybean": 2.8, "Cowpea": 2.0,
            "Bambara Groundnut": 1.8, "Melon": 25, "Pumpkin": 20,
            "Garden Egg": 24, "African Spinach": 12
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
        """Apply consistent green styling to the application."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5fcf4;
            }
            QLabel {
                font-size: 13px;
                color: #1b3a0f;
                background-color: transparent;
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
            QGroupBox::title {
                color: #2d5016;
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
            "Enter your farm details to calculate optimized investment plan"
        )
        self.statusBar().setStyleSheet(
            "background-color: #e8f5e9; color: #2d5016; font-weight: bold;"
        )
    
    def _create_header(self):
        """Create the page header."""
        header = QLabel("Agricultural Optimization - Balanced Approach")
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
        
        # Add description section
        desc_group = self._create_description_section()
        scroll_layout.addWidget(desc_group)
        
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
        input_group = QGroupBox("Farm Details")
        input_layout = QFormLayout()
        input_layout.setSpacing(12)
        
        # Land size input
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
        return input_group
    
    def _create_description_section(self):
        """Create the approach description section."""
        desc_group = QGroupBox("Balanced Approach (75% Quality)")
        desc_layout = QVBoxLayout()
        
        desc_text = (
            "This approach balances quality and cost-effectiveness:\n\n"
            "• Uses quality certified seeds (good grade)\n"
            "• Applies balanced fertilization program\n"
            "• Implements integrated pest management\n"
            "• Moderate mechanization (50-60%)\n"
            "• Targets mainstream markets with good prices\n\n"
            "Ideal for most farmers seeking optimal returns."
        )
        
        desc_label = QLabel(desc_text)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(
            "font-size: 12px; padding: 8px; color: #1b3a0f; "
            "background-color: white; border-radius: 5px;"
        )
        desc_layout.addWidget(desc_label)
        
        desc_group.setLayout(desc_layout)
        return desc_group
    
    def _create_calculate_button(self):
        """Create the calculate button."""
        calc_btn = QPushButton("Calculate Investment Plan")
        calc_btn.setObjectName("calculateButton")
        calc_btn.setCursor(Qt.PointingHandCursor)
        calc_btn.clicked.connect(self.calculate_optimization)
        return calc_btn
    
    def _create_results_section(self):
        """Create the results display section."""
        results_group = QGroupBox("Investment Plan & Projections")
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
        """Calculate and display the optimized investment plan."""
        try:
            # Get and validate inputs
            inputs = self._get_and_validate_inputs()
            
            # Calculate all costs
            costs = self._calculate_all_costs(inputs)
            
            # Calculate projections
            projections = self._calculate_projections(inputs, costs)
            
            # Display results
            self._display_results(inputs, costs, projections)
            
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
        
        region = self.region_combo.currentText()
        crop = self.crop_combo.currentText()
        
        return {
            'land_size': land_size,
            'region': region,
            'crop': crop
        }
    
    def _calculate_all_costs(self, inputs):
        """Calculate all costs based on 75% quality factor."""
        land_size = inputs['land_size']
        crop = inputs['crop']
        region = inputs['region']
        quality = self.quality_factor
        
        # Land preparation (interpolate between min and max)
        land_prep_cost_per_ha = (
            self.min_land_prep_cost + 
            (self.max_land_prep_cost - self.min_land_prep_cost) * quality
        )
        land_prep = land_prep_cost_per_ha * land_size
        
        # Seed costs (apply quality factor to premium seeds)
        seed_data = self.max_seed_costs[crop]
        seed_cost = (seed_data[0] * quality) * seed_data[1] * land_size
        
        # Fertilizer costs (apply quality factor)
        fert_data = self.max_fertilizer_costs[crop]
        fertilizer_cost = (fert_data[0] * quality) * fert_data[1] * land_size
        
        # Pesticide costs (apply quality factor)
        pest_data = self.max_pesticide_costs[crop]
        pesticide_cost = (pest_data[0] * quality) * pest_data[1] * land_size
        
        # Irrigation costs (interpolate)
        irrigation_percentage = self.regions[region]
        base_irrigation = (
            self.min_base_irrigation_cost + 
            (self.max_base_irrigation_cost - self.min_base_irrigation_cost) * quality
        )
        irrigation_cost = base_irrigation * irrigation_percentage * land_size
        
        # Equipment costs (interpolate)
        equipment_cost_per_ha = (
            self.min_equipment_cost + 
            (self.max_equipment_cost - self.min_equipment_cost) * quality
        )
        equipment_cost = equipment_cost_per_ha * land_size
        
        # Labor costs (inverse relationship - higher quality = less labor)
        labor_cost_per_ha = (
            self.max_labor_cost + 
            (self.min_labor_cost - self.max_labor_cost) * (1 - quality)
        )
        labor_cost = labor_cost_per_ha * land_size
        
        # Expected yield (scale from 50% to 100% based on quality)
        max_yield = self.max_yields[crop]
        expected_yield_per_ha = max_yield * (0.5 + 0.5 * quality)
        expected_yield = expected_yield_per_ha * land_size
        
        # Transportation and storage
        transport_cost = self.transport_cost_per_ton * expected_yield
        storage_cost = (
            self.storage_cost_per_ton_month * 
            self.storage_months * 
            expected_yield
        )
        
        # Total investment
        total_cost = (
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
            'expected_yield_per_ha': expected_yield_per_ha,
            'max_yield': max_yield,
            'total_cost': total_cost
        }
    
    def _calculate_projections(self, inputs, costs):
        """Calculate revenue and profit projections."""
        crop = inputs['crop']
        land_size = inputs['land_size']
        
        market_price = self.market_prices[crop]
        expected_revenue = costs['expected_yield'] * market_price
        expected_profit = expected_revenue - costs['total_cost']
        
        roi = 0
        if costs['total_cost'] > 0:
            roi = (expected_profit / costs['total_cost']) * 100
        
        return {
            'market_price': market_price,
            'expected_revenue': expected_revenue,
            'expected_profit': expected_profit,
            'roi': roi,
            'revenue_per_hectare': expected_revenue / land_size,
            'profit_per_hectare': expected_profit / land_size,
            'investment_per_hectare': costs['total_cost'] / land_size
        }
    
    # ========================================================================
    # DISPLAY METHODS
    # ========================================================================
    
    def _display_results(self, inputs, costs, projections):
        """Display complete calculation results."""
        
        # Calculate percentages
        total = costs['total_cost']
        percentages = {
            'land_prep': (costs['land_prep'] / total) * 100,
            'seed': (costs['seed_cost'] / total) * 100,
            'fertilizer': (costs['fertilizer_cost'] / total) * 100,
            'pesticide': (costs['pesticide_cost'] / total) * 100,
            'irrigation': (costs['irrigation_cost'] / total) * 100,
            'equipment': (costs['equipment_cost'] / total) * 100,
            'labor': (costs['labor_cost'] / total) * 100,
            'transport': (costs['transport_cost'] / total) * 100,
            'storage': (costs['storage_cost'] / total) * 100
        }
        
        # Get ROI assessment
        roi_assessment = self._get_roi_assessment(projections['roi'])
        
        # Calculate yield efficiency
        yield_efficiency = (
            costs['expected_yield_per_ha'] / costs['max_yield']
        ) * 100
        
        # Format results
        results = f"""
╔═══════════════════════════════════════════════════════════╗
║     AGRICULTURAL OPTIMIZATION - BALANCED APPROACH         ║
╚═══════════════════════════════════════════════════════════╝

📍 FARM INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Land Size:            {inputs['land_size']:,.2f} hectares
• Region:               {inputs['region']}
• Crop:                 {inputs['crop']}
• Quality Level:        75% (Balanced)
• Approach:             Quality Inputs + Balanced Mechanization
• Mechanization Level:  Moderate (50-60%)

💰 INVESTMENT BREAKDOWN (XAF)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                             Amount (XAF)    % of Total
──────────────────────────────────────────────────────────
1. Land Preparation      {costs['land_prep']:>12,.0f}    {percentages['land_prep']:>6.1f}%
2. Seeds (75% Quality)   {costs['seed_cost']:>12,.0f}    {percentages['seed']:>6.1f}%
3. Fertilizers (75%)     {costs['fertilizer_cost']:>12,.0f}    {percentages['fertilizer']:>6.1f}%
4. Pesticides (75%)      {costs['pesticide_cost']:>12,.0f}    {percentages['pesticide']:>6.1f}%
5. Irrigation System     {costs['irrigation_cost']:>12,.0f}    {percentages['irrigation']:>6.1f}%
6. Equipment/Machinery   {costs['equipment_cost']:>12,.0f}    {percentages['equipment']:>6.1f}%
7. Labor Costs           {costs['labor_cost']:>12,.0f}    {percentages['labor']:>6.1f}%
8. Transportation        {costs['transport_cost']:>12,.0f}    {percentages['transport']:>6.1f}%
9. Storage (2 months)    {costs['storage_cost']:>12,.0f}    {percentages['storage']:>6.1f}%
──────────────────────────────────────────────────────────
TOTAL INVESTMENT:        {total:>12,.0f}       100.0%

📊 PROJECTED RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Expected Yield:        {costs['expected_yield']:,.2f} tons
• Yield per Hectare:     {costs['expected_yield_per_ha']:,.2f} tons/ha
• Yield Efficiency:      {yield_efficiency:.1f}% of maximum
• Market Price:          {projections['market_price']:,.0f} XAF/ton
• Expected Revenue:      {projections['expected_revenue']:,.0f} XAF
• Expected Profit:       {projections['expected_profit']:,.0f} XAF
• Return on Investment:  {projections['roi']:,.1f}%

📈 PER HECTARE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Investment/Hectare:    {projections['investment_per_hectare']:,.0f} XAF
• Revenue/Hectare:       {projections['revenue_per_hectare']:,.0f} XAF
• Profit/Hectare:        {projections['profit_per_hectare']:,.0f} XAF

⚖️  OPTIMIZATION BALANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Input Quality:           ███████▒▒  75%  (Good)
Cost Efficiency:         ███████▒▒  75%  (Balanced)
Labor Intensity:         █████▒▒▒▒  50%  (Moderate)
Expected Yield:          ███████▒▒  75%  (Good)

This approach balances quality and cost-effectiveness with
moderate mechanization. Ideal for most farmers.

✅ RECOMMENDATIONS & STRATEGY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{roi_assessment}

Best Practices:
• Use quality certified seeds (good grade)
• Apply balanced fertilization program
• Implement integrated pest management
• Use selective mechanization for key operations
• Balance manual and mechanized labor
• Target mainstream markets with good prices
• Maintain flexible cost management
• Monitor crop development weekly

Specific Actions for {inputs['region']}:
• Adjust irrigation based on {inputs['region']} climate patterns
• Irrigation needs: {costs['irrigation_percentage']*100:.0f}% of area
• Consider local weather patterns when scheduling operations
• Join farmer cooperatives for input discounts

Financial Planning:
• Maintain {(total*0.1):,.0f} XAF (10%) as contingency fund
• Plan for seasonal cash flow variations
• Consider phasing investments over multiple seasons
• Explore agricultural credit options if needed

💡 COST OPTIMIZATION TIPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Largest cost: {self._get_largest_cost(costs, percentages)}
• Buy inputs in bulk through cooperatives for 10-15% savings
• Share equipment with neighboring farmers
• Implement soil testing to optimize fertilizer use
• Use integrated pest management to reduce pesticide costs
• Plan harvest timing for peak market prices
• Maintain detailed records for better planning

⚠️  IMPORTANT CONSIDERATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Market prices can vary ±20% based on season and demand
• Weather conditions significantly affect irrigation needs
• Actual yields depend on farm management practices
• Labor availability may vary by season
• Consider crop insurance if available
• Keep emergency fund for unexpected costs
• Review and adjust strategy after first season

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This balanced optimization provides good returns while managing
costs effectively. Adjust as needed based on your specific
circumstances and available resources.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        self.results_display.setPlainText(results)
        self.statusBar().showMessage(
            f"Investment plan calculated for {inputs['land_size']} hectares "
            f"of {inputs['crop']}"
        )
    
    def _get_roi_assessment(self, roi):
        """Get ROI assessment message based on return value."""
        if roi > 40:
            return "★★★ Excellent investment with strong profit potential!"
        elif roi > 25:
            return "★★ Very good returns with balanced approach."
        elif roi > 10:
            return "★ Positive returns with reasonable profit margin."
        else:
            return "⚠ Lower returns projected. Consider different crop or region."
    
    def _get_largest_cost(self, costs, percentages):
        """Identify the largest cost component."""
        cost_items = {
            'Land Preparation': (costs['land_prep'], percentages['land_prep']),
            'Seeds': (costs['seed_cost'], percentages['seed']),
            'Fertilizers': (costs['fertilizer_cost'], percentages['fertilizer']),
            'Pesticides': (costs['pesticide_cost'], percentages['pesticide']),
            'Irrigation': (costs['irrigation_cost'], percentages['irrigation']),
            'Equipment': (costs['equipment_cost'], percentages['equipment']),
            'Labor': (costs['labor_cost'], percentages['labor'])
        }
        
        largest = max(cost_items.items(), key=lambda x: x[1][0])
        return f"{largest[0]} ({largest[1][1]:.1f}%)"
    
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
    window = AgriculturalOptimizationPage()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()