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
#
# Stock Robot
#
################################################################################
import sys
from datetime import datetime

# Apache will not let you set the lib from an imported library.
# So, this *assumes* that it can import all other libraries from the same directory.
import stockAccount as StockAccount

ROBOT_VALUE_NONE 	= 0
ROBOT_VALUE_RSI 	= 1
ROBOT_VALUE_DATE        = 2

RELATION_EQUAL 		= 0
RELATION_LESS_THAN 	= 1
RELATION_LESS_THAN_EQUAL = 2
RELATION_GREATER_THAN 	= 3
RELATION_GREATER_THAN_EQUAL = 4



################################################################################
#
# class CStockRobot
#
################################################################################
class CStockRobot(object):
    #####################################################
    # Constructor - This method is part of any class
    #####################################################
    def __init__(self):
        self.m_LogStrList = []
    # End -  __init__


    #####################################################
    # [CStockRobot::
    # Destructor - This method is part of any class
    #####################################################
    def __del__(self):
        return
    # End of destructor


    #####################################################
    # [CStockRobotRule::ProcessNewPrice]
    #####################################################
    def ProcessNewPrice(self, stockTicker, account, year, month, day, openPrice, lowPrice, highPrice, closePrice, volume, rsi):
        return
    # End - ProcessNewPrice


    #####################################################
    # [CStockRobotRule::WriteToXML]
    #####################################################
    def WriteToXML(self):
        xmlStr = ""
        return xmlStr   
    # End - WriteToXML


    #####################################################
    # [CStockRobotRule::ReadFromXML]
    #####################################################
    def ReadFromXML(self, xmlStr):
        fValid = True

        return fValid   
    # End - ReadFromXML
# End - CStockRobot






################################################################################
#
# class CStockRobotBuyAndHold
#
################################################################################
class CStockRobotBuyAndHold(CStockRobot):
    #####################################################
    # Constructor - This method is part of any class
    #####################################################
    def __init__(self):
        super().__init__()
        self.InCash = True
    # End -  __init__


    #####################################################
    # [CStockRobotBuyAndHold::
    # Destructor - This method is part of any class
    #####################################################
    def __del__(self):
        super().__del__()
    # End of destructor



    #####################################################
    # [CStockRobotBuyAndHold::ProcessNewPrice]
    #####################################################
    def ProcessNewPrice(self, stockTicker, account, year, month, day, openPrice, lowPrice, highPrice, closePrice, volume, rsi):
        fDebug = False

        if (fDebug):
            print("CStockRobotBuyAndHold::ProcessNewPrice")
            print("     year=" + str(year) + ", month=" + str(month) + ", day=" + str(day))
            print("     closePrice=" + str(closePrice) + ", openPrice=" + str(openPrice))
            print("     lowPrice=" + str(lowPrice) + ", highPrice=" + str(highPrice) + ", volume=" + str(volume) + ", rsi=" + str(rsi))
            print("     self.DatesToBeInCash=" + str(self.DatesToBeInCash))

        if (self.InCash):
            if (fDebug):
                print("CStockRobotSkipDays::ProcessNewPrice Call account.BuyStock")
            account.BuyStock(stockTicker, StockAccount.TRADE_TYPE_ALL, closePrice, -1)
            self.InCash = False
        # End - elif (self.InCash):
    # End - ProcessNewPrice

# End - CStockRobotBuyAndHold






################################################################################
#
# class CStockRobotSkipDays
#
################################################################################
class CStockRobotSkipDays(CStockRobot):
    #####################################################
    # Constructor - This method is part of any class
    #####################################################
    def __init__(self):
        super().__init__()

        self.InCash = True
        self.DaysUntilBuyIn = 0

        self.DatesToBeInCash = []
        self.NumDatesToBeInCash = 0
    # End -  __init__


    #####################################################
    # [CStockRobot::
    # Destructor - This method is part of any class
    #####################################################
    def __del__(self):
        super().__del__()
    # End of destructor


    #####################################################
    # [CStockRobotSkipDays::SetDatesForCash]
    #####################################################
    def SetDatesForCash(self, numDates, dateList):
        self.DatesToBeInCash = dateList
        self.NumDatesToBeInCash = numDates
    # End - SetDatesForCash



    #####################################################
    # [CStockRobotSkipDays::ProcessNewPrice]
    #####################################################
    def ProcessNewPrice(self, stockTicker, account, year, month, day, openPrice, lowPrice, highPrice, closePrice, volume, rsi):
        fDebug = False
        fSellEverything = False

        if (fDebug):
            print("CStockRobotSkipDays::ProcessNewPrice")
            print("     year=" + str(year) + ", month=" + str(month) + ", day=" + str(day))
            print("     closePrice=" + str(closePrice) + ", openPrice=" + str(openPrice))
            print("     lowPrice=" + str(lowPrice) + ", highPrice=" + str(highPrice) + ", volume=" + str(volume) + ", rsi=" + str(rsi))
            print("     self.DatesToBeInCash=" + str(self.DatesToBeInCash))

        for index in range(self.NumDatesToBeInCash):
            currentDate = self.DatesToBeInCash[index]
            if (fDebug):
                print("CStockRobotSkipDays::ProcessNewPrice. currentDate=" + str(currentDate))
            if ((year == currentDate['y']) and (month == currentDate['m']) and (day == currentDate['d'])):
                fSellEverything = True
                break
        # for index in range(self.NumDatesToBeInCash):

        if (fDebug):
            print("CStockRobotSkipDays::ProcessNewPrice fSellEverything=" + str(fSellEverything))

        if (fSellEverything):
            account.SellStock(stockTicker, StockAccount.TRADE_TYPE_ALL, closePrice, -1)
            self.DaysUntilBuyIn = 1
            self.InCash = True
        elif (self.InCash):
            self.DaysUntilBuyIn = self.DaysUntilBuyIn - 1
            if (fDebug):
                print("CStockRobotSkipDays::ProcessNewPrice self.DaysUntilBuyIn=" + str(self.DaysUntilBuyIn))

            if (self.DaysUntilBuyIn <= 0):
                if (fDebug):
                    print("CStockRobotSkipDays::ProcessNewPrice self.Call account.BuyStock")
                account.BuyStock(stockTicker, StockAccount.TRADE_TYPE_ALL, closePrice, -1)
                self.InCash = False
                self.DaysUntilBuyIn = 0
            # End - if (self.DaysUntilBuyIn <= 0):
        # End - elif (self.InCash):
    # End - ProcessNewPrice

# End - CStockRobotSkipDays







################################################################################
#
# class CStockRobotValueThreshold
#
################################################################################
class CStockRobotValueThreshold(CStockRobot):
    #####################################################
    # Constructor - This method is part of any class
    #####################################################
    def __init__(self):
        super().__init__()

        self.BuyStockValueType = ROBOT_VALUE_NONE
        self.BuyStockRelation = 0
        self.BuyStockThreshold = 0

        self.SellStockValueType = ROBOT_VALUE_NONE
        self.SellStockRelation = 0
        self.SellStockThreshold = 0
    # End -  __init__


    #####################################################
    # [CStockRobotValueThreshold::
    # Destructor - This method is part of any class
    #####################################################
    def __del__(self):
        super().__del__()
    # End of destructor


    #####################################################
    # [CStockRobotValueThreshold::SetTradingParams]
    #####################################################
    def SetTradingParams(self, buyStockValueType, buyStockRelation, buyStockThreshold, sellStockValueType, sellStockRelation, sellStockThreshold):
        self.BuyStockValueType = buyStockValueType
        self.BuyStockRelation = buyStockRelation
        self.BuyStockThreshold = buyStockThreshold

        self.SellStockValueType = sellStockValueType
        self.SellStockRelation = sellStockRelation
        self.SellStockThreshold = sellStockThreshold
    # End - SetTradingParams



    #####################################################
    # [CStockRobotValueThreshold::ProcessNewPrice]
    #####################################################
    def ProcessNewPrice(self, stockTicker, account, year, month, day, openPrice, lowPrice, highPrice, closePrice, volume, rsi):
        fDebug = False
        fExecuteBuy = False
        fExecuteSell = False
        indicatorValue = 0

        if (fDebug):
            print("CStockRobotValueThreshold::ProcessNewPrice")
            print("     year=" + str(year) + ", month=" + str(month) + ", day=" + str(day))
            print("     closePrice=" + str(closePrice) + ", openPrice=" + str(openPrice))
            print("     lowPrice=" + str(lowPrice) + ", highPrice=" + str(highPrice) + ", volume=" + str(volume) + ", rsi=" + str(rsi))

        ######################################################
        if (self.BuyStockValueType != ROBOT_VALUE_NONE):
            indicatorValue = 0
            if (self.BuyStockValueType == ROBOT_VALUE_RSI):
                indicatorValue = rsi
            elif (self.BuyStockValueType == ROBOT_VALUE_DATE):
                indicatorValue = day

            if ((self.BuyStockRelation == RELATION_EQUAL) and (indicatorValue == self.BuyStockThreshold)):
                fExecuteBuy = True
            elif ((self.BuyStockRelation == RELATION_LESS_THAN) and (indicatorValue < self.BuyStockThreshold)):
                fExecuteBuy = True
            elif ((self.BuyStockRelation == RELATION_LESS_THAN_EQUAL) and (indicatorValue <= self.BuyStockThreshold)):
                fExecuteBuy = True
            elif ((self.BuyStockRelation == RELATION_GREATER_THAN) and (indicatorValue > self.BuyStockThreshold)):
                fExecuteBuy = True
            elif ((self.BuyStockRelation == RELATION_GREATER_THAN_EQUAL) and (indicatorValue >= self.BuyStockThreshold)):
                fExecuteBuy = True

            # Only buy at the end of the month
            if ((self.BuyStockValueType == ROBOT_VALUE_DATE) and (indicatorValue < 15)):
                fExecuteBuy = False

            if (fDebug):
                print("CStockRobotValueThreshold::ProcessNewPrice. Consider buying. indicatorValue=" + str(indicatorValue))
                print("     self.BuyStockRelation=" + str(self.BuyStockRelation) + ", fExecuteBuy=" + str(fExecuteBuy))
        # End - if (self.BuyStockValueType != ROBOT_VALUE_NONE)



        ######################################################
        if ((not fExecuteBuy) and (self.SellStockValueType != ROBOT_VALUE_NONE)):
            indicatorValue = 0
            if (self.SellStockValueType == ROBOT_VALUE_RSI):
                indicatorValue = rsi
            elif (self.BuyStockValueType == ROBOT_VALUE_DATE):
                indicatorValue = day

            if ((self.SellStockRelation == RELATION_EQUAL) and (indicatorValue == self.SellStockThreshold)):
                fExecuteSell = True
            elif ((self.SellStockRelation == RELATION_LESS_THAN) and (indicatorValue < self.SellStockThreshold)):
                fExecuteSell = True
            elif ((self.SellStockRelation == RELATION_LESS_THAN_EQUAL) and (indicatorValue <= self.SellStockThreshold)):
                fExecuteSell = True
            elif ((self.SellStockRelation == RELATION_GREATER_THAN) and (indicatorValue > self.SellStockThreshold)):
                fExecuteSell = True
            elif ((self.SellStockRelation == RELATION_GREATER_THAN_EQUAL) and (indicatorValue >= self.SellStockThreshold)):
                fExecuteSell = True

            # Only sell at the beginning of the month
            if ((self.BuyStockValueType == ROBOT_VALUE_DATE) and (indicatorValue >= 15)):
                fExecuteSell = False

            if (fDebug):
                print("CStockRobotValueThreshold::ProcessNewPrice. Consider Selling. indicatorValue=" + str(indicatorValue))
                print("     self.SellStockRelation=" + str(self.SellStockRelation) + ", fExecuteSell=" + str(fExecuteSell))
        # End - if (self.SellStockValueType != ROBOT_VALUE_NONE)


        if (fExecuteBuy):
            account.BuyStock(stockTicker, StockAccount.TRADE_TYPE_ALL, closePrice, -1)
        elif (fExecuteSell):
            account.SellStock(stockTicker, StockAccount.TRADE_TYPE_ALL, closePrice, -1)
    # End - ProcessNewPrice

# End - CStockRobotValueThreshold





################################################################################
# 
# PUBLIC PROCEDURES
# 
################################################################################


################################################################################
#
# [MakeSkipDatesRobot]
#
################################################################################
def MakeSkipDatesRobot(numExtremePriceDays, priceList, extremePriceDays, extremePricePrevDays):
    newRobot = CStockRobotSkipDays()
    newRobot.SetDatesForCash(numExtremePriceDays, extremePricePrevDays)
    return newRobot
# End - MakeSkipDatesRobot()




################################################################################
#
# [MakeThresholdRobot]
#
################################################################################
def MakeThresholdRobot(buyStockValueType, buyStockRelation, buyStockThreshold, sellStockValueType, sellStockRelation, sellStockThreshold):
    newRobot = CStockRobotValueThreshold()
    newRobot.SetTradingParams(buyStockValueType, buyStockRelation, buyStockThreshold, sellStockValueType, sellStockRelation, sellStockThreshold)

    return newRobot
# End - MakeThresholdRobot()

