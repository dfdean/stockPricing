#!/usr/bin/python3
################################################################################
# 
# Copyright (c) 2024 Dawson Dean
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
################################################################################
# Ideas to Explore
#
# Strategies
# - Miss 10 best or worst days
# - Buy when RSI is +, sell when negative
# - Dollar-cost average buy
# 
# - If daily drop is >= 50% of one of the 10 biggest drops in past 5 years, then sell.
#   Buy after the first day it is positive
#
# Daily cron job to download price info and load it into a file. 
#    Then, the CGI just reads it from the file
# Apache + mod_wsgi
#
# - Dependency graphs
#       A link is either a producer or consumer relationship or else a covariance
#       Time order the graphs, based on relative dates of earnings announcements or lags in effects
# So, event happens in node x, and what will be the downstream effects.
#
# 1. Backmarket simulation of different strategies
#   Skip N best and worst days
#   Dollar cost averaging over different tapers
#
# 2. Simulate a market with N ai's trading against each other
#
################################################################################
import sys
from datetime import datetime

# Apache will not let you set the lib from an imported library.
# So, this *assumes* that it can import all other libraries from the same directory.
import stockTicker as StockTicker

TRADE_TYPE_ALL      = 0
TRADE_TYPE_DOLLARS  = 1




################################################################################
#
# class CStockAccount
#
################################################################################
class CStockAccount(object):
    #####################################################
    # Constructor - This method is part of any class
    #####################################################
    def __init__(self, initialCash):
        self.TotalAccountValue = initialCash
        self.CashTotal = initialCash
        self.StockHoldings = {}

        self.m_DailyTotalValueList = []
    # End -  __init__


    #####################################################
    # [CStockAccount::
    # Destructor - This method is part of any class
    #####################################################
    def __del__(self):
        return
    # End of destructor


    #####################################################
    # [CStockAccount::GetAccountValue]
    #####################################################
    def GetAccountValue(self):
        return(self.TotalAccountValue)


    #####################################################
    # [CStockAccount::GetDailyValueList]
    #####################################################
    def GetDailyValueList(self):
        return(self.m_DailyTotalValueList)


    #####################################################
    # [CStockAccount::StartRun]
    #####################################################
    def StartRun(self):
        return   
    # End - StartRun


    #####################################################
    # [CStockAccount::FinishRun]
    #####################################################
    def FinishRun(self):
        return   
    # End - FinishRun


    #####################################################
    # [CStockAccount::FinishDay]
    #####################################################
    def FinishDay(self, stockTicker, year, month, day, closePrice):
        fDebug = False

        self.TotalAccountValue = self.CashTotal
        if (fDebug):
           print("FinishDay. Start with cash. self.TotalAccountValue=" + str(self.TotalAccountValue))

        for index, (tickerName, stockHolding) in enumerate(self.StockHoldings.items()):
            if (fDebug):
                print("FinishDay. tickerName=" + str(tickerName) + ", stockHolding['numShares']=" + str(stockHolding['numShares']))

            if (tickerName == stockTicker.GetStockSymbol()):
                stockValue = stockHolding['numShares'] * closePrice
                self.TotalAccountValue += stockValue
                if (fDebug):
                    print("FinishDay. stockValue=" + str(stockValue) + ", self.TotalAccountValue=" + str(self.TotalAccountValue))
         # End - for index, (tickerName, stockHolding) in enumerate(self.StockHoldings.items()):

        self.m_DailyTotalValueList.append(self.TotalAccountValue)
    # End - FinishDay





    #####################################################
    # [CStockAccount::BuyStock]
    #####################################################
    def BuyStock(self, stockTicker, tradeType, pricePerShare, amount):
        fDebug = False

        stockHolding = self.GetStockHolding(stockTicker, True)
        if (fDebug):
           print("BuyStock. stockTicker=" + str(stockTicker.GetStockSymbol()) + ", stockHolding=" + str(stockHolding))
        if (stockHolding is None):
            return

        if (tradeType == TRADE_TYPE_ALL):
            numSharesToTrade = self.CashTotal / pricePerShare
        elif (tradeType == TRADE_TYPE_DOLLARS):
            amount = min(amount, self.CashTotal)
            numSharesToTrade = amount / pricePerShare
        else:
            return

        if (fDebug):
            print("BuyStock. numSharesToTrade=" + str(numSharesToTrade) + ", pricePerShare=" + str(pricePerShare))

        tradeValue = numSharesToTrade * pricePerShare
        stockHolding['numShares'] = stockHolding['numShares'] + numSharesToTrade
        self.CashTotal = self.CashTotal - tradeValue

        if (fDebug):
            print("BuyStock. tradeValue=" + str(tradeValue) + ", self.CashTotal=" + str(self.CashTotal))
            print("     stockHolding=" + str(stockHolding))
    # End - BuyStock





    #####################################################
    # [CStockAccount::SellStock]
    #####################################################
    def SellStock(self, stockTicker, tradeType, pricePerShare, totalAmount):
        fDebug = False

        if (fDebug):
            print("SellStock. stockTicker=" + str(stockTicker) + ", totalAmount=" + str(totalAmount))

        stockHolding = self.GetStockHolding(stockTicker, False)
        if (stockHolding is None):
            return

        if (tradeType == TRADE_TYPE_ALL):
            numSharesToTrade = stockHolding['numShares']
        elif (tradeType == TRADE_TYPE_DOLLARS):
            numSharesToTrade = amount / pricePerShare
        else:
            return

        if (fDebug):
            print("SellStock. numSharesToTrade=" + str(numSharesToTrade) + ", pricePerShare=" + str(pricePerShare))

        tradeValue = numSharesToTrade * pricePerShare
        stockHolding['numShares'] = stockHolding['numShares'] - numSharesToTrade
        self.CashTotal += tradeValue
        if (fDebug):
            print("SellStock. tradeValue=" + str(tradeValue) + ", self.CashTotal=" + str(self.CashTotal))
            print("     stockHolding=" + str(stockHolding))
            print("     self.CashTotal=" + str(self.CashTotal))
    # End - SellStock





    #####################################################
    # [CStockAccount::ReadFromXML]
    #####################################################
    def ReadFromXML(self, xmlStr):
        fValid = True
        return fValid   
    # End - ReadFromXML



    #####################################################
    #
    #####################################################
    def GetStockHolding(self, stockTicker, fAddIfMissing):
        fDebug = False
        stockHolding = None

        tickerName = stockTicker.GetStockSymbol()
        #tickerName = tickerName.lower()

        if (tickerName in self.StockHoldings):
            stockHolding = self.StockHoldings[tickerName]

        if ((stockHolding is None) and (fAddIfMissing)):
            stockHolding = { 't': stockTicker, 'numShares': 0}
            self.StockHoldings[tickerName] = stockHolding

        return stockHolding
    # End - GetStockHolding


# End - CStockAccount






################################################################################
#
# [MakeTradingAccount]
#
################################################################################
def MakeTradingAccount(initialValueDollars):
    newAccount = CStockAccount(initialValueDollars)

    return newAccount
# End - MakeTradingAccount()



