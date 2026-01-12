"""
Cameroon Agricultural Data Constants
Based on 2024-2025 market research and regional pricing
All prices in XAF (Central African Franc)
Exchange rate reference: 1 USD ≈ 612 XAF (as of 2025)
"""

# ============================================================================
# COST VARIABLES (per hectare basis)
# ============================================================================

# LAND PREPARATION COSTS
LAND_PREP_COSTS = {
    'tillage_per_ha': 65000,  # Tillage/ploughing cost
    'harrowing_per_ha': 32000,  # Harrowing/leveling
    'irrigation_setup_per_ha': 85000,  # Basic irrigation setup
}

# SEED COSTS (XAF per kg)
SEED_COSTS = {
    'maize_improved': 2100,  # Improved hybrid maize seed
    'maize_local': 800,  # Local variety
    'rice_improved': 1800,
    'rice_local': 700,
    'cassava_stems': 400,  # Per bundle
    'groundnut': 1200,
    'beans': 1500,
}

# SEED REQUIREMENTS (kg per hectare for optimal yield)
SEED_REQUIREMENTS = {
    'maize_improved': 25,  # 25 kg/ha for improved varieties
    'maize_local': 30,
    'rice_improved': 80,
    'rice_local': 100,
    'groundnut': 90,
    'beans': 70,
}

# FERTILIZER COSTS (XAF per 50kg bag)
# Note: Fertilizer prices have been volatile, averaging around 4x increase from 2021
FERTILIZER_COSTS = {
    'npk_compound': 32000,  # NPK 20-10-10 or similar
    'urea': 28000,  # Urea 46%
    'dap': 35000,  # Di-ammonium phosphate
    'organic_manure_ton': 18000,  # Per ton of organic manure
}

# FERTILIZER REQUIREMENTS (bags per hectare for yield maximization)
FERTILIZER_REQUIREMENTS = {
    'maize': {
        'npk_bags': 4,  # 200 kg NPK
        'urea_bags': 3,  # 150 kg Urea
    },
    'rice': {
        'npk_bags': 5,
        'urea_bags': 4,
    },
    'cassava': {
        'npk_bags': 3,
        'organic_manure_tons': 2,
    },
    'groundnut': {
        'npk_bags': 2,
        'organic_manure_tons': 1,
    },
    'beans': {
        'npk_bags': 2,
        'dap_bags': 2,
    },
}

# PESTICIDE & HERBICIDE COSTS (per hectare treatment)
PESTICIDE_COSTS = {
    'herbicide_per_ha': 28000,  # Pre and post-emergence herbicides
    'insecticide_per_ha': 22000,  # Fall armyworm control, etc.
    'fungicide_per_ha': 18000,  # Fungal disease control
}

# LABOR COSTS (XAF)
# Based on agricultural minimum wage: 45,000 XAF/month (agricultural sector)
# Daily wage approximately: 1,500 - 2,000 XAF/day
LABOR_COSTS = {
    'daily_wage': 1800,  # Average daily wage
    'planting_days_per_ha': 8,  # Days needed for planting 1 hectare
    'weeding_days_per_ha': 12,  # Days for weeding (2 rounds)
    'harvesting_days_per_ha': 10,  # Days for harvesting
    'other_operations_days_per_ha': 6,  # Fertilizer application, pest control, etc.
}

# IRRIGATION COSTS (for areas with irrigation)
IRRIGATION_COSTS = {
    'water_cost_per_ha_season': 45000,  # Water fees and pumping
    'pump_operation_per_ha': 35000,  # Fuel for irrigation pumps
}

# EQUIPMENT & MACHINERY COSTS (per hectare)
EQUIPMENT_COSTS = {
    'tractor_ploughing_per_ha': 65000,
    'tractor_harrowing_per_ha': 32000,
    'mechanical_planting_per_ha': 25000,
    'mechanical_harvesting_per_ha': 55000,
    'fuel_operations_per_ha': 28000,
}

# TRANSPORTATION COSTS
TRANSPORT_COSTS = {
    'farm_to_market_per_ton': 8500,  # Average cost to transport 1 ton to market
    'storage_per_ton_month': 3500,  # Storage at warehouse/depot
}

# STORAGE COSTS
STORAGE_COSTS = {
    'on_farm_storage_per_ton': 2500,  # Basic on-farm storage
    'improved_storage_per_ton': 6000,  # Improved warehouse storage
}

# ============================================================================
# YIELD DATA (tons per hectare)
# ============================================================================

# EXPECTED YIELDS with proper management (tons/ha)
EXPECTED_YIELDS = {
    'maize_with_inputs': 3.5,  # With fertilizer and improved seeds
    'maize_basic': 1.8,  # Basic farming, Cameroon average
    'rice_with_inputs': 4.2,
    'rice_basic': 2.0,
    'cassava_with_inputs': 18.0,
    'cassava_basic': 12.0,
    'groundnut_with_inputs': 2.5,
    'groundnut_basic': 1.2,
    'beans_with_inputs': 1.8,
    'beans_basic': 0.9,
}

# OPTIMAL YIELDS (with maximum inputs - for yield maximization strategy)
OPTIMAL_YIELDS = {
    'maize': 4.5,  # With intensive management
    'rice': 5.5,
    'cassava': 22.0,
    'groundnut': 3.0,
    'beans': 2.2,
}

# ============================================================================
# MARKET PRICES (XAF per kg)
# ============================================================================

# Current market prices (wholesale/farmgate)
MARKET_PRICES = {
    'maize': 617,  # 617 XAF/kg retail (farmgate ~500 XAF/kg)
    'rice': 850,  # Higher due to heavy imports
    'cassava_fresh': 180,
    'cassava_processed': 450,  # Gari, flour, etc.
    'groundnut': 1100,
    'beans': 950,
}

# Farmgate prices (what farmers actually receive, typically 70-80% of retail)
FARMGATE_PRICES = {
    'maize': 480,
    'rice': 680,
    'cassava_fresh': 150,
    'cassava_processed': 380,
    'groundnut': 900,
    'beans': 780,
}

# ============================================================================
# CROP-SPECIFIC INFORMATION
# ============================================================================

CROP_SEASONS = {
    'maize': {
        'growing_days': 120,  # 3-4 months
        'seasons_per_year': 2,  # Bimodal rainfall areas
        'best_planting_months': ['March-April', 'August-September'],
    },
    'rice': {
        'growing_days': 120,
        'seasons_per_year': 2,
        'best_planting_months': ['March-May', 'August-October'],
    },
    'cassava': {
        'growing_days': 365,  # 10-12 months
        'seasons_per_year': 1,
        'best_planting_months': ['March-May'],
    },
    'groundnut': {
        'growing_days': 100,
        'seasons_per_year': 2,
        'best_planting_months': ['March-April', 'August-September'],
    },
    'beans': {
        'growing_days': 90,
        'seasons_per_year': 2,
        'best_planting_months': ['March-April', 'September-October'],
    },
}

# POST-HARVEST LOSSES (percentage)
POST_HARVEST_LOSSES = {
    'maize': 0.11,  # 11% average loss
    'rice': 0.15,
    'cassava': 0.30,  # High perishability
    'groundnut': 0.12,
    'beans': 0.10,
}

# ============================================================================
# CLIMATE ZONES IN CAMEROON
# ============================================================================

CLIMATE_ZONES = {
    'humid_forest': {
        'regions': ['South', 'East', 'Centre', 'Littoral'],
        'rainfall_mm': 1500-3000,
        'best_crops': ['cassava', 'cocoa', 'plantain', 'oil_palm'],
    },
    'high_plateau': {
        'regions': ['West', 'Northwest'],
        'rainfall_mm': 1500-2500,
        'best_crops': ['maize', 'beans', 'potato', 'vegetables'],
    },
    'sudano_sahel': {
        'regions': ['North', 'Far North', 'Adamawa'],
        'rainfall_mm': 600-1500,
        'best_crops': ['maize', 'rice', 'groundnut', 'cotton', 'sorghum'],
    },
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_total_input_cost(crop_type, hectares, use_optimal=True):
    """
    Calculate total input costs for a crop
    
    Args:
        crop_type: Type of crop (e.g., 'maize', 'rice')
        hectares: Number of hectares
        use_optimal: If True, use optimal inputs for yield maximization
        
    Returns:
        Dictionary with cost breakdown
    """
    costs = {}
    
    # Land preparation
    costs['land_preparation'] = (
        LAND_PREP_COSTS['tillage_per_ha'] + 
        LAND_PREP_COSTS['harrowing_per_ha']
    ) * hectares
    
    # Seeds
    if crop_type in SEED_REQUIREMENTS:
        seed_key = f"{crop_type}_improved" if use_optimal else f"{crop_type}_local"
        if seed_key in SEED_COSTS:
            costs['seeds'] = (
                SEED_COSTS[seed_key] * 
                SEED_REQUIREMENTS.get(seed_key, SEED_REQUIREMENTS.get(crop_type, 0)) * 
                hectares
            )
    
    # Fertilizers
    if crop_type in FERTILIZER_REQUIREMENTS:
        fert_req = FERTILIZER_REQUIREMENTS[crop_type]
        fert_cost = 0
        
        if 'npk_bags' in fert_req:
            fert_cost += fert_req['npk_bags'] * FERTILIZER_COSTS['npk_compound']
        if 'urea_bags' in fert_req:
            fert_cost += fert_req['urea_bags'] * FERTILIZER_COSTS['urea']
        if 'dap_bags' in fert_req:
            fert_cost += fert_req['dap_bags'] * FERTILIZER_COSTS['dap']
        if 'organic_manure_tons' in fert_req:
            fert_cost += fert_req['organic_manure_tons'] * FERTILIZER_COSTS['organic_manure_ton']
        
        costs['fertilizers'] = fert_cost * hectares
    
    # Pesticides/Herbicides
    costs['pesticides'] = (
        PESTICIDE_COSTS['herbicide_per_ha'] + 
        PESTICIDE_COSTS['insecticide_per_ha']
    ) * hectares
    
    if use_optimal:
        costs['pesticides'] += PESTICIDE_COSTS['fungicide_per_ha'] * hectares
    
    # Labor
    total_labor_days = (
        LABOR_COSTS['planting_days_per_ha'] + 
        LABOR_COSTS['weeding_days_per_ha'] + 
        LABOR_COSTS['harvesting_days_per_ha'] + 
        LABOR_COSTS['other_operations_days_per_ha']
    )
    costs['labor'] = total_labor_days * LABOR_COSTS['daily_wage'] * hectares
    
    # Equipment/machinery
    costs['equipment'] = (
        EQUIPMENT_COSTS['tractor_ploughing_per_ha'] + 
        EQUIPMENT_COSTS['tractor_harrowing_per_ha'] +
        EQUIPMENT_COSTS['fuel_operations_per_ha']
    ) * hectares
    
    if use_optimal:
        costs['equipment'] += EQUIPMENT_COSTS['mechanical_harvesting_per_ha'] * hectares
    
    # Total
    costs['total_cost'] = sum(costs.values())
    
    return costs


def calculate_expected_revenue(crop_type, hectares, use_optimal=True):
    """
    Calculate expected revenue from crop production
    
    Args:
        crop_type: Type of crop
        hectares: Number of hectares
        use_optimal: If True, use optimal yield projections
        
    Returns:
        Dictionary with revenue details
    """
    revenue = {}
    
    # Get yield
    if use_optimal and crop_type in OPTIMAL_YIELDS:
        yield_per_ha = OPTIMAL_YIELDS[crop_type]
    else:
        yield_key = f"{crop_type}_with_inputs" if use_optimal else f"{crop_type}_basic"
        yield_per_ha = EXPECTED_YIELDS.get(yield_key, 0)
    
    # Calculate total production
    total_production = yield_per_ha * hectares
    
    # Account for post-harvest losses
    loss_rate = POST_HARVEST_LOSSES.get(crop_type, 0.10)
    marketable_production = total_production * (1 - loss_rate)
    
    # Calculate revenue
    price_per_kg = FARMGATE_PRICES.get(crop_type, MARKET_PRICES.get(crop_type, 0))
    gross_revenue = marketable_production * 1000 * price_per_kg  # Convert tons to kg
    
    # Transportation costs
    transport_cost = marketable_production * TRANSPORT_COSTS['farm_to_market_per_ton']
    
    # Net revenue
    net_revenue = gross_revenue - transport_cost
    
    revenue['yield_per_ha_tons'] = yield_per_ha
    revenue['total_production_tons'] = total_production
    revenue['marketable_production_tons'] = marketable_production
    revenue['post_harvest_loss_tons'] = total_production - marketable_production
    revenue['price_per_kg'] = price_per_kg
    revenue['gross_revenue'] = gross_revenue
    revenue['transportation_cost'] = transport_cost
    revenue['net_revenue'] = net_revenue
    
    return revenue


def calculate_profit(crop_type, hectares, use_optimal=True):
    """
    Calculate net profit for a crop
    
    Returns:
        Dictionary with profit analysis
    """
    costs = get_total_input_cost(crop_type, hectares, use_optimal)
    revenue = calculate_expected_revenue(crop_type, hectares, use_optimal)
    
    net_profit = revenue['net_revenue'] - costs['total_cost']
    roi = (net_profit / costs['total_cost'] * 100) if costs['total_cost'] > 0 else 0
    
    return {
        'costs': costs,
        'revenue': revenue,
        'net_profit': net_profit,
        'roi_percentage': roi,
        'break_even_price': costs['total_cost'] / (revenue['marketable_production_tons'] * 1000) if revenue['marketable_production_tons'] > 0 else 0,
    }


# ============================================================================
# RECOMMENDATIONS SYSTEM
# ============================================================================

def get_crop_recommendations(region=None, season=None):
    """
    Get crop recommendations based on region and season
    """
    recommendations = []
    
    # General high-yield crops for Cameroon
    if not region:
        recommendations = [
            {
                'crop': 'maize',
                'reason': 'Most cultivated cereal, high demand, 2 seasons per year possible',
                'expected_yield': OPTIMAL_YIELDS['maize'],
                'investment_level': 'Medium',
            },
            {
                'crop': 'rice',
                'reason': 'High import substitution potential, government support',
                'expected_yield': OPTIMAL_YIELDS['rice'],
                'investment_level': 'Medium-High',
            },
            {
                'crop': 'cassava',
                'reason': 'Staple food, drought resistant, high yield potential',
                'expected_yield': OPTIMAL_YIELDS['cassava'],
                'investment_level': 'Low-Medium',
            },
        ]
    
    return recommendations