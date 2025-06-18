import requests

class QuotexClient:
    def __init__(self):
        self.base_url = "https://quotex.com/api"
        self.session = requests.Session()
        
    def get_candles(self, pair="EURUSD", timeframe=1, count=100):
        response = self.session.get(
            f"{self.base_url}/candles",
            params={
                "pair": pair,
                "timeframe": timeframe,
                "count": count
            }
        )
        return response.json()