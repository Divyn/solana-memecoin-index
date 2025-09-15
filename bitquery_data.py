import requests
import json
from string import Template
from config import AUTH_TOKEN

def fetch_memecoin_data_by_volume():
    """
    Fetch memecoin data from Bitquery API ordered by volume.
    
    Returns:
        Dictionary containing the API response data
    """
    url = "https://streaming.bitquery.io/eap"

    payload = json.dumps({
       "query": "{\n  Solana {\n    DEXTradeByTokens(\n      limit: {count: 100}\n      orderBy: {descendingByField: \"volume\"}\n      where: {Trade: {Currency: {MintAddress: {notIn: [\"Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB\", \"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v\", \"So11111111111111111111111111111111111111111\", \"So11111111111111111111111111111111111111112\", \"11111111111111111111111111111111\", \"27G8MtK7VtTcCHkpASjSDdkWWYfoqT6ggEuKidVJidD4\", \"cbbtcf3aa214zXHbiAZQwf4122FBYbraNdFqgw4iMij\", \"2b1kV6DkPAnxd5ixfnxCpjxmKwqjjaYmCZfHsFu24GXo\", \"DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263\"]}, Name: {not: \"\"}}, PriceAsymmetry: {lt: 0.1}}, Block: {Date: {since: \"2024-07-01\"}}}\n    ) {\n      volume: sum(of: Trade_Amount)\n      volatility_token: standard_deviation(of: Trade_Price)\n      Trade {\n        high: Price(maximum: Trade_Price)\n        low: Price(minimum: Trade_Price)\n        open: Price(minimum: Block_Slot)\n        close: Price(maximum: Block_Slot)\n        Currency {\n          Name\n          MintAddress\n          Symbol\n        }\n        Side{\n          Currency{\n            Name\n            MintAddress\n            Symbol\n          }\n        }\n      }\n      count\n    }\n  }\n}\n",
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
        print(f"Error fetching volume-ordered data: {response.status_code}")
        print(response.text)
        return None

def fetch_memecoin_data_by_volatility():
    """
    Fetch memecoin data from Bitquery API ordered by volatility.
    
    Returns:
        Dictionary containing the API response data
    """
    url = "https://streaming.bitquery.io/eap"

    payload = json.dumps({
       "query": "{\n  Solana {\n    DEXTradeByTokens(\n      limit: {count: 100}\n      orderBy: {descendingByField: \"volatility_token\"}\n      where: {Trade: {Currency: {MintAddress: {notIn: [\"Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB\", \"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v\", \"So11111111111111111111111111111111111111111\", \"So11111111111111111111111111111111111111112\", \"11111111111111111111111111111111\", \"27G8MtK7VtTcCHkpASjSDdkWWYfoqT6ggEuKidVJidD4\", \"cbbtcf3aa214zXHbiAZQwf4122FBYbraNdFqgw4iMij\", \"2b1kV6DkPAnxd5ixfnxCpjxmKwqjjaYmCZfHsFu24GXo\", \"DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263\"]}, Name: {not: \"\"}}, PriceAsymmetry: {lt: 0.1}}, Block: {Date: {since: \"2024-07-01\"}}}\n    ) {\n      volume: sum(of: Trade_Amount)\n      volatility_token: standard_deviation(of: Trade_Price)\n      Trade {\n        high: Price(maximum: Trade_Price)\n        low: Price(minimum: Trade_Price)\n        open: Price(minimum: Block_Slot)\n        close: Price(maximum: Block_Slot)\n        Currency {\n          Name\n          MintAddress\n          Symbol\n        }\n        Side{\n          Currency{\n            Name\n            MintAddress\n            Symbol\n          }\n        }\n      }\n      count\n    }\n  }\n}\n",
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
        print(f"Error fetching volatility-ordered data: {response.status_code}")
        print(response.text)
        return None

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

if __name__ == "__main__":
    # Simple test of data fetching
    print("Testing Bitquery data fetching...")
    data = fetch_memecoin_data()
    
    if data:
        print("Data fetched successfully!")
        print(f"Volume data keys: {list(data['volume_ordered'].keys())}")
        print(f"Volatility data keys: {list(data['volatility_ordered'].keys())}")
    else:
        print("Failed to fetch data.")
