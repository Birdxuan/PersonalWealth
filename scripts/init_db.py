#!/usr/bin/env python3
"""初始化数据库脚本"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db import Database
from src.config import ACCOUNTS, ASSET_CATEGORIES

def init_database():
    """初始化数据库和基础数据"""
    
    # 创建数据库和表
    db = Database()
    db.init_database()
    
    # 添加账户
    print("\n📱 添加账户...")
    for account_name, account_type in ACCOUNTS.items():
        if db.add_account(account_name, account_type):
            print(f"  ✅ {account_name}")
        else:
            print(f"  ⚠️  {account_name} 已存在")
    
    # 添加资产类型
    print("\n📦 添加资产类型...")
    for category in ASSET_CATEGORIES:
        if db.add_category(category):
            print(f"  ✅ {category}")
        else:
            print(f"  ⚠️  {category} 已存在")
    
    print("\n✅ 数据库初始化完成！")
    print("\n下一步: python scripts/add_sample_data.py")

if __name__ == '__main__':
    init_database()
