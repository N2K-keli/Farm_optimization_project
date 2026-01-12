"""
Cost Minimization Calculator for Cameroon Farms
Optimizes agricultural production for minimum cost while meeting production goals
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


class CostMinimizationCalculator:
    """
    Calculator for cost minimization strategy
    Focuses on achieving production goals at minimum cost
    """
    
    def __init__(self, crop_type, land_size_hectares, budget=None, target_yield=None):
        """
        Initialize calculator
        
        Args:
            crop_type: Type of crop to grow (e.g., 'maize', 'rice')
            land_size_hectares: Size of land in hectares
            budget: Maximum budget in XAF (optional)
            target_yield: Target yield in tons (optional)
        """
        self.crop_type = crop_type
        self.land_size = land_size_hectares
        self.budget = budget
        self.target_yield = target_yield
        
    def calculate_minimal_plan(self):
        """
        Calculate minimal cost farming plan
        Uses local seeds, minimal fertilizers, manual labor, etc.
        
        Returns:
            Dictionary with complete analysis
        """
        costs = {}
        
        # 1. LAND PREPARATION (Reduced - manual methods)
        # Use manual labor instead of tractor where possible
        costs['land_preparation'] = (
            LAND_PREP_COSTS['tillage_per_ha'] * 0.6  # Manual/ox ploughing cheaper
        ) * self.land_size
        
        # 2. SEEDS (Use local varieties - cheaper)
        seed_key = f"{self.crop_type}_local"
        if seed_key not in SEED_COSTS:
            seed_key = self.crop_type
        
        seed_cost_per_kg = SEED_COSTS.get(seed_key, SEED_COSTS.get(f"{self.crop_type}_improved", 1000))
        seed_qty = SEED_REQUIREMENTS.get(seed_key, SEED_REQUIREMENTS.get(self.crop_type, 25))
        
        costs['seeds'] = seed_cost_per_kg * seed_qty * self.land_size
        
        # 3. FERTILIZERS (Minimal - organic focus)
        # Use reduced amounts and prefer organic manure over chemical
        if self.crop_type in FERTILIZER_REQUIREMENTS:
            fert_req = FERTILIZER_REQUIREMENTS[self.crop_type]
            fert_cost = 0
            
            # Use only 50% of recommended NPK
            if 'npk_bags' in fert_req:
                fert_cost += (fert_req['npk_bags'] * 0.5) * FERTILIZER_COSTS['npk_compound']
            
            # Skip expensive inputs like DAP, use organic instead
            if 'organic_manure_tons' in fert_req:
                fert_cost += fert_req['organic_manure_tons'] * FERTILIZER_COSTS['organic_manure_ton']
            else:
                # Add minimal organic manure (1 ton/ha)
                fert_cost += 1 * FERTILIZER_COSTS['organic_manure_ton']
            
            costs['fertilizers'] = fert_cost * self.land_size
        else:
            costs['fertilizers'] = FERTILIZER_COSTS['organic_manure_ton'] * self.land_size
        
        # 4. PESTICIDES (Minimal - spot treatment only)
        # Use only herbicides, skip expensive pesticides/fungicides
        costs['pesticides'] = (
            PESTICIDE_COSTS['herbicide_per_ha'] * 0.7  # Reduced herbicide
        ) * self.land_size
        
        # 5. LABOR (Use family/community labor)
        # Assume 50% family labor, 50% hired
        total_labor_days = (
            LABOR_COSTS['planting_days_per_ha'] + 
            LABOR_COSTS['weeding_days_per_ha'] + 
            LABOR_COSTS['harvesting_days_per_ha'] + 
            LABOR_COSTS['other_operations_days_per_ha']
        )
        costs['labor'] = (total_labor_days * 0.5) * LABOR_COSTS['daily_wage'] * self.land_size
        
        # 6. EQUIPMENT (Minimal - rent only essentials)
        # Skip mechanical planting/harvesting, use manual methods
        costs['equipment'] = (
            EQUIPMENT_COSTS['tractor_ploughing_per_ha'] * 0.4  # Cheaper ox/manual
        ) * self.land_size
        
        # 7. SKIP IRRIGATION (Rain-fed only)
        costs['irrigation'] = 0
        
        # 8. TRANSPORTATION (Use local markets)
        # Reduced transport cost by selling locally
        costs['transportation'] = 0  # Calculated later based on yield
        
        # 9. STORAGE (Basic on-farm storage)
        costs['storage'] = 0  # Calculated later
        
        # Total cost
        costs['total_cost'] = sum(costs.values())
        
        # Calculate expected yield with minimal inputs (50-60% of optimal)
        optimal_yield_key = self.crop_type
        basic_yield_key = f"{self.crop_type}_basic"
        
        if basic_yield_key in EXPECTED_YIELDS:
            yield_per_ha = EXPECTED_YIELDS[basic_yield_key]
        else:
            # Use 55% of optimal yield as estimate for minimal inputs
            yield_per_ha = OPTIMAL_YIELDS.get(optimal_yield_key, 2.0) * 0.55
        
        total_production = yield_per_ha * self.land_size
        
        # Post-harvest losses
        loss_rate = POST_HARVEST_LOSSES.get(self.crop_type, 0.10)
        marketable_production = total_production * (1 - loss_rate)
        
        # Transportation costs (now calculated)
        transport_cost = marketable_production * TRANSPORT_COSTS['farm_to_market_per_ton'] * 0.7  # Local market
        costs['transportation'] = transport_cost
        costs['total_cost'] += transport_cost
        
        # Storage costs (basic)
        storage_cost = marketable_production * STORAGE_COSTS['on_farm_storage_per_ton']
        costs['storage'] = storage_cost
        costs['total_cost'] += storage_cost
        
        # Revenue calculation
        price_per_kg = FARMGATE_PRICES.get(self.crop_type, 500)
        gross_revenue = marketable_production * 1000 * price_per_kg
        net_revenue = gross_revenue - transport_cost
        
        # Profit
        net_profit = net_revenue - costs['total_cost']
        roi = (net_profit / costs['total_cost'] * 100) if costs['total_cost'] > 0 else 0
        
        # Get crop info
        crop_info = CROP_SEASONS.get(self.crop_type, {})
        
        results = {
            'crop_type': self.crop_type,
            'land_size_hectares': self.land_size,
            'land_size_acres': self.land_size * 2.471,
            'strategy': 'COST MINIMIZATION',
            
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
            
            # Budget analysis
            'within_budget': True if not self.budget else (costs['total_cost'] <= self.budget),
            'budget_specified': self.budget,
            'budget_remaining': (self.budget - costs['total_cost']) if self.budget else None,
            
            # Crop timing
            'growing_days': crop_info.get('growing_days', 'N/A'),
            'seasons_per_year': crop_info.get('seasons_per_year', 1),
            'best_planting_months': crop_info.get('best_planting_months', []),
            
            # Recommendations
            'recommendations': self._generate_recommendations(costs, net_profit, roi),
        }
        
        return results
    
    def _generate_recommendations(self, costs, net_profit, roi):
        """Generate specific recommendations for cost minimization"""
        recommendations = []
        
        # Profitability check
        if net_profit > 0:
            recommendations.append({
                'type': 'positive',
                'message': f"Cost minimization strategy is profitable with net profit of {net_profit:,.0f} XAF (ROI: {roi:.1f}%)"
            })
        else:
            recommendations.append({
                'type': 'warning',
                'message': f"This minimal cost approach shows a loss of {abs(net_profit):,.0f} XAF. Consider increasing budget slightly or choosing different crop."
            })
        
        # Cost saving tips
        recommendations.append({
            'type': 'tip',
            'message': "Use local seed varieties - they're cheaper and better adapted to local conditions"
        })
        
        recommendations.append({
            'type': 'tip',
            'message': "Maximize use of organic manure (compost, animal waste) - free or very cheap and improves soil"
        })
        
        recommendations.append({
            'type': 'tip',
            'message': "Form cooperative groups to share equipment and reduce individual costs"
        })
        
        recommendations.append({
            'type': 'tip',
            'message': "Use family/community labor exchange systems to reduce hired labor costs"
        })
        
        recommendations.append({
            'type': 'tip',
            'message': "Practice intercropping (e.g., maize + beans) to maximize land use without extra cost"
        })
        
        recommendations.append({
            'type': 'tip',
            'message': "Sell at local markets to avoid high transportation costs to distant markets"
        })
        
        # Budget specific
        if self.budget:
            budget_used_pct = (costs['total_cost'] / self.budget * 100)
            if budget_used_pct <= 80:
                recommendations.append({
                    'type': 'positive',
                    'message': f"You're using only {budget_used_pct:.1f}% of your budget. Consider adding minimal fertilizer to boost yield."
                })
            elif budget_used_pct <= 100:
                recommendations.append({
                    'type': 'positive',
                    'message': f"Budget well utilized at {budget_used_pct:.1f}%. You're within limits."
                })
            else:
                recommendations.append({
                    'type': 'warning',
                    'message': f"Cost exceeds budget by {budget_used_pct - 100:.1f}%. Reduce land size or seek additional funds."
                })
        
        return recommendations
    
    def compare_strategies(self):
        """Compare cost minimization with other strategies"""
        from yield_maximization import YieldMaximizationCalculator
        
        # Minimal cost strategy
        minimal = self.calculate_minimal_plan()
        
        # Optimal yield strategy
        optimal_calc = YieldMaximizationCalculator(self.crop_type, self.land_size)
        optimal = optimal_calc.calculate_optimal_plan()
        
        # Medium strategy (60% of optimal inputs)
        medium_cost = optimal['cost_breakdown']['total_cost'] * 0.6
        medium_yield = optimal['expected_yield_per_ha_tons'] * 0.75  # 75% of optimal yield
        medium_production = medium_yield * self.land_size
        medium_marketable = medium_production * (1 - POST_HARVEST_LOSSES.get(self.crop_type, 0.10))
        medium_revenue = medium_marketable * 1000 * FARMGATE_PRICES.get(self.crop_type, 500)
        medium_transport = medium_marketable * TRANSPORT_COSTS['farm_to_market_per_ton']
        medium_profit = medium_revenue - medium_cost - medium_transport
        medium_roi = (medium_profit / medium_cost * 100) if medium_cost > 0 else 0
        
        comparison = {
            'minimal_cost': {
                'strategy': 'Minimal Cost (Local seeds, organic focus)',
                'total_cost': minimal['cost_breakdown']['total_cost'],
                'production_tons': minimal['marketable_production_tons'],
                'revenue': minimal['net_revenue'],
                'profit': minimal['net_profit'],
                'roi': minimal['roi_percentage'],
                'cost_per_kg_produced': minimal['cost_breakdown']['total_cost'] / (minimal['marketable_production_tons'] * 1000) if minimal['marketable_production_tons'] > 0 else 0,
            },
            'medium_input': {
                'strategy': 'Medium Input (Some improved inputs)',
                'total_cost': medium_cost,
                'production_tons': medium_marketable,
                'revenue': medium_revenue - medium_transport,
                'profit': medium_profit,
                'roi': medium_roi,
                'cost_per_kg_produced': medium_cost / (medium_marketable * 1000) if medium_marketable > 0 else 0,
            },
            'optimal_yield': {
                'strategy': 'Yield Maximization (All improved inputs)',
                'total_cost': optimal['cost_breakdown']['total_cost'],
                'production_tons': optimal['marketable_production_tons'],
                'revenue': optimal['net_revenue'],
                'profit': optimal['net_profit'],
                'roi': optimal['roi_percentage'],
                'cost_per_kg_produced': optimal['cost_breakdown']['total_cost'] / (optimal['marketable_production_tons'] * 1000) if optimal['marketable_production_tons'] > 0 else 0,
            }
        }
        
        return comparison
    
    def optimize_within_budget(self):
        """
        Find the best approach within budget constraints
        Returns recommendations for budget allocation
        """
        if not self.budget:
            return None
        
        minimal = self.calculate_minimal_plan()
        total_cost = minimal['cost_breakdown']['total_cost']
        
        if total_cost > self.budget:
            # Budget too low - need to reduce land size
            affordable_land = (self.budget / total_cost) * self.land_size
            return {
                'feasible': False,
                'message': f"Budget of {self.budget:,.0f} XAF is insufficient for {self.land_size} hectares.",
                'recommendation': f"With this budget, you can afford approximately {affordable_land:.2f} hectares using minimal cost approach.",
                'alternative': "Consider: 1) Increase budget, 2) Reduce land size, 3) Seek credit/loan, 4) Form cooperative"
            }
        else:
            # Budget sufficient
            remaining = self.budget - total_cost
            remaining_pct = (remaining / self.budget * 100)
            
            suggestions = []
            if remaining >= 50000:  # Enough for some improvements
                suggestions.append(f"Add {remaining // 35000:.0f} bags of NPK fertilizer (+15-20% yield)")
            if remaining >= 30000:
                suggestions.append(f"Upgrade to improved seeds ({remaining // (SEED_COSTS.get(f'{self.crop_type}_improved', 2000) * SEED_REQUIREMENTS.get(self.crop_type, 25)):.1f} ha worth)")
            if remaining >= 20000:
                suggestions.append("Hire additional labor for better weed control")
            
            return {
                'feasible': True,
                'budget_used': total_cost,
                'budget_remaining': remaining,
                'remaining_percentage': remaining_pct,
                'message': f"Budget is sufficient! You have {remaining:,.0f} XAF ({remaining_pct:.1f}%) remaining.",
                'suggestions': suggestions if suggestions else ["Budget tightly utilized - good planning!"]
            }
    
    def get_summary_report(self):
        """Generate a concise summary report"""
        results = self.calculate_minimal_plan()
        
        budget_section = ""
        if self.budget:
            budget_section = f"""
BUDGET ANALYSIS:
  Budget Specified:         {self.budget:>15,.0f} XAF
  Budget Used:              {results['cost_breakdown']['total_cost']:>15,.0f} XAF
  Budget Remaining:         {results['budget_remaining']:>15,.0f} XAF
  Within Budget:            {'✓ YES' if results['within_budget'] else '✗ NO'}
"""
        
        summary = f"""
╔════════════════════════════════════════════════════════════════╗
║          COST MINIMIZATION ANALYSIS - {self.crop_type.upper()}           
╚════════════════════════════════════════════════════════════════╝

STRATEGY: Minimal Cost Approach
  - Local seed varieties
  - Organic-focused fertilization
  - Manual/family labor prioritized
  - Rain-fed cultivation
  - Local market sales

LAND SIZE: {self.land_size} hectares ({results['land_size_acres']:.2f} acres)

INVESTMENT REQUIRED:
  Total Cost:               {results['cost_breakdown']['total_cost']:>15,.0f} XAF
  Cost per Hectare:         {results['cost_per_hectare']:>15,.0f} XAF
{budget_section}
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
  Break-Even Price:         {results['break_even_price_per_kg']:>15,.0f} XAF/kg

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
    print("EXAMPLE 1: Cost Minimization for 1 hectare of Maize")
    print("="*70)
    
    # Create calculator
    calculator = CostMinimizationCalculator('maize', 1.0)
    
    # Get complete analysis
    print(calculator.get_summary_report())
    
    # Compare strategies
    print("\n" + "="*70)
    print("STRATEGY COMPARISON")
    print("="*70)
    comparison = calculator.compare_strategies()
    
    print(f"\n{'Strategy':<40} {'Cost':>12} {'Yield':>10} {'Profit':>15} {'ROI':>8}")
    print("-" * 90)
    for key, data in comparison.items():
        print(f"{data['strategy']:<40} {data['total_cost']:>12,.0f} {data['production_tons']:>10.2f}t {data['profit']:>15,.0f} {data['roi']:>7.1f}%")
    
    # Budget optimization
    print("\n" + "="*70)
    print("EXAMPLE 2: Working with Budget Constraint (500,000 XAF)")
    print("="*70)
    
    calculator2 = CostMinimizationCalculator('maize', 1.0, budget=500000)
    print(calculator2.get_summary_report())
    
    budget_analysis = calculator2.optimize_within_budget()
    if budget_analysis:
        print("\nBUDGET OPTIMIZATION:")
        print(f"  Feasible: {budget_analysis['feasible']}")
        print(f"  Message: {budget_analysis['message']}")
        if 'suggestions' in budget_analysis:
            print(f"  Suggestions:")
            for suggestion in budget_analysis['suggestions']:
                print(f"    • {suggestion}")


if __name__ == "__main__":
    main()