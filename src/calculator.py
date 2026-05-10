"""Asset calculation and analysis"""

from typing import Dict, List, Tuple
from src.db import Database
from src.config import ASSET_PRICES, EXCHANGE_RATE

class Calculator:
    """Asset calculation and analysis"""
    
    def __init__(self, db: Database):
        self.db = db
        self.exchange_rate = EXCHANGE_RATE['USD_TO_CNY']
    
    def get_asset_value(self, symbol: str, quantity: float, currency: str) -> float:
        """Calculate asset value in CNY"""
        price = ASSET_PRICES.get(symbol, 1.0)
        value = price * quantity
        
        if currency == 'USD':
            value *= self.exchange_rate
        
        return value
    
    def get_total_wealth(self) -> float:
        """Calculate total wealth in CNY"""
        assets = self.db.get_assets()
        total = 0.0
        
        for asset in assets:
            value = self.get_asset_value(
                asset['symbol'],
                asset['quantity'],
                asset['currency']
            )
            total += value
        
        return round(total, 2)
    
    def get_wealth_by_account(self) -> Dict[str, float]:
        """Get wealth distribution by account"""
        accounts = self.db.get_accounts()
        result = {}
        
        for account in accounts:
            assets = self.db.get_assets(account=account['name'])
            total = 0.0
            
            for asset in assets:
                value = self.get_asset_value(
                    asset['symbol'],
                    asset['quantity'],
                    asset['currency']
                )
                total += value
            
            result[account['name']] = round(total, 2)
        
        return result
    
    def get_wealth_by_category(self) -> Dict[str, float]:
        """Get wealth distribution by asset category"""
        categories = self.db.get_categories()
        result = {}
        
        for category in categories:
            result[category['name']] = 0.0
        
        assets = self.db.get_assets()
        for asset in assets:
            value = self.get_asset_value(
                asset['symbol'],
                asset['quantity'],
                asset['currency']
            )
            result[asset['category']] = result.get(asset['category'], 0.0) + value
        
        # Round all values
        return {k: round(v, 2) for k, v in result.items()}
    
    def get_asset_details(self) -> List[Dict]:
        """Get detailed asset information"""
        assets = self.db.get_assets()
        result = []
        
        for asset in assets:
            value = self.get_asset_value(
                asset['symbol'],
                asset['quantity'],
                asset['currency']
            )
            
            profit = value - (asset['avg_cost'] * asset['quantity'])
            if asset['currency'] == 'USD':
                profit = profit / self.exchange_rate  # Convert back for calculation
            
            profit_rate = (profit / (asset['avg_cost'] * asset['quantity'])) * 100 if asset['avg_cost'] > 0 else 0
            
            result.append({
                'account': asset['account'],
                'category': asset['category'],
                'symbol': asset['symbol'],
                'quantity': asset['quantity'],
                'avg_cost': asset['avg_cost'],
                'current_price': ASSET_PRICES.get(asset['symbol'], asset['avg_cost']),
                'value_cny': round(value, 2),
                'profit': round(profit, 2),
                'profit_rate': round(profit_rate, 2),
                'currency': asset['currency']
            })
        
        return result
    
    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        wealth_by_category = self.get_wealth_by_category()
        wealth_by_account = self.get_wealth_by_account()
        total = self.get_total_wealth()
        
        return {
            'total_wealth': total,
            'by_account': wealth_by_account,
            'by_category': wealth_by_category,
            'stock_value': wealth_by_category.get('股票', 0),
            'fund_value': wealth_by_category.get('基金', 0),
            'cash_value': wealth_by_category.get('现金', 0),
            'crypto_value': wealth_by_category.get('加密货币', 0),
        }
