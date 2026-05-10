#!/usr/bin/env python3
"""Initialize the database with schema"""

import sqlite3
from src.config import DB_PATH, ACCOUNTS, ASSET_CATEGORIES
import os

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# Create accounts table
cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    type TEXT NOT NULL,
    currency TEXT DEFAULT 'CNY',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create asset_categories table
cursor.execute('''
CREATE TABLE IF NOT EXISTS asset_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create assets table (core holdings)
cursor.execute('''
CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account TEXT NOT NULL,
    category TEXT NOT NULL,
    symbol TEXT NOT NULL,
    quantity REAL NOT NULL,
    avg_cost REAL NOT NULL,
    currency TEXT DEFAULT 'CNY',
    updated_time TEXT,
    UNIQUE(account, symbol),
    FOREIGN KEY(account) REFERENCES accounts(name),
    FOREIGN KEY(category) REFERENCES asset_categories(name)
)
''')

# Create transactions table
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
    time TEXT,
    FOREIGN KEY(account) REFERENCES accounts(name)
)
''')

# Create daily_snapshot table (for trend analysis)
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

connection.commit()

# Insert default accounts
for account in ACCOUNTS:
    try:
        cursor.execute(
            'INSERT INTO accounts (name, type, currency) VALUES (?, ?, ?)',
            (account['name'], account['type'], account['currency'])
        )
    except sqlite3.IntegrityError:
        pass  # Account already exists

# Insert default categories
for category in ASSET_CATEGORIES:
    try:
        cursor.execute(
            'INSERT INTO asset_categories (name) VALUES (?)',
            (category,)
        )
    except sqlite3.IntegrityError:
        pass  # Category already exists

connection.commit()
connection.close()

print(f'✅ Database initialized at: {DB_PATH}')
