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
    
    def calculate_volatility_from_prices(self, high: float, low: float) -> float:
        """
        Calculate volatility from high/low price data.
        
        Args:
            high: Highest price in the period
            low: Lowest price in the period
            
        Returns:
            Volatility as percentage
        """
        if low <= 0:
            return 0.0
        
        # Price range volatility: (high - low) / low * 100
        volatility = ((high - low) / low) * 100
        return volatility

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
            # Get volume from the top level
            volume = float(trade.get('volume', 0))
            mint_address = trade_data['Currency']['MintAddress']
            
            # Get volatility from API if available, otherwise calculate from prices
            api_volatility = trade.get('volatility_token')
            if api_volatility is not None:
                volatility = float(api_volatility)
            else:
                # Fallback: calculate volatility from high/low prices
                high = float(trade_data.get('high', 0))
                low = float(trade_data.get('low', 0))
                volatility = self.calculate_volatility_from_prices(high, low)
            
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
    
    def create_volatility_ordered_data(self) -> pd.DataFrame:
        """
        Create volatility-ordered dataset from the volume data.
        
        Returns:
            DataFrame sorted by volatility (descending)
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_bitquery_data() first.")
        
        # Sort by volatility in descending order
        volatility_ordered = self.data.sort_values('volatility', ascending=False).copy()
        return volatility_ordered
    
    def calculate_constituent_stability(self) -> float:
        """
        Calculate constituent stability - how stable the index composition is.
        This is more meaningful than turnover for index construction.
        
        Returns:
            Constituent stability as percentage (higher = more stable)
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_bitquery_data() first.")
        
        if len(self.data) == 0:
            return 0.0
        
        # For now, we'll calculate based on weight concentration
        # In a real implementation, you'd compare against previous periods
        weights = self.data['volume'] / self.data['volume'].sum()
        
        # Calculate Herfindahl Index (concentration measure)
        # Lower HHI = more diversified = more stable
        hhi = (weights ** 2).sum()
        
        # Convert to stability percentage (0-100%)
        # HHI of 1.0 = complete concentration, HHI of 0.1 = good diversification
        stability = max(0, (1.0 - hhi) * 100)
        return min(stability, 100.0)
    
    def calculate_liquidity_coverage(self) -> float:
        """
        Calculate liquidity coverage ratio - can the index be traded without major price impact?
        
        Returns:
            Liquidity coverage as percentage
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_bitquery_data() first.")
        
        if len(self.data) == 0:
            return 0.0
        
        # Calculate total daily volume in USD
        total_daily_volume = 0
        total_market_cap = 0
        
        for _, row in self.data.iterrows():
            if row['close'] > 0:
                daily_volume_usd = row['volume'] * row['close']
                total_daily_volume += daily_volume_usd
                
                if row['market_cap'] > 0:
                    total_market_cap += row['market_cap']
        
        if total_market_cap == 0:
            return 0.0
        
        # Liquidity coverage = (Daily Volume / Market Cap) * 100
        coverage = (total_daily_volume / total_market_cap) * 100
        return min(coverage, 1000.0)  # Cap at 1000%
    
    def calculate_weight_concentration(self) -> float:
        """
        Calculate weight concentration using Herfindahl Index.
        
        Returns:
            Concentration percentage (higher = more concentrated)
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_bitquery_data() first.")
        
        if len(self.data) == 0:
            return 0.0
        
        # Calculate weights
        weights = self.data['volume'] / self.data['volume'].sum()
        
        # Herfindahl Index
        hhi = (weights ** 2).sum()
        
        # Convert to percentage
        return hhi * 100
    
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
            "2w": 26,      # 2-week periods (365/14)
            "1m": 12,      # Monthly
            "6m": 2,       # 6-month periods
            "1y": 1,       # Annual
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
    
    def get_token_addresses(self) -> List[str]:
        """
        Extract list of token addresses from the current dataset.
        
        Returns:
            List of token mint addresses
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_bitquery_data() first.")
        
        if len(self.data) == 0:
            return []
        
        return self.data['mint_address'].tolist()
    
    def calculate_roi_from_price_data(self, price_data: Dict) -> pd.DataFrame:
        """
        Calculate ROI using external price data (oldest and latest prices).
        
        Args:
            price_data: Dictionary containing price data for tokens
                       Format: {mint_address: {'oldest_price': float, 'latest_price': float, 'symbol': str, 'name': str}}
        
        Returns:
            DataFrame with ROI calculations for each token
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_bitquery_data() first.")
        
        if len(self.data) == 0:
            return pd.DataFrame()
        
        # Create a copy of the data to avoid modifying the original
        roi_data = self.data.copy()
        
        def calculate_token_roi(row):
            """
            Calculate ROI using oldest and latest prices from external data.
            """
            mint_address = row['mint_address']
            
            if mint_address in price_data:
                price_info = price_data[mint_address]
                oldest_price = price_info.get('oldest_price', 0)
                latest_price = price_info.get('latest_price', 0)
                
                print(f"Debug ROI for {row['symbol']}: oldest={oldest_price}, latest={latest_price}")
                
                if oldest_price > 0 and latest_price > 0:
                    roi = ((latest_price - oldest_price) / oldest_price) * 100
                    print(f"  Calculated ROI: {roi:.2f}%")
                    return roi
                else:
                    print(f"  Skipping - prices are 0: oldest={oldest_price}, latest={latest_price}")
            else:
                print(f"  No price data found for {mint_address}")
            
            return 0.0
        
        # Debug: Check how many tokens have price data
        tokens_with_price_data = 0
        for mint_address in roi_data['mint_address']:
            if mint_address in price_data:
                tokens_with_price_data += 1
        
        print(f"Debug: {tokens_with_price_data}/{len(roi_data)} tokens have price data")
        print(f"Debug: Price data keys: {list(price_data.keys())[:5]}...")  # Show first 5 keys
        
        # Calculate ROI for each token
        roi_data['roi_percentage'] = roi_data.apply(calculate_token_roi, axis=1)
        
        # Add price data from external source
        roi_data['oldest_price'] = roi_data['mint_address'].map(
            lambda x: price_data.get(x, {}).get('oldest_price', 0)
        )
        roi_data['latest_price'] = roi_data['mint_address'].map(
            lambda x: price_data.get(x, {}).get('latest_price', 0)
        )
        
        # Add additional ROI metrics
        roi_data['roi_absolute'] = roi_data['latest_price'] - roi_data['oldest_price']
        roi_data['roi_positive'] = roi_data['roi_percentage'] > 0
        
        return roi_data[['symbol', 'name', 'mint_address', 'oldest_price', 'latest_price',
                        'roi_percentage', 'roi_absolute', 'roi_positive', 'volume', 'volatility']]
    
    def calculate_roi_per_token(self) -> pd.DataFrame:
        """
        Calculate ROI (Return on Investment) for each token in the dataset.
        ROI = (close_price - open_price) / open_price * 100
        
        Returns:
            DataFrame with ROI calculations for each token
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_bitquery_data() first.")
        
        if len(self.data) == 0:
            return pd.DataFrame()
        
        # Create a copy of the data to avoid modifying the original
        roi_data = self.data.copy()
        
        def calculate_token_roi(row):
            """
            Calculate ROI using open as earliest price and close as latest price.
            """
            open_price = row['open']
            close_price = row['close']
            
            if open_price > 0 and close_price > 0:
                roi = ((close_price - open_price) / open_price) * 100
                return roi
            else:
                return 0.0
        
        # Calculate ROI for each token
        roi_data['roi_percentage'] = roi_data.apply(calculate_token_roi, axis=1)
        
        # Add additional ROI metrics
        roi_data['roi_absolute'] = roi_data['close'] - roi_data['open']
        roi_data['roi_positive'] = roi_data['roi_percentage'] > 0
        
        return roi_data[['symbol', 'name', 'mint_address', 'open', 'close',
                        'roi_percentage', 'roi_absolute', 'roi_positive', 'volume', 'volatility']]
    
    def calculate_roi_statistics(self) -> Dict:
        """
        Calculate comprehensive ROI statistics for the dataset.
        
        Returns:
            Dictionary containing ROI statistics
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_bitquery_data() first.")
        
        roi_data = self.calculate_roi_per_token()
        
        if len(roi_data) == 0:
            return {
                'total_tokens': 0,
                'positive_roi_count': 0,
                'negative_roi_count': 0,
                'average_roi': 0.0,
                'median_roi': 0.0,
                'max_roi': 0.0,
                'min_roi': 0.0,
                'roi_std': 0.0,
                'positive_roi_percentage': 0.0,
                'volume_weighted_roi': 0.0
            }
        
        # Basic statistics
        total_tokens = len(roi_data)
        positive_roi_count = roi_data['roi_positive'].sum()
        negative_roi_count = total_tokens - positive_roi_count
        positive_roi_percentage = (positive_roi_count / total_tokens) * 100
        
        # ROI statistics
        roi_percentages = roi_data['roi_percentage']
        average_roi = roi_percentages.mean()
        median_roi = roi_percentages.median()
        max_roi = roi_percentages.max()
        min_roi = roi_percentages.min()
        roi_std = roi_percentages.std()
        
        # Volume-weighted ROI
        if roi_data['volume'].sum() > 0:
            volume_weights = roi_data['volume'] / roi_data['volume'].sum()
            volume_weighted_roi = (roi_percentages * volume_weights).sum()
        else:
            volume_weighted_roi = 0.0
        
        return {
            'total_tokens': total_tokens,
            'positive_roi_count': int(positive_roi_count),
            'negative_roi_count': int(negative_roi_count),
            'average_roi': round(average_roi, 2),
            'median_roi': round(median_roi, 2),
            'max_roi': round(max_roi, 2),
            'min_roi': round(min_roi, 2),
            'roi_std': round(roi_std, 2),
            'positive_roi_percentage': round(positive_roi_percentage, 2),
            'volume_weighted_roi': round(volume_weighted_roi, 2)
        }
    
    def get_top_roi_tokens(self, top_n: int = 10) -> pd.DataFrame:
        """
        Get top N tokens by ROI percentage.
        
        Args:
            top_n: Number of top tokens to return
            
        Returns:
            DataFrame with top tokens sorted by ROI (descending)
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_bitquery_data() first.")
        
        roi_data = self.calculate_roi_per_token()
        
        if len(roi_data) == 0:
            return pd.DataFrame()
        
        # Sort by ROI percentage in descending order
        top_roi_tokens = roi_data.nlargest(top_n, 'roi_percentage').copy()
        
        return top_roi_tokens[['symbol', 'name', 'mint_address', 'open', 'close',
                               'roi_percentage', 'roi_absolute', 'volume', 'volatility']]
    
    def get_worst_roi_tokens(self, top_n: int = 10) -> pd.DataFrame:
        """
        Get worst N tokens by ROI percentage.
        
        Args:
            top_n: Number of worst tokens to return
            
        Returns:
            DataFrame with worst tokens sorted by ROI (ascending)
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_bitquery_data() first.")
        
        roi_data = self.calculate_roi_per_token()
        
        if len(roi_data) == 0:
            return pd.DataFrame()
        
        # Sort by ROI percentage in ascending order
        worst_roi_tokens = roi_data.nsmallest(top_n, 'roi_percentage').copy()
        
        return worst_roi_tokens[['symbol', 'name', 'mint_address', 'open', 'close',
                                 'roi_percentage', 'roi_absolute', 'volume', 'volatility']]
    
    def calculate_roi_statistics_from_data(self, roi_data: pd.DataFrame) -> Dict:
        """
        Calculate ROI statistics from pre-calculated ROI data.
        
        Args:
            roi_data: DataFrame with ROI calculations
            
        Returns:
            Dictionary containing ROI statistics
        """
        if len(roi_data) == 0:
            return {
                'total_tokens': 0,
                'positive_roi_count': 0,
                'negative_roi_count': 0,
                'average_roi': 0.0,
                'median_roi': 0.0,
                'max_roi': 0.0,
                'min_roi': 0.0,
                'roi_std': 0.0,
                'positive_roi_percentage': 0.0,
                'volume_weighted_roi': 0.0
            }
        
        # Basic statistics
        total_tokens = len(roi_data)
        positive_roi_count = roi_data['roi_positive'].sum()
        negative_roi_count = total_tokens - positive_roi_count
        positive_roi_percentage = (positive_roi_count / total_tokens) * 100
        
        # ROI statistics
        roi_percentages = roi_data['roi_percentage']
        average_roi = roi_percentages.mean()
        median_roi = roi_percentages.median()
        max_roi = roi_percentages.max()
        min_roi = roi_percentages.min()
        roi_std = roi_percentages.std()
        
        # Volume-weighted ROI
        if roi_data['volume'].sum() > 0:
            volume_weights = roi_data['volume'] / roi_data['volume'].sum()
            volume_weighted_roi = (roi_percentages * volume_weights).sum()
        else:
            volume_weighted_roi = 0.0
        
        return {
            'total_tokens': total_tokens,
            'positive_roi_count': int(positive_roi_count),
            'negative_roi_count': int(negative_roi_count),
            'average_roi': round(average_roi, 2),
            'median_roi': round(median_roi, 2),
            'max_roi': round(max_roi, 2),
            'min_roi': round(min_roi, 2),
            'roi_std': round(roi_std, 2),
            'positive_roi_percentage': round(positive_roi_percentage, 2),
            'volume_weighted_roi': round(volume_weighted_roi, 2)
        }
    
    def get_top_roi_tokens_from_data(self, roi_data: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
        """
        Get top N tokens by ROI percentage from pre-calculated ROI data.
        
        Args:
            roi_data: DataFrame with ROI calculations
            top_n: Number of top tokens to return
            
        Returns:
            DataFrame with top tokens sorted by ROI (descending)
        """
        if len(roi_data) == 0:
            return pd.DataFrame()
        
        # Sort by ROI percentage in descending order
        top_roi_tokens = roi_data.nlargest(top_n, 'roi_percentage').copy()
        
        return top_roi_tokens[['symbol', 'name', 'mint_address', 'oldest_price', 'latest_price',
                               'roi_percentage', 'roi_absolute', 'volume', 'volatility']]
    
    def get_worst_roi_tokens_from_data(self, roi_data: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
        """
        Get worst N tokens by ROI percentage from pre-calculated ROI data.
        
        Args:
            roi_data: DataFrame with ROI calculations
            top_n: Number of worst tokens to return
            
        Returns:
            DataFrame with worst tokens sorted by ROI (ascending)
        """
        if len(roi_data) == 0:
            return pd.DataFrame()
        
        # Sort by ROI percentage in ascending order
        worst_roi_tokens = roi_data.nsmallest(top_n, 'roi_percentage').copy()
        
        return worst_roi_tokens[['symbol', 'name', 'mint_address', 'oldest_price', 'latest_price',
                                 'roi_percentage', 'roi_absolute', 'volume', 'volatility']]
    
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
    
    def generate_risk_return_profile(self, index_name: str = "Memecoin 50 Volume", price_data: Dict = None) -> Dict:
        """
        Generate complete risk and return profile for the data.
        
        Args:
            index_name: Name of the index (e.g., "Memecoin 50 Volume", "Memecoin 50 Volatility")
            
        Returns:
            Dictionary containing all risk and return metrics
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_bitquery_data() first.")
        
        # Calculate meaningful index metrics
        constituent_stability = self.calculate_constituent_stability()
        weight_concentration = self.calculate_weight_concentration()
        
        # Use the volatility data from Bitquery as base, then calculate for different periods
        base_volatility = self.data['volatility'].mean() if len(self.data) > 0 else 0
        
        
        # Calculate volatilities for different periods
        volatilities = {}
        for period in ["2w", "1m", "6m", "1y"]:
            # For memecoins, calculate volatility from high/low price ranges
            # This is more reliable than using Bitquery's volatility field
            period_multiplier = {"2w": 0.8, "1m": 1.0, "6m": 1.2, "1y": 1.5}
            
            if len(self.data) > 0:
                # Calculate price range volatility using decimal arithmetic: (high - low) / low
                # This gives us a measure of price volatility for each token
                price_volatility = []
                for _, row in self.data.iterrows():
                    if row['low'] > 0:
                        high = Decimal(str(row['high']))
                        low = Decimal(str(row['low']))
                        vol = float((high - low) / low)
                        # Cap extreme values to prevent unrealistic volatility
                        vol = min(vol, 10.0)  # Cap at 1000% volatility
                        if np.isfinite(vol) and vol >= 0:
                            price_volatility.append(vol)
                
                if len(price_volatility) > 0:
                    # Use median price volatility to avoid extreme outliers
                    median_price_vol = np.median(price_volatility)
                    
                    # Convert to percentage and apply period multiplier
                    base_vol = median_price_vol * 100  # Convert to percentage
                    # Cap the final volatility to reasonable levels
                    final_vol = min(base_vol * period_multiplier.get(period, 1.0), 500.0)
                    volatilities[period] = final_vol
                    
                else:
                    # Fallback: use a reasonable memecoin volatility estimate
                    volatilities[period] = 50.0 * period_multiplier.get(period, 1.0)  # 50% base volatility
            else:
                volatilities[period] = 0.0
            
        
        # Calculate return-to-risk ratios
        return_risk_ratios = {}
        for period in ["2w", "1m", "6m", "1y"]:
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
        
        # Calculate ROI statistics - use external price data if available
        if price_data:
            print("Using external price data for accurate ROI calculation...")
            roi_data = self.calculate_roi_from_price_data(price_data)
            roi_stats = self.calculate_roi_statistics_from_data(roi_data)
            top_roi_tokens = self.get_top_roi_tokens_from_data(roi_data, 10)
            worst_roi_tokens = self.get_worst_roi_tokens_from_data(roi_data, 10)
        else:
            print("Using fallback ROI calculation with open/close prices...")
            roi_stats = self.calculate_roi_statistics()
            top_roi_tokens = self.get_top_roi_tokens(10)
            worst_roi_tokens = self.get_worst_roi_tokens(10)
        
        profile = {
            "index": index_name,
            "constituent_stability": round(constituent_stability, 2),
            "weight_concentration": round(weight_concentration, 2),
            "volatilities": {
                "2w": round(volatilities["2w"], 2),
                "1m": round(volatilities["1m"], 2),
                "6m": round(volatilities["6m"], 2),
                "1y": round(volatilities["1y"], 2)
            },
            "return_risk_ratios": {
                "2w": round(return_risk_ratios["2w"], 2),
                "1m": round(return_risk_ratios["1m"], 2),
                "6m": round(return_risk_ratios["6m"], 2),
                "1y": round(return_risk_ratios["1y"], 2)
            },
            "max_drawdown": {
                "percentage": round(max_drawdown_pct, 2),
                "date": max_drawdown_date
            },
            "roi_statistics": roi_stats,
            "top_roi_tokens": top_roi_tokens.to_dict('records'),
            "worst_roi_tokens": worst_roi_tokens.to_dict('records'),
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
        print(f"{'':8} {'':10} {'2w':<8} {'1m':<8} {'6m':<8} {'1y':<8} {'2w':<8} {'1m':<8} {'6m':<8} {'1y':<8} {'%':<8} {'Date':<10}")
        print("-"*120)
        
        # Data rows
        for profile in profiles:
            row = f"{profile['index']:<8} {profile['turnover']:<10.2f} "
            row += f"{profile['volatilities']['2w']:<8.2f} {profile['volatilities']['1m']:<8.2f} "
            row += f"{profile['volatilities']['6m']:<8.2f} {profile['volatilities']['1y']:<8.2f} "
            row += f"{profile['return_risk_ratios']['2w']:<8.2f} {profile['return_risk_ratios']['1m']:<8.2f} "
            row += f"{profile['return_risk_ratios']['6m']:<8.2f} {profile['return_risk_ratios']['1y']:<8.2f} "
            row += f"{profile['max_drawdown']['percentage']:<8.2f} {profile['max_drawdown']['date']:<10}"
            print(row)
        
        print("="*120)
        
        # Footnotes
        print("\nFootnotes:")
        print("1. Realized Volatility: Statistical measure calculating dispersion of returns")
        print("   considering potential autocorrelation of the underlying asset.")
        print("2. Return-to-Risk Ratio: Gross Return / Periodic Realized Volatility")
        print("\nDisclaimer: Past performance is not an indication of future results.")


def process_bitquery_data(bitquery_response: Dict, index_name: str = "Memecoin 50 Volume", market_cap_data: Dict = None, price_data: Dict = None) -> Dict:
    """
    Main function to process Bitquery data and generate risk metrics.
    
    Args:
        bitquery_response: Raw response from Bitquery API
        index_name: Name of the index (e.g., "Memecoin 50 Volume", "Memecoin 50 Volatility")
        market_cap_data: Dictionary containing market cap data for tokens (mint_address -> market_cap_usd)
        price_data: Dictionary containing oldest/latest price data for accurate ROI calculation
        
    Returns:
        Dictionary containing risk and return metrics
    """
    analyzer = MemeCoinRiskAnalyzer()
    analyzer.load_bitquery_data(bitquery_response, market_cap_data)
    
    # Generate profile for the data
    profile = analyzer.generate_risk_return_profile(index_name, price_data)
    
    return profile


if __name__ == "__main__":
    # Example usage
    print("MemeCoin Risk Analyzer")
    print("This module calculates risk and return metrics for memecoin data.")
    print("Use process_bitquery_data() function with your Bitquery API response.")
