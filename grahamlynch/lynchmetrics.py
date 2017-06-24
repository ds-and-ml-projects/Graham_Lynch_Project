

def graham_stocks(self, *args):
    stocks_db, conn = args
    aggregate_pts = 9.0/3.0

    retrieve_graham("LynchScore", "PEGRatio", 1, ">", aggregate_pts)
    retrieve_graham("LynchScore", "DebtEquity", .3, ">", aggregate_pts)
    retrieve_graham("LynchScore", "EPSGrowth", .1, ">", aggregate_pts/2.0)
    retrieve_graham("LynchScore", "EPSGrowth", .25, ">", aggregate_pts/2.0)



retrieve_graham



class StockMethod(object):
    def __init__(self):
        self.GrahamStocks()
        self.LynchStocks()


    def GrahamStocks(self):
        aggregate_pts = 9.0/4.0
        self.CMPRSION("GrahamScore", "PE", 15, ">", aggregate_pts)
        self.CMPRSION("GrahamScore", "CurrentRatio", 1.5, "<", aggregate_pts)
        self.CMPRSION("GrahamScore", "BV", 1.5, ">", aggregate_pts)
        self.CMPRSION("GrahamScore", "DebtAsset", 1.15, ">", aggregate_pts)

    def LynchStocks(self, *args):
        aggregate_pts = 9.0/3.0
        self.CMPRSION("LynchScore", "PEGRatio", 1, ">", aggregate_pts)
        self.CMPRSION("LynchScore", "DebtEquity", .3, ">", aggregate_pts)
        self.CMPRSION("LynchScore", "EPSGrowth", .1, ">", aggregate_pts/2.0)
        self.CMPRSION("LynchScore", "EPSGrowth", .25, ">", aggregate_pts/2.0)

    def CMPRSION(*args):
        def cmpr_lssr(*args):
            c.execute("SELECT STOCK, %s, %s from Stock_STAT WHERE %s < ? " % (args[2], args[1], args[2]), (args[3],))
            for DB_List in c.fetchall():
                if isinstance(DB_List[2],float):
                    updated_score = DB_List[2] + args[5]
                    DB_Store = StockDATAbase(DB_List[0], updated_score, args[1]) # storing into the database indivdiually
                    DB_Store.IFEXIST()
                else:
                    score = args[5]
                    DB_Store = StockDATAbase(DB_List[0], score, args[1]) # storing into the database indivdiually
                    DB_Store.IFEXIST()

        def cmpr_grtr(*args):
            c.execute("SELECT STOCK, %s, %s from Stock_STAT WHERE %s > ? " % (args[2], args[1], args[2]), (args[3],))
            for DB_List in c.fetchall():
                if isinstance(DB_List[2],float):
                    updated_score = DB_List[2] + args[5]
                    DB_Store = StockDATAbase(DB_List[0], updated_score, args[1]) # storing into the database indivdiually
                    DB_Store.IFEXIST()
                else:
                    score = args[5]
                    DB_Store = StockDATAbase(DB_List[0], score, args[1]) # storing into the database indivdiually
                    DB_Store.IFEXIST()

        if args[4] == '<':
            cmpr_lssr(*args)
        elif args[4] == '>':
            cmpr_grtr(*args)
