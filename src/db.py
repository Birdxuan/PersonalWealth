"""数据库操作模块 - PersonalWealth"""

import sqlite3
import os
from datetime import datetime
from src.config import DB_PATH, DATE_FORMAT

class Database:
    """SQLite 数据库操作类"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_PATH
        self.ensure_dir()
    
    def ensure_dir(self):
        """确保数据库目录存在"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """初始化数据库，创建所有表"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # 账户表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    type TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 资产类型表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS asset_categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 资产持仓表（核心）
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS assets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account TEXT NOT NULL,
                    category TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    quantity REAL NOT NULL DEFAULT 0,
                    avg_cost REAL NOT NULL DEFAULT 0,
                    currency TEXT NOT NULL DEFAULT 'CNY',
                    updated_at TEXT,
                    UNIQUE(account, category, symbol)
                )
            ''')
            
            # 交易记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    category TEXT NOT NULL,
                    type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    price REAL NOT NULL,
                    fee REAL DEFAULT 0,
                    time TEXT NOT NULL
                )
            ''')
            
            # 每日资产快照表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_snapshot (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    total_cny REAL NOT NULL,
                    stock_cny REAL DEFAULT 0,
                    fund_cny REAL DEFAULT 0,
                    cash_cny REAL DEFAULT 0,
                    crypto_cny REAL DEFAULT 0,
                    date TEXT UNIQUE NOT NULL
                )
            ''')
            
            conn.commit()
            print("✅ 数据库初始化成功！")
            
        except sqlite3.Error as e:
            print(f"❌ 数据库初始化失败: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    # ========== 账户操作 ==========
    
    def add_account(self, name, type_):
        """添加账户"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO accounts (name, type) VALUES (?, ?)', (name, type_))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_accounts(self):
        """获取所有账户"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name, type FROM accounts ORDER BY name')
        return [dict(name=row[0], type=row[1]) for row in cursor.fetchall()]
    
    # ========== 资产类型操作 ==========
    
    def add_category(self, name):
        """添加资产类型"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO asset_categories (name) VALUES (?)', (name,))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_categories(self):
        """获取所有资产类型"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM asset_categories ORDER BY name')
        return [row[0] for row in cursor.fetchall()]
    
    # ========== 资产持仓操作 ==========
    
    def add_asset(self, account, category, symbol, quantity, avg_cost, currency='CNY'):
        """添加或更新资产"""
        conn = self.get_connection()
        cursor = conn.cursor()
        now = datetime.now().strftime(DATE_FORMAT)
        
        try:
            # 尝试更新
            cursor.execute('''
                UPDATE assets 
                SET quantity=?, avg_cost=?, updated_at=?
                WHERE account=? AND category=? AND symbol=?
            ''', (quantity, avg_cost, now, account, category, symbol))
            
            if cursor.rowcount == 0:
                # 如果没有更新任何行，则插入新行
                cursor.execute('''
                    INSERT INTO assets (account, category, symbol, quantity, avg_cost, currency, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (account, category, symbol, quantity, avg_cost, currency, now))
            
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"❌ 添加资产失败: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_assets(self, account=None):
        """获取资产列表"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if account:
            cursor.execute('''
                SELECT account, category, symbol, quantity, avg_cost, currency, updated_at
                FROM assets
                WHERE account=?
                ORDER BY account, category, symbol
            ''', (account,))
        else:
            cursor.execute('''
                SELECT account, category, symbol, quantity, avg_cost, currency, updated_at
                FROM assets
                ORDER BY account, category, symbol
            ''')
        
        result = []
        for row in cursor.fetchall():
            result.append({
                'account': row[0],
                'category': row[1],
                'symbol': row[2],
                'quantity': row[3],
                'avg_cost': row[4],
                'currency': row[5],
                'updated_at': row[6]
            })
        
        conn.close()
        return result
    
    def delete_asset(self, account, category, symbol):
        """删除资产"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                DELETE FROM assets
                WHERE account=? AND category=? AND symbol=?
            ''', (account, category, symbol))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"❌ 删除资产失败: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    # ========== 交易记录操作 ==========
    
    def add_transaction(self, account, symbol, category, type_, amount, price, fee=0, time=None):
        """添加交易记录"""
        conn = self.get_connection()
        cursor = conn.cursor()
        time = time or datetime.now().strftime(DATE_FORMAT)
        
        try:
            cursor.execute('''
                INSERT INTO transactions (account, symbol, category, type, amount, price, fee, time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (account, symbol, category, type_, amount, price, fee, time))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"❌ 添加交易记录失败: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_transactions(self, account=None, symbol=None):
        """获取交易记录"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT account, symbol, category, type, amount, price, fee, time FROM transactions'
        params = []
        
        if account or symbol:
            query += ' WHERE'
            if account:
                query += ' account=?'
                params.append(account)
            if symbol:
                if account:
                    query += ' AND'
                query += ' symbol=?'
                params.append(symbol)
        
        query += ' ORDER BY time DESC'
        
        cursor.execute(query, params)
        result = []
        for row in cursor.fetchall():
            result.append({
                'account': row[0],
                'symbol': row[1],
                'category': row[2],
                'type': row[3],
                'amount': row[4],
                'price': row[5],
                'fee': row[6],
                'time': row[7]
            })
        
        conn.close()
        return result
    
    # ========== 快照操作 ==========
    
    def add_snapshot(self, total_cny, stock_cny=0, fund_cny=0, cash_cny=0, crypto_cny=0, date=None):
        """添加每日快照"""
        conn = self.get_connection()
        cursor = conn.cursor()
        date = date or datetime.now().strftime('%Y-%m-%d')
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO daily_snapshot (total_cny, stock_cny, fund_cny, cash_cny, crypto_cny, date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (total_cny, stock_cny, fund_cny, cash_cny, crypto_cny, date))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"❌ 添加快照失败: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_snapshots(self, days=30):
        """获取最近 N 天的快照"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT date, total_cny, stock_cny, fund_cny, cash_cny, crypto_cny
            FROM daily_snapshot
            ORDER BY date DESC
            LIMIT {days}
        ''')
        
        result = []
        for row in cursor.fetchall():
            result.append({
                'date': row[0],
                'total_cny': row[1],
                'stock_cny': row[2],
                'fund_cny': row[3],
                'cash_cny': row[4],
                'crypto_cny': row[5]
            })
        
        conn.close()
        return sorted(result, key=lambda x: x['date'])  # 按日期升序排列
