import sqlite3
import csv
import urllib2
import quandl
import warnings
import yahoo_finance
import operator
import math
from yahoo_finance import Share

from .Database import create_table
from .Database import check_for_metric
from .Database import insert_new_stock
from .Database import add_new_col
from .grahammetrics import specific_investing_calc

conn = sqlite3.connect('stocks.db') # creating a table for the key statistics
c = conn.cursor()

"""
ERROR CHECKS:
These are frequent error that occur with the database.
For example, sometimes there are no values or the values aren't numeric.
"""
yahoo_errors = (TypeError, urllib2.HTTPError, yahoo_finance.YQLResponseMalformedError)
quandl_errors = (TypeError, quandl.errors.quandl_error.NotFoundError, quandl.errors.quandl_error.QuandlError)


class StockInformation:

    def __init__(self):
        self.list_of_tick = self.get_all_tickers()
        self.create_database()
        self.calling_metric_func()
        self.graham_lynch_metrics()

    def get_all_tickers(self):

        with open('/Users/alexguanga/all_projects/grahamlynch/grahamlynch/companylist.csv', 'rb') as csvfile:
            file_of_tickers = csv.reader(csvfile, quotechar = '|')
            all_tickers = []

            for ticker_row in file_of_tickers:
                if ticker_row[3] != "n/a":
                    all_tickers.append([ticker_row[0]])

            '''
            if you would like for this program to run quicker, maybe choose a smaller amount of stocks to evaulate
            use this : amnt_stocks = len(key_statistic)
            '''
            return all_tickers

    '''
    These errors are frequent when either checking yahoo finance or the quandl database
    '''

    def create_database(self):
        self.conn, self.stock_DB = create_table()

    def calling_metric_func(self):
        self.marketshare()
        self.pe_ratio()
        self.bv_ratio()
        self.peg_ratio()
        self.current_ratio()
        self.debtasset_ratio()
        self.debtequity_ratio()
        #self.eps_growth_rate()
        self.market_cap()

    def using_quandl(self, value):
        warnings.simplefilter("ignore", category=RuntimeWarning)
        mean_values = value.values.mean()
        return mean_values

    def db_validate(self, *args):
        val, ticker, col_name = args

        database_search = check_for_metric(self.stock_DB, ticker)
        db_list_of_parameters = [self.stock_DB, self.conn, val, ticker, col_name] # INFO that will be used for database_search

        if not database_search:
            insert_new_stock(*db_list_of_parameters)
        if database_search:
            add_new_col(*db_list_of_parameters)

    def marketshare(self):
        for i in range(10): # CHANGE END VALUE WITH SELF.list_of_tickers
            try:
                ticker = self.list_of_tick[i][0]
                info_stock = Share(ticker)
                mktshare_val = float(info_stock.get_price())

                if isinstance(mktshare_val, float) == True:
                    self.db_validate(mktshare_val, ticker, "Share")

            except yahoo_errors:
                pass

    def pe_ratio(self):
        for i in range(10):
            try:
                ticker = self.list_of_tick[i][0]
                info_stock = Share(ticker)
                pe_val = float(info_stock.get_price_earnings_ratio())

                if isinstance(pe_val, float) == True:
                    self.db_validate(pe_val, ticker, "PE")

            except yahoo_errors:
                pass

    def bv_ratio(self):
        for i in range(10):
            try:
                ticker = self.list_of_tick[i][0]
                info_stock = Share(ticker)
                bv_val = float(info_stock.get_price_book())

                if isinstance(bv_val, float) == True:
                    self.db_validate(bv_val, ticker, "BV")

            except yahoo_errors:
                pass

    def peg_ratio(self):
        for i in range(10):
            try:
                ticker = self.list_of_tick[i][0]
                info_stock = Share(ticker)
                pegrowth_val = float(info_stock.get_price_earnings_growth_ratio())

                if isinstance(pegrowth_val, float) == True:
                    self.db_validate(pegrowth_val, ticker, "PEGRatio")

            except yahoo_errors:
                pass

    def current_ratio(self):
        for i in range (10):
            try:
                ticker = self.list_of_tick[i][0]
                crnt_val = quandl.get("SF0/"+str(ticker)+"_CURRENTRATIO_MRY", authtoken="ivu6KgaViZxoyqic7QkE")
                with warnings.catch_warnings():
                    cr_mean_val = self.using_quandl(crnt_val)

                    if (cr_mean_val != True):
                        self.db_validate(cr_mean_val, ticker, "CurrentRatio")

            except quandl_errors:
                pass

    def debtasset_ratio(self):
        for i in range(10):
            try:
                ticker = self.list_of_tick[i][0]
                currasset_val = quandl.get("SF0/"+str(ticker)+"_ASSETSC_MRY", authtoken="ivu6KgaViZxoyqic7QkE")
                ttldebt_val = quandl.get("SF0/"+str(ticker)+"_DEBT_MRY", authtoken="ivu6KgaViZxoyqic7QkE")

                with warnings.catch_warnings():
                    ca_mean_val = self.using_quandl(currasset_val) # Avg. of the current assets (approx. 5 years)
                    td_mean_val = self.using_quandl(ttldebt_val) # Avg. of the total debt (approx. 5 years)

                    # When values in QUANDL are n/a, they will output True when computing their mean...
                    if ((ca_mean_val != True) or (td_mean_val != True)):
                        debtasset_val = ca_mean_val/td_mean_val # the ratio of Total Debt to Current Asset Ratio. Hence, DA...
                        self.db_validate(debtasset_val, ticker, "DebtAsset")

            except quandl_errors:
                pass

    def debtequity_ratio(self):
        for i in range(10):
            try:
                ticker = self.list_of_tick[i][0]
                ttlequity_val = quandl.get("SF0/"+str(ticker)+"_EQUITY_MRY", authtoken="ivu6KgaViZxoyqic7QkE")
                ttldebt_val = quandl.get("SF0/"+str(ticker)+"_DEBT_MRY", authtoken="ivu6KgaViZxoyqic7QkE")

                with warnings.catch_warnings():
                    te_mean_val = self.using_quandl(ttlequity_val) # Avg. of the current assets (approx. 5 years)
                    td_mean_val = self.using_quandl(ttldebt_val) # Avg. of the total debt (approx. 5 years)

                    # When values in QUANDL are n/a, they will output True when computing their mean...
                    if ((td_mean_val != True) or (te_mean_val != True)):
                        debtequity_val = td_mean_val/te_mean_val # Ratio of Total Debt to Current Asset Ratio. Hence, DA...
                        self.db_validate(debtequity_val, ticker, "DebtEquity")

            except quandl_errors:
                pass

    def market_cap(self):
        mid_cap, large_cap = 2000000000, 10000000000
        for i in range(10):
            try:
                ticker = self.list_of_tick[i][0]
                info_stock = Share(ticker)
                illions_of_stock = info_stock.get_market_cap()[-1]
                mktcap_val = float(info_stock.get_market_cap()[:-1])

                if isinstance(mktcap_val, float) == True:
                    ttl_mktcap_val = self.mktcap_cnvrs(illions_of_stock, mktcap_val)

                    if ttl_mktcap_val > large_cap:
                        self.db_validate("Large-Market Cap", ticker, "MarketCap")

                    elif ttl_mktcap_val > mid_cap:
                        self.db_validate("Mid-Market Cap", ticker, "MarketCap")

                    else:
                        self.db_validate("Small-Market Cap", ticker, "MarketCap")

            except yahoo_errors:
                pass

    def eps_growth_rate(self):
        for i in range(10):
            try:
                ticker = self.list_of_tick[i][0]
                EPS = quandl.get("SF0/"+str(ticker)+"_EPS_MRY", authtoken="ivu6KgaViZxoyqic7QkE")

                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)

                    for j in range((len(EPS.values)-1), -1, -1):
                        if (EPS.values[j] > 0):
                            current_year = EPS.values[j]
                            print current_year
                            break

                    for k in range(len(EPS.values)):
                        if (EPS.values[k] > 0):
                            last_avail_yr = EPS.values[k]
                            print last_avail_yr
                            break

                    for num in (num for num,x in enumerate(EPS.values) if x == current_year):
                        pos_current_yr = num
                    for num in ( num for num,x in enumerate(EPS.values) if x == last_avail_yr):
                        pos_last_yr = num
                    ttl_yrs = (pos_current_yr - pos_last_yr) + 1
                    eps_growth_diff = current_year/last_avail_yr
                    yrs_exponent = (1/float(ttl_yrs))
                    eps_growth_growth = round(((eps_growth_diff ** yrs_exponent)-1)*100, 2)

                    '''if eps_growth_growth != 0:
                        DB_Store = StockDATAbase(self.key_statistic[i][0], eps_growth_growth, "EPSGrowth") # storing into the database indivdiually
                        DB_Store.IFEXIST()'''

            except quandl_errors:
                pass

    def mktcap_cnvrs(self, mult, mkt_cap):
        if mult == 'M':
            return int(mkt_cap * 1000000)
        elif mult == 'B':
            return int(mkt_cap * 1000000000)

    def graham_lynch_metrics(self):
        specific_investing_calc(self.conn, self.stock_DB)





StockInformation()
