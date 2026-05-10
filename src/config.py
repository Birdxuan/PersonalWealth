"""配置文件 - PersonalWealth"""

import os
from datetime import datetime

# ========== 数据库配置 ==========
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'wealth.db')

# ========== 汇率配置 ==========
USD_TO_CNY = 7.08  # 美元兑人民币（可手动更新或接入实时汇率API）

# ========== 账户配置 ==========
ACCOUNTS = {
    '微信': 'wallet',
    '支付宝': 'wallet',
    'A股': 'broker',
    'IBKR(盈透)': 'broker',
    '众安银行': 'bank',
    '其他': 'other'
}

# ========== 资产类型 ==========
ASSET_CATEGORIES = [
    '现金',
    '基金',
    '股票',
    'ETF',
    '理财',
    '加密货币'
]

# ========== 颜色配置（用于图表） ==========
COLORS = {
    '微信': '#09B981',
    '支付宝': '#3B82F6',
    'A股': '#F59E0B',
    'IBKR(盈透)': '#8B5CF6',
    '众安银行': '#EC4899',
    '其他': '#6B7280',
}

CATEGORY_COLORS = {
    '现金': '#10B981',
    '基金': '#3B82F6',
    '股票': '#F59E0B',
    'ETF': '#8B5CF6',
    '理财': '#EC4899',
    '加密货币': '#EF4444'
}

# ========== 其他配置 ==========
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
SHORT_DATE_FORMAT = '%Y-%m-%d'

def get_now():
    """获取当前时间"""
    return datetime.now().strftime(DATE_FORMAT)

def get_today():
    """获取今天日期"""
    return datetime.now().strftime(SHORT_DATE_FORMAT)
