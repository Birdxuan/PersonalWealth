# 📊 PersonalWealth - 个人资产统计系统

一个功能完整的**多账户、多资产类型的个人财富管理系统**。支持微信、支付宝、A股、美股（盈透/众安）、加密货币等多平台资产统一查看和分析。

## ✨ 核心功能

### 🎯 资产管理
- ✅ 微信、支付宝、A股、美股(IBKR)、众安、其他账户管理
- ✅ 现金、基金、股票、ETF、加密货币等多种资产类型
- ✅ 自动汇率换算（美元→人民币）
- ✅ 实时资产估值计算

### 📊 可视化仪表板
- 📱 总资产卡片（总值、股票、基金、现金、加密）
- 🥧 账户分布饼图（微信/支付宝/A股/IBKR等）
- 📦 资产类型分布饼图
- 📈 30天资产趋势曲线
- 📋 详细持仓表格

### 🔄 数据追踪
- 每日自动快照记录
- 资产变化历史
- 交易记录管理

## 🚀 快速开始

### 前置要求
- Python 3.8+
- pip

### 安装步骤

#### 1️⃣ 克隆仓库
```bash
git clone https://github.com/Birdxuan/PersonalWealth.git
cd PersonalWealth
```

#### 2️⃣ 安装依赖
```bash
pip install -r requirements.txt
```

#### 3️⃣ 初始化数据库
```bash
python scripts/init_db.py
```

#### 4️⃣ 添加示例数据
```bash
python scripts/add_sample_data.py
```

#### 5️⃣ 启动本地服务
```bash
python -m http.server 8000
```

#### 6️⃣ 打开仪表板
在浏览器访问：
```
http://localhost:8000/dashboard/index.html
```

## 📁 项目结构

```
PersonalWealth/
├── src/
│   ├── __init__.py          # 包初始化
│   ├── config.py            # 配置文件（汇率、账户等）
│   ├── db.py                # 数据库操作（SQLite CRUD）
│   └── calculator.py        # 资产计算和分析
├── scripts/
│   ├── init_db.py           # 初始化数据库
│   ├── add_sample_data.py   # 添加示例数据
│   └── daily_snapshot.py    # 每日快照脚本
├── dashboard/
│   ├── index.html           # 仪表板主页
│   ├── style.css            # 样式文件
│   └── chart.js             # 图表逻辑
├── data/
│   └── wealth.db            # SQLite 数据库（自动生成）
├── requirements.txt         # Python 依赖
├── .gitignore              # Git 忽略配置
└── README.md               # 本文件
```

## 💾 数据库设计

### 核心表结构

#### accounts（账户）
```sql
id, name, type, currency
```
示例：
- 微信（wallet）
- 支付宝（wallet）
- A股（broker）
- IBKR（broker）

#### asset_categories（资产类型）
```sql
id, name
```
示例：现金、基金、股票、ETF、加密货币

#### assets（资产持仓）
```sql
id, account, category, symbol, quantity, avg_cost, currency, updated_time
```
核心表，存储所有持仓信息

#### transactions（交易记录）
```sql
id, account, symbol, category, type, amount, price, fee, time
```
支持 buy/sell/deposit/withdraw 等交易类型

#### daily_snapshot（每日快照）
```sql
id, total_cny, stock_cny, fund_cny, cash_cny, crypto_cny, date
```
用于绘制资产趋势曲线

## 🛠️ 使用指南

### 添加自己的资产

编辑 `scripts/add_sample_data.py`：

```python
# 修改示例数据为你的真实资产
db.add_asset(
    account='微信',
    category='余额',
    symbol='CNY',
    quantity=5000,
    avg_cost=1.0,
    currency='CNY'
)
```

### 每日更新资产

```bash
# 手动记录每日快照
python scripts/daily_snapshot.py
```

### 查询资产信息

```python
from src.db import Database
from src.calculator import Calculator

db = Database('data/wealth.db')
calc = Calculator(db)

# 获取总资产
total = calc.get_total_wealth()
print(f'总资产: {total} CNY')

# 获取各账户分布
by_account = calc.get_wealth_by_account()
for account, value in by_account.items():
    print(f'{account}: {value} CNY')
```

## 📊 示例数据

系统预装了示例数据（运行 `add_sample_data.py` 后）：

| 账户 | 类型 | 标的 | 数量 | 成本价 | 当前价格 | 估值 |
|------|------|------|------|--------|---------|------|
| 微信 | 现金 | CNY | 10,000 | 1.0 | 1.0 | 10,000 |
| 支付宝 | 基金 | 易方达沪深300 | 1,000 | 3.5 | 3.8 | 3,800 |
| A股 | 股票 | 茅台 | 10 | 2000 | 2500 | 25,000 |
| IBKR | 股票 | AAPL | 100 | 120 | 180 | 18,000(CNY) |
| 其他 | 加密 | BTC | 0.1 | 300,000 | 420,000 | 42,000 |

## 🔮 进阶功能（V2 及以后）

- [ ] FastAPI 后端服务
- [ ] 用户认证和多用户支持
- [ ] 实时数据源集成（Yahoo Finance、币安API等）
- [ ] 自动定时更新
- [ ] Docker 容器化部署
- [ ] 云端同步
- [ ] 移动端适配
- [ ] 报表导出（PDF/Excel）

## 📝 配置说明

编辑 `src/config.py` 自定义：

```python
# 汇率配置
EXCHANGE_RATE = {
    'USD_TO_CNY': 7.1,  # 美元到人民币汇率
}

# 资产价格配置（示例）
ASSET_PRICES = {
    'BTC': 420000,
    'ETH': 25000,
    'AAPL': 180,
    'TSLA': 250,
}
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 💬 反馈

有任何问题或建议，欢迎在 Issues 中反馈！

---

**祝你的个人财富管理之旅顺利！** 🚀
