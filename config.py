

class Config:
    COINT_MARKET_URL = 'https://pro-api.coinmarketcap.com'
    COINT_MARKET_API_KEY = '19bc5ef9-2916-40d2-b4f6-4b490c8bfd43'
    FAKE_RESPONSE = '''
        {
    "status": {
        "timestamp": "2023-02-18T15:53:52.050Z",
        "error_code": 0,
        "error_message": null,
        "elapsed": 19,
        "credit_count": 1,
        "notice": null,
        "total_count": 8967
    },
    "data": [
        {
            "id": 1,
            "name": "Bitcoin",
            "symbol": "BTC",
            "slug": "bitcoin",
            "num_market_pairs": 9985,
            "date_added": "2013-04-28T00:00:00.000Z",
            "tags": [
                "mineable",
                "pow",
                "sha-256",
                "store-of-value",
                "state-channel",
                "coinbase-ventures-portfolio",
                "three-arrows-capital-portfolio",
                "polychain-capital-portfolio",
                "binance-labs-portfolio",
                "blockchain-capital-portfolio",
                "boostvc-portfolio",
                "cms-holdings-portfolio",
                "dcg-portfolio",
                "dragonfly-capital-portfolio",
                "electric-capital-portfolio",
                "fabric-ventures-portfolio",
                "framework-ventures-portfolio",
                "galaxy-digital-portfolio",
                "huobi-capital-portfolio",
                "alameda-research-portfolio",
                "a16z-portfolio",
                "1confirmation-portfolio",
                "winklevoss-capital-portfolio",
                "usv-portfolio",
                "placeholder-ventures-portfolio",
                "pantera-capital-portfolio",
                "multicoin-capital-portfolio",
                "paradigm-portfolio"
            ],
            "max_supply": 21000000,
            "circulating_supply": 19294856,
            "total_supply": 19294856,
            "platform": null,
            "cmc_rank": 1,
            "self_reported_circulating_supply": null,
            "self_reported_market_cap": null,
            "tvl_ratio": null,
            "last_updated": "2023-02-18T15:52:00.000Z",
            "quote": {
                "USD": {
                    "price": 24698.760157808465,
                    "volume_24h": 31141936404.325283,
                    "volume_change_24h": -24.9326,
                    "percent_change_1h": 0.42643877,
                    "percent_change_24h": 2.3573855,
                    "percent_change_7d": 13.59210068,
                    "percent_change_30d": 18.28474463,
                    "percent_change_60d": 45.75268575,
                    "percent_change_90d": 48.95264162,
                    "market_cap": 476559020623.4516,
                    "market_cap_dominance": 42.5876,
                    "fully_diluted_market_cap": 518673963313.98,
                    "tvl": null,
                    "last_updated": "2023-02-18T15:52:00.000Z"
                }
            }
        }
    ]
}
        '''