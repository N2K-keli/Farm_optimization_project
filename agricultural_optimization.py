"""
Agricultural Optimization Calculator for Cameroon Farms
Balanced optimization considering both yield and cost factors
Finds the optimal balance between maximizing production and minimizing expenses
"""

from cameroon_agri_data import (
    LAND_PREP_COSTS,
    SEED_COSTS,
    SEED_REQUIREMENTS,
    FERTILIZER_COSTS,
    FERTILIZER_REQUIREMENTS,
    PESTICIDE_COSTS,
    LABOR_COSTS,
    EQUIPMENT_COSTS,
    TRANSPORT_COSTS,
    STORAGE_COSTS,
    IRRIGATION_COSTS,
    EXPECTED_YIELDS,
    OPTIMAL_YIELDS,
    FARMGATE_PRICES,
    CROP_SEASONS,
    POST_HARVEST_LOSSES,
)


class AgriculturalOptimizationCalculator:
    """
    Calculator for agricultural optimization strategy
    Balances yield maximization with cost minimization
    Aims for best profit efficiency (ROI) rather than max yield or min cost
    """
    
    def __init__(self, crop_type, land_size_hectares, priority='balanced'):
        """
        Initialize calculator
        
        Args:
            crop_type: Type of crop to grow (e.g., 'maize', 'rice')
            land_size_hectares: Size of land in hectares
            priority: 'balanced', 'yield_focus', or 'cost_focus'
        """
        self.crop_type = crop_type
        self.land_size = land_size_hectares
        self.priority = priority
        
        # Optimization weights based on priority
        if priority == 'yield_focus':
            self.input_level = 0.85  # 85% of optimal inputs
        elif priority == 'cost_focus':
            self.input_level = 0.65  # 65% of optimal inputs
        else:  # balanced
            self.input_level = 0.75  # 75% of optimal inputs (sweet spot)
    
    def calculate_optimized_plan(self):
        """
        Calculate optimized farming plan
        Uses medium inputs - balance of improved and local methods
        
        Returns:
            Dictionary with complete analysis
        """
        costs = {}
        input_factor = self.input_level
        
        # 1. LAND PREPARATION (Optimized - selective mechanization)
        # Use tractor for main ploughing, manual for harrowing
        costs['land_preparation'] = (
            LAND_PREP_COSTS['tillage_per_ha'] * 0.85 +  # Tractor ploughing
            LAND_PREP_COSTS['harrowing_per_ha'] * 0.7   # Manual harrowing
        ) * self.land_size
        
        # 2. SEEDS (Mix of improved and local)
        # Use improved seeds but at slightly reduced rate
        seed_key = f"{self.crop_type}_improved"
        if seed_key not in SEED_COSTS:
            seed_key = self.crop_type
        
        seed_cost_per_kg = SEED_COSTS.get(seed_key, SEED_COSTS.get(f"{self.crop_type}_local", 1000))
        seed_qty = SEED_REQUIREMENTS.get(seed_key, SEED_REQUIREMENTS.get(self.crop_type, 25))
        
        costs['seeds'] = seed_cost_per_kg * seed_qty * input_factor * self.land_size
        
        # 3. FERTILIZERS (Balanced - chemical + organic)
        # Use 75% of optimal chemical fertilizer + organic supplement
        if self.crop_type in FERTILIZER_REQUIREMENTS:
            fert_req = FERTILIZER_REQUIREMENTS[self.crop_type]
            fert_cost = 0
            
            # Use reduced NPK
            if 'npk_bags' in fert_req:
                fert_cost += (fert_req['npk_bags'] * input_factor) * FERTILIZER_COSTS['npk_compound']
            
            # Use reduced Urea
            if 'urea_bags' in fert_req:
                fert_cost += (fert_req['urea_bags'] * input_factor) * FERTILIZER_COSTS['urea']
            
            # Use reduced DAP if needed
            if 'dap_bags' in fert_req:
                fert_cost += (fert_req['dap_bags'] * input_factor) * FERTILIZER_COSTS['dap']
            
            # Add organic manure (1.5 tons/ha)
            organic_amount = fert_req.get('organic_manure_tons', 1.5)
            fert_cost += organic_amount * FERTILIZER_COSTS['organic_manure_ton']
            
            costs['fertilizers'] = fert_cost * self.land_size
        else:
            costs['fertilizers'] = 1.5 * FERTILIZER_COSTS['organic_manure_ton'] * self.land_size
        
        # 4. PESTICIDES (Targeted application)
        # Use herbicides and selective insecticide application
        costs['pesticides'] = (
            PESTICIDE_COSTS['herbicide_per_ha'] * 0.9 +  # Full herbicide
            PESTICIDE_COSTS['insecticide_per_ha'] * 0.8  # Targeted insecticide
        ) * self.land_size
        
        # 5. LABOR (Mix of hired and family)
        # Assume 30% family labor, 70% hired
        total_labor_days = (
            LABOR_COSTS['planting_days_per_ha'] + 
            LABOR_COSTS['weeding_days_per_ha'] + 
            LABOR_COSTS['harvesting_days_per_ha'] + 
            LABOR_COSTS['other_operations_days_per_ha']
        )
        costs['labor'] = (total_labor_days * 0.7) * LABOR_COSTS['daily_wage'] * self.land_size
        
        # 6. EQUIPMENT (Selective mechanization)
        # Use tractor for key operations, manual for others
        costs['equipment'] = (
            EQUIPMENT_COSTS['tractor_ploughing_per_ha'] * 0.85 +
            EQUIPMENT_COSTS['tractor_harrowing_per_ha'] * 0.5 +
            EQUIPMENT_COSTS['fuel_operations_per_ha'] * 0.7
        ) * self.land_size
        
        # 7. IRRIGATION (Minimal supplementary)
        # Small-scale supplementary irrigation in dry periods
        costs['irrigation'] = (
            IRRIGATION_COSTS['pump_operation_per_ha'] * 0.3 if input_factor > 0.7 else 0
        ) * self.land_size
        
        # 8. TRANSPORTATION (Regional markets)
        costs['transportation'] = 0  # Calculated later based on yield
        
        # 9. STORAGE (Improved on-farm)
        costs['storage'] = 0  # Calculated later
        
        # Total cost (preliminary)
        costs['total_cost'] = sum(costs.values())
        
        # Calculate expected yield (75-85% of optimal)
        optimal_yield_key = self.crop_type
        
        if optimal_yield_key in OPTIMAL_YIELDS:
            # Yield scales with input level but with diminishing returns
            # At 75% inputs, expect ~80% of optimal yield
            yield_factor = 0.60 + (input_factor * 0.45)  # 60% base + 45% from inputs
            yield_per_ha = OPTIMAL_YIELDS[optimal_yield_key] * yield_factor
        else:
            with_inputs_key = f"{self.crop_type}_with_inputs"
            yield_per_ha = EXPECTED_YIELDS.get(with_inputs_key, 2.5)
        
        total_production = yield_per_ha * self.land_size
        
        # Post-harvest losses (reduced by 30% due to better handling)
        base_loss_rate = POST_HARVEST_LOSSES.get(self.crop_type, 0.10)
        loss_rate = base_loss_rate * 0.7  # 30% reduction in losses
        marketable_production = total_production * (1 - loss_rate)
        
        # Transportation costs (now calculated)
        transport_cost = marketable_production * TRANSPORT_COSTS['farm_to_market_per_ton'] * 0.85
        costs['transportation'] = transport_cost
        costs['total_cost'] += transport_cost
        
        # Storage costs (improved storage)
        storage_cost = marketable_production * STORAGE_COSTS['improved_storage_per_ton'] * 0.5
        costs['storage'] = storage_cost
        costs['total_cost'] += storage_cost
        
        # Revenue calculation
        price_per_kg = FARMGATE_PRICES.get(self.crop_type, 500)
        gross_revenue = marketable_production * 1000 * price_per_kg
        net_revenue = gross_revenue - transport_cost
        
        # Profit
        net_profit = net_revenue - costs['total_cost']
        roi = (net_profit / costs['total_cost'] * 100) if costs['total_cost'] > 0 else 0
        
        # Efficiency metrics
        profit_per_hectare = net_profit / self.land_size
        cost_per_kg = costs['total_cost'] / (marketable_production * 1000) if marketable_production > 0 else 0
        profit_per_kg = net_profit / (marketable_production * 1000) if marketable_production > 0 else 0
        
        # Get crop info
        crop_info = CROP_SEASONS.get(self.crop_type, {})
        
        results = {
            'crop_type': self.crop_type,
            'land_size_hectares': self.land_size,
            'land_size_acres': self.land_size * 2.471,
            'strategy': 'AGRICULTURAL OPTIMIZATION',
            'input_level_percentage': input_factor * 100,
            
            # Cost breakdown
            'cost_breakdown': costs,
            'cost_per_hectare': costs['total_cost'] / self.land_size,
            
            # Production details
            'expected_yield_per_ha_tons': yield_per_ha,
            'total_production_tons': total_production,
            'total_production_kg': total_production * 1000,
            'marketable_production_tons': marketable_production,
            'post_harvest_loss_percentage': loss_rate * 100,
            'post_harvest_loss_tons': total_production - marketable_production,
            
            # Revenue details
            'farmgate_price_per_kg': price_per_kg,
            'gross_revenue': gross_revenue,
            'transportation_cost': transport_cost,
            'net_revenue': net_revenue,
            
            # Profit analysis
            'net_profit': net_profit,
            'roi_percentage': roi,
            'break_even_price_per_kg': costs['total_cost'] / (marketable_production * 1000) if marketable_production > 0 else 0,
            
            # Efficiency metrics
            'profit_per_hectare': profit_per_hectare,
            'cost_per_kg_produced': cost_per_kg,
            'profit_per_kg_produced': profit_per_kg,
            'production_efficiency': (marketable_production / self.land_size) / (costs['total_cost'] / self.land_size) if costs['total_cost'] > 0 else 0,
            
            # Crop timing
            'growing_days': crop_info.get('growing_days', 'N/A'),
            'seasons_per_year': crop_info.get('seasons_per_year', 1),
            'best_planting_months': crop_info.get('best_planting_months', []),
            
            # Recommendations
            'recommendations': self._generate_recommendations(costs, net_profit, roi, yield_per_ha),
        }
        
        return results
    
    def _generate_recommendations(self, costs, net_profit, roi, yield_per_ha):
        """Generate specific recommendations for agricultural optimization"""
        recommendations = []
        
        # Performance assessment
        if roi > 250:
            recommendations.append({
                'type': 'positive',
                'message': f"Excellent optimization! ROI of {roi:.1f}% shows great balance between cost and yield."
            })
        elif roi > 150:
            recommendations.append({
                'type': 'positive',
                'message': f"Good optimization with ROI of {roi:.1f}%. This balanced approach is working well."
            })
        elif net_profit > 0:
            recommendations.append({
                'type': 'positive',
                'message': f"Profitable with {net_profit:,.0f} XAF profit and {roi:.1f}% ROI."
            })
        else:
            recommendations.append({
                'type': 'warning',
                'message': f"Current plan shows a loss. Consider adjusting input levels or crop choice."
            })
        
        # Balanced approach tips
        recommendations.append({
            'type': 'tip',
            'message': "Balanced approach uses improved seeds with reduced chemical fertilizers supplemented by organic manure"
        })
        
        recommendations.append({
            'type': 'tip',
            'message': "Selective mechanization (tractor for heavy work, manual for light tasks) optimizes cost-benefit"
        })
        
        recommendations.append({
            'type': 'tip',
            'message': "Combining family labor (30%) with hired labor (70%) reduces costs while ensuring timely operations"
        })
        
        recommendations.append({
            'type': 'tip',
            'message': "Improved storage and handling reduces post-harvest losses by 30%, increasing profit"
        })
        
        recommendations.append({
            'type': 'tip',
            'message': "Target regional markets for better prices while keeping transport costs manageable"
        })
        
        # Optimization suggestions
        optimal_yield = OPTIMAL_YIELDS.get(self.crop_type, 4.0)
        yield_efficiency = (yield_per_ha / optimal_yield * 100) if optimal_yield > 0 else 0
        
        if yield_efficiency < 70:
            recommendations.append({
                'type': 'warning',
                'message': f"Current yield is {yield_efficiency:.1f}% of maximum. Consider increasing inputs slightly."
            })
        elif yield_efficiency > 85:
            recommendations.append({
                'type': 'tip',
                'message': f"You're achieving {yield_efficiency:.1f}% of maximum yield - excellent efficiency!"
            })
        
        return recommendations
    
    def compare_all_strategies(self):
        """Compare all three optimization strategies"""
        from yield_maximization import YieldMaximizationCalculator
        from cost_minimization import CostMinimizationCalculator
        
        # Agricultural optimization (current)
        optimized = self.calculate_optimized_plan()
        
        # Yield maximization
        yield_calc = YieldMaximizationCalculator(self.crop_type, self.land_size)
        yield_max = yield_calc.calculate_optimal_plan()
        
        # Cost minimization
        cost_calc = CostMinimizationCalculator(self.crop_type, self.land_size)
        cost_min = cost_calc.calculate_minimal_plan()
        
        comparison = {
            'cost_minimization': {
                'strategy': 'Cost Minimization (Lowest investment)',
                'total_cost': cost_min['cost_breakdown']['total_cost'],
                'production_tons': cost_min['marketable_production_tons'],
                'revenue': cost_min['net_revenue'],
                'profit': cost_min['net_profit'],
                'roi': cost_min['roi_percentage'],
                'cost_per_kg': cost_min['cost_breakdown']['total_cost'] / (cost_min['marketable_production_tons'] * 1000) if cost_min['marketable_production_tons'] > 0 else 0,
                'profit_per_ha': cost_min['net_profit'] / self.land_size,
            },
            'agricultural_optimization': {
                'strategy': 'Agricultural Optimization (Balanced approach)',
                'total_cost': optimized['cost_breakdown']['total_cost'],
                'production_tons': optimized['marketable_production_tons'],
                'revenue': optimized['net_revenue'],
                'profit': optimized['net_profit'],
                'roi': optimized['roi_percentage'],
                'cost_per_kg': optimized['cost_per_kg_produced'],
                'profit_per_ha': optimized['profit_per_hectare'],
            },
            'yield_maximization': {
                'strategy': 'Yield Maximization (Maximum production)',
                'total_cost': yield_max['cost_breakdown']['total_cost'],
                'production_tons': yield_max['marketable_production_tons'],
                'revenue': yield_max['net_revenue'],
                'profit': yield_max['net_profit'],
                'roi': yield_max['roi_percentage'],
                'cost_per_kg': yield_max['cost_breakdown']['total_cost'] / (yield_max['marketable_production_tons'] * 1000) if yield_max['marketable_production_tons'] > 0 else 0,
                'profit_per_ha': yield_max['net_profit'] / self.land_size,
            }
        }
        
        # Determine best strategy
        best_roi = max(comparison.values(), key=lambda x: x['roi'])
        best_profit = max(comparison.values(), key=lambda x: x['profit'])
        best_efficiency = min(comparison.values(), key=lambda x: x['cost_per_kg'])
        
        comparison['recommendations'] = {
            'highest_roi': best_roi['strategy'],
            'highest_profit': best_profit['strategy'],
            'most_efficient': best_efficiency['strategy'],
        }
        
        return comparison
    
    def sensitivity_analysis(self):
        """
        Analyze how profit changes with different input levels
        """
        scenarios = []
        
        for input_pct in [50, 60, 70, 75, 80, 85, 90, 95, 100]:
            # Temporarily adjust input level
            original = self.input_level
            self.input_level = input_pct / 100
            
            # Calculate
            result = self.calculate_optimized_plan()
            
            scenarios.append({
                'input_level_pct': input_pct,
                'total_cost': result['cost_breakdown']['total_cost'],
                'production_tons': result['marketable_production_tons'],
                'net_profit': result['net_profit'],
                'roi': result['roi_percentage'],
                'profit_per_ha': result['profit_per_hectare'],
            })
            
            # Restore original
            self.input_level = original
        
        # Find sweet spot (highest profit per hectare / cost ratio)
        best_scenario = max(scenarios, key=lambda x: x['roi'])
        
        return {
            'scenarios': scenarios,
            'recommended_input_level': best_scenario['input_level_pct'],
            'optimal_profit': best_scenario['net_profit'],
            'optimal_roi': best_scenario['roi'],
        }
    
    def get_summary_report(self):
        """Generate a concise summary report"""
        results = self.calculate_optimized_plan()
        
        summary = f"""
╔════════════════════════════════════════════════════════════════╗
║       AGRICULTURAL OPTIMIZATION ANALYSIS - {self.crop_type.upper()}           
╚════════════════════════════════════════════════════════════════╝

STRATEGY: Balanced Agricultural Optimization
  - Mix of improved and local methods
  - Moderate chemical fertilizers + organic supplement
  - Selective mechanization (where cost-effective)
  - Family + hired labor mix (30% / 70%)
  - Supplementary irrigation if needed
  - Improved post-harvest handling
  - Input Level: {results['input_level_percentage']:.0f}% of maximum

LAND SIZE: {self.land_size} hectares ({results['land_size_acres']:.2f} acres)

INVESTMENT REQUIRED:
  Total Cost:               {results['cost_breakdown']['total_cost']:>15,.0f} XAF
  Cost per Hectare:         {results['cost_per_hectare']:>15,.0f} XAF
  Cost per kg Produced:     {results['cost_per_kg_produced']:>15,.0f} XAF/kg

EXPECTED PRODUCTION:
  Yield per Hectare:        {results['expected_yield_per_ha_tons']:>15.2f} tons
  Total Production:         {results['total_production_tons']:>15.2f} tons
  Marketable Production:    {results['marketable_production_tons']:>15.2f} tons
  Post-Harvest Loss:        {results['post_harvest_loss_percentage']:>15.1f} %

REVENUE PROJECTIONS:
  Farmgate Price:           {results['farmgate_price_per_kg']:>15,.0f} XAF/kg
  Gross Revenue:            {results['gross_revenue']:>15,.0f} XAF
  Transportation Cost:      {results['transportation_cost']:>15,.0f} XAF
  Net Revenue:              {results['net_revenue']:>15,.0f} XAF

PROFITABILITY:
  Net Profit:               {results['net_profit']:>15,.0f} XAF
  Return on Investment:     {results['roi_percentage']:>15.1f} %
  Profit per Hectare:       {results['profit_per_hectare']:>15,.0f} XAF/ha
  Profit per kg:            {results['profit_per_kg_produced']:>15,.0f} XAF/kg
  Break-Even Price:         {results['break_even_price_per_kg']:>15,.0f} XAF/kg

EFFICIENCY METRICS:
  Production Efficiency:    {results['production_efficiency']:>15.2f}

TIMING:
  Growing Period:           {results['growing_days']} days
  Seasons per Year:         {results['seasons_per_year']}
  Planting Months:          {', '.join(results['best_planting_months'])}

═══════════════════════════════════════════════════════════════════
"""
        return summary


def main():
    """Example usage"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Agricultural Optimization for 1 hectare of Maize")
    print("="*70)
    
    # Create calculator
    calculator = AgriculturalOptimizationCalculator('maize', 1.0)
    
    # Get complete analysis
    print(calculator.get_summary_report())
    
    # Compare all strategies
    print("\n" + "="*70)
    print("COMPLETE STRATEGY COMPARISON")
    print("="*70)
    comparison = calculator.compare_all_strategies()
    
    print(f"\n{'Strategy':<45} {'Cost':>12} {'Yield':>10} {'Profit':>15} {'ROI':>8}")
    print("-" * 95)
    for key, data in comparison.items():
        if key != 'recommendations':
            print(f"{data['strategy']:<45} {data['total_cost']:>12,.0f} {data['production_tons']:>10.2f}t {data['profit']:>15,.0f} {data['roi']:>7.1f}%")
    
    print("\n" + "="*70)
    print("RECOMMENDATIONS:")
    print(f"  • Highest ROI: {comparison['recommendations']['highest_roi']}")
    print(f"  • Highest Total Profit: {comparison['recommendations']['highest_profit']}")
    print(f"  • Most Cost Efficient: {comparison['recommendations']['most_efficient']}")
    
    # Sensitivity analysis
    print("\n" + "="*70)
    print("SENSITIVITY ANALYSIS - Input Level vs Profitability")
    print("="*70)
    
    sensitivity = calculator.sensitivity_analysis()
    
    print(f"\n{'Input Level':<12} {'Cost':>12} {'Yield':>10} {'Profit':>15} {'ROI':>8} {'Profit/ha':>12}")
    print("-" * 75)
    for scenario in sensitivity['scenarios']:
        print(f"{scenario['input_level_pct']:>3.0f}%         {scenario['total_cost']:>12,.0f} {scenario['production_tons']:>10.2f}t "
              f"{scenario['net_profit']:>15,.0f} {scenario['roi']:>7.1f}% {scenario['profit_per_ha']:>12,.0f}")
    
    print(f"\n✓ RECOMMENDED INPUT LEVEL: {sensitivity['recommended_input_level']}% for optimal ROI")


if __name__ == "__main__":
    main()