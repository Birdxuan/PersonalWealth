"""Database operations for PersonalWealth"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from src.config import DB_PATH

class Database:
    """SQLite database operations"""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Connect to database"""
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    def execute(self, query: str, params: tuple = ()):
        """Execute SQL query"""
        if not self.cursor:
            self.connect()
        self.cursor.execute(query, params)
        self.connection.commit()
    
    def fetch_one(self, query: str, params: tuple = ()):
        """Fetch one result"""
        if not self.cursor:
            self.connect()
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def fetch_all(self, query: str, params: tuple = ()):
        """Fetch all results"""
        if not self.cursor:
            self.connect()
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    # Account operations
    def add_account(self, name: str, type: str, currency: str = 'CNY'):
        """Add new account"""
        query = 'INSERT INTO accounts (name, type, currency) VALUES (?, ?, ?)'
        self.execute(query, (name, type, currency))
    
    def get_accounts(self) -> List[Dict]:
        """Get all accounts"""
        query = 'SELECT id, name, type, currency FROM accounts'
        results = self.fetch_all(query)
        return [{
            'id': r[0],
            'name': r[1],
            'type': r[2],
            'currency': r[3]
        } for r in results]
    
    # Asset category operations
    def add_category(self, name: str):
        """Add asset category"""
        query = 'INSERT INTO asset_categories (name) VALUES (?)'
        self.execute(query, (name,))
    
    def get_categories(self) -> List[Dict]:
        """Get all categories"""
        query = 'SELECT id, name FROM asset_categories'
        results = self.fetch_all(query)
        return [{'id': r[0], 'name': r[1]} for r in results]
    
    # Asset operations
    def add_asset(self, account: str, category: str, symbol: str, 
                  quantity: float, avg_cost: float, currency: str = 'CNY'):
        """Add or update asset"""
        updated_time = datetime.now().isoformat()
        
        # Check if asset exists
        query = 'SELECT id FROM assets WHERE account = ? AND symbol = ?'
        existing = self.fetch_one(query, (account, symbol))
        
        if existing:
            # Update existing asset
            query = '''UPDATE assets 
                      SET category = ?, quantity = ?, avg_cost = ?, 
                          currency = ?, updated_time = ?
                      WHERE account = ? AND symbol = ?'''
            self.execute(query, (category, quantity, avg_cost, currency, 
                                updated_time, account, symbol))
        else:
            # Insert new asset
            query = '''INSERT INTO assets 
                      (account, category, symbol, quantity, avg_cost, currency, updated_time)
                      VALUES (?, ?, ?, ?, ?, ?, ?)'''
            self.execute(query, (account, category, symbol, quantity, 
                                avg_cost, currency, updated_time))
    
    def get_assets(self, account: str = None) -> List[Dict]:
        """Get assets, optionally filtered by account"""
        if account:
            query = '''SELECT id, account, category, symbol, quantity, avg_cost, 
                              currency, updated_time 
                       FROM assets WHERE account = ?'''
            results = self.fetch_all(query, (account,))
        else:
            query = '''SELECT id, account, category, symbol, quantity, avg_cost, 
                              currency, updated_time FROM assets'''
            results = self.fetch_all(query)
        
        return [{
            'id': r[0],
            'account': r[1],
            'category': r[2],
            'symbol': r[3],
            'quantity': r[4],
            'avg_cost': r[5],
            'currency': r[6],
            'updated_time': r[7]
        } for r in results]
    
    # Transaction operations
    def add_transaction(self, account: str, symbol: str, category: str,
                       type: str, amount: float, price: float, 
                       fee: float = 0, time: str = None):
        """Add transaction"""
        if not time:
            time = datetime.now().isoformat()
        
        query = '''INSERT INTO transactions 
                  (account, symbol, category, type, amount, price, fee, time)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        self.execute(query, (account, symbol, category, type, amount, price, fee, time))
    
    def get_transactions(self, account: str = None, symbol: str = None) -> List[Dict]:
        """Get transactions"""
        query = 'SELECT id, account, symbol, category, type, amount, price, fee, time FROM transactions WHERE 1=1'
        params = []
        
        if account:
            query += ' AND account = ?'
            params.append(account)
        if symbol:
            query += ' AND symbol = ?'
            params.append(symbol)
        
        query += ' ORDER BY time DESC'
        results = self.fetch_all(query, tuple(params))
        
        return [{
            'id': r[0],
            'account': r[1],
            'symbol': r[2],
            'category': r[3],
            'type': r[4],
            'amount': r[5],
            'price': r[6],
            'fee': r[7],
            'time': r[8]
        } for r in results]
    
    # Daily snapshot operations
    def add_snapshot(self, total_cny: float, stock_cny: float, 
                    fund_cny: float, cash_cny: float, crypto_cny: float,
                    date: str = None):
        """Add daily snapshot"""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        query = '''INSERT INTO daily_snapshot 
                  (total_cny, stock_cny, fund_cny, cash_cny, crypto_cny, date)
                  VALUES (?, ?, ?, ?, ?, ?)'''
        self.execute(query, (total_cny, stock_cny, fund_cny, cash_cny, crypto_cny, date))
    
    def get_snapshots(self, days: int = 30) -> List[Dict]:
        """Get recent snapshots"""
        query = '''SELECT id, total_cny, stock_cny, fund_cny, cash_cny, crypto_cny, date 
                   FROM daily_snapshot 
                   ORDER BY date DESC LIMIT ?'''
        results = self.fetch_all(query, (days,))
        
        return [{
            'id': r[0],
            'total_cny': r[1],
            'stock_cny': r[2],
            'fund_cny': r[3],
            'cash_cny': r[4],
            'crypto_cny': r[5],
            'date': r[6]
        } for r in reversed(results)]  # Reverse to get chronological order
