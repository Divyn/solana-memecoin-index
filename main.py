"""
Main execution module for memecoin risk analysis.
Orchestrates data fetching, analysis, and display.
"""

from bitquery_data import fetch_memecoin_data
from analysis import analyze_memecoin_risk, calculate_performance_comparison
from display import display_risk_analysis_results, display_performance_comparison

def main():
    """
    Main function to run the complete memecoin risk analysis.
    """
    print("Fetching memecoin data from Bitquery...")
    data = fetch_memecoin_data()
    
    if data is None:
        print("Failed to fetch data. Please check your API token and connection.")
        return
    
    # Analyze the data
    results = analyze_memecoin_risk(data)
    
    if results is None:
        print("Failed to analyze data.")
        return
    
    volume_profile = results['volume_index']
    volatility_profile = results['volatility_index']
    
    # Display basic results
    display_risk_analysis_results(volume_profile, volatility_profile)
    
    # Calculate and display performance comparison
    performance_analysis = calculate_performance_comparison(volume_profile, volatility_profile)
    display_performance_comparison(volume_profile, volatility_profile, performance_analysis)
    
    return results

if __name__ == "__main__":
    # Run the complete analysis
    results = main()
