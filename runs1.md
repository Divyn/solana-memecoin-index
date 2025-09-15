Fetching memecoin data from Bitquery...
Fetching volume-ordered data...
Fetching volatility-ordered data...
Fetching market cap data for 111 tokens...
Fetching SOL price...
Found 93 TokenSupplyUpdates
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
Turnover (%)              0.00                 2576.60             

Realized Volatility (%)  
  15d Volatility (%)<25 0.32                 2.77                
  1m Volatility (%)<25 0.41                 3.47                
  3m Volatility (%)<25 0.49                 4.16                
  1y Volatility (%)<25 0.61                 5.20                
  3y Volatility (%)<25 0.53                 4.51                

Return-to-Risk Ratio     
  15d Return-to-Risk<25 59.50                1000.00             
  1m Return-to-Risk<25 47.60                1000.00             
  3m Return-to-Risk<25 39.67                1000.00             
  1y Return-to-Risk<25 31.73                1000.00             
  3y Return-to-Risk<25 36.61                1000.00             

Max Drawdown (%)          -94.61               -100.00             

====================================================================================================
TOP 10 TOKENS COMPARISON
====================================================================================================
MEMECOIN 50 VOLUME INDEX - Top 10 by Volume:
Rank Symbol       Name                 Mint Address                                 Volume          Volatility   Weight  
------------------------------------------------------------------------------------------------------------------------
1    JOEY         Joey                 4kN8iUGp...PzqcHnzW                          39941209656472784 0.00         41.74   %
2    JOEY         Joey                 4kN8iUGp...PzqcHnzW                          39941209656472784 0.00         41.74   %
3    NAZIELON     NAZI ELON            Fv4RBwqq...kisLy7xm                          3838988204819346 0.00         4.01    %
4    AMERICAI     AMERICA AI Agent     Hk3K1bxE...cgTTK6V1                          2318883103286744 0.00         2.42    %
5    DOGEMARS     DOGE TO MARS         A3t4ap3o...TMzF9kzb                          2277236170365386 0.00         2.38    %
6    $GOLD        $GOLD                H1PevUqm...7GZ7qpRE                          1941826482061258 0.00         2.03    %
7    DOGEMARS     DOGEMARS             3EqTrNuC...Gd8BLhy6                          1400000000000000 0.00         1.46    %
8    UnitreeDOG   Unitree AI Robot Dog 6LrY2g3d...NEstNT7D                          1400000000000000 0.00         1.46    %
9    PEON         Peon                 CMxgFgoi...J1xo8b78                          1319704719013886 0.00         1.38    %
10   STARGATEAI   Stargate AI Agent    8aTrwd62...diyA6WiL                          1304492078755302 0.00         1.36    %

MEMECOIN 50 VOLATILITY INDEX - Top 10 by Volatility:
Rank Symbol       Name                 Mint Address                                 Volume          Volatility   Weight  
------------------------------------------------------------------------------------------------------------------------
1    $PAWKER      Peter PAWker         DnKkDNX1...W3V2P3h6                          125693          4996476.62   34.68   %
2    $PAWKER      Peter PAWker         DnKkDNX1...W3V2P3h6                          124465          1436983.84   34.35   %
3    $PAWKER      Peter PAWker         DnKkDNX1...W3V2P3h6                          89059           470831.02    24.58   %
4    BITTY        The Bitcoin Mascot   dTzEP9JU...1APBpump                          5869            5158789.00   1.62    %
5    YZY          BANK OF YZY          AHxE3UAj...kTHhxszS                          3915            58541597.55  1.08    %
6    ai16z        ai16z                HeLp6NuQ...n4V98jwC                          3467            354829.28    0.96    %
7    IMT          INTERNET MONEY THING 3EMheh5M...uXxspump                          3290            202749.56    0.91    %
8    ARB          Arbitrage Loop       EDcdVtzW...XpQFUk3s                          3023            11149237.85  0.83    %
9    USELESS      USELESS COIN         Dz9mQ9Nz...iW8Mbonk                          2362            621803.87    0.65    %
10   PUMP         Pump                 pumpCmXq...8H7H9Dfn                          1250            2430742.95   0.34    %

====================================================================================================
INDEX CONSTRUCTION METHODOLOGY
====================================================================================================
Metric                         Memecoin 50 Volume   Memecoin 50 Volatility
----------------------------------------------------------------------
Total Tokens                   100                  100                 
Total Volume                   126,441,271,006,488,912 363,088
Top 10 Contribution (%)        75.67                99.81               

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
  15d Volatility (%)<25 0.32                 2.77                 Volume         
  1m Volatility (%)<25 0.41                 3.47                 Volume         
  3m Volatility (%)<25 0.49                 4.16                 Volume         
  1y Volatility (%)<25 0.61                 5.20                 Volume         
  3y Volatility (%)<25 0.53                 4.51                 Volume         

RETURN-TO-RISK ANALYSIS       
-------------------------------------------------------------------------------------
  15d Return-to-Risk<25 59.50                1000.00              Volatility     
  1m Return-to-Risk<25 47.60                1000.00              Volatility     
  3m Return-to-Risk<25 39.67                1000.00              Volatility     
  1y Return-to-Risk<25 31.73                1000.00              Volatility     
  3y Return-to-Risk<25 36.61                1000.00              Volatility     

RISK ASSESSMENT               
-------------------------------------------------------------------------------------
  Turnover (%)<25 0.00                 2576.60              Volatility     
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
