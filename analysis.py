"""
Risk analysis module for memecoin data.
Handles all risk calculations and analysis logic.
"""

from calculations import process_bitquery_data

def analyze_memecoin_risk(data):
    """
    Main function to analyze risk metrics for both volume and volatility indices.
    
    Args:
        data: Dictionary containing both volume and volatility ordered data
        
    Returns:
        Dictionary containing both risk profiles
    """
    print("Data fetched successfully!")
    
    # Process volume-ordered data (Memecoin 50 Volume Index)
    print("\n" + "="*80)
    print("PROCESSING VOLUME-ORDERED DATA (Memecoin 50 Volume Index)")
    print("="*80)
    
    volume_data = data['volume_ordered']
    market_cap_data = data.get('market_cap_data', {})
    
    if volume_data and 'data' in volume_data and volume_data['data'] is not None:
        if 'Solana' in volume_data['data']:
            volume_tokens = volume_data['data']['Solana']['DEXTradeByTokens']
            print(f"Found {len(volume_tokens)} tokens in volume-ordered data")
            volume_profile = process_bitquery_data(volume_data['data'], "Memecoin 50 Volume", market_cap_data)
        else:
            print("No 'Solana' key found in volume data")
            return None
    else:
        print("Unexpected volume data structure or data is None")
        return None
    
    # Process volatility-ordered data (Memecoin 50 Volatility Index)
    print("\n" + "="*80)
    print("PROCESSING VOLATILITY-ORDERED DATA (Memecoin 50 Volatility Index)")
    print("="*80)
    
    volatility_data = data['volatility_ordered']
    
    if volatility_data and 'data' in volatility_data and volatility_data['data'] is not None:
        if 'Solana' in volatility_data['data']:
            volatility_tokens = volatility_data['data']['Solana']['DEXTradeByTokens']
            print(f"Found {len(volatility_tokens)} tokens in volatility-ordered data")
            volatility_profile = process_bitquery_data(volatility_data['data'], "Memecoin 50 Volatility", market_cap_data)
        else:
            print("No 'Solana' key found in volatility data")
            return None
    else:
        print("Unexpected volatility data structure or data is None")
        return None
    
    return {
        'volume_index': volume_profile,
        'volatility_index': volatility_profile
    }

def calculate_performance_comparison(volume_profile, volatility_profile):
    """
    Calculate comprehensive performance comparison between volume and volatility indexes.
    
    Args:
        volume_profile: Risk profile for volume-ordered index
        volatility_profile: Risk profile for volatility-ordered index
        
    Returns:
        Dictionary with performance analysis results
    """
    # Count wins for each index
    volatility_wins = 0
    return_risk_wins = 0
    risk_wins = 0
    
    # Volatility comparison (lower is better)
    for period in ["15d", "1m", "3m", "1y", "3y"]:
        vol_vol = volume_profile['volatilities'][period]
        vol_vol_vol = volatility_profile['volatilities'][period]
        if vol_vol < vol_vol_vol:
            volatility_wins += 1
    
    # Return-to-Risk comparison (higher is better)
    for period in ["15d", "1m", "3m", "1y", "3y"]:
        vol_ratio = volume_profile['return_risk_ratios'][period]
        vol_vol_ratio = volatility_profile['return_risk_ratios'][period]
        if vol_ratio > vol_vol_ratio:
            return_risk_wins += 1
    
    # Risk assessment (lower drawdown is better)
    vol_drawdown = volume_profile['max_drawdown']['percentage']
    vol_vol_drawdown = volatility_profile['max_drawdown']['percentage']
    if vol_drawdown > vol_vol_drawdown:
        risk_wins += 1
    
    # Determine winners
    volatility_winner = "Volume" if volatility_wins > 2 else "Volatility" if volatility_wins < 2 else "Tie"
    return_risk_winner = "Volume" if return_risk_wins > 2 else "Volatility" if return_risk_wins < 2 else "Tie"
    risk_winner = "Volume" if vol_drawdown < vol_vol_drawdown else "Volatility" if vol_vol_drawdown < vol_drawdown else "Tie"
    
    # Overall winner based on majority
    total_wins = (1 if volatility_winner == "Volume" else 0) + (1 if return_risk_winner == "Volume" else 0) + (1 if risk_winner == "Volume" else 0)
    overall_winner = "Volume" if total_wins >= 2 else "Volatility" if total_wins <= 1 else "Tie"
    
    return {
        'volatility_winner': volatility_winner,
        'return_risk_winner': return_risk_winner,
        'risk_winner': risk_winner,
        'overall_winner': overall_winner,
        'volatility_wins': volatility_wins,
        'return_risk_wins': return_risk_wins,
        'total_wins': total_wins
    }
