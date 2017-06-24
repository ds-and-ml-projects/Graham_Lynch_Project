import sqlite3

def create_table():
    conn = sqlite3.connect('stocks.db') # creating a table for the key statistics
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Stock_STAT
            (STOCK TEXT PRIMARY KEY,
             Share REAL,
             PE REAL,
             BV REAL,
             DebtAsset REAL,
             DebtEquity REAL,
             EPSGrowth REAL,
             CurrentRatio REAL,
             PEGRatio REAL,
             MarketCap TEXT,
             GrahamScore REAL,
             LynchScore REAL)''')
    conn.commit()
    return (conn, c)

def check_for_metric(*args):
    stock_db, p_key = args
    info_on_stock = stock_db.execute("SELECT STOCK FROM Stock_STAT WHERE STOCK = ? ", (p_key,))
    atleast_one_value = info_on_stock.fetchone()

    if atleast_one_value:
        return True
    if not atleast_one_value:
        return False

def insert_new_stock(*args):
    stock_db, conn, val, p_key, colm = args
    stock_db.execute("INSERT INTO STOCK_STAT(STOCK, %s) VALUES(?, ?)" % (colm), (p_key, val,))
    conn.commit()

def add_new_col(*args):
    stock_db, conn, val, p_key, colm = args
    stock_db.execute("UPDATE STOCK_STAT SET %s = ? WHERE STOCK = ?" %(colm), (val, p_key,))
    conn.commit()
