import requests
import json
from string import Template
from config import AUTH_TOKEN

def fetch_memecoin_data_by_period(start_date, end_date, order_by="volume"):
    """
    Fetch memecoin data from Bitquery API for a specific time period.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format  
        order_by: Field to order by ("volume" or "volatility_token")
    
    Returns:
        Dictionary containing the API response data
    """
    url = "https://streaming.bitquery.io/eap"

    # Build the query with date range
    query = f"""{{
  Solana(dataset: archive) {{
    DEXTradeByTokens(
      limit: {{count: 100}}
      orderBy: {{descendingByField: "{order_by}"}}
      where: {{
        Trade: {{
          Currency: {{
            MintAddress: {{
              notIn: [
                "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
                "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "So11111111111111111111111111111111111111111",
                "So11111111111111111111111111111111111111112",
                "11111111111111111111111111111111",
                "27G8MtK7VtTcCHkpASjSDdkWWYfoqT6ggEuKidVJidD4",
                "cbbtcf3aa214zXHbiAZQwf4122FBYbraNdFqgw4iMij",
                "2b1kV6DkPAnxd5ixfnxCpjxmKwqjjaYmCZfHsFu24GXo",
                "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
              ]
            }},
            Name: {{not: ""}}
          }},
          PriceAsymmetry: {{lt: 0.1}}
        }},
        Block: {{Date: {{since: "{start_date}", till: "{end_date}"}}}}
      }}
    ) {{
      volume: sum(of: Trade_Amount)
      volatility_token: calculate(
        expression: "(($Trade_high-$Trade_low)/$Trade_low)* 100"
      )
      Trade {{
        high: Price(maximum: Trade_Price)
        low: Price(minimum: Trade_Price)
        open: Price(minimum: Trade_Price)
        close: Price(maximum: Trade_Price)
        Currency {{
          Name
          MintAddress
          Symbol
        }}
        Side {{
          Currency {{
            Name
            MintAddress
            Symbol
          }}
        }}
      }}
      count
    }}
  }}
}}"""

    payload = json.dumps({
       "query": query,
       "variables": "{}"
    })
    
    headers = {
       'Content-Type': 'application/json',
       'Authorization': 'Bearer ' + AUTH_TOKEN
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {start_date} to {end_date}: {response.status_code}")
        print(response.text)
        return None

def fetch_memecoin_data_by_volume():
    """
    Fetch memecoin data from Bitquery API ordered by volume for the last 6 months.
    
    Returns:
        Dictionary containing the API response data
    """
    from datetime import datetime, timedelta
    
    # Get data for the last 6 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)  # 6 months
    
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    print(f"Fetching volume data from {start_str} to {end_str}")
    return fetch_memecoin_data_by_period(start_str, end_str, "volume")

def fetch_memecoin_data_by_volume_run2():
    """
    Fetch memecoin data from Bitquery API ordered by volume for Run 2.
    Hardcoded date range: 2024-09-01 to 2025-03-30
    
    Returns:
        Dictionary containing the API response data
    """
    start_str = "2024-09-01"
    end_str = "2025-03-30"
    
    print(f"Fetching volume data for Run 2 from {start_str} to {end_str}")
    return fetch_memecoin_data_by_period(start_str, end_str, "volume")

def fetch_memecoin_data_by_volatility():
    """
    Fetch memecoin data from Bitquery API ordered by volatility for the last 6 months.
    
    Returns:
        Dictionary containing the API response data
    """
    from datetime import datetime, timedelta
    
    # Get data for the last 6 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)  # 6 months
    
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    print(f"Fetching volatility data from {start_str} to {end_str}")
    return fetch_memecoin_data_by_period(start_str, end_str, "volatility_token")

def fetch_memecoin_data_by_volatility_run2():
    """
    Fetch memecoin data from Bitquery API ordered by volatility for Run 2.
    Hardcoded date range: 2024-09-01 to 2025-03-30
    
    Returns:
        Dictionary containing the API response data
    """
    start_str = "2024-09-01"
    end_str = "2025-03-30"
    
    print(f"Fetching volatility data for Run 2 from {start_str} to {end_str}")
    return fetch_memecoin_data_by_period(start_str, end_str, "volatility_token")


def fetch_sol_price():
    """
    Fetch current SOL price in USD.
    
    Returns:
        SOL price in USD, or 0 if fetch fails
    """
    url = "https://streaming.bitquery.io/eap"
    
    query = """
    query MyQuery {
      Trading {
        Tokens(
          where: {Currency: {Id: {is: "bid:solana"}}, Interval: {Time: {Duration: {eq: 1}}}}
          limit: {count: 1}
          orderBy: {descending: Block_Time}
        ) {
          Price {
            Ohlc {
              Close
            }
          }
        }
      }
    }
    """
    
    payload = json.dumps({
        "query": query,
        "variables": "{}"
    })
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + AUTH_TOKEN
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'Trading' in data['data'] and 'Tokens' in data['data']['Trading']:
            tokens = data['data']['Trading']['Tokens']
            if tokens and len(tokens) > 0:
                sol_price = float(tokens[0]['Price']['Ohlc']['Close'])
                return sol_price
    else:
        print(f"Error fetching SOL price: {response.status_code}")
        print(response.text)
    
    return 0.0

def fetch_token_supply_data(token_addresses):
    """
    Fetch market cap data for a list of token addresses using TokenSupplyUpdates.
    For memecoins, we get PostBalance in SOL and convert to USD using current SOL price.
    
    Args:
        token_addresses: List of token mint addresses
        
    Returns:
        Dictionary containing market cap data for each token (mint_address -> market_cap_usd)
    """
    if not token_addresses:
        return {}
    
    # First, get current SOL price
    print("Fetching SOL price...")
    sol_price = fetch_sol_price()
    if sol_price == 0:
        print("Warning: Could not fetch SOL price, using 0 for market cap calculations")
    
    url = "https://streaming.bitquery.io/eap"
    
    # Create the query for market cap data using TokenSupplyUpdates
    # Format token addresses as a GraphQL array
    token_addresses_str = '["' + '", "'.join(token_addresses) + '"]'
    
    # Use Template string to avoid f-string brace escaping issues
    query_template = Template("""
    query MyQuery {
      Solana {
        TokenSupplyUpdates(
          where: {TokenSupplyUpdate: {Currency: {MintAddress: {in: $token_addresses}}}}
          limit: {count: 1000}
          orderBy: {descending: Block_Time}
          limitBy: {by: TokenSupplyUpdate_Currency_MintAddress, count: 1}
        ) {
          TokenSupplyUpdate {
            PostBalanceInUSD
            PostBalance
            Currency {
              MintAddress
            }
          }
        }
      }
    }
    """)
    
    query = query_template.substitute(token_addresses=token_addresses_str)
    
    payload = json.dumps({
        "query": query,
        "variables": "{}"
    })
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + AUTH_TOKEN
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code == 200:
        data = response.json()
        
        # Check for errors first
        if 'errors' in data and data['errors']:
            print(f"API Errors: {data['errors']}")
            return {}
        
        # Process the data to create a simple address -> market_cap mapping
        market_cap_data = {}
        
        # Add proper null checks
        if data and 'data' in data and data['data'] and 'Solana' in data['data'] and 'TokenSupplyUpdates' in data['data']['Solana']:
            print(f"Found {len(data['data']['Solana']['TokenSupplyUpdates'])} TokenSupplyUpdates")
            for token_update in data['data']['Solana']['TokenSupplyUpdates']:
                mint_address = token_update['TokenSupplyUpdate']['Currency']['MintAddress']
                
                # Try PostBalanceInUSD first, fallback to PostBalance * SOL price
                post_balance_usd = float(token_update['TokenSupplyUpdate'].get('PostBalanceInUSD', 0))
                post_balance_sol = float(token_update['TokenSupplyUpdate'].get('PostBalance', 0))
                
                # print(f"Token {mint_address}: PostBalanceInUSD={post_balance_usd}, PostBalance={post_balance_sol}")
                
                if post_balance_usd > 0:
                    # Direct USD value available
                    market_cap_usd = post_balance_usd
                elif post_balance_sol > 0 and sol_price > 0:
                    # Convert SOL to USD
                    market_cap_usd = post_balance_sol * sol_price
                else:
                    # No data available
                    market_cap_usd = 0
                
                # print(f"Calculated market cap: ${market_cap_usd:,.2f}")
                market_cap_data[mint_address] = market_cap_usd
        else:
            print("Warning: No TokenSupplyUpdates data found in response")
            if data:
                print(f"Response structure: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                if 'data' in data and data['data']:
                    print(f"Data structure: {list(data['data'].keys()) if isinstance(data['data'], dict) else 'Not a dict'}")
                else:
                    print("data['data'] is None or empty")
        
        return market_cap_data
    else:
        print(f"Error fetching market cap data: {response.status_code}")
        print(response.text)
        return {}

def fetch_memecoin_data():
    """
    Fetch both volume-ordered and volatility-ordered memecoin data, plus market cap data.
    
    Returns:
        Dictionary containing both datasets and market cap data
    """
    print("Fetching volume-ordered data...")
    volume_data = fetch_memecoin_data_by_volume()
    
    print("Fetching volatility-ordered data...")
    volatility_data = fetch_memecoin_data_by_volatility()
    
    if volume_data is None or volatility_data is None:
        return None
    
    # Extract token addresses from both datasets
    token_addresses = set()
    
    if 'data' in volume_data and 'Solana' in volume_data['data']:
        for token in volume_data['data']['Solana']['DEXTradeByTokens']:
            mint_address = token['Trade']['Currency']['MintAddress']
            token_addresses.add(mint_address)
    
    if 'data' in volatility_data and 'Solana' in volatility_data['data']:
        for token in volatility_data['data']['Solana']['DEXTradeByTokens']:
            mint_address = token['Trade']['Currency']['MintAddress']
            token_addresses.add(mint_address)
    
    print(f"Fetching market cap data for {len(token_addresses)} tokens...")
    market_cap_data = fetch_token_supply_data(list(token_addresses))
    
    return {
        'volume_ordered': volume_data,
        'volatility_ordered': volatility_data,
        'market_cap_data': market_cap_data
    }

def fetch_token_oldest_latest_prices(token_addresses, start_date, end_date):
    """
    Fetch oldest and latest prices for a list of token addresses within a date range.
    
    Args:
        token_addresses: List of token mint addresses
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        Dictionary containing price data for each token
        Format: {mint_address: {'oldest_price': float, 'latest_price': float, 'symbol': str, 'name': str}}
    """
    if not token_addresses:
        return {}
    
    url = "https://streaming.bitquery.io/eap"
    
    # Create the query for oldest and latest prices using the exact structure provided
    token_addresses_str = '["' + '", "'.join(token_addresses) + '"]'
    
    query = f"""{{
  Solana(dataset: archive) {{
    DEXTradeByTokens(
      limit: {{count: 1000}}
      where: {{
        Trade: {{
          Currency: {{
            MintAddress: {{
              in: {token_addresses_str}
            }},
            Name: {{
              not: ""
            }}
          }},
          PriceAsymmetry: {{
            lt: 0.1
          }},
          Side: {{
            Currency: {{
              MintAddress: {{
                in: ["So11111111111111111111111111111111111111112", "So11111111111111111111111111111111111111111"]
              }}
            }}
          }}
        }},
        Block: {{
          Date: {{
            since: "{start_date}",
            till: "{end_date}"
          }}
        }}
      }}
      limitBy: {{
        by: Trade_Currency_MintAddress,
        count: 1
      }}
    ) {{
      Trade {{
        oldest_price: Price(minimum: Block_Time)
        latest_price: Price(maximum: Block_Time)
        Currency {{
          Name
          MintAddress
          Symbol
        }}
        Side {{
          Currency {{
            Name
            MintAddress
            Symbol
          }}
        }}
      }}
    }}
  }}
}}"""
    
    payload = json.dumps({
        "query": query,
        "variables": "{}"
    })
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + AUTH_TOKEN
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code == 200:
        data = response.json()
        
        # Debug: Print response structure
        print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
        if 'data' in data and data['data']:
            print(f"Data keys: {list(data['data'].keys()) if isinstance(data['data'], dict) else 'Not a dict'}")
            if 'Solana' in data['data'] and data['data']['Solana']:
                print(f"Solana keys: {list(data['data']['Solana'].keys()) if isinstance(data['data']['Solana'], dict) else 'Not a dict'}")
                if 'DEXTradeByTokens' in data['data']['Solana']:
                    print(f"Found {len(data['data']['Solana']['DEXTradeByTokens'])} DEXTradeByTokens")
        
        # Process the data to create price mapping
        price_data = {}
        
        if data and 'data' in data and data['data'] and 'Solana' in data['data'] and 'DEXTradeByTokens' in data['data']['Solana']:
            for i, token in enumerate(data['data']['Solana']['DEXTradeByTokens']):
                print(f"Processing token {i+1}: {list(token.keys())}")
                
                if 'Trade' in token and token['Trade']:
                    trade_data = token['Trade']
                    print(f"Trade data keys: {list(trade_data.keys())}")
                    
                    if 'Currency' in trade_data and trade_data['Currency']:
                        mint_address = trade_data['Currency']['MintAddress']
                        print(f"Token {i+1} - MintAddress: {mint_address}")
                        print(f"Token {i+1} - oldest_price (raw): {trade_data.get('oldest_price', 'NOT_FOUND')}")
                        print(f"Token {i+1} - latest_price (raw): {trade_data.get('latest_price', 'NOT_FOUND')}")
                        
                        # Convert to float and handle scientific notation
                        oldest_price_raw = trade_data.get('oldest_price', 0)
                        latest_price_raw = trade_data.get('latest_price', 0)
                        
                        # Scale up prices by 1e18 to work with larger numbers for calculations
                        scale_factor = 1e18
                        
                        if oldest_price_raw != 0:
                            oldest_price_float = float(oldest_price_raw) * scale_factor
                            print(f"Token {i+1} - oldest_price (raw): {oldest_price_raw}")
                            print(f"Token {i+1} - oldest_price (scaled): {oldest_price_float:.10f}")
                        else:
                            oldest_price_float = 0.0
                            print(f"Token {i+1} - oldest_price (scaled): 0.0000000000")
                            
                        if latest_price_raw != 0:
                            latest_price_float = float(latest_price_raw) * scale_factor
                            print(f"Token {i+1} - latest_price (raw): {latest_price_raw}")
                            print(f"Token {i+1} - latest_price (scaled): {latest_price_float:.10f}")
                        else:
                            latest_price_float = 0.0
                            print(f"Token {i+1} - latest_price (scaled): 0.0000000000")
                        
                        price_data[mint_address] = {
                            'oldest_price': oldest_price_float,
                            'latest_price': latest_price_float,
                            'symbol': trade_data['Currency']['Symbol'],
                            'name': trade_data['Currency']['Name']
                        }
                    else:
                        print(f"Token {i+1} - No Currency data found")
                else:
                    print(f"Token {i+1} - No Trade data found")
        
        print(f"Processed {len(price_data)} tokens with price data")
        return price_data
    else:
        print(f"Error fetching price data: {response.status_code}")
        print(response.text)
        return {}

def fetch_memecoin_data_run2():
    """
    Fetch both volume-ordered and volatility-ordered memecoin data for Run 2.
    Hardcoded date range: 2024-09-01 to 2025-03-30
    
    Returns:
        Dictionary containing both datasets and market cap data
    """
    print("Fetching volume-ordered data for Run 2...")
    volume_data = fetch_memecoin_data_by_volume_run2()
    
    print("Fetching volatility-ordered data for Run 2...")
    volatility_data = fetch_memecoin_data_by_volatility_run2()
    
    if volume_data is None or volatility_data is None:
        return None
    
    # Extract token addresses from both datasets
    token_addresses = set()
    
    if 'data' in volume_data and 'Solana' in volume_data['data']:
        for token in volume_data['data']['Solana']['DEXTradeByTokens']:
            mint_address = token['Trade']['Currency']['MintAddress']
            token_addresses.add(mint_address)
    
    if 'data' in volatility_data and 'Solana' in volatility_data['data']:
        for token in volatility_data['data']['Solana']['DEXTradeByTokens']:
            mint_address = token['Trade']['Currency']['MintAddress']
            token_addresses.add(mint_address)
    
    print(f"Fetching market cap data for {len(token_addresses)} tokens...")
    market_cap_data = fetch_token_supply_data(list(token_addresses))
    
    return {
        'volume_ordered': volume_data,
        'volatility_ordered': volatility_data,
        'market_cap_data': market_cap_data
    }


