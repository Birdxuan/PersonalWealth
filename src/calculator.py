"""资产计算和分析模块 - PersonalWealth"""

from src.db import Database
from src.config import USD_TO_CNY
from collections import defaultdict

class Calculator:
    """资产计算和分析类"""
    
    def __init__(self, db_path=None):
        self.db = Database(db_path)
    
    def convert_to_cny(self, amount, currency='CNY'):
        """转换为人民币"""
        if currency == 'USD':
            return amount * USD_TO_CNY
        return amount
    
    def calculate_total_assets(self):
        """计算总资产"""
        assets = self.db.get_assets()
        
        result = {
            'total_cny': 0,
            'stock_cny': 0,
            'fund_cny': 0,
            'cash_cny': 0,
            'crypto_cny': 0
        }
        
        for asset in assets:
            value = asset['quantity'] * asset['avg_cost']
            value_cny = self.convert_to_cny(value, asset['currency'])
            
            # 按资产类型分类
            if asset['category'] == '股票':
                result['stock_cny'] += value_cny
            elif asset['category'] == '基金':
                result['fund_cny'] += value_cny
            elif asset['category'] == '现金':
                result['cash_cny'] += value_cny
            elif asset['category'] == '加密货币':
                result['crypto_cny'] += value_cny
            
            result['total_cny'] += value_cny
        
        return result
    
    def get_assets_by_account(self):
        """按账户统计资产"""
        assets = self.db.get_assets()
        result = defaultdict(float)
        
        for asset in assets:
            value = asset['quantity'] * asset['avg_cost']
            value_cny = self.convert_to_cny(value, asset['currency'])
            result[asset['account']] += value_cny
        
        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
    
    def get_assets_by_category(self):
        """按资产类型统计资产"""
        assets = self.db.get_assets()
        result = defaultdict(float)
        
        for asset in assets:
            value = asset['quantity'] * asset['avg_cost']
            value_cny = self.convert_to_cny(value, asset['currency'])
            result[asset['category']] += value_cny
        
        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
    
    def get_account_detail(self, account):
        """获取账户详情"""
        assets = self.db.get_assets(account)
        result = {
            'account': account,
            'total_cny': 0,
            'assets': []
        }
        
        for asset in assets:
            value = asset['quantity'] * asset['avg_cost']
            value_cny = self.convert_to_cny(value, asset['currency'])
            
            result['assets'].append({
                'symbol': asset['symbol'],
                'category': asset['category'],
                'quantity': asset['quantity'],
                'avg_cost': asset['avg_cost'],
                'value_cny': value_cny,
                'currency': asset['currency']
            })
            
            result['total_cny'] += value_cny
        
        return result
    
    def get_summary(self):
        """获取资产总结"""
        total = self.calculate_total_assets()
        by_account = self.get_assets_by_account()
        by_category = self.get_assets_by_category()
        
        return {
            'total': total,
            'by_account': by_account,
            'by_category': by_category,
            'snapshots': self.db.get_snapshots(30)
        }
    
    def print_summary(self):
        """打印资产总结（命令行）"""
        summary = self.get_summary()
        total = summary['total']
        by_account = summary['by_account']
        by_category = summary['by_category']
        
        print("\n" + "="*50)
        print("📊 个人资产统计")
        print("="*50)
        
        print(f"\n💰 总资产: ¥{total['total_cny']:.2f}")
        print(f"  - 股票: ¥{total['stock_cny']:.2f}")
        print(f"  - 基金: ¥{total['fund_cny']:.2f}")
        print(f"  - 现金: ¥{total['cash_cny']:.2f}")
        print(f"  - 加密货币: ¥{total['crypto_cny']:.2f}")
        
        print("\n📱 账户分布:")
        for account, value in by_account.items():
            percentage = (value / total['total_cny'] * 100) if total['total_cny'] > 0 else 0
            print(f"  - {account}: ¥{value:.2f} ({percentage:.1f}%)")
        
        print("\n📦 资产类型分布:")
        for category, value in by_category.items():
            percentage = (value / total['total_cny'] * 100) if total['total_cny'] > 0 else 0
            print(f"  - {category}: ¥{value:.2f} ({percentage:.1f}%)")
        
        print("\n" + "="*50 + "\n")
