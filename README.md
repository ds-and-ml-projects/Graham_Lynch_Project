# Graham-Lynch Stock Interface
***

This repository performs three functionalities.

Using *Yahoo Finance*, I query over 3000 stock into Python's library, SQLite. Also, it calculates the risk tolerance of the user. Lastly, it finds stocks that fit below the threshold of the user's riskiness.

## Table of Contents
1. [Installation][Install]
2. [Functionality][Functionality]



# Installation
***
```
git clone https://github.com/alexguanga/Graham_Lynch_Project.git
cd grahamlynch/
python -m grahamlynch.userinterface.__init__
```

# Functionality
***
### Interface
The interface asks a some questions. These questions are generated from typical risk tolerance questionaries. After answering these questions, you'll be scored a __Risk Tolerance score__.  

The code can be located doing the following:
```
cd grahamlynch/grahamlynch/userinterface
atom gui_for_stock.py
```

### Database
The code to the database can be located using the following commands, if you're in the grahamlynch folder
```
cd grahamlynch/grahamlynch/
atom Database.py
```
In the interface, you will be given the option to **Retrieve** the information. If selected, you will restore the stock database. To query over 3000 stocks, across different features, this will take approximately an hour.

**Database Columns**
- STOCK
- Share
- STOCK
- PE REAL
- BV REAL
- DebtAsset
- DebtEquity
- EPSGrowth
- CurrentRatio
- PEGRatio
- MarketCap
- GrahamScore
- LynchScore

# Calculation
***
### Benjamin Graham and Peter Lynch
A lot of the investment information derived from these gentleman. Besides their contributions to investing, they have their unique way of viewing risk. I suggest reading _The Intelligent Investor by Benjamin Graham_ and _Beating the Street by Peter Lynch_.

The code can be located doing the following:
```
cd grahamlynch/grahamlynch
atom Storing_Stock_Statistics.py
```



[Install]: #Installation
[Functionality]: #Functionality
