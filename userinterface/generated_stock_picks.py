import sqlite3

def key_ratios(*args):
    col_name, ttl_score = args

    sqlite_file = '/Users/alexguanga/all_projects/grahamlynch/stocks.db'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    c.execute("SELECT STOCK FROM Stock_STAT WHERE %s < ? " % (col_name), (ttl_score,))
    return (c.fetchall())

    c.close()
    conn.close()
