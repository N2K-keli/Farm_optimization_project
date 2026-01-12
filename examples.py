"""
Example Usage Script - Cameroon Farm Optimization
Demonstrates how to use the yield maximization calculator programmatically
"""

from yield_maximization import YieldMaximizationCalculator
from cameroon_agri_data import OPTIMAL_YIELDS, FARMGATE_PRICES


def example_1_simple_calculation():
    """Example 1: Simple calculation for 1 hectare of maize"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Simple Maize Calculation (1 hectare)")
    print("="*70)
    
    calculator = YieldMaximizationCalculator('maize', 1.0)
    print(calculator.get_summary_report())


def example_2_multiple_crops():
    """Example 2: Compare different crops on same land"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Comparing Different Crops (2 hectares)")
    print("="*70)
    
    crops = ['maize', 'rice', 'beans', 'groundnut']
    land_size = 2.0
    
    results = []
    for crop in crops:
        calculator = YieldMaximizationCalculator(crop, land_size)
        analysis = calculator.calculate_optimal_plan()
        results.append({
            'crop': crop,
            'investment': analysis['cost_breakdown']['total_cost'],
            'production': analysis['marketable_production_tons'],
            'revenue': analysis['net_revenue'],
            'profit': analysis['net_profit'],
            'roi': analysis['roi_percentage']
        })
    
    print(f"\nComparison for {land_size} hectares:\n")
    print(f"{'Crop':<12} {'Investment':>15} {'Production':>12} {'Net Profit':>15} {'ROI':>8}")
    print("-" * 70)
    
    for r in results:
        print(f"{r['crop'].capitalize():<12} {r['investment']:>15,.0f} {r['production']:>12.2f}t {r['profit']:>15,.0f} {r['roi']:>7.1f}%")
    
    # Find most profitable
    best = max(results, key=lambda x: x['profit'])
    print(f"\n✓ Most Profitable: {best['crop'].capitalize()} with {best['profit']:,.0f} XAF profit")


def example_3_scale_analysis():
    """Example 3: Analyze different farm sizes"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Scale Analysis - Maize at Different Sizes")
    print("="*70)
    
    crop = 'maize'
    sizes = [0.5, 1.0, 2.0, 5.0, 10.0]
    
    print(f"\n{'Size (ha)':<10} {'Investment':>15} {'Production':>12} {'Profit':>15} {'ROI':>8}")
    print("-" * 70)
    
    for size in sizes:
        calculator = YieldMaximizationCalculator(crop, size)
        analysis = calculator.calculate_optimal_plan()
        
        print(f"{size:<10.1f} {analysis['cost_breakdown']['total_cost']:>15,.0f} "
              f"{analysis['marketable_production_tons']:>12.2f}t "
              f"{analysis['net_profit']:>15,.0f} {analysis['roi_percentage']:>7.1f}%")


def example_4_seasonal_planning():
    """Example 4: Multi-season planning"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Annual Planning - 2 Seasons of Maize (2 hectares)")
    print("="*70)
    
    calculator = YieldMaximizationCalculator('maize', 2.0)
    single_season = calculator.calculate_optimal_plan()
    
    # Calculate for 2 seasons
    annual_investment = single_season['cost_breakdown']['total_cost'] * 2
    annual_production = single_season['marketable_production_tons'] * 2
    annual_revenue = single_season['net_revenue'] * 2
    annual_profit = single_season['net_profit'] * 2
    annual_roi = (annual_profit / annual_investment * 100)
    
    print(f"\nSINGLE SEASON (120 days):")
    print(f"  Investment:          {single_season['cost_breakdown']['total_cost']:>15,.0f} XAF")
    print(f"  Production:          {single_season['marketable_production_tons']:>15.2f} tons")
    print(f"  Net Profit:          {single_season['net_profit']:>15,.0f} XAF")
    print(f"  ROI:                 {single_season['roi_percentage']:>15.1f} %")
    
    print(f"\nANNUAL (2 seasons):")
    print(f"  Total Investment:    {annual_investment:>15,.0f} XAF")
    print(f"  Total Production:    {annual_production:>15.2f} tons")
    print(f"  Total Net Profit:    {annual_profit:>15,.0f} XAF")
    print(f"  Annual ROI:          {annual_roi:>15.1f} %")


def example_5_optimal_vs_basic():
    """Example 5: Compare optimal vs basic farming"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Optimal vs Basic Farming Comparison (1 hectare Maize)")
    print("="*70)
    
    calculator = YieldMaximizationCalculator('maize', 1.0)
    comparison = calculator.compare_with_basic_farming()
    
    print("\nBASIC FARMING (Minimal inputs):")
    print(f"  Investment:          {comparison['basic']['total_cost']:>15,.0f} XAF")
    print(f"  Production:          {comparison['basic']['production_tons']:>15.2f} tons")
    print(f"  Net Profit:          {comparison['basic']['profit']:>15,.0f} XAF")
    print(f"  ROI:                 {comparison['basic']['roi']:>15.1f} %")
    
    print("\nOPTIMAL FARMING (Maximum yield inputs):")
    print(f"  Investment:          {comparison['optimal']['total_cost']:>15,.0f} XAF")
    print(f"  Production:          {comparison['optimal']['production_tons']:>15.2f} tons")
    print(f"  Net Profit:          {comparison['optimal']['profit']:>15,.0f} XAF")
    print(f"  ROI:                 {comparison['optimal']['roi']:>15.1f} %")
    
    print("\nADDITIONAL BENEFITS OF OPTIMAL:")
    print(f"  Extra Investment:    {comparison['difference']['additional_investment']:>15,.0f} XAF")
    print(f"  Extra Production:    {comparison['difference']['additional_production']:>15.2f} tons")
    print(f"  Extra Profit:        {comparison['difference']['additional_profit']:>15,.0f} XAF")
    print(f"  ROI Improvement:     {comparison['difference']['roi_improvement']:>15.1f} %")
    
    # Calculate return ratio
    if comparison['difference']['additional_investment'] > 0:
        return_ratio = comparison['difference']['additional_profit'] / comparison['difference']['additional_investment']
        print(f"\n  → For every 1 XAF invested extra, you gain {return_ratio:.2f} XAF in profit")


def example_6_break_even_analysis():
    """Example 6: Break-even price analysis"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Break-Even Price Analysis (1 hectare Rice)")
    print("="*70)
    
    calculator = YieldMaximizationCalculator('rice', 1.0)
    analysis = calculator.calculate_optimal_plan()
    
    current_price = analysis['farmgate_price_per_kg']
    break_even = analysis['break_even_price_per_kg']
    margin = current_price - break_even
    margin_pct = (margin / current_price * 100)
    
    print(f"\nPRICE ANALYSIS:")
    print(f"  Current Farmgate Price:  {current_price:>10,.0f} XAF/kg")
    print(f"  Break-Even Price:        {break_even:>10,.0f} XAF/kg")
    print(f"  Safety Margin:           {margin:>10,.0f} XAF/kg ({margin_pct:.1f}%)")
    
    print(f"\nPRICE SCENARIOS:")
    scenarios = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
    for scenario in scenarios:
        price = current_price * scenario
        production = analysis['marketable_production_tons'] * 1000
        revenue = price * production
        costs = analysis['cost_breakdown']['total_cost']
        profit = revenue - costs - analysis['transportation_cost']
        
        status = "✓ PROFIT" if profit > 0 else "✗ LOSS"
        print(f"  {scenario*100:>3.0f}% price ({price:>6,.0f} XAF/kg): {profit:>12,.0f} XAF {status}")


def main():
    """Run all examples"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*15 + "CAMEROON FARM OPTIMIZATION EXAMPLES" + " "*18 + "║")
    print("╚" + "="*68 + "╝")
    
    examples = [
        example_1_simple_calculation,
        example_2_multiple_crops,
        example_3_scale_analysis,
        example_4_seasonal_planning,
        example_5_optimal_vs_basic,
        example_6_break_even_analysis,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\nError in {example.__name__}: {str(e)}")
    
    print("\n" + "="*70)
    print("Examples completed! Use these patterns in your own calculations.")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()