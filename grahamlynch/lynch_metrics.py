

def LynchStocks(self, *args):
    aggregate_pts = 9.0/3.0
    self.CMPRSION("LynchScore", "PEGRatio", 1, ">", aggregate_pts)
    self.CMPRSION("LynchScore", "DebtEquity", .3, ">", aggregate_pts)
    self.CMPRSION("LynchScore", "EPSGrowth", .1, ">", aggregate_pts/2.0)
    self.CMPRSION("LynchScore", "EPSGrowth", .25, ">", aggregate_pts/2.0)
