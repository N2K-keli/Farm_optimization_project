"""
Yield Maximization Calculator for Cameroon Farms
Optimizes agricultural production for maximum yield output
"""

from cameroon_agri_data import (
    get_total_input_cost,
    calculate_expected_revenue,
    calculate_profit,
    OPTIMAL_YIELDS,
    EXPECTED_YIELDS,
    FARMGATE_PRICES,
    CROP_SEASONS,
    POST_HARVEST_LOSSES,
)


class YieldMaximizationCalculator:
    """
    Calculator for yield maximization strategy
    Focuses on achieving highest possible production per hectare
    """
    
    def __init__(self, crop_type, land_size_hectares, region=None):
        """
        Initialize calculator
        
        Args:
            crop_type: Type of crop to grow (e.g., 'maize', 'rice')
            land_size_hectares: Size of land in hectares
            region: Optional region specification
        """
        self.crop_type = crop_type
        self.land_size = land_size_hectares
        self.region = region
        
    def calculate_optimal_plan(self):
        """
        Calculate optimal farming plan for yield maximization
        
        Returns:
            Dictionary with complete analysis
        """
        # Get cost breakdown
        costs = get_total_input_cost(self.crop_type, self.land_size, use_optimal=True)
        
        # Get revenue projections
        revenue = calculate_expected_revenue(self.crop_type, self.land_size, use_optimal=True)
        
        # Calculate profit
        profit_analysis = calculate_profit(self.crop_type, self.land_size, use_optimal=True)
        
        # Get crop-specific details
        crop_info = CROP_SEASONS.get(self.crop_type, {})
        
        # Compile results
        results = {
            'crop_type': self.crop_type,
            'land_size_hectares': self.land_size,
            'land_size_acres': self.land_size * 2.471,  # Convert to acres
            
            # Cost breakdown
            'cost_breakdown': costs,
            'cost_per_hectare': costs['total_cost'] / self.land_size,
            
            # Production details
            'expected_yield_per_ha_tons': revenue['yield_per_ha_tons'],
            'total_production_tons': revenue['total_production_tons'],
            'total_production_kg': revenue['total_production_tons'] * 1000,
            'marketable_production_tons': revenue['marketable_production_tons'],
            'post_harvest_loss_percentage': POST_HARVEST_LOSSES.get(self.crop_type, 0.10) * 100,
            'post_harvest_loss_tons': revenue['post_harvest_loss_tons'],
            
            # Revenue details
            'farmgate_price_per_kg': revenue['price_per_kg'],
            'gross_revenue': revenue['gross_revenue'],
            'transportation_cost': revenue['transportation_cost'],
            'net_revenue': revenue['net_revenue'],
            
            # Profit analysis
            'net_profit': profit_analysis['net_profit'],
            'roi_percentage': profit_analysis['roi_percentage'],
            'break_even_price_per_kg': profit_analysis['break_even_price'],
            
            # Crop timing
            'growing_days': crop_info.get('growing_days', 'N/A'),
            'seasons_per_year': crop_info.get('seasons_per_year', 1),
            'best_planting_months': crop_info.get('best_planting_months', []),
            
            # Recommendations
            'recommendations': self._generate_recommendations(costs, revenue, profit_analysis),
        }
        
        return results
    
    def _generate_recommendations(self, costs, revenue, profit_analysis):
        """
        Generate specific recommendations for yield maximization
        """
        recommendations = []
        
        # Check profitability
        if profit_analysis['net_profit'] > 0:
            recommendations.append({
                'type': 'positive',
                'message': f"This farming plan is profitable with an estimated net profit of {profit_analysis['net_profit']:,.0f} XAF and ROI of {profit_analysis['roi_percentage']:.1f}%"
            })
        else:
            recommendations.append({
                'type': 'warning',
                'message': f"This plan shows a loss of {abs(profit_analysis['net_profit']):,.0f} XAF. Consider cost reduction strategies or alternative crops."
            })
        
        # Yield optimization tips
        recommendations.append({
            'type': 'tip',
            'message': "For maximum yield, ensure timely application of all fertilizers in split doses"
        })
        
        recommendations.append({
            'type': 'tip',
            'message': "Use certified improved seeds for significantly higher yields (2-3x increase possible)"
        })
        
        recommendations.append({
            'type': 'tip',
            'message': "Implement integrated pest management to minimize crop losses, especially for fall armyworm in maize"
        })
        
        recommendations.append({
            'type': 'tip',
            'message': "Consider small-scale irrigation to reduce dependency on rainfall and increase yields by 30-50%"
        })
        
        # Post-harvest recommendations
        loss_pct = POST_HARVEST_LOSSES.get(self.crop_type, 0.10) * 100
        if loss_pct > 15:
            recommendations.append({
                'type': 'warning',
                'message': f"Post-harvest losses for {self.crop_type} average {loss_pct:.0f}%. Invest in proper storage and timely processing."
            })
        
        # ROI-based recommendations
        if profit_analysis['roi_percentage'] < 30:
            recommendations.append({
                'type': 'warning',
                'message': "ROI is below 30%. Consider improving efficiency or exploring value-addition opportunities."
            })
        elif profit_analysis['roi_percentage'] > 50:
            recommendations.append({
                'type': 'positive',
                'message': f"Excellent ROI of {profit_analysis['roi_percentage']:.1f}%! This is a highly profitable venture."
            })
        
        return recommendations
    
    def get_input_schedule(self):
        """
        Generate detailed input application schedule
        """
        crop_info = CROP_SEASONS.get(self.crop_type, {})
        growing_days = crop_info.get('growing_days', 120)
        
        schedule = []
        
        # Planting stage
        schedule.append({
            'stage': 'Land Preparation',
            'timing': 'Weeks 1-2 before planting',
            'activities': [
                'Clear and plough the land',
                'Apply organic manure if available',
                'Harrow and level the field',
                'Mark planting rows',
            ]
        })
        
        schedule.append({
            'stage': 'Planting',
            'timing': 'Day 0',
            'activities': [
                f'Plant certified improved {self.crop_type} seeds',
                'Apply basal fertilizer (NPK)',
                'Ensure proper spacing for optimal yield',
                'Treat seeds with fungicide before planting',
            ]
        })
        
        # Early growth
        schedule.append({
            'stage': 'Early Growth',
            'timing': f'Weeks 2-4 ({int(growing_days * 0.2)} days)',
            'activities': [
                'First weeding (or herbicide application)',
                'Monitor for pests and diseases',
                'Ensure adequate moisture',
                'Thin plants if necessary for optimal spacing',
            ]
        })
        
        # Mid-season
        schedule.append({
            'stage': 'Vegetative Growth',
            'timing': f'Weeks 4-8 ({int(growing_days * 0.5)} days)',
            'activities': [
                'Apply first top-dressing fertilizer (Urea)',
                'Second weeding',
                'Pest control (especially for fall armyworm in maize)',
                'Irrigation if rainfall is insufficient',
            ]
        })
        
        # Late season
        schedule.append({
            'stage': 'Reproductive Stage',
            'timing': f'Weeks 8-12 ({int(growing_days * 0.75)} days)',
            'activities': [
                'Apply second top-dressing fertilizer',
                'Continue pest and disease monitoring',
                'Ensure adequate water during flowering',
                'Apply fungicide if disease pressure is high',
            ]
        })
        
        # Harvest
        schedule.append({
            'stage': 'Maturity & Harvest',
            'timing': f'Week {growing_days // 7} ({growing_days} days)',
            'activities': [
                'Harvest at optimal maturity',
                'Dry produce to proper moisture content',
                'Sort and grade for market',
                'Store in improved storage facilities',
            ]
        })
        
        return schedule
    
    def compare_with_basic_farming(self):
        """
        Compare optimal (yield maximization) vs basic farming
        """
        # Optimal farming
        optimal = calculate_profit(self.crop_type, self.land_size, use_optimal=True)
        
        # Basic farming
        basic = calculate_profit(self.crop_type, self.land_size, use_optimal=False)
        
        comparison = {
            'optimal': {
                'total_cost': optimal['costs']['total_cost'],
                'production_tons': optimal['revenue']['marketable_production_tons'],
                'revenue': optimal['revenue']['net_revenue'],
                'profit': optimal['net_profit'],
                'roi': optimal['roi_percentage'],
            },
            'basic': {
                'total_cost': basic['costs']['total_cost'],
                'production_tons': basic['revenue']['marketable_production_tons'],
                'revenue': basic['revenue']['net_revenue'],
                'profit': basic['net_profit'],
                'roi': basic['roi_percentage'],
            },
            'difference': {
                'additional_investment': optimal['costs']['total_cost'] - basic['costs']['total_cost'],
                'additional_production': optimal['revenue']['marketable_production_tons'] - basic['revenue']['marketable_production_tons'],
                'additional_revenue': optimal['revenue']['net_revenue'] - basic['revenue']['net_revenue'],
                'additional_profit': optimal['net_profit'] - basic['net_profit'],
                'roi_improvement': optimal['roi_percentage'] - basic['roi_percentage'],
            }
        }
        
        return comparison
    
    def get_summary_report(self):
        """
        Generate a concise summary report
        """
        results = self.calculate_optimal_plan()
        
        summary = f"""
╔════════════════════════════════════════════════════════════════╗
║          YIELD MAXIMIZATION ANALYSIS - {self.crop_type.upper()}           
╚════════════════════════════════════════════════════════════════╝

LAND SIZE: {self.land_size} hectares ({results['land_size_acres']:.2f} acres)

INVESTMENT REQUIRED:
  Total Cost:               {results['cost_breakdown']['total_cost']:>15,.0f} XAF
  Cost per Hectare:         {results['cost_per_hectare']:>15,.0f} XAF

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
    """
    Example usage
    """
    # Create calculator for 2 hectares of maize
    calculator = YieldMaximizationCalculator('maize', 2.0)
    
    # Get complete analysis
    results = calculator.calculate_optimal_plan()
    
    # Print summary
    print(calculator.get_summary_report())
    
    # Get input schedule
    schedule = calculator.get_input_schedule()
    print("\nFARMING SCHEDULE:")
    for stage in schedule:
        print(f"\n{stage['stage']} - {stage['timing']}")
        for activity in stage['activities']:
            print(f"  • {activity}")
    
    # Compare with basic farming
    comparison = calculator.compare_with_basic_farming()
    print("\n\nCOMPARISON WITH BASIC FARMING:")
    print(f"Additional Investment: {comparison['difference']['additional_investment']:,.0f} XAF")
    print(f"Additional Production: {comparison['difference']['additional_production']:.2f} tons")
    print(f"Additional Profit: {comparison['difference']['additional_profit']:,.0f} XAF")


if __name__ == "__main__":
    main()