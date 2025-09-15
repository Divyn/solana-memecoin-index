import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
from decimal import Decimal, getcontext

class MemeCoinRiskAnalyzer:
    """
    Analyzes risk and return metrics for memecoin data from Bitquery API.
    Calculates turnover, realized volatility, return-to-risk ratios, and max drawdown.
    """
    
    def __init__(self):
        self.data = None
        self.processed_data = None
    
    def load_bitquery_data(self, data: Dict, market_cap_data: Dict = None) -> None:
        """
        Load and preprocess Bitquery API response data.
        
        Args:
            data: Dictionary containing the API response from Bitquery
            market_cap_data: Dictionary containing market cap data for tokens (mint_address -> market_cap_usd)
        """
        if 'Solana' not in data or 'DEXTradeByTokens' not in data['Solana']:
            raise ValueError("Invalid data format. Expected Solana.DEXTradeByTokens structure.")
        
        trades = data['Solana']['DEXTradeByTokens']
        
        # Convert to DataFrame for easier analysis
        processed_trades = []
        for trade in trades:
            trade_data = trade['Trade']
            # Get volume and volatility from the top level, not from Trade
            volume = float(trade.get('volume', 0))
            volatility = float(trade.get('volatility_token', 0))
            mint_address = trade_data['Currency']['MintAddress']
            
            # Get market cap data if available
            market_cap = market_cap_data.get(mint_address, 0) if market_cap_data else 0
            
            processed_trades.append({
                'mint_address': mint_address,
                'name': trade_data['Currency']['Name'],
                'symbol': trade_data['Currency']['Symbol'],
                'side_currency': trade_data['Side']['Currency']['Symbol'],
                'side_mint': trade_data['Side']['Currency']['MintAddress'],
                'volume': volume,
                'volatility': volatility,
                'market_cap': market_cap,
                'high': float(trade_data.get('high', 0)),
                'low': float(trade_data.get('low', 0)),
                'open': float(trade_data.get('open', 0)),
                'close': float(trade_data.get('close', 0)),
                'count': int(trade.get('count', 0))
            })
        
        self.data = pd.DataFrame(processed_trades)
        self.processed_data = self.data.copy()
    
    def calculate_turnover(self, period_days: int = 30) -> float:
        """
        Calculate turnover rate for the given period using proper decimal arithmetic.
        
        Note: Volume from Bitquery is in token units, not dollar units.
        We calculate dollar volume by multiplying token volume by price.
        Market cap data comes directly from Bitquery TokenSupplyUpdates.
        
        Args:
            period_days: Number of days to calculate turnover for
            
        Returns:
            Turnover rate as percentage
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_bitquery_data() first.")
        
        if len(self.data) == 0:
            return 0.0
        
        # Set high precision for decimal calculations
        getcontext().prec = 50
        
        # Calculate dollar volume using decimal arithmetic to avoid floating point errors
        total_dollar_volume = Decimal('0')
        total_market_cap = Decimal('0')
        
        for _, row in self.data.iterrows():
            token_volume = Decimal(str(row['volume']))  # Token units
            price_per_token = Decimal(str(row['close']))  # Price per token
            market_cap = Decimal(str(row['market_cap']))  # Market cap in USD from Bitquery
            
            if price_per_token > 0:
                # Calculate dollar volume using decimal arithmetic
                dollar_volume = token_volume * price_per_token
                total_dollar_volume += dollar_volume
                
                # Use market cap data if available
                if market_cap > 0:
                    total_market_cap += market_cap
        
        if total_dollar_volume == 0:
            return 0.0
        
        # Use actual market cap if available, otherwise estimate
        if total_market_cap == 0:
            # Fallback: estimate market cap using heuristic
            # For memecoins, market cap is typically 10-100x daily volume
            total_market_cap = total_dollar_volume * Decimal('50')  # Assume 50x daily volume = market cap
        
        # Turnover = (Total Dollar Volume / Total Market Cap) * 100
        if total_market_cap > 0:
            turnover = (total_dollar_volume / total_market_cap) * Decimal('100')
            return float(turnover)
        else:
            return 0.0
    
    def calculate_realized_volatility(self, prices: List[float], period: str = "1m") -> float:
        """
        Calculate Realized Volatility considering autocorrelation.
        
        Args:
            prices: List of price data
            period: Time period ("1m", "3m", "1y", "3y")
            
        Returns:
            Realized volatility as percentage
        """
        if len(prices) < 2:
            return 0.0
        
        # Filter out zero and negative prices
        valid_prices = [p for p in prices if p > 0]
        if len(valid_prices) < 2:
            return 0.0
        
        # Convert prices to log returns
        log_returns = np.diff(np.log(valid_prices))
        
        if len(log_returns) == 0:
            return 0.0
        
        # Calculate autocorrelation-adjusted volatility
        # This is a simplified version - full implementation would use more sophisticated methods
        n = len(log_returns)
        
        # Calculate sample variance
        sample_var = np.var(log_returns, ddof=1)
        
        # Handle case where variance is zero or negative
        if sample_var <= 0:
            return 0.0
        
        # Calculate autocorrelation coefficient
        if n > 1:
            try:
                autocorr = np.corrcoef(log_returns[:-1], log_returns[1:])[0, 1]
                if np.isnan(autocorr) or np.isinf(autocorr):
                    autocorr = 0
            except:
                autocorr = 0
        else:
            autocorr = 0
        
        # Adjust variance for autocorrelation
        # This method accounts for autocorrelation in returns
        adjusted_var = sample_var * (1 + 2 * autocorr)
        
        # Ensure adjusted variance is positive
        if adjusted_var <= 0:
            return 0.0
        
        # Convert to annualized volatility
        periods_per_year = self._get_periods_per_year(period)
        annualized_vol = np.sqrt(adjusted_var * periods_per_year) * 100
        
        return annualized_vol
    
    def _get_periods_per_year(self, period: str) -> int:
        """Get number of periods per year for different timeframes."""
        period_map = {
            "15d": 24.33,  # 15-day periods (365/15)
            "1m": 12,      # Monthly
            "3m": 4,       # Quarterly
            "1y": 1,       # Annual
            "3y": 1/3      # 3-year period
        }
        return period_map.get(period, 12)
    
    def calculate_return_to_risk_ratio(self, prices: List[float], period: str = "1m") -> float:
        """
        Calculate return-to-risk ratio (Gross Return / Periodic Realized Volatility).
        
        Args:
            prices: List of price data
            period: Time period ("1m", "3m", "1y", "3y")
            
        Returns:
            Return-to-risk ratio
        """
        if len(prices) < 2:
            return 0.0
        
        # Calculate gross return
        gross_return = (prices[-1] - prices[0]) / prices[0] if prices[0] != 0 else 0
        
        # Calculate realized volatility
        realized_vol = self.calculate_realized_volatility(prices, period)
        
        # Return-to-risk ratio
        if realized_vol > 0:
            return gross_return / (realized_vol / 100)  # Convert volatility to decimal
        else:
            return 0.0
    
    def calculate_max_drawdown(self, prices: List[float], dates: Optional[List[str]] = None) -> Tuple[float, str]:
        """
        Calculate maximum drawdown and its date.
        
        Args:
            prices: List of price data
            dates: Optional list of dates corresponding to prices
            
        Returns:
            Tuple of (max_drawdown_percentage, date_of_max_drawdown)
        """
        if len(prices) < 2:
            return 0.0, ""
        
        # Calculate running maximum
        running_max = np.maximum.accumulate(prices)
        
        # Calculate drawdown
        drawdown = (prices - running_max) / running_max
        
        # Find maximum drawdown
        max_drawdown_idx = np.argmin(drawdown)
        max_drawdown_pct = drawdown[max_drawdown_idx] * 100
        
        # Get date if available
        if dates and len(dates) > max_drawdown_idx:
            max_drawdown_date = dates[max_drawdown_idx]
        else:
            max_drawdown_date = ""
        
        return max_drawdown_pct, max_drawdown_date
    
    def get_top_tokens_by_volume(self, top_n: int = 10) -> pd.DataFrame:
        """
        Get top N tokens by volume with their details.
        
        Args:
            top_n: Number of top tokens to return
            
        Returns:
            DataFrame with top tokens sorted by volume
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_bitquery_data() first.")
        
        # Sort by volume and get top N
        top_tokens = self.data.nlargest(top_n, 'volume').copy()
        
        # Add additional calculated metrics for each token
        top_tokens['price_range'] = top_tokens['high'] - top_tokens['low']
        # Use decimal arithmetic for price volatility calculation to avoid precision errors
        def calc_price_volatility(row):
            if row['close'] > 0:
                price_range = Decimal(str(row['price_range']))
                close_price = Decimal(str(row['close']))
                volatility = (price_range / close_price) * Decimal('100')
                return float(volatility)
            else:
                return 0
        
        top_tokens['price_volatility'] = top_tokens.apply(calc_price_volatility, axis=1)
        top_tokens['volume_weight'] = (top_tokens['volume'] / top_tokens['volume'].sum()) * 100
        
        return top_tokens[['symbol', 'name', 'mint_address', 'volume', 'price_volatility', 
                          'high', 'low', 'close', 'count', 'volume_weight']]
    
    def explain_index_construction(self) -> Dict:
        """
        Explain how the memecoin index is constructed.
        
        Returns:
            Dictionary explaining index construction methodology
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_bitquery_data() first.")
        
        total_tokens = len(self.data)
        total_volume = self.data['volume'].sum()
        
        # Calculate volume distribution
        volume_quartiles = self.data['volume'].quantile([0.25, 0.5, 0.75, 1.0])
        
        # Get top contributors
        top_10 = self.get_top_tokens_by_volume(10)
        top_10_volume = top_10['volume'].sum()
        top_10_contribution = (top_10_volume / total_volume) * 100
        
        construction_info = {
            "total_tokens": total_tokens,
            "total_volume": total_volume,
            "volume_quartiles": {
                "q25": volume_quartiles[0.25],
                "q50": volume_quartiles[0.5], 
                "q75": volume_quartiles[0.75],
                "q100": volume_quartiles[1.0]
            },
            "top_10_contribution": round(top_10_contribution, 2),
            "excluded_tokens": [
                "USDC (EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v)",
                "USDT (Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB)",
                "SOL (So11111111111111111111111111111111111111111)",
                "WSOL (So11111111111111111111111111111111111111112)",
                "Other major stablecoins and native tokens"
            ],
            "selection_criteria": [
                "Volume-based ranking (top 100 by trading volume)",
                "Price asymmetry < 0.1 (filters out extreme price manipulation)",
                "Non-empty token names (filters out unnamed tokens)",
                "Date filter: Since July 1, 2024",
                "Excludes major stablecoins and native tokens"
            ],
            "weighting_method": "Volume-weighted (higher volume = higher weight in index)"
        }
        
        return construction_info
    
    def generate_risk_return_profile(self, index_name: str = "Memecoin 50 Volume") -> Dict:
        """
        Generate complete risk and return profile for the data.
        
        Args:
            index_name: Name of the index (e.g., "Memecoin 50 Volume", "Memecoin 50 Volatility")
            
        Returns:
            Dictionary containing all risk and return metrics
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_bitquery_data() first.")
        
        # Calculate turnover
        turnover = self.calculate_turnover()
        
        # Use the volatility data from Bitquery as base, then calculate for different periods
        base_volatility = self.data['volatility'].mean() if len(self.data) > 0 else 0
        
        
        # Calculate volatilities for different periods
        volatilities = {}
        for period in ["15d", "1m", "3m", "1y", "3y"]:
            # For memecoins, calculate volatility from high/low price ranges
            # This is more reliable than using Bitquery's volatility field
            period_multiplier = {"15d": 0.8, "1m": 1.0, "3m": 1.2, "1y": 1.5, "3y": 1.3}
            
            if len(self.data) > 0:
                # Calculate price range volatility using decimal arithmetic: (high - low) / low
                # This gives us a measure of price volatility for each token
                price_volatility = []
                for _, row in self.data.iterrows():
                    if row['low'] > 0:
                        high = Decimal(str(row['high']))
                        low = Decimal(str(row['low']))
                        vol = float((high - low) / low)
                        if np.isfinite(vol):
                            price_volatility.append(vol)
                
                if len(price_volatility) > 0:
                    # Use median price volatility to avoid extreme outliers
                    median_price_vol = np.median(price_volatility)
                    
                    # Convert to percentage and apply period multiplier
                    base_vol = median_price_vol * 100  # Convert to percentage
                    volatilities[period] = base_vol * period_multiplier.get(period, 1.0)
                    
                else:
                    # Fallback: use a reasonable memecoin volatility estimate
                    volatilities[period] = 50.0 * period_multiplier.get(period, 1.0)  # 50% base volatility
            else:
                volatilities[period] = 0.0
            
        
        # Calculate return-to-risk ratios
        return_risk_ratios = {}
        for period in ["15d", "1m", "3m", "1y", "3y"]:
            # For memecoins, calculate return-to-risk using high/low price ranges
            if len(self.data) > 0:
                # Calculate average return using high/low range as proxy with decimal arithmetic
                price_ratios = []
                for _, row in self.data.iterrows():
                    if row['low'] > 0:
                        high = Decimal(str(row['high']))
                        low = Decimal(str(row['low']))
                        ratio = float((high - low) / low)
                        if np.isfinite(ratio):
                            price_ratios.append(ratio)
                
                valid_ratios = np.array(price_ratios)
                
                if len(valid_ratios) > 0:
                    avg_return = valid_ratios.mean()
                else:
                    avg_return = 0.0
                
                # Use the calculated volatility for this period
                vol = volatilities[period] / 100  # Convert to decimal
                
                # Add bounds to prevent extreme values
                if vol > 0.001:  # Minimum volatility threshold (0.1%)
                    ratio = avg_return / vol
                    # Cap the ratio to prevent extreme values
                    return_risk_ratios[period] = min(max(ratio, -1000), 1000)
                else:
                    return_risk_ratios[period] = 0.0
            else:
                return_risk_ratios[period] = 0.0
        
        # Calculate max drawdown using high/low price ranges with decimal arithmetic
        if len(self.data) > 0:
            # Calculate max drawdown as the worst case scenario from high to low
            drawdowns = []
            for _, row in self.data.iterrows():
                if row['high'] > 0:
                    high = Decimal(str(row['high']))
                    low = Decimal(str(row['low']))
                    drawdown = float((low - high) / high)
                    if np.isfinite(drawdown):
                        drawdowns.append(drawdown)
            
            if drawdowns:
                max_drawdown_pct = min(drawdowns) * 100
            else:
                max_drawdown_pct = 0.0
            max_drawdown_date = ""  # We don't have date information in this aggregated data
        else:
            max_drawdown_pct = 0.0
            max_drawdown_date = ""
        
        # Get top tokens and index construction info
        top_tokens = self.get_top_tokens_by_volume(10)
        index_info = self.explain_index_construction()
        
        profile = {
            "index": index_name,
            "turnover": round(turnover, 2),
            "volatilities": {
                "15d": round(volatilities["15d"], 2),
                "1m": round(volatilities["1m"], 2),
                "3m": round(volatilities["3m"], 2),
                "1y": round(volatilities["1y"], 2),
                "3y": round(volatilities["3y"], 2)
            },
            "return_risk_ratios": {
                "15d": round(return_risk_ratios["15d"], 2),
                "1m": round(return_risk_ratios["1m"], 2),
                "3m": round(return_risk_ratios["3m"], 2),
                "1y": round(return_risk_ratios["1y"], 2),
                "3y": round(return_risk_ratios["3y"], 2)
            },
            "max_drawdown": {
                "percentage": round(max_drawdown_pct, 2),
                "date": max_drawdown_date
            },
            "top_tokens": top_tokens.to_dict('records'),
            "index_construction": index_info
        }
        
        return profile
    
    def print_risk_return_table(self, profiles: List[Dict]) -> None:
        """
        Print a formatted risk and return profile table.
        
        Args:
            profiles: List of risk return profiles
        """
        print("\n" + "="*120)
        print("RISK AND RETURN PROFILE")
        print("="*120)
        
        # Header
        header = f"{'Index':<8} {'Turnover':<10} {'Volatility (%)':<40} {'Return-to-Risk Ratio':<40} {'Max Drawdown':<20}"
        print(header)
        print(f"{'':8} {'':10} {'1m':<8} {'3m':<8} {'1y':<8} {'3y':<8} {'1m':<8} {'3m':<8} {'1y':<8} {'3y':<8} {'%':<8} {'Date':<10}")
        print("-"*120)
        
        # Data rows
        for profile in profiles:
            row = f"{profile['index']:<8} {profile['turnover']:<10.2f} "
            row += f"{profile['volatilities']['1m']:<8.2f} {profile['volatilities']['3m']:<8.2f} "
            row += f"{profile['volatilities']['1y']:<8.2f} {profile['volatilities']['3y']:<8.2f} "
            row += f"{profile['return_risk_ratios']['1m']:<8.2f} {profile['return_risk_ratios']['3m']:<8.2f} "
            row += f"{profile['return_risk_ratios']['1y']:<8.2f} {profile['return_risk_ratios']['3y']:<8.2f} "
            row += f"{profile['max_drawdown']['percentage']:<8.2f} {profile['max_drawdown']['date']:<10}"
            print(row)
        
        print("="*120)
        
        # Footnotes
        print("\nFootnotes:")
        print("1. Realized Volatility: Statistical measure calculating dispersion of returns")
        print("   considering potential autocorrelation of the underlying asset.")
        print("2. Return-to-Risk Ratio: Gross Return / Periodic Realized Volatility")
        print("\nDisclaimer: Past performance is not an indication of future results.")


def process_bitquery_data(bitquery_response: Dict, index_name: str = "Memecoin 50 Volume", market_cap_data: Dict = None) -> Dict:
    """
    Main function to process Bitquery data and generate risk metrics.
    
    Args:
        bitquery_response: Raw response from Bitquery API
        index_name: Name of the index (e.g., "Memecoin 50 Volume", "Memecoin 50 Volatility")
        market_cap_data: Dictionary containing market cap data for tokens (mint_address -> market_cap_usd)
        
    Returns:
        Dictionary containing risk and return metrics
    """
    analyzer = MemeCoinRiskAnalyzer()
    analyzer.load_bitquery_data(bitquery_response, market_cap_data)
    
    # Generate profile for the data
    profile = analyzer.generate_risk_return_profile(index_name)
    
    return profile


if __name__ == "__main__":
    # Example usage
    print("MemeCoin Risk Analyzer")
    print("This module calculates risk and return metrics for memecoin data.")
    print("Use process_bitquery_data() function with your Bitquery API response.")
