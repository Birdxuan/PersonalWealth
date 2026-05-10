#!/usr/bin/env python3
"""每日快照脚本 - 自动记录当日资产"""

import sys
import os
from datetime import datetime

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db import Database
from src.calculator import Calculator

def take_daily_snapshot():
    """记录每日快照"""
    
    db = Database()
    calc = Calculator()
    
    print("\n📸 记录每日快照...")
    print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 计算当日资产
    summary = calc.get_summary()
    total = summary['total']
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 添加快照
    if db.add_snapshot(
        total_cny=total['total_cny'],
        stock_cny=total['stock_cny'],
        fund_cny=total['fund_cny'],
        cash_cny=total['cash_cny'],
        crypto_cny=total['crypto_cny'],
        date=today
    ):
        print(f"\n✅ 快照记录成功！")
        print(f"   日期: {today}")
        print(f"   总资产: ¥{total['total_cny']:.2f}")
        print(f"   - 股票: ¥{total['stock_cny']:.2f}")
        print(f"   - 基金: ¥{total['fund_cny']:.2f}")
        print(f"   - 现金: ¥{total['cash_cny']:.2f}")
        print(f"   - 加密货币: ¥{total['crypto_cny']:.2f}")
    else:
        print(f"\n❌ 快照记录失败！")

if __name__ == '__main__':
    take_daily_snapshot()
