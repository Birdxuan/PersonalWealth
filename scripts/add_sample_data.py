#!/usr/bin/env python3
"""Add sample data to the database"""

from src.db import Database
from src.config import DB_PATH
from datetime import datetime, timedelta

db = Database(DB_PATH)
db.connect()

# Sample assets data
samples = [
    # 微信
    {'account': '微信', 'category': '现金', 'symbol': 'CNY', 'quantity': 10000, 'avg_cost': 1.0, 'currency': 'CNY'},
    
    # 支付宝
    {'account': '支付宝', 'category': '余额宝', 'symbol': 'CNY', 'quantity': 8000, 'avg_cost': 1.0, 'currency': 'CNY'},
    {'account': '支付宝', 'category': '基金', 'symbol': '易方达沪深300', 'quantity': 1000, 'avg_cost': 3.5, 'currency': 'CNY'},
    
    # A股
    {'account': 'A股', 'category': '股票', 'symbol': '茅台', 'quantity': 10, 'avg_cost': 2000, 'currency': 'CNY'},
    {'account': 'A股', 'category': 'ETF', 'symbol': '510300', 'quantity': 500, 'avg_cost': 4.0, 'currency': 'CNY'},
    
    # 美股（IBKR盈透）
    {'account': '盈透(IBKR)', 'category': '股票', 'symbol': 'AAPL', 'quantity': 100, 'avg_cost': 120, 'currency': 'USD'},
    {'account': '盈透(IBKR)', 'category': '股票', 'symbol': 'TSLA', 'quantity': 50, 'avg_cost': 200, 'currency': 'USD'},
    {'account': '盈透(IBKR)', 'category': '现金', 'symbol': 'USD', 'quantity': 5000, 'avg_cost': 1.0, 'currency': 'USD'},
    
    # 众安银行
    {'account': '众安银行', 'category': '现金', 'symbol': 'USD', 'quantity': 3000, 'avg_cost': 1.0, 'currency': 'USD'},
    
    # 加密货币
    {'account': '其他', 'category': '加密货币', 'symbol': 'BTC', 'quantity': 0.1, 'avg_cost': 300000, 'currency': 'CNY'},
    {'account': '其他', 'category': '加密货币', 'symbol': 'ETH', 'quantity': 1.0, 'avg_cost': 25000, 'currency': 'CNY'},
]

# Add sample assets
for sample in samples:
    db.add_asset(
        account=sample['account'],
        category=sample['category'],
        symbol=sample['symbol'],
        quantity=sample['quantity'],
        avg_cost=sample['avg_cost'],
        currency=sample['currency']
    )
    print(f"✅ Added: {sample['account']} - {sample['symbol']}")

# Add sample transactions
transactions = [
    {'account': '微信', 'symbol': 'CNY', 'category': '现金', 'type': 'deposit', 'amount': 10000, 'price': 1.0},
    {'account': '支付宝', 'symbol': 'CNY', 'category': '余额宝', 'type': 'deposit', 'amount': 8000, 'price': 1.0},
    {'account': 'A股', 'symbol': '茅台', 'category': '股票', 'type': 'buy', 'amount': 10, 'price': 2000},
    {'account': '盈透(IBKR)', 'symbol': 'AAPL', 'category': '股票', 'type': 'buy', 'amount': 100, 'price': 120},
]

for tx in transactions:
    db.add_transaction(
        account=tx['account'],
        symbol=tx['symbol'],
        category=tx['category'],
        type=tx['type'],
        amount=tx['amount'],
        price=tx['price']
    )

print(f"\n✅ Sample data added successfully!")

# Add sample daily snapshots (last 30 days)
from src.calculator import Calculator

calc = Calculator(db)

for i in range(30, 0, -1):
    date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
    total = calc.get_total_wealth() - (i * 100)  # Simulate growth
    stats = calc.get_statistics()
    
    db.add_snapshot(
        total_cny=max(0, total),
        stock_cny=stats['stock_value'],
        fund_cny=stats['fund_value'],
        cash_cny=stats['cash_value'],
        crypto_cny=stats['crypto_value'],
        date=date
    )

print(f"✅ Daily snapshots added (30 days)")

db.close()

print("\n" + "="*50)
print("Sample data initialization complete!")
print("="*50)
