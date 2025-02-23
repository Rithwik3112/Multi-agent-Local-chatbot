import yfinance as yf

def get_stock_price(symbol: str) -> float:
    ticker = yf.Ticker(symbol)
    price_attrs = ['regularMarketPrice', 'currentPrice', 'price']
    
    for attr in price_attrs:
        if attr in ticker.info and ticker.info[attr] is not None:
            return ticker.info[attr]
            
    fast_info = ticker.fast_info
    if hasattr(fast_info, 'last_price') and fast_info.last_price is not None:
        return fast_info.last_price
        
    raise Exception("Could not find valid price data")
