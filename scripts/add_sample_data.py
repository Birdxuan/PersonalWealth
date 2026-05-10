#!/usr/bin/env python3
"""添加示例数据脚本"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db import Database
from src.calculator import Calculator
from datetime import datetime, timedelta

def add_sample_data():
    """添加示例数据"""
    
    db = Database()
    
    print("\n📝 添加示例资产数据...\n")
    
    # 微信
    db.add_asset('微信', '现金', 'CNY', 5000, 1.0, 'CNY')
    db.add_asset('微信', '基金', '易方达沪深300', 1000, 5.0, 'CNY')
    print("✅ 微信: ¥5,000 (现金) + ¥5,000 (基金) = ¥10,000")
    
    # 支付宝
    db.add_asset('支付宝', '现金', 'CNY', 15000, 1.0, 'CNY')
    db.add_asset('支付宝', '基金', '余额宝', 5000, 1.0, 'CNY')
    print("✅ 支付宝: ¥15,000 (现金) + ¥5,000 (基金) = ¥20,000")
    
    # A股
    db.add_asset('A股', '股票', '贵州茅台', 10, 1800, 'CNY')
    db.add_asset('A股', 'ETF', '沪深300', 100, 300, 'CNY')
    print("✅ A股: ¥18,000 (贵州茅台) + ¥30,000 (沪深300) = ¥48,000")
    
    # IBKR (美股)
    db.add_asset('IBKR(盈透)', '股票', 'AAPL', 10, 150, 'USD')
    db.add_asset('IBKR(盈透)', '现金', 'USD', 5000, 1.0, 'USD')
    print("✅ IBKR: $1,500 (AAPL) + $5,000 (现金) = $6,500 ≈ ¥46,020")
    
    # 众安银行
    db.add_asset('众安银行', '现金', 'CNY', 6000, 1.0, 'CNY')
    print("✅ 众安银行: ¥6,000")
    
    # 其他 (加密货币)
    db.add_asset('其他', '加密货币', 'BTC', 0.5, 40000, 'USD')
    db.add_asset('其他', '加密货币', 'ETH', 5, 2500, 'USD')
    print("✅ 其他: 0.5 BTC + 5 ETH ≈ ¥88,900")
    
    # 计算总资产
    calc = Calculator()
    summary = calc.get_summary()
    total_cny = summary['total']['total_cny']
    
    print(f"\n💰 总资产: ¥{total_cny:.2f}")
    
    # 打印账户分布
    print("\n📱 账户分布:")
    for account, value in summary['by_account'].items():
        percentage = (value / total_cny * 100) if total_cny > 0 else 0
        print(f"  {account}: ¥{value:.2f} ({percentage:.1f}%)")
    
    # 打印资产类型分布
    print("\n📦 资产类型分布:")
    for category, value in summary['by_category'].items():
        percentage = (value / total_cny * 100) if total_cny > 0 else 0
        print(f"  {category}: ¥{value:.2f} ({percentage:.1f}%)")
    
    # 添加快照
    db.add_snapshot(
        total_cny=total_cny,
        stock_cny=summary['total']['stock_cny'],
        fund_cny=summary['total']['fund_cny'],
        cash_cny=summary['total']['cash_cny'],
        crypto_cny=summary['total']['crypto_cny'],
        date=datetime.now().strftime('%Y-%m-%d')
    )
    
    # 添加历史快照（模拟 30 天数据）
    print("\n📊 生成 30 天历史数据...")
    for i in range(1, 31):
        # 模拟每日波动
        fluctuation = 1 + (i * 0.01)  # 每天增长约 1%
        date = (datetime.now() - timedelta(days=30-i)).strftime('%Y-%m-%d')
        db.add_snapshot(
            total_cny=total_cny * fluctuation,
            stock_cny=summary['total']['stock_cny'] * fluctuation,
            fund_cny=summary['total']['fund_cny'] * fluctuation,
            cash_cny=summary['total']['cash_cny'] * fluctuation,
            crypto_cny=summary['total']['crypto_cny'] * fluctuation,
            date=date
        )
    
    print("✅ 示例数据添加完成！")
    print("\n下一步: 启动本地服务")
    print("  python -m http.server 8000")
    print("\n然后访问: http://localhost:8000/dashboard/index.html")

if __name__ == '__main__':
    add_sample_data()
