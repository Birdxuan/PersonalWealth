# 💰 PersonalWealth

**个人多账户资产统一看板** - 一个实时的个人财富管理系统

支持同时管理：微信、支付宝、A股、美股(IBKR)、美股(众安)、加密货币等多账户资产。

## 📊 核心功能

- ✅ **多账户集成** - 微信/支付宝/A股/美股/加密货币
- ✅ **资产类型分类** - 现金/基金/股票/ETF等
- ✅ **实时资产汇总** - 统一换算成人民币/美元
- ✅ **资产结构分析** - 饼图展示资产分布
- ✅ **历史曲线** - 追踪资产增长趋势
- ✅ **每日快照** - 自动记录每日资产状态
- ✅ **交易记录** - 保留完整的买卖交易历史

## 🏗️ 项目结构

```
PersonalWealth/
├── data/
│   ├── wealth.db                 # SQLite数据库（自动创建）
│   └── sample_data.json          # 示例数据
├── scripts/
│   ├── init_db.py                # 初始化数据库
│   ├── sync_wealth.py            # 同步资产数据
│   └── daily_snapshot.py         # 每日快照脚本
├── frontend/
│   ├── index.html                # 主页面
│   ├── dashboard.html            # 资产看板
│   └── assets/
│       ├── style.css
│       └── chart.js
├── config/
│   └── config.example.json       # 配置模板
├── requirements.txt              # Python依赖
└── README.md                     # 项目说明
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/Birdxuan/PersonalWealth.git
cd PersonalWealth
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 初始化数据库

```bash
python scripts/init_db.py
```

### 4. 导入示例数据（可选）

```bash
python scripts/sync_wealth.py --sample
```

### 5. 启动查看

打开 `frontend/dashboard.html` 即可查看资产看板

## 💻 数据结构

### 数据库设计（SQLite）

#### 1. 账户表 (accounts)
```
- id: 账户ID
- name: 账户名称（微信/支付宝/IBKR等）
- type: 账户类型（wallet/broker/bank）
- currency: 货币单位（CNY/USD）
```

#### 2. 资产类型表 (asset_categories)
```
- id: 分类ID
- name: 分类名称（现金/基金/股票/ETF等）
```

#### 3. 资产持仓表 (assets)
```
- id: 资产ID
- account: 账户名称
- category: 资产分类
- symbol: 标的代码（AAPL/BTC/易方达等）
- quantity: 持仓数量
- avg_cost: 成本价
- currency: 货币单位
- current_price: 当前价格
- total_value: 总价值
- updated_at: 更新时间
```

#### 4. 交易记录表 (transactions)
```
- id: 交易ID
- account: 账户名称
- symbol: 标的代码
- type: 交易类型（buy/sell/deposit/withdraw）
- quantity: 交易数量
- price: 交易价格
- fee: 手续费
- created_at: 交易时间
```

#### 5. 每日快照表 (daily_snapshots)
```
- id: 快照ID
- total_cny: 总资产(人民币)
- total_usd: 总资产(美元)
- cash_cny: 现金(人民币)
- stock_cny: 股票(人民币)
- fund_cny: 基金(人民币)
- crypto_cny: 加密货币(人民币)
- created_at: 快照时间
```

## 📈 使用场景

### 场景1：查看当前总资产

```python
from scripts.sync_wealth import WealthManager

wm = WealthManager()
total = wm.get_total_wealth()
print(f"总资产: {total['total_cny']} 元")
```

### 场景2：查看各账户资产分布

```python
breakdown = wm.get_account_breakdown()
for account, value in breakdown.items():
    print(f"{account}: {value} 元")
```

### 场景3：导入新资产

```bash
# 编辑 data/sample_data.json，然后执行
python scripts/sync_wealth.py --import data/sample_data.json
```

## 🔄 自动化（Linux Crontab）

每天00:00自动记录资产快照：

```bash
0 0 * * * /usr/bin/python3 /path/to/PersonalWealth/scripts/daily_snapshot.py
```

## 📊 前端功能

### Dashboard 包含：

- 📌 **总资产卡片** - 实时显示总资产
- 📊 **资产分布饼图** - 各账户占比
- 📈 **资产曲线图** - 30天/90天/1年趋势
- 💼 **账户明细** - 各平台详细资产
- 🎯 **目标追踪** - 投资目标进度

## 🔐 隐私说明

- 所有数据存储在本地 SQLite 数据库
- 不上传到任何远程服务器
- 支持 `.gitignore` 排除 `data/wealth.db`

## 🛠️ 配置文件

复制 `config/config.example.json` 并修改：

```json
{
  "currency": {
    "primary": "CNY",
    "exchange_rate": {
      "USD_CNY": 7.0
    }
  },
  "accounts": [
    {
      "name": "微信",
      "type": "wallet",
      "currency": "CNY"
    },
    {
      "name": "支付宝",
      "type": "wallet",
      "currency": "CNY"
    }
  ]
}
```

## 📅 更新计划

- [ ] V1 - 基础资产汇总和展示（当前）
- [ ] V2 - Web API + 实时更新
- [ ] V3 - 自动同步币安/Yahoo Finance/IBKR API
- [ ] V4 - 投资分析和收益追踪
- [ ] V5 - Docker 部署和云端同步

## 🤝 贡献

欢迎提交 Issue 或 PR 来改进这个项目！

## 📝 License

MIT License

---

**💡 提示**：这是一个个人金融工具，建议定期备份 `data/wealth.db` 文件。
