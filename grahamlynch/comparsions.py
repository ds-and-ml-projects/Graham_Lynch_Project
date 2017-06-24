from .Database import add_new_col

def less_than_comparison(*args):
    stocks_db, conn, col_graham, col_cmpr, trshld_val, ttl_pts = args

    stocks_db.execute("SELECT STOCK, %s from Stock_STAT WHERE %s > ? " % (col_graham, col_cmpr), (trshld_val,))
    graham_total = stocks_db.fetchall()

    for graham_info in graham_total:
        ticker, look_for_graham_val = graham_info

        if isinstance(look_for_graham_val, float):
            updated_score = look_for_graham_val + ttl_pts
            add_new_col(stocks_db, conn, updated_score, ticker, col_graham)

        else:
            add_new_col(stocks_db, conn, ttl_pts, ticker, col_graham)

def greater_than_comparison(*args):
    stocks_db, conn, col_graham, col_cmpr, trshld_val, ttl_pts = args

    stocks_db.execute("SELECT STOCK, %s from Stock_STAT WHERE %s > ? " % (col_graham, col_cmpr), (trshld_val,))
    graham_total = stocks_db.fetchall()

    for graham_info in graham_total:
        ticker, look_for_graham_val = graham_info

        if isinstance(look_for_graham_val, float):
            updated_score = look_for_graham_val + ttl_pts
            add_new_col(stocks_db, conn, updated_score, ticker, col_graham)

        else:
            add_new_col(stocks_db, conn, ttl_pts, ticker, col_graham)
