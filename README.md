# PersonalWealth 💰

个人多账户、多资产统一管理系统（Personal Multi-Account Asset Management System）

## 📊 项目简介

PersonalWealth 是一个集合微信、支付宝、A股、美股(IBKR/众安)、加密货币等多个账户的**个人资产统一看板系统**。

不仅仅是记账工具，而是：

- 📈 **实时资产可视化** - 清晰展示所有资产总额和分布
- 📊 **智能分析** - 账户占比、资产类型分布、趋势变化
- 💱 **自动汇率换算** - 美元自动转换为人民币
- 📉 **历史追踪** - 每日快照记录，长期追踪资产变化
- 🤖 **自动化** - 支持定时更新，GitHub Actions 集成

---

## 🗂️ 项目结构

```
PersonalWealth/
├── src/
│   ├── __init__.py
│   ├── config.py           # 配置文件（汇率、账户等）
│   ├── db.py               # 数据库操作模块
│   └── calculator.py       # 资产计算和分析
├── scripts/
│   ├── init_db.py          # 初始化数据库
│   ├── add_sample_data.py  # 添加示例数据
│   └── daily_snapshot.py   # 每日快照脚本
├── dashboard/
│   ├── index.html          # 可视化仪表板
│   ├── style.css           # 样式文件
│   └── chart.js            # 前端逻辑
├── data/
│   └── wealth.db           # SQLite 数据库（自动生成）
├── requirements.txt        # Python 依赖
├── .gitignore             # Git 忽略
└── README.md              # 本文件
```

---

## 🚀 快速开始

### 前置要求

- Python 3.9+
- pip

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

### 2️⃣ 初始化数据库

```bash
python scripts/init_db.py
```

输出：
```
✅ 数据库初始化成功！
✅ 表创建完成
```

### 3️⃣ 添加示例数据

```bash
python scripts/add_sample_data.py
```

输出：
```
✅ 示例数据添加成功！
微信: ¥10,000 (现金 ¥5,000 + 基金 ¥5,000)
支付宝: ¥20,000 (余额宝 ¥15,000 + 基金 ¥5,000)
...
总资产: ¥130,000
```

### 4️⃣ 启动本地服务

```bash
python -m http.server 8000
```

### 5️⃣ 打开仪表板

在浏览器打开：
```
http://localhost:8000/dashboard/index.html
```

你将看到：
- 📊 总资产金额
- 🥧 账户分布饼图
- 📦 资产类型分布
- 📈 30天趋势曲线
- 📋 详细资产表格

---

## 📚 核心功能

### 1️⃣ 多账户支持

已内置账户：

| 账户 | 类型 | 支持资产 |
|------|------|----------|
| 微信 | wallet | 现金、基金、理财 |
| 支付宝 | wallet | 现金、基金、理财 |
| A股 | broker | 股票、ETF、基金 |
| IBKR(盈透) | broker | 股票、ETF、现金 |
| 众安银行 | bank | 现金、理财 |
| 其他 | other | 加密货币、其他 |

### 2️⃣ 多资产类型

- 💵 **现金** - 钱包余额
- 💹 **股票** - 个股持仓
- 📈 **基金** - 基金产品
- 📊 **ETF** - 交易所交易基金
- 💎 **加密货币** - BTC、ETH等
- 🏦 **理财产品** - 银行理财

### 3️⃣ 智能计算

- ✅ 自动汇率转换（美元 → 人民币）
- ✅ 总资产计算
- ✅ 账户占比分析
- ✅ 资产类型分布
- ✅ 持仓成本分析

### 4️⃣ 数据持久化

- ✅ SQLite 数据库存储
- ✅ 每日快照记录
- ✅ 交易历史追踪
- ✅ 长期趋势分析

---

## 📊 数据库设计

### 核心表结构

#### 1. accounts（账户表）
```sql
id          INTEGER PRIMARY KEY
name        TEXT              -- 微信/支付宝/IBKR等
type        TEXT              -- wallet/broker/bank
```

#### 2. asset_categories（资产类型表）
```sql
id          INTEGER PRIMARY KEY
name        TEXT              -- 现金/基金/股票等
```

#### 3. assets（资产持仓表）⭐核心表
```sql
id          INTEGER PRIMARY KEY
account     TEXT              -- 所属账户
category    TEXT              -- 资产类型
symbol      TEXT              -- 标的代码
quantity    REAL              -- 持仓数量
avg_cost    REAL              -- 成本价
currency    TEXT              -- 货币（CNY/USD）
updated_at  TEXT              -- 更新时间
```

#### 4. transactions（交易记录表）
```sql
id          INTEGER PRIMARY KEY
account     TEXT
symbol      TEXT
category    TEXT
type        TEXT              -- buy/sell/deposit/redeem
amount      REAL
price       REAL
fee         REAL
time        TEXT
```

#### 5. daily_snapshot（每日快照表）
```sql
id          INTEGER PRIMARY KEY
total_cny   REAL              -- 总资产(人民币)
stock_cny   REAL              -- 股票(人民币)
fund_cny    REAL              -- 基金(人民币)
cash_cny    REAL              -- 现金(人民币)
crypto_cny  REAL              -- 加密货币(人民币)
date        TEXT              -- 日期
```

---

## 🎯 核心 API

### Python 模块使用

#### 初始化数据库
```python
from src.db import Database

db = Database('data/wealth.db')
db.init_database()
```

#### 添加资产
```python
db.add_asset(
    account='微信',
    category='现金',
    symbol='CNY',
    quantity=5000,
    avg_cost=1.0,
    currency='CNY'
)
```

#### 查询总资产
```python
from src.calculator import Calculator

calc = Calculator('data/wealth.db')
total = calc.calculate_total_assets()
print(f"总资产: ¥{total['total_cny']:.2f}")
```

#### 获取账户分布
```python
by_account = calc.get_assets_by_account()
print(by_account)
# Output: {'微信': 10000, '支付宝': 20000, ...}
```

---

## 🔧 配置说明

编辑 `src/config.py` 自定义：

```python
# 汇率配置
USD_TO_CNY = 7.08  # 美元兑人民币

# 账户配置
ACCOUNTS = {
    'WeChat': 'wallet',
    'Alipay': 'wallet',
    'A-Stock': 'broker',
    'IBKR': 'broker',
    'ZhongAn': 'bank',
    'Other': 'other'
}

# 资产类型
ASSET_CATEGORIES = ['现金', '基金', '股票', 'ETF', '理财', '加密货币']
```

---

## 📈 使用示例

### 场景1：每天记录一次资产

```bash
# 更新资产数据
python scripts/add_sample_data.py

# 记录每日快照
python scripts/daily_snapshot.py

# 刷新网页查看最新数据
# http://localhost:8000/dashboard/index.html
```

### 场景2：查看账户分布

1. 打开仪表板
2. 查看左侧 **账户分布饼图**
3. 清晰看到每个账户占比

### 场景3：分析资产类型

1. 打开仪表板
2. 查看右侧 **资产类型分布**
3. 了解现金/股票/基金占比

### 场景4：追踪长期趋势

1. 每天自动运行 `daily_snapshot.py`
2. 打开仪表板 **30天趋势图**
3. 观察资产增长或回撤

---

## 🤖 自动化

### GitHub Actions（可选）

项目包含 `.github/workflows/update-dashboard.yml` 配置：

- ⏰ 每天午夜自动运行
- 🔄 自动更新数据
- 📸 生成每日快照
- 💾 自动提交到仓库

启用方法：
1. 在项目设置中启用 Actions
2. 仓库会每天自动更新数据

---

## 🧩 如何添加新账户

### 步骤1：编辑配置

编辑 `src/config.py`：

```python
ACCOUNTS = {
    'WeChat': 'wallet',
    'Alipay': 'wallet',
    'A-Stock': 'broker',
    'IBKR': 'broker',
    'ZhongAn': 'bank',
    'Other': 'other',
    'NewAccount': 'broker'  # 添加新账户
}
```

### 步骤2：添加数据

编辑 `scripts/add_sample_data.py`：

```python
db.add_asset(
    account='NewAccount',
    category='股票',
    symbol='AAPL',
    quantity=10,
    avg_cost=150,
    currency='USD'
)
```

### 步骤3：重新生成数据

```bash
python scripts/init_db.py
python scripts/add_sample_data.py
```

---

## 🚀 进阶功能（V2 计划）

- [ ] FastAPI 后端 REST API
- [ ] 用户认证和权限
- [ ] 实时行情接口（币安、雪球等）
- [ ] A股/美股 自动同步
- [ ] 定时任务服务（APScheduler）
- [ ] 数据导入/导出（CSV）
- [ ] 邮件/钉钉 定时推送
- [ ] Docker 容器化
- [ ] 云端部署（Vercel/Railway）
- [ ] 手机响应式设计

---

## 💡 常见问题

### Q1: 如何更新汇率？

A: 编辑 `src/config.py` 中的 `USD_TO_CNY` 值，或集成实时汇率 API。

### Q2: 数据存储在哪里？

A: 所有数据存储在 `data/wealth.db` SQLite 数据库中。

### Q3: 如何导出数据？

A: 可以用 SQLite 工具直接打开 `.db` 文件，或编写脚本导出为 CSV。

### Q4: 支持多用户吗？

A: V1 不支持，V2 计划添加用户认证系统。

### Q5: 性能如何？

A: SQLite 支持 100万+ 条交易记录，足以满足个人使用。

---

## 📝 License

MIT License - 自由使用和修改

---

## 🙏 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📞 联系方式

GitHub: [@Birdxuan](https://github.com/Birdxuan)

---

**Happy Wealth Tracking! 🚀**
