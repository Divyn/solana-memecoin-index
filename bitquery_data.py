import requests
import json
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

def fetch_memecoin_data():
    """
    Fetch both volume-ordered and volatility-ordered memecoin data.
    
    Returns:
        Dictionary containing both datasets
    """
    print("Fetching volume-ordered data...")
    volume_data = fetch_memecoin_data_by_volume()
    
    print("Fetching volatility-ordered data...")
    volatility_data = fetch_memecoin_data_by_volatility()
    
    if volume_data is None or volatility_data is None:
        return None
    
    return {
        'volume_ordered': volume_data,
        'volatility_ordered': volatility_data
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