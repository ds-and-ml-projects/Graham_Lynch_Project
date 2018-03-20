import sqlite3

class StockDATAbase(object):

    def __init__(self, P_KEY, VALUE, clmn_title):
        self.P_KEY = P_KEY
        self.VALUE = VALUE
        self.clmn_title = clmn_title

    def CREATE_TABLE(self):
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

    def IFEXIST(self):
        check_exists = c.execute("SELECT STOCK FROM Stock_STAT WHERE STOCK = ? ", (self.P_KEY,))
        CHECK_REAL = check_exists.fetchone()
        if not CHECK_REAL:
            self.INSERT_TABLE()
        if CHECK_REAL:
            self.UPDATE()

    def INSERT_TABLE(self):
        c.execute("INSERT INTO STOCK_STAT(STOCK, %s) VALUES(?, ?)" % (self.clmn_title), (self.P_KEY, self.VALUE,))
        conn.commit()

    def UPDATE(self):
        c.execute("UPDATE STOCK_STAT SET %s = ? WHERE STOCK = ?" %(self.clmn_title), (self.VALUE, self.P_KEY,))
        conn.commit()

    @classmethod
    def CLOSE(self):
        c.close()
        conn.close()
