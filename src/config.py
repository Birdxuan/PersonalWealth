"""Configuration file for PersonalWealth"""

# Database path
DB_PATH = 'data/wealth.db'

# Exchange rates (USD to CNY)
EXCHANGE_RATE = {
    'USD_TO_CNY': 7.1,
}

# Asset prices (for calculation)
# These are example prices, update them with real data
ASSET_PRICES = {
    'BTC': 420000,
    'ETH': 25000,
    'AAPL': 180,
    'TSLA': 250,
    '茅台': 2500,
    '易方达沪深300': 3.8,
}

# Accounts configuration
ACCOUNTS = [
    {'name': '微信', 'type': 'wallet', 'currency': 'CNY'},
    {'name': '支付宝', 'type': 'wallet', 'currency': 'CNY'},
    {'name': 'A股', 'type': 'broker', 'currency': 'CNY'},
    {'name': '盈透(IBKR)', 'type': 'broker', 'currency': 'USD'},
    {'name': '众安银行', 'type': 'bank', 'currency': 'USD'},
    {'name': '其他', 'type': 'other', 'currency': 'CNY'},
]

# Asset categories
ASSET_CATEGORIES = [
    '现金',
    '基金',
    '股票',
    'ETF',
    '理财',
    '加密货币',
]
