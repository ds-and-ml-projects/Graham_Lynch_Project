



def GrahamStocks(self):
    aggregate_pts = 9.0/4.0
    self.CMPRSION("GrahamScore", "PE", 15, ">", aggregate_pts)
    self.CMPRSION("GrahamScore", "CurrentRatio", 1.5, "<", aggregate_pts)
    self.CMPRSION("GrahamScore", "BV", 1.5, ">", aggregate_pts)
    self.CMPRSION("GrahamScore", "DebtAsset", 1.15, ">", aggregate_pts)
