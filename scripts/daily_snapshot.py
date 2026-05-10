#!/usr/bin/env python3
"""Record daily asset snapshot"""

from src.db import Database
from src.calculator import Calculator
from src.config import DB_PATH
from datetime import datetime

db = Database(DB_PATH)
db.connect()

calc = Calculator(db)
stats = calc.get_statistics()

# Add daily snapshot
db.add_snapshot(
    total_cny=stats['total_wealth'],
    stock_cny=stats['stock_value'],
    fund_cny=stats['fund_value'],
    cash_cny=stats['cash_value'],
    crypto_cny=stats['crypto_value']
)

db.close()

print(f"✅ Daily snapshot recorded at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"   Total wealth: ¥{stats['total_wealth']:,.2f}")
print(f"   Stock: ¥{stats['stock_value']:,.2f}")
print(f"   Fund: ¥{stats['fund_value']:,.2f}")
print(f"   Cash: ¥{stats['cash_value']:,.2f}")
print(f"   Crypto: ¥{stats['crypto_value']:,.2f}")
