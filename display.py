"""
Display module for memecoin risk analysis results.
Handles all output formatting and presentation.
"""

def display_risk_analysis_results(volume_profile, volatility_profile):
    """
    Display comprehensive risk analysis results for both indices.
    
    Args:
        volume_profile: Risk profile for volume-ordered index
        volatility_profile: Risk profile for volatility-ordered index
    """
    print("\n" + "="*100)
    print("MEMECOIN RISK ANALYSIS RESULTS - COMPARISON")
    print("="*100)
    
    # Create comparison table
    print(f"{'Metric':<25} {'Memecoin 50 Volume':<20} {'Memecoin 50 Volatility':<20}")
    print("-"*55)
    print(f"{'Turnover (%)':<25} {volume_profile['turnover']:<20.2f} {volatility_profile['turnover']:<20.2f}")
    
    print(f"\n{'Realized Volatility (%)':<25}")
    for period in ["15d", "1m", "3m", "1y", "3y"]:
        print(f"  {period} Volatility (%)<25 {volume_profile['volatilities'][period]:<20.2f} {volatility_profile['volatilities'][period]:<20.2f}")
    
    print(f"\n{'Return-to-Risk Ratio':<25}")
    for period in ["15d", "1m", "3m", "1y", "3y"]:
        print(f"  {period} Return-to-Risk<25 {volume_profile['return_risk_ratios'][period]:<20.2f} {volatility_profile['return_risk_ratios'][period]:<20.2f}")
    
    print(f"\n{'Max Drawdown (%)':<25} {volume_profile['max_drawdown']['percentage']:<20.2f} {volatility_profile['max_drawdown']['percentage']:<20.2f}")
    
    # Display top tokens for both indices
    print("\n" + "="*100)
    print("TOP 10 TOKENS COMPARISON")
    print("="*100)
    
    print("MEMECOIN 50 VOLUME INDEX - Top 10 by Volume:")
    print(f"{'Rank':<4} {'Symbol':<12} {'Name':<20} {'Mint Address':<44} {'Volume':<15} {'Volatility':<12} {'Weight':<8}")
    print("-"*120)
    for i, token in enumerate(volume_profile['top_tokens'], 1):
        mint_short = token['mint_address'][:8] + "..." + token['mint_address'][-8:] if len(token['mint_address']) > 20 else token['mint_address']
        print(f"{i:<4} {token['symbol']:<12} {token['name'][:20]:<20} {mint_short:<44} "
              f"{token['volume']:<15.0f} {token['price_volatility']:<12.2f} {token['volume_weight']:<8.2f}%")
    
    print("\nMEMECOIN 50 VOLATILITY INDEX - Top 10 by Volatility:")
    print(f"{'Rank':<4} {'Symbol':<12} {'Name':<20} {'Mint Address':<44} {'Volume':<15} {'Volatility':<12} {'Weight':<8}")
    print("-"*120)
    for i, token in enumerate(volatility_profile['top_tokens'], 1):
        mint_short = token['mint_address'][:8] + "..." + token['mint_address'][-8:] if len(token['mint_address']) > 20 else token['mint_address']
        print(f"{i:<4} {token['symbol']:<12} {token['name'][:20]:<20} {mint_short:<44} "
              f"{token['volume']:<15.0f} {token['price_volatility']:<12.2f} {token['volume_weight']:<8.2f}%")
    
    # Display index construction details
    print("\n" + "="*100)
    print("INDEX CONSTRUCTION METHODOLOGY")
    print("="*100)
    
    vol_info = volume_profile['index_construction']
    vol_vol_info = volatility_profile['index_construction']
    
    print(f"{'Metric':<30} {'Memecoin 50 Volume':<20} {'Memecoin 50 Volatility':<20}")
    print("-"*70)
    print(f"{'Total Tokens':<30} {vol_info['total_tokens']:<20} {vol_vol_info['total_tokens']:<20}")
    print(f"{'Total Volume':<30} {vol_info['total_volume']:,.0f} {vol_vol_info['total_volume']:,.0f}")
    print(f"{'Top 10 Contribution (%)':<30} {vol_info['top_10_contribution']:<20.2f} {vol_vol_info['top_10_contribution']:<20.2f}")
    
    print("\nSelection Criteria:")
    for criterion in vol_info['selection_criteria']:
        print(f"  • {criterion}")
    
    print(f"\nWeighting Method: {vol_info['weighting_method']}")
    print("Note: Volatility Index uses volatility-based ranking instead of volume-based ranking")
    print("Note: 15-day metrics are included as memecoins typically have short lifespans")
    
    print("\nExcluded Tokens:")
    for token in vol_info['excluded_tokens']:
        print(f"  • {token}")
    
    print("="*100)

def display_performance_comparison(volume_profile, volatility_profile, performance_analysis):
    """
    Display comprehensive performance comparison between volume and volatility indexes.
    
    Args:
        volume_profile: Risk profile for volume-ordered index
        volatility_profile: Risk profile for volatility-ordered index
        performance_analysis: Performance comparison results
    """
    print("\n" + "="*100)
    print("PERFORMANCE COMPARISON: VOLUME vs VOLATILITY INDEXES")
    print("="*100)
    
    # Display performance comparison table
    print(f"\n{'Metric':<30} {'Volume Index':<20} {'Volatility Index':<20} {'Winner':<15}")
    print("-"*85)
    
    # Volatility comparison
    print(f"\n{'VOLATILITY ANALYSIS':<30}")
    print("-"*85)
    for period in ["15d", "1m", "3m", "1y", "3y"]:
        vol_vol = volume_profile['volatilities'][period]
        vol_vol_vol = volatility_profile['volatilities'][period]
        winner = "Volume" if vol_vol < vol_vol_vol else "Volatility" if vol_vol_vol < vol_vol else "Tie"
        print(f"  {period} Volatility (%)<25 {vol_vol:<20.2f} {vol_vol_vol:<20.2f} {winner:<15}")
    
    # Return-to-Risk comparison
    print(f"\n{'RETURN-TO-RISK ANALYSIS':<30}")
    print("-"*85)
    for period in ["15d", "1m", "3m", "1y", "3y"]:
        vol_ratio = volume_profile['return_risk_ratios'][period]
        vol_vol_ratio = volatility_profile['return_risk_ratios'][period]
        winner = "Volume" if vol_ratio > vol_vol_ratio else "Volatility" if vol_vol_ratio > vol_ratio else "Tie"
        print(f"  {period} Return-to-Risk<25 {vol_ratio:<20.2f} {vol_vol_ratio:<20.2f} {winner:<15}")
    
    # Risk assessment
    print(f"\n{'RISK ASSESSMENT':<30}")
    print("-"*85)
    vol_turnover = volume_profile['turnover']
    vol_vol_turnover = volatility_profile['turnover']
    vol_drawdown = volume_profile['max_drawdown']['percentage']
    vol_vol_drawdown = volatility_profile['max_drawdown']['percentage']
    
    print(f"  Turnover (%)<25 {vol_turnover:<20.2f} {vol_vol_turnover:<20.2f} {'Volume' if vol_turnover > vol_vol_turnover else 'Volatility' if vol_vol_turnover > vol_turnover else 'Tie':<15}")
    print(f"  Max Drawdown (%)<25 {vol_drawdown:<20.2f} {vol_vol_drawdown:<20.2f} {'Volume' if vol_drawdown > vol_vol_drawdown else 'Volatility' if vol_vol_drawdown > vol_drawdown else 'Tie':<15}")
    
    # Overall performance summary
    print(f"\n{'OVERALL PERFORMANCE SUMMARY':<30}")
    print("-"*85)
    print(f"  Lower Volatility Winner<25 {performance_analysis['volatility_winner']:<20}")
    print(f"  Higher Return-to-Risk Winner<25 {performance_analysis['return_risk_winner']:<20}")
    print(f"  Lower Risk Winner<25 {performance_analysis['risk_winner']:<20}")
    print(f"  Overall Winner<25 {performance_analysis['overall_winner']:<20}")
    
    # Investment recommendations
    print(f"\n{'INVESTMENT RECOMMENDATIONS':<30}")
    print("-"*85)
    print("  Memecoin 50 Volume Index:")
    print("    • Better for: Conservative investors, stable returns")
    print("    • Lower volatility across all timeframes")
    print("    • More predictable risk-return profile")
    print("    • Suitable for longer-term positions")
    
    print("\n  Memecoin 50 Volatility Index:")
    print("    • Better for: Aggressive traders, high-risk strategies")
    print("    • Higher volatility, potential for higher returns")
    print("    • More suitable for short-term trading")
    print("    • Higher risk, higher reward potential")
    
    print("="*100)
