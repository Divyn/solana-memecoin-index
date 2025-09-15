Fetching memecoin data from Bitquery...
Fetching volume-ordered data...
Fetching volatility-ordered data...
Fetching market cap data for 112 tokens...
Fetching SOL price...
Found 90 TokenSupplyUpdates
Data fetched successfully!

================================================================================
PROCESSING VOLUME-ORDERED DATA (Memecoin 50 Volume Index)
================================================================================
Found 100 tokens in volume-ordered data

================================================================================
PROCESSING VOLATILITY-ORDERED DATA (Memecoin 50 Volatility Index)
================================================================================
Found 100 tokens in volatility-ordered data

====================================================================================================
MEMECOIN RISK ANALYSIS RESULTS - COMPARISON
====================================================================================================
Metric                    Memecoin 50 Volume   Memecoin 50 Volatility
-------------------------------------------------------
Turnover (%)              0.00                 3846.16             

Realized Volatility (%)  
  15d Volatility (%)<25 0.49                 3.34                
  1m Volatility (%)<25 0.61                 4.18                
  3m Volatility (%)<25 0.73                 5.01                
  1y Volatility (%)<25 0.91                 6.26                
  3y Volatility (%)<25 0.79                 5.43                

Return-to-Risk Ratio     
  15d Return-to-Risk<25 40.17                1000.00             
  1m Return-to-Risk<25 32.14                1000.00             
  3m Return-to-Risk<25 26.78                1000.00             
  1y Return-to-Risk<25 21.42                1000.00             
  3y Return-to-Risk<25 24.72                1000.00             

Max Drawdown (%)          -94.61               -100.00             

====================================================================================================
TOP 10 TOKENS COMPARISON
====================================================================================================
MEMECOIN 50 VOLUME INDEX - Top 10 by Volume:
Rank Symbol       Name                 Mint Address                                 Volume          Volatility   Weight  
------------------------------------------------------------------------------------------------------------------------
1    JOEY         Joey                 4kN8iUGp...PzqcHnzW                          39941209656472784 0.00         41.30   %
2    JOEY         Joey                 4kN8iUGp...PzqcHnzW                          39941209656472784 0.00         41.30   %
3    NAZIELON     NAZI ELON            Fv4RBwqq...kisLy7xm                          3838988204819346 0.00         3.97    %
4    AMERICAI     AMERICA AI Agent     Hk3K1bxE...cgTTK6V1                          2318883103286744 0.00         2.40    %
5    DOGEMARS     DOGE TO MARS         A3t4ap3o...TMzF9kzb                          2284958360167751 0.00         2.36    %
6    PEON         Peon                 CMxgFgoi...J1xo8b78                          1973948333465020 0.00         2.04    %
7    $GOLD        $GOLD                H1PevUqm...7GZ7qpRE                          1948975891138060 0.00         2.02    %
8    STONKS       Stank Memes          9nvM2qJZ...Hmcj6NU7                          1654987551993816 0.00         1.71    %
9    DOGEMARS     DOGEMARS             3EqTrNuC...Gd8BLhy6                          1400000000000000 0.00         1.45    %
10   UnitreeDOG   Unitree AI Robot Dog 6LrY2g3d...NEstNT7D                          1400000000000000 0.00         1.45    %

MEMECOIN 50 VOLATILITY INDEX - Top 10 by Volatility:
Rank Symbol       Name                 Mint Address                                 Volume          Volatility   Weight  
------------------------------------------------------------------------------------------------------------------------
1    USDUC        unstable coin        CB9dDufT...XxHKpump                          473150          305917.82    56.85   %
2    $PAWKER      Peter PAWker         DnKkDNX1...W3V2P3h6                          125693          4996476.62   15.10   %
3    $PAWKER      Peter PAWker         DnKkDNX1...W3V2P3h6                          124465          1436983.84   14.96   %
4    $PAWKER      Peter PAWker         DnKkDNX1...W3V2P3h6                          89059           470831.02    10.70   %
5    BITTY        The Bitcoin Mascot   dTzEP9JU...1APBpump                          5869            5158789.00   0.71    %
6    YZY          BANK OF YZY          AHxE3UAj...kTHhxszS                          3915            58541597.55  0.47    %
7    ai16z        ai16z                HeLp6NuQ...n4V98jwC                          3467            354829.28    0.42    %
8    ARB          Arbitrage Loop       EDcdVtzW...XpQFUk3s                          3023            11149237.85  0.36    %
9    USELESS      USELESS COIN         Dz9mQ9Nz...iW8Mbonk                          2362            621803.87    0.28    %
10   PUMP         Pump                 pumpCmXq...8H7H9Dfn                          1250            2430742.95   0.15    %

====================================================================================================
INDEX CONSTRUCTION METHODOLOGY
====================================================================================================
Metric                         Memecoin 50 Volume   Memecoin 50 Volatility
----------------------------------------------------------------------
Total Tokens                   100                  100                 
Total Volume                   129,703,365,499,506,512 833,655
Top 10 Contribution (%)        74.56                99.83               

Selection Criteria:
  • Volume-based ranking (top 100 by trading volume)
  • Price asymmetry < 0.1 (filters out extreme price manipulation)
  • Non-empty token names (filters out unnamed tokens)
  • Date filter: Since July 1, 2024
  • Excludes major stablecoins and native tokens

Weighting Method: Volume-weighted (higher volume = higher weight in index)
Note: Volatility Index uses volatility-based ranking instead of volume-based ranking
Note: 15-day metrics are included as memecoins typically have short lifespans

Excluded Tokens:
  • USDC (EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v)
  • USDT (Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB)
  • SOL (So11111111111111111111111111111111111111111)
  • WSOL (So11111111111111111111111111111111111111112)
  • Other major stablecoins and native tokens
====================================================================================================

====================================================================================================
PERFORMANCE COMPARISON: VOLUME vs VOLATILITY INDEXES
====================================================================================================

Metric                         Volume Index         Volatility Index     Winner         
-------------------------------------------------------------------------------------

VOLATILITY ANALYSIS           
-------------------------------------------------------------------------------------
  15d Volatility (%)<25 0.49                 3.34                 Volume         
  1m Volatility (%)<25 0.61                 4.18                 Volume         
  3m Volatility (%)<25 0.73                 5.01                 Volume         
  1y Volatility (%)<25 0.91                 6.26                 Volume         
  3y Volatility (%)<25 0.79                 5.43                 Volume         

RETURN-TO-RISK ANALYSIS       
-------------------------------------------------------------------------------------
  15d Return-to-Risk<25 40.17                1000.00              Volatility     
  1m Return-to-Risk<25 32.14                1000.00              Volatility     
  3m Return-to-Risk<25 26.78                1000.00              Volatility     
  1y Return-to-Risk<25 21.42                1000.00              Volatility     
  3y Return-to-Risk<25 24.72                1000.00              Volatility     

RISK ASSESSMENT               
-------------------------------------------------------------------------------------
  Turnover (%)<25 0.00                 3846.16              Volatility     
  Max Drawdown (%)<25 -94.61               -100.00              Volume         

OVERALL PERFORMANCE SUMMARY   
-------------------------------------------------------------------------------------
  Lower Volatility Winner<25 Volume              
  Higher Return-to-Risk Winner<25 Volatility          
  Lower Risk Winner<25 Volatility          
  Overall Winner<25 Volatility          

INVESTMENT RECOMMENDATIONS    
-------------------------------------------------------------------------------------
  Memecoin 50 Volume Index:
    • Better for: Conservative investors, stable returns
    • Lower volatility across all timeframes
    • More predictable risk-return profile
    • Suitable for longer-term positions

  Memecoin 50 Volatility Index:
    • Better for: Aggressive traders, high-risk strategies
    • Higher volatility, potential for higher returns
    • More suitable for short-term trading
    • Higher risk, higher reward potential
====================================================================================================
divyasshree@Divyasshrees-MacBook-Air memecoin-index % 
