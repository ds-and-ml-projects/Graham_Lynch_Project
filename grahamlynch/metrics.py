from .comparsions import less_than_comparison
from .comparsions import greater_than_comparison

def specific_investing_calc(*args):
    conn, stocks_db = args
    total_graham_pts = 9.0/4.0
    total_lynch_pts = 9.0/3.0

    less_or_greater(stocks_db, conn, "GrahamScore", "PE", 15, ">", total_graham_pts)
    less_or_greater(stocks_db, conn, "GrahamScore", "CurrentRatio", 1.5, "<", total_graham_pts)
    less_or_greater(stocks_db, conn, "GrahamScore", "BV", 1.5, ">", total_graham_pts)
    less_or_greater(stocks_db, conn, "GrahamScore", "DebtAsset", 1.15, ">", total_graham_pts)

    less_or_greater(stocks_db, conn, "LynchScore", "PEGRatio", 1, ">", total_lynch_pts)
    less_or_greater(stocks_db, conn, "LynchScore", "DebtEquity", .3, ">", total_lynch_pts)
    less_or_greater(stocks_db, conn, "LynchScore", "EPSGrowth", .1, ">", total_lynch_pts)
    less_or_greater(stocks_db, conn, "LynchScore", "EPSGrowth", .25, ">", total_lynch_pts)

def less_or_greater(*args):
    '''
    KEY defintions:

    col_of_investor:
        It's either Graham or Lynch's column in the database
    col_cmpr:
        This is one of the metrics that these investors believe have an impact on investing
    trshld_val:
        The point where these investors felt that anything below that number is risk-averse, anything above is risky
    sign_cmpr:
        Because these value mean different under differnt circumstance, we need to specify if they think a greater than or less than is riskier
    ttl_pts:
        The total score of the respective investor (a higher number means that its more risker, hence, it's more fitting for
        riskier investors who have a higher risk tolerance)
    '''

    stock_db, conn, col_of_investor, col_cmpr, trshld_val, sign_cmpr, ttl_pts = args
    cmrp_parameters = [stock_db, conn, col_of_investor, col_cmpr, trshld_val, ttl_pts]

    if sign_cmpr == '<':
        less_than_comparison(*cmrp_parameters)

    elif sign_cmpr == '>':
        greater_than_comparison(*cmrp_parameters)
