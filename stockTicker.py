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
# Yahoo
# https://pypi.org/project/yfinance/
#
# Google Finance
# https://pypi.org/project/googlefinance/
#
# NASDAQ Data
# https://docs.data.nasdaq.com/docs/python
# https://docs.data.nasdaq.com/docs/python-tables
#
################################################################################
import sys
from datetime import datetime

#import statistics
#from scipy import stats
#from scipy.stats import spearmanr
#import numpy as np

STAT_SCORE_CORRELATION_WITH_PRICE_T1 = "corrPriceT1"
STAT_SCORE_CORRELATION_WITH_PRICE_T4 = "corrPriceT4"

SP500_TICKER = '^GSPC'
GOLDEN_DRAGON_TICKER = '^HXC'

YAHOO_FINANCE = "yahoo"

# OpCodes for GetExtremes
EXTREMES_MAX_PRICES = "maxPrices"
EXTREMES_MIN_PRICES = "minPrices"
EXTREMES_MAX_PRICE_CHANGES = "maxPriceChanges"
EXTREMES_MAX_PRICE_INCREASES = "maxPriceIncreases"
EXTREMES_MAX_PRICE_DECLINES = "maxPriceDeclines"

# OpCodes for CompareDates
DATE_COMPARE_GREATER_THAN_EQUAL = 1

DEFAULT_RSI_NUM_DATA = 15



g_DaysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
################################################################################
# 
# [GetDateForNumDaysOffset]
#
# Note, g_DaysInMonth is 0-based, while the date strings use months that are 1-based.
################################################################################
def GetDateForNumDaysOffset(startYear, startMonth, startDay, deltaDays):
    fDebug = False
    newYear = startYear
    newMonth = startMonth
    newDay = startDay

    if (fDebug):
        print("GetDateForNumDaysOffset. deltaDays=" + str(deltaDays))
        print("     startYear=" + str(startYear) + ", startMonth=" + str(startMonth) + ", startDay=" + str(startDay))
        print("     newYear=" + str(newYear) + ", newMonth=" + str(newMonth) + ", newDay=" + str(newDay))

    # Back up years
    while (deltaDays >= 365):
        # 1900 was NOT a leap year but 2000 was a leap year
        fIsStartDateLeapYear = False
        if (((newYear - 1900) % 4) == 0):
            if ((newMonth > 2) or ((newMonth == 2) and (newDay == 29))):
                fIsStartDateLeapYear = True

        newYear = newYear - 1
        deltaDays = deltaDays - 365
        if (fIsStartDateLeapYear):
            fIsStartDateLeapYear = False
            deltaDays = deltaDays - 1
    # End - while (deltaDays >= 365):

    # Decide if we end up on a leap year.
    # 1900 was NOT a leap year but 2000 was a leap year
    fInLeapYear = (((newYear - 1900) % 4) == 0)

    if (fDebug):
        print("GetDateForNumDaysOffset. Subtracted years. deltaDays=" + str(deltaDays))
        print("     newYear=" + str(newYear) + ", newMonth=" + str(newMonth) + ", newDay=" + str(newDay))

    # Back up months
    if ((fInLeapYear) and (newMonth == 2)):
        numDaysInMonth = 29
    else:
        numDaysInMonth = g_DaysInMonth[newMonth - 1]
    while (deltaDays >= numDaysInMonth):
        deltaDays = deltaDays - numDaysInMonth

        newMonth = newMonth - 1
        if (newMonth <= 0):
            newMonth = 12
            newYear = newYear - 1
            fInLeapYear = (((newYear - 1900) % 4) == 0)

        # Do this for the next iteration
        if ((fInLeapYear) and (newMonth == 2)):
            numDaysInMonth = 29
        else:
            numDaysInMonth = g_DaysInMonth[newMonth - 1]
    # End  - while (deltaDays >= 30):

    if (fDebug):
        print("GetDateForNumDaysOffset. Subtracted months. deltaDays=" + str(deltaDays))
        print("     newYear=" + str(newYear) + ", newMonth=" + str(newMonth) + ", newDay=" + str(newDay))

    # Back up days   
    newDay = newDay - deltaDays
    while (newDay <= 0):
        newMonth = newMonth - 1
        if (newMonth <= 0):
            newMonth = 12
            newYear = newYear - 1
            fInLeapYear = (((newYear - 1900) % 4) == 0)

        if ((fInLeapYear) and (newMonth == 2)):
            numDaysInMonth = 29
        else:
            numDaysInMonth = g_DaysInMonth[newMonth - 1]

        # Add, since we are adding a negtaive number
        newDay = numDaysInMonth + newDay   
    # End - while (newDay < 0):

    if (fDebug):
        print("GetDateForNumDaysOffset. Subtracted days. deltaDays=" + str(deltaDays))
        print("     newYear=" + str(newYear) + ", newMonth=" + str(newMonth) + ", newDay=" + str(newDay))

    return newYear, newMonth, newDay
# End - GetDateForNumDaysOffset




################################################################################
# 
# [CompareDates]
#
# Note, g_DaysInMonth is 0-based, while the date strings use months that are 1-based.
################################################################################
def CompareDates(opCode, year1, month1, day1, year2, month2, day2):
    ######################################
    if (opCode == DATE_COMPARE_GREATER_THAN_EQUAL):
        if (year1 > year2):
            return True
        elif (year1 < year2):
            return False
        else:  # (year1 == year2)
            if (month1 > month2):
                return True
            elif (month1 < month2):
                return False
            else:  # (month1 == month2)
                if (day1 >= day2):
                    return True
                else:
                    return False
    else:
        print("ERROR! CompareDates given an Invalid opCode: " + str(opCode))
        return False
# End - CompareDates






################################################################################
#
# class CStockTicker
#
# This is the runtime for a single stock
################################################################################
class CStockTicker(object):
    #####################################################
    # Constructor - This method is part of any class
    #####################################################
    def __init__(self, tickerSymbol):
        self.tickerSymbol = tickerSymbol
        self.CompanyName = tickerSymbol

        # Iterator
        self.IteratorIndex = 0

        # Current price action for today
        self.CurrentPrice = 0
        self.PrevClose = 0
        self.TodayOpenPrice = 0
        self.TodayLowPrice = 0
        self.TodayHighPrice = 0
        self.Bid = 0
        self.Ask = 0
        self.volume = 0

        # Averages from today
        self.TrailingPE = 0
        self.ForwardPE = 0
        self.FiftyTwoWeekLow = 0
        self.FiftyTwoWeekHigh = 0
        self.FiftyDayAverage = 0
        self.TwoHundredDayAverage = 0
        self.avgVolume = 0
        self.PEGRatio = 0

        # Derived values for today
        self.m_RSI = 0
        self.EMA12 = 0
        self.EMA26 = 0
        self.MACD = 0
        self.BiggestRecentDropPercent = 0
        self.kStochastic = 0
        self.dStochastic = 0

        # Various confidence values for the stats
        self.m_RSICovariances = {}
        self.EMA12Covariances = {}
        self.EMA26Covariances = {}
        self.MACDCovariances = {}
        self.BiggestRecentDropPercentCovariances = {}
        self.kStochasticCovariances = {}
        self.dStochasticScores = {}

        # Past Values
        self.OptionDates = 0
        self.PastPriceList = []
    # End -  __init__


    #####################################################
    # [CStockTicker::
    # Destructor - This method is part of any class
    #####################################################
    def __del__(self):
        return
    # End of destructor



    ##########################################################################################################
    #
    # GET
    #
    ##########################################################################################################


    #####################################################
    # [CStockTicker::GetStockSymbol]
    #####################################################
    def GetStockSymbol(self):
        return self.tickerSymbol

    #####################################################
    # [CStockTicker::GetCompanyName]
    #####################################################
    def GetCompanyName(self):
        return self.CompanyName

    #####################################################
    # [CStockTicker::GetCurrentPrice]
    #####################################################
    def GetCurrentPrice(self):
        return self.CurrentPrice

    #####################################################
    # [CStockTicker::GetCurrentBid]
    #####################################################
    def GetCurrentBid(self):
        return self.Bid

    #####################################################
    # [CStockTicker::GetCurrentAsk]
    #####################################################
    def GetCurrentAsk(self):
        return self.Ask

    #####################################################
    # [CStockTicker::GetBidAskSpread]
    #####################################################
    def GetBidAskSpread(self):
        spread = round((self.Bid - self.Ask), 2)
        spreadPercent = round(((spread / self.CurrentPrice) * 100.0), 2)
        return spread, spreadPercent

    #####################################################
    # [CStockTicker::GetPEGRatio
    #####################################################
    def GetPEGRatio(self):
        return self.PEGRatio

    #####################################################
    # [CStockTicker::GetRSI]
    #####################################################
    def GetRSI(self):
        return round(self.m_RSI, 2), round(self.m_RSICovariances[STAT_SCORE_CORRELATION_WITH_PRICE_T1], 2), round(self.m_RSICovariances[STAT_SCORE_CORRELATION_WITH_PRICE_T4], 2)

    #####################################################
    # [CStockTicker::GetStockEMA]
    #####################################################
    def GetEMA(self):
        return round(self.EMA26, 2)

    #####################################################
    # [CStockTicker::GetBiggestRecentDropPercent]
    #####################################################
    def GetBiggestRecentDropPercent(self):
        return round(self.BiggestRecentDropPercent, 2), round(self.BiggestRecentDropPercentCovariances[STAT_SCORE_CORRELATION_WITH_PRICE_T1], 2), round(self.BiggestRecentDropPercentCovariances[STAT_SCORE_CORRELATION_WITH_PRICE_T4], 2)

    #####################################################
    # [CStockTicker::GetKStochastic]
    #####################################################
    def GetKStochastic(self):
        return round(self.kStochastic, 2), round(self.kStochasticCovariances[STAT_SCORE_CORRELATION_WITH_PRICE_T1], 2), round(self.kStochasticCovariances[STAT_SCORE_CORRELATION_WITH_PRICE_T4], 2)


    #####################################################
    # [CStockTicker::GetDStochastic]
    #####################################################
    def GetDStochastic(self):
        return round(self.dStochastic, 2)

    #####################################################
    # [CStockTicker::GetMACD]
    #####################################################
    def GetMACD(self):
        return round(self.MACD, 2), round(self.MACDCovariances[STAT_SCORE_CORRELATION_WITH_PRICE_T1], 2), round(self.MACDCovariances[STAT_SCORE_CORRELATION_WITH_PRICE_T4], 2)


    #####################################################
    # [CStockTicker::GetPrevDayChange]
    #####################################################
    def GetPrevDayChange(self):
        fDebug = False
        percentChange = 0
        absChange = 0

        newestPriceIndex = len(self.PastPriceList) - 1
        secondNewestPriceIndex = newestPriceIndex - 1
        newestPriceInfo = self.PastPriceList[newestPriceIndex]
        newestClosePrice = newestPriceInfo['Cl']
        secondNewestPriceInfo = self.PastPriceList[secondNewestPriceIndex]
        secondNewestClosePrice = secondNewestPriceInfo['Cl']

        absChange = round((newestClosePrice - secondNewestClosePrice), 2)
        percentChange = round(((absChange / secondNewestClosePrice) * 100.0), 2)

        if (fDebug):
            print("GetPrevDayChange")
            print("   self.CurrentPrice = " + str(self.CurrentPrice))
            print("   newestPriceInfo = " + str(newestPriceInfo))
            print("   secondNewestPriceInfo = " + str(secondNewestPriceInfo))
            print("   newestClosePrice = " + str(newestClosePrice))
            print("   secondNewestClosePrice = " + str(secondNewestClosePrice))
            print("   absChange = " + str(absChange))
            print("   percentChange = " + str(percentChange))
            sys.exit(0)

        return percentChange, absChange
    # End - GetPrevDayChange



    #####################################################
    # [CStockTicker::GetLatestDate]
    #####################################################
    def GetLatestDate(self):
        fDebug = False
        newestPriceIndex = len(self.PastPriceList) - 1
        newestPriceInfo = self.PastPriceList[newestPriceIndex]

        return newestPriceInfo['y'], newestPriceInfo['m'], newestPriceInfo['d']
    # End - GetLatestDate





    ##########################################################################################################
    #
    # SET
    #
    ##########################################################################################################

    #####################################################
    # [CStockTicker::SetOptionDates
    #####################################################
    def SetOptionDates(self, value):
        self.OptionDates = value

    #####################################################
    # [CStockTicker::SetCompanyName
    #####################################################
    def SetCompanyName(self, value):
        self.CompanyName = value

    #####################################################
    # [CStockTicker::SetCurrentPrice
    #####################################################
    def SetCurrentPrice(self, value):
        self.CurrentPrice = value

    #####################################################
    # [CStockTicker::SetPrevClose
    #####################################################
    def SetPrevClose(self, value):
        self.PrevClose = value

    #####################################################
    # [CStockTicker::SetTodayOpenPrice
    #####################################################
    def SetTodayOpenPrice(self, value):
        self.TodayOpenPrice = value

    #####################################################
    # [CStockTicker::SetTodayLowPrice
    #####################################################
    def SetTodayLowPrice(self, value):
        self.TodayLowPrice = value

    #####################################################
    # [CStockTicker::SetTodayHighPrice
    #####################################################
    def SetTodayHighPrice(self, value):
        self.TodayHighPrice = value

    #####################################################
    # [CStockTicker::SetTrailingPE
    #####################################################
    def SetTrailingPE(self, value):
        self.TrailingPE = value

    #####################################################
    # [CStockTicker::SetForwardPE
    #####################################################
    def SetForwardPE(self, value):
        self.ForwardPE = value

    #####################################################
    # [CStockTicker::SetBid
    #####################################################
    def SetBid(self, value):
        self.Bid = value

    #####################################################
    # [CStockTicker::SetAsk
    #####################################################
    def SetAsk(self, value):
        self.Ask = value

    #####################################################
    # [CStockTicker::SetFiftyTwoWeekLow
    #####################################################
    def SetFiftyTwoWeekLow (self, value):
        self.FiftyTwoWeekLow = value

    #####################################################
    # [CStockTicker::SetFiftyTwoWeekHigh
    #####################################################
    def SetFiftyTwoWeekHigh(self, value):
        self.FiftyTwoWeekHigh = value

    #####################################################
    # [CStockTicker::SetFiftyDayAverage
    #####################################################
    def SetFiftyDayAverage (self, value):
        self.FiftyDayAverage = value

    #####################################################
    # [CStockTicker::SetTwoHundredDayAverage
    #####################################################
    def SetTwoHundredDayAverage(self, value):
        self.TwoHundredDayAverage = value

    #####################################################
    # [CStockTicker::SetVolume
    #####################################################
    def SetVolume(self, value):
        self.volume = value

    #####################################################
    # [CStockTicker::SetAvgVolume
    #####################################################
    def SetAvgVolume(self, value):
        self.avgVolume = value

    #####################################################
    # [CStockTicker::SetPEGRatio
    #####################################################
    def SetPEGRatio(self, value):
        self.PEGRatio = value

    #####################################################
    # [CStockTicker::SetPastValues
    #####################################################
    def SetPastValues(self, year, month, day, openPrice, closePrice, volume, highPrice, lowPrice, rsi, ema12, ema26, macd, kStochastic, dStochastic, biggestPriceDrop):
        newQueueEntry = {'y': year, 'm': month, 'd': day,
                        'Cl': closePrice, 'Op': openPrice, 'Hi': highPrice, 'Lo': lowPrice, 'Vo': volume,
                        'RSI': rsi, 'EMA12': ema12, 'EMA26': ema26, 'MACD': macd, 'KStochastic': kStochastic,
                        'BiggestRecentDropPercent': biggestPriceDrop }
        self.PastPriceList.append(newQueueEntry)
    # End - SetPastValues





    ##########################################################################################################
    #
    # Calculate Stats
    #
    ##########################################################################################################

    #####################################################
    # [CStockTicker::ComputeAllStats]
    #####################################################
    def ComputeAllStats(self):
        fDebug = False

        if (fDebug):
            print("ComputeAllStats")

        # Compute the current stats for the latest pric information
        self.m_RSI = self.ComputeRSI(0, DEFAULT_RSI_NUM_DATA)
        self.EMA12 = self.GetExponentialMovingAverage(0, 12)
        self.EMA26 = self.GetExponentialMovingAverage(0, 26)
        self.MACD = self.EMA12 - self.EMA26
        self.kStochastic, self.dStochastic = self.GetStochastic(0)
        self.BiggestRecentDropPercent = self.ComputeBiggestRecentDrop(0, 7)

        # Compute the stats for each historical day
        newestPriceIndex = len(self.PastPriceList) - 1
        numPastPrices = len(self.PastPriceList)
        for index in range(numPastPrices):
            #print("ComputeAllStats - index=" + str(index))
            currentPriceInfo = self.PastPriceList[newestPriceIndex]

            currentPriceInfo['RSI'] = self.ComputeRSI(index, DEFAULT_RSI_NUM_DATA)
            currentPriceInfo['EMA12'] = self.GetExponentialMovingAverage(index, 12)
            currentPriceInfo['EMA26'] = self.GetExponentialMovingAverage(index, 26)
            currentPriceInfo['MACD'] = currentPriceInfo['EMA12'] - currentPriceInfo['EMA26']
            currentPriceInfo['KStochastic'], currentPriceInfo['DStochastic'] = self.GetStochastic(index)
            currentPriceInfo['BiggestRecentDropPercent'] = self.ComputeBiggestRecentDrop(index, 7)

            newestPriceIndex = newestPriceIndex - 1
        # End - for index in range(numPastPrices):

        # Now, compute the covariance for each stat, which correlates the list of stats with 
        # a synchronized list of future prices
        self.m_RSICovariances = self.ComputeCovarianceForOneStat('RSI')
        self.EMA12Covariances = self.ComputeCovarianceForOneStat('EMA12')
        self.EMA26Covariances = self.ComputeCovarianceForOneStat('EMA26')
        self.MACDCovariances = self.ComputeCovarianceForOneStat('MACD')
        self.kStochasticCovariances = self.ComputeCovarianceForOneStat('KStochastic')
        self.BiggestRecentDropPercentCovariances = self.ComputeCovarianceForOneStat('BiggestRecentDropPercent')
    # End - ComputeAllStats(self)






    #####################################################
    # [CStockTicker::ComputeCovarianceForOneStat]
    #####################################################
    def ComputeCovarianceForOneStat(self, statName):
        fDebug = False
        newestPriceIndex = len(self.PastPriceList) - 1

        # Compute the covariance for each value
        statList, futurePriceList = self.GetSynchronizedStatAndFuturePriceLists(statName, newestPriceIndex, 1)
        nextDayCorrelation, _ = spearmanr(statList, futurePriceList)

        # Compute the covariance for each value
        statList, futurePriceList = self.GetSynchronizedStatAndFuturePriceLists(statName, newestPriceIndex, 4)
        futureDayCorrelation, _ = spearmanr(statList, futurePriceList)

        scoresDict = { STAT_SCORE_CORRELATION_WITH_PRICE_T1: nextDayCorrelation, 
                        STAT_SCORE_CORRELATION_WITH_PRICE_T4: futureDayCorrelation }

        if (fDebug):
            print("ComputeCovarianceForOneStat. " + statName + ": ")
            print("     nextDayCorrelation=" + str(nextDayCorrelation))
            print("     futureDayCorrelation=" + str(futureDayCorrelation))
            print("     Dict=" + str(scoresDict))

        return scoresDict
    # End - ComputeCovarianceForOneStat(self)




    #####################################################
    #
    # [CStockTicker::GetPastPrices]
    #
    # The oldest price is index 0, and the latest price is at index numPrices-1
    #####################################################
    def GetPastPrices(self, startingFromNDaysBeforeNow, numPrices):
        fDebug = False
        if (fDebug):
            print("GetPastPrices. startingFromNDaysBeforeNow=" + str(startingFromNDaysBeforeNow) + ", numPrices=" + str(numPrices))
 
        maxAvailPrices = len(self.PastPriceList) - abs(startingFromNDaysBeforeNow)
        # Subtract 1 because the indexes are 0-based
        newestPriceIndex = maxAvailPrices - 1
        # Add 1 because the oldest index is a valid result values.
        oldestPriceIndex = (newestPriceIndex - numPrices) + 1
        oldestPriceIndex = max(0, oldestPriceIndex)
        # Add 1 because we include both the oldest and newest indexes as result values.
        numPrices = newestPriceIndex - oldestPriceIndex

        if (fDebug):
            print("GetPastPrices. List length=" + str(len(self.PastPriceList)))
            print("GetPastPrices. maxAvailPrices=" + str(maxAvailPrices))
            print("GetPastPrices. newestPriceIndex=" + str(newestPriceIndex))
            print("GetPastPrices. oldestPriceIndex=" + str(oldestPriceIndex))
            print("GetPastPrices. numPrices=" + str(numPrices))

        resultList = [0] * numPrices
        lastDestIndex = numPrices - 1
        for index in range(numPrices):
            resultList[lastDestIndex - index] = self.PastPriceList[newestPriceIndex - index]['Cl']
            if (fDebug):
                print("Copy from " + str(newestPriceIndex - index) + " to " + str(lastDestIndex - index) + ": " + str(resultList[lastDestIndex - index]))
        # End - for index in range(numPrices):

        if (fDebug):
            print("GetPastPrices. resultList=" + str(resultList))
            print("GetPastPrices. self.PastPriceList=" + str(self.PastPriceList))

        return resultList
    # End - GetPastPrices()





    #####################################################
    #
    # [CStockTicker::GetSynchronizedStatAndFuturePriceLists]
    #
    # The oldest price is index 0, and the latest price is at index numPrices-1
    #####################################################
    def GetSynchronizedStatAndFuturePriceLists(self, markerName, startOffset, daysInFuturePrice):
        fDebug = False
        statList = []
        futurePriceList = []
        if (fDebug):
            print("GetSynchronizedStatAndFuturePriceLists. markerName=" + str(markerName))
            print("     startOffset=" + str(startOffset))
            print("     daysInFuturePrice=" + str(daysInFuturePrice))
 
        maxAvailPrices = len(self.PastPriceList) - abs(daysInFuturePrice)
        if (fDebug):
            print("GetPastPrices. List length=" + str(len(self.PastPriceList)))
            print("GetPastPrices. maxAvailPrices=" + str(maxAvailPrices))

        for index in range(maxAvailPrices):
            currentPriceInfo = self.PastPriceList[index]
            if (markerName not in currentPriceInfo):
                continue
            currentMarker = currentPriceInfo[markerName]

            futurePriceInfo = self.PastPriceList[index + daysInFuturePrice]
            if ('Cl' not in futurePriceInfo):
                continue
            futurePrice = futurePriceInfo['Cl']

            if (fDebug):
                print("Iteration. index = " + str(index))
                print("     index + daysInFuturePrice = " + str(index + daysInFuturePrice))
                print("     len(self.PastPriceList) = " + str(len(self.PastPriceList)))
                print("     len(currentMarker) = " + str(currentMarker))
                print("     len(futurePrice) = " + str(futurePrice))

            statList.append(currentMarker)
            futurePriceList.append(futurePrice)
        # End - for index in range(maxAvailPrices):

        if (fDebug):
            #print("GetSynchronizedStatAndFuturePriceLists. self.PastPriceList=" + str(self.PastPriceList))
            print("GetSynchronizedStatAndFuturePriceLists. statList=" + str(statList))
            print("GetSynchronizedStatAndFuturePriceLists. futurePriceList=" + str(futurePriceList))

        return statList, futurePriceList
    # End - GetSynchronizedStatAndFuturePriceLists()







    #####################################################
    #
    # [CStockTicker::GetExponentialMovingAverage]
    #
    # References:
    # https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/32f868169964ba3cf5015de880cf2172_MIT18_S096F13_lecnote9.pdf
    # https://www.cs.cornell.edu/courses/cs4787/2020sp/lectures/Lecture9.pdf
    #
    # The oldest price is index 0, and the latest price is at index numPrices-1
    #####################################################
    def GetExponentialMovingAverage(self, startingFromNDaysBeforeNow, numPrices):
        fDebug = False
        if (fDebug):
            print("GetExponentialMovingAverage. numPrices=" + str(numPrices))

        pastPriceList = self.GetPastPrices(startingFromNDaysBeforeNow, numPrices)
        numActualPrices = len(pastPriceList)
        if (fDebug):
            print("     pastPriceList = " + str(pastPriceList))
        if (numActualPrices == 0):
            return 0

        # Traverse the list from the oldest (index 0) to the newest (index length-1)
        indexList = list(range(1, numActualPrices))
        currentEMA = pastPriceList[0]
        if (fDebug):
            print("GetExponentialMovingAverage. Before loop, currentEMA = " + str(currentEMA))
            print("GetExponentialMovingAverage. indexList = " + str(indexList))
        sequenceLength = 1
        for index in indexList:
            currentAlpha = 2.0 / (float(sequenceLength) + 1.0)
            if (fDebug):
                print("sequenceLength = " + str(sequenceLength))
                print("    index = " + str(index))
                print("    currentAlpha = " + str(currentAlpha))
                print("    currentEMA = " + str(currentEMA))

            currentPrice = pastPriceList[index]
            currentEMA = (currentAlpha * currentPrice) + ((1 - currentAlpha) * currentEMA)
            if (fDebug):
                print("    currentPrice = " + str(currentPrice) + ", New currentEMA = " + str(currentEMA))

            sequenceLength += 1
        # End - for valueLength in range(sequenceLength - 1):

        if (fDebug):
            print("GetExponentialMovingAverage. currentEMA=" + str(currentEMA))

        return currentEMA
    # End of GetExponentialMovingAverage






    #####################################################
    # [CStockTicker::ComputeRSI]
    #
    # References:
    # https://www.thestreet.com/dictionary/relative-strength-index-rsi
    #####################################################
    def ComputeRSI(self, startingFromNDaysBeforeNow, numPrices):
        fDebug = False
        if (fDebug):
            print("ComputeRSI. numPrices=" + str(numPrices))

        pastPriceList = self.GetPastPrices(startingFromNDaysBeforeNow, numPrices)
        if (fDebug):
            print("    pastPriceList = " + str(pastPriceList))

        numPriceChanges = len(pastPriceList) - 1
        percentChangeList = [0] * numPriceChanges
        percentGainList = [0] * numPriceChanges
        percentLossList = [0] * numPriceChanges
        for index in range(1, numPriceChanges + 1):
            oldVal = pastPriceList[index - 1]
            newVal = pastPriceList[index]
            deltaVal = newVal - oldVal
            percentChange = float(deltaVal / oldVal) * 100.0
            percentChangeList[index - 1] = percentChange
            if (fDebug):
                print("index = " + str(index) + ", percentChange = " + str(percentChange))
        # End - for index in range(numPriceChanges):

        if (fDebug):
            print("ComputeRSI. percentChangeList=" + str(percentChangeList))

        for index in range(numPriceChanges):
            percentChange = percentChangeList[index]
            if (percentChange > 0):
                percentGainList[index] = percentChange
            else:
                percentLossList[index] = -percentChange
        # End - for index in range(numPriceChanges):

        if (fDebug):
            print("ComputeRSI. percentGainList=" + str(percentGainList))
            print("ComputeRSI. percentLossList=" + str(percentLossList))

        if (numPriceChanges > 0):
            avgPercentGain = sum(percentGainList) / numPriceChanges
            avgPercentLoss = sum(percentLossList) / numPriceChanges
        else:
            avgPercentGain = 0
            avgPercentLoss = 0
        if (fDebug):
            print("ComputeRSI. avgPercentGain=" + str(avgPercentGain))
            print("ComputeRSI. avgPercentLoss=" + str(avgPercentLoss))

        if (avgPercentLoss == 0):
            relativeStrength = 0.0
        else:
            relativeStrength = avgPercentGain / avgPercentLoss
        relativeStrengthIndex = 100.0 - (100.0 / (1.0 + relativeStrength))
        if (fDebug):
            print("ComputeRSI. relativeStrength=" + str(relativeStrength))
            print("ComputeRSI. relativeStrengthIndex=" + str(relativeStrengthIndex))

        return relativeStrengthIndex
    # End of ComputeRSI




    #####################################################
    # [CStockTicker::GetStochastic]
    # The oldest price is index 0, and the latest price is at index numPrices-1
    #####################################################
    def GetStochastic(self, startingFromNDaysBeforeNow):
        fDebug = False
 
        maxAvailPrices = len(self.PastPriceList) - abs(startingFromNDaysBeforeNow)
        newestPriceIndex = (len(self.PastPriceList) - 1) - startingFromNDaysBeforeNow
        lowestPriceIn14Days = -1
        highestPriceIn14Days = -1
        lowestPriceIn3Days = -1
        highestPriceIn3Days = -1
        latestClosingPrice = self.PastPriceList[newestPriceIndex]['Cl']

        ##################################
        # Get the highest and lowest price in the past 14 trading days
        oldestPriceIndex = newestPriceIndex - 13
        oldestPriceIndex = max(0, oldestPriceIndex)
        numPrices = (newestPriceIndex - oldestPriceIndex) + 1
        if (fDebug):
            print("GetStochastic. maxAvailPrices=" + str(maxAvailPrices))
            print("    newestPriceIndex=" + str(newestPriceIndex))
            print("    oldestPriceIndex=" + str(oldestPriceIndex))
            print("    numPrices=" + str(numPrices))
        for index in range(numPrices):
            if (fDebug):
                print("GetStochastic. Current=" + str(self.PastPriceList[newestPriceIndex - index]))

            closingPrice = self.PastPriceList[newestPriceIndex - index]['Cl']
            if ((lowestPriceIn14Days < 0) or (closingPrice < lowestPriceIn14Days)):
                lowestPriceIn14Days = closingPrice
            if ((highestPriceIn14Days < 0) or (closingPrice > highestPriceIn14Days)):
                highestPriceIn14Days = closingPrice
        # End - for index in range(numPrices):

        if (fDebug):
            print("GetStochastic. lowestPriceIn14Days=" + str(lowestPriceIn14Days) + ", highestPriceIn14Days=" + str(highestPriceIn14Days))


        ##################################
        # Get the highest and lowest price in the past 3 trading days
        oldestPriceIndex = newestPriceIndex - 2
        oldestPriceIndex = max(0, oldestPriceIndex)
        numPrices = (newestPriceIndex - oldestPriceIndex) + 1
        for index in range(numPrices):
            if (fDebug):
                print("GetStochastic. Current=" + str(self.PastPriceList[newestPriceIndex - index]))

            closingPrice = self.PastPriceList[newestPriceIndex - index]['Cl']
            if ((lowestPriceIn3Days < 0) or (closingPrice < lowestPriceIn3Days)):
                lowestPriceIn3Days = closingPrice
            if ((highestPriceIn3Days < 0) or (closingPrice > highestPriceIn3Days)):
                highestPriceIn3Days = closingPrice
        # End - for index in range(numPrices):

        if (fDebug):
            print("GetStochastic. lowestPriceIn3Days=" + str(lowestPriceIn3Days) + ", highestPriceIn3Days=" + str(highestPriceIn3Days))

        ##################################
        # 
        # K is the closing price as a percent of the recent price range
        # It ranges between 0 and 100. 
        # K over 80 is overbought, a bearish indicator
        # K below 20 is oversold, a bullish indicator
        denom = highestPriceIn14Days - lowestPriceIn14Days
        if (denom <= 0):
            kVal = 0.0
        else:
            kVal = 100.0 * (float(latestClosingPrice - lowestPriceIn14Days) / float(denom))

        if (lowestPriceIn3Days <= 0):
            dVal = 0.0
        else:
            dVal = 100.0 * (float(highestPriceIn3Days) / float(lowestPriceIn3Days))
        if (fDebug):
            print("GetStochastic. kVal=" + str(kVal) + ", dVal=" + str(dVal))

        return kVal, dVal
    # End - GetStochastic()






    #####################################################
    #
    # [CStockTicker::ComputeBiggestRecentDrop]
    #
    #####################################################
    def ComputeBiggestRecentDrop(self, startingFromNDaysBeforeNow, numPrices):
        fDebug = False
        if (fDebug):
            print("ComputeBiggestRecentDrop. numPrices=" + str(numPrices))

        pastPriceList = self.GetPastPrices(startingFromNDaysBeforeNow, numPrices)
        numActualPrices = len(pastPriceList)
        if (fDebug):
            print("ComputeBiggestRecentDrop. pastPriceList = " + str(pastPriceList))
            print("ComputeBiggestRecentDrop. numActualPrices = " + str(numActualPrices))
        if (numActualPrices == 0):
            return 0

        newestPriceIndex = (len(self.PastPriceList) - 1) - startingFromNDaysBeforeNow
        latestClosingPrice = self.PastPriceList[newestPriceIndex]['Cl']
        highestPastPrice = max(pastPriceList)
        if (fDebug):
            print("ComputeBiggestRecentDrop. highestPastPrice=" + str(highestPastPrice))

        if (highestPastPrice > latestClosingPrice):
            bigestPriceDrop = float(highestPastPrice - latestClosingPrice)
            bigestPriceDropPercent = -1 * float(bigestPriceDrop / highestPastPrice) * 100.0
        else:
            bigestPriceDrop = 0


        if (fDebug):
            print("ComputeBiggestRecentDrop. bigestPriceDrop = " + str(bigestPriceDrop))

        return bigestPriceDrop
    # End of ComputeBiggestRecentDrop







    ##########################################################################################################
    #
    # Covariance
    #
    ##########################################################################################################


    #####################################################
    # 
    # [GetCovarianceWithPredictedStockTicker]
    # 
    # ValueNames:
    # 'Cl': closePrice
    # 'Op': openPrice
    # 'Hi': highPrice
    # 'Lo': lowPrice
    # 'Vo': volume
    #
    # Percent rise --> rise
    # Average Multiplier
    #####################################################
    def GetCovarianceWithPredictedStockTicker(self, predictedStockTicker, daysOffsetInPredictedStock):
        fDebug = False
        myValueList = []
        otherValueList = []
        myDeltaValueList = []
        otherDeltaValueList = []
        valueName = "Cl"
        if (fDebug):
            print("GetCovarianceWithPredictedStockTicker. valueName=" + str(valueName) + ", daysOffsetInPredictedStock=" + str(daysOffsetInPredictedStock))

        myMaxAvailPrices = len(self.PastPriceList)
        otherMaxAvailPrices = len(predictedStockTicker.PastPriceList)
        mostRecentOtherIndex = 0
        myPrevValue = -1
        otherPrevValue = -1
        numRisesInMyStock = 0
        numRisesInpredictedStockTickerWhenMyStockRises = 0
        totalRiseInMyStock = 0
        totalRiseInpredictedStockTicker = 0
        for index in range(myMaxAvailPrices):
            myEntry = self.PastPriceList[index]

            foundOtherEntry = False
            otherIndex = mostRecentOtherIndex
            while (otherIndex < otherMaxAvailPrices):
                otherEntry = predictedStockTicker.PastPriceList[otherIndex]
                if ((myEntry['y'] == otherEntry['y']) and (myEntry['m'] == otherEntry['m']) and (myEntry['d'] == otherEntry['d'])):
                    foundOtherEntry = True
                    mostRecentOtherIndex = otherIndex + 1
                    break
                otherIndex += 1
            # End - while (otherIndex < otherMaxAvailPrices):

            if (not foundOtherEntry):
                break

            if (daysOffsetInPredictedStock != 0):
                otherIndex = otherIndex + daysOffsetInPredictedStock
                if ((otherIndex >= 0) and (otherIndex < otherMaxAvailPrices)):
                    otherEntry = predictedStockTicker.PastPriceList[otherIndex]
                else:
                    #print("Error. Could not find another entry (2)")
                    break
            # End - while (otherIndex < otherMaxAvailPrices):
                
            if (fDebug):
                print("Found another entry")
                print("     myEntry=" + str(myEntry))
                print("     otherEntry=" + str(otherEntry))


            myCurrentValue = myEntry[valueName]
            otherCurrentValue = otherEntry[valueName]
            myValueList.append(myCurrentValue)
            otherValueList.append(otherCurrentValue)
            if ((myPrevValue > 0) and (otherPrevValue > 0)):
                myDelta = myCurrentValue - myPrevValue
                otherDelta = otherCurrentValue - otherPrevValue

                myDeltaValueList.append(myDelta)
                otherDeltaValueList.append(otherDelta)

                if (myDelta > 0):
                    numRisesInMyStock += 1
                    if (otherDelta > 0):
                        numRisesInpredictedStockTickerWhenMyStockRises += 1
                        totalRiseInMyStock += myDelta
                        totalRiseInpredictedStockTicker += otherDelta
                # End - if (myDelta > 0):
            # End - if ((myPrevValue > 0) and (otherPrevValue > 0)):

            myPrevValue = myCurrentValue
            otherPrevValue = otherCurrentValue
        # End - for index in range(myMaxAvailPrices):

        if (fDebug):
            print("myValueList=" + str(myValueList))
            print("otherValueList=" + str(otherValueList))

        valueCorrelation, _ = spearmanr(myValueList, otherValueList)
        deltaCorrelation, _ = spearmanr(myDeltaValueList, otherDeltaValueList)
        if (numRisesInMyStock > 0):
            fractionMyRisesLeadToOtherRise = float(numRisesInpredictedStockTickerWhenMyStockRises) / float(numRisesInMyStock)
        else:
            fractionMyRisesLeadToOtherRise = 0

        if (totalRiseInMyStock > 0):
            ratioOfOtherRiseToMyRise = float(totalRiseInMyStock) / float(totalRiseInMyStock)
        else:
            ratioOfOtherRiseToMyRise = 0


        return valueCorrelation, deltaCorrelation, fractionMyRisesLeadToOtherRise, ratioOfOtherRiseToMyRise
    # End - GetCovarianceWithPredictedStockTicker





    #####################################################
    #
    # [CStockTicker::GetDaysWithExtremePrices]
    #
    # The oldest price is index 0, and the latest price is at index numPrices-1
    #####################################################
    def GetDaysWithExtremePrices(self, opCodeStr, numExtremePrices):
        fDebug = False
        fLookForLargestValues = False
        numPrices = 0
        priceList = [0] * numExtremePrices
        priceDateList = [{'y': 0}] * numExtremePrices
        pricePrevDateList = [{'y': 0}] * numExtremePrices

        if (fDebug):
            print("GetDaysWithExtremePrices. opCodeStr=" + opCodeStr)
            print("    numExtremePrices=" + str(numExtremePrices))


        ####################
        # Set some flags for the comparison, so we are using bools not comparing strings. 
        fLookForLargestValues = True
        if (opCodeStr in [EXTREMES_MIN_PRICES, EXTREMES_MAX_PRICE_DECLINES]):
            fLookForLargestValues = False

        fComparePriceChanges = False
        if (opCodeStr in [EXTREMES_MAX_PRICE_CHANGES, EXTREMES_MAX_PRICE_INCREASES, EXTREMES_MAX_PRICE_DECLINES]):
            fComparePriceChanges = True

        fCompareAbsoluteValues = False
        if (opCodeStr in [EXTREMES_MAX_PRICE_CHANGES]):
            fCompareAbsoluteValues = True


        ####################
        # Get the array indexes. Subtract 1 because the indexes are 0-based
        newestPriceIndex = len(self.PastPriceList) - 1
        newestPriceIndex = max(0, newestPriceIndex)
        #oldestPriceIndex = (newestPriceIndex - numPricesToSearch) + 1
        #oldestPriceIndex = max(0, oldestPriceIndex)
        oldestPriceIndex = 0
        # Add 1 because we include both the oldest and newest indexes as result values.
        numPricesToSearch = (newestPriceIndex - oldestPriceIndex) + 1

        if (fDebug):
            print("GetDaysWithExtremePrices. List length=" + str(len(self.PastPriceList)))
            print("     newestPriceIndex=" + str(newestPriceIndex))
            print("     oldestPriceIndex=" + str(oldestPriceIndex))
            print("     numExtremePrices=" + str(numExtremePrices))
            print("     numPricesToSearch=" + str(numPricesToSearch))


        #############################
        # Look at every available price
        prevDate = {'y': 0, 'm': 0, 'd': 0}
        prevPrice = (self.PastPriceList[oldestPriceIndex])['Cl']
        for index in range(numPricesToSearch):
            # Search in forward direction, so we can record the previous date.
            # We are looking for peaks and valleys, so it does not matter whether we approach
            # them from the future or the past.
            # currentPriceInfo = self.PastPriceList[newestPriceIndex - index]
            currentPriceInfo = self.PastPriceList[oldestPriceIndex + index]
            currentPrice = currentPriceInfo['Cl']
            currentDate = {'y': currentPriceInfo['y'], 'm': currentPriceInfo['m'], 'd': currentPriceInfo['d'] }

            if (fComparePriceChanges):
                currentValue = (currentPrice - prevPrice)
            else:  # elif (opCodeStr in (EXTREMES_MAX_PRICE_CHANGES, EXTREMES_MIN_PRICE_CHANGES)):
                currentValue = currentPrice

            if (fCompareAbsoluteValues):
                currentValue = abs(currentValue)

            if (fDebug):
                print("GetDaysWithExtremePrices. currentValue=" + str(currentValue) + ", currentDate=" + str(currentDate))

            ###################################
            # Look to see if this is one of the extreme prices
            if (numPrices < numExtremePrices):
                if (fDebug):
                    print("GetDaysWithExtremePrices. numPrices=" + str(numPrices) + ", numExtremePrices=" + str(numExtremePrices))
                priceList[numPrices] = currentValue
                priceDateList[numPrices] = currentDate
                pricePrevDateList[numPrices] = prevDate
                numPrices += 1
            ###################################
            else:
                bestMatchIndex = -1
                if (fLookForLargestValues):
                    bestMatchValue = 100000000
                else:
                    bestMatchValue = -100000000                

                for compareIndex in range(numExtremePrices):
                    compareValue = priceList[compareIndex]
                    if (fDebug):
                        print("     Compare currentValue=" + str(currentValue) + ", compareValue=" + str(compareValue))

                    if (fLookForLargestValues):
                        # Remove the smallest of the large values
                        if ((currentValue > compareValue) and (compareValue < bestMatchValue)):
                            bestMatchIndex = compareIndex
                            bestMatchValue = compareValue
                        # End - if ((currentValue > compareValue) and (compareValue < bestMatchValue)):
                    else:   # if (not fLookForLargestValues):
                        # Remove the largest of the small values
                        if ((currentValue < compareValue) and (compareValue > bestMatchValue)):
                            bestMatchIndex = compareIndex
                            bestMatchValue = compareValue
                        # End - if ((currentValue > compareValue) and (compareValue < bestMatchValue)):
                # End - for compareIndex in range(numExtremePrices):

                if (bestMatchIndex >= 0):
                    if (fDebug):
                        print("     GetDaysWithExtremePrices found Match. currentValue=" + str(currentValue))
                    priceList[bestMatchIndex] = currentValue                    
                    priceDateList[bestMatchIndex] = currentDate
                    pricePrevDateList[bestMatchIndex] = prevDate
                # End - if (bestMatchIndex >= 0)
            # End - We have already found numExtremePrices extremes, now find the most extreme.

            prevPrice = currentPrice
            prevDate = currentDate
        # End - for index in range(numPricesToSearch):

        if (fDebug):
            print("GetDaysWithExtremePrices. numPrices=" + str(numPrices) + ", priceList=" + str(priceList))
            print("     priceDateList=" + str(priceDateList))
            print("     pricePrevDateList=" + str(pricePrevDateList))

        return numPrices, priceList, priceDateList, pricePrevDateList
    # End - GetDaysWithExtremePrices()





    ##########################################################################################################
    #
    # Iterator
    #
    ##########################################################################################################


    #####################################################
    #
    # [CStockTicker::GotoFirstDate]
    #
    #####################################################
    def GotoFirstDate(self):
        if (len(self.PastPriceList) <= 0):
            return False

        self.IteratorIndex = 0
        return True
    # End of GotoFirstDate



    #####################################################
    #
    # [CStockTicker::GotoDate]
    #
    #####################################################
    def GotoDate(self, startYear, startMonth, startDay):
        fDebug = False
        fFoundDate = False
        if (fDebug):
            print("GotoDate. startYear=" + str(startYear) + ", startMonth=" + str(startMonth) + ", startDay=" + str(startDay))

        self.IteratorIndex = len(self.PastPriceList) - 1
        while (self.IteratorIndex >= 0):
            priceInfo = self.PastPriceList[self.IteratorIndex]
            if (fDebug):
                print("     priceInfo=" + str(priceInfo))
            if (CompareDates(DATE_COMPARE_GREATER_THAN_EQUAL, startYear, startMonth, startDay, priceInfo['y'], priceInfo['m'], priceInfo['d'])):
                if (fDebug):
                    print("     Found Matching Date")
                fFoundDate = True
                break

            self.IteratorIndex = self.IteratorIndex - 1
        # End - while (self.IteratorIndex >= 0):

        if (self.IteratorIndex < 0):
            self.IteratorIndex = 0

        return fFoundDate
    # End of GotoDate



    #####################################################
    #
    # [CStockTicker::GotoNextDate]
    #
    #####################################################
    def GotoNextDate(self):
        fDebug = False
        if (fDebug):
            print("GotoNextDate")

        if (self.IteratorIndex >= (len(self.PastPriceList) - 1)):
            return False

        self.IteratorIndex += 1
        return True
    # End of GotoNextDate





    #####################################################
    #
    # [CStockTicker::GetIteratorCurrentPriceInfo]
    #
    #####################################################
    def GetIteratorCurrentPriceInfo(self):
        fDebug = False
        if (fDebug):
            print("GetIteratorCurrentPriceInfo")

        if ((self.IteratorIndex < 0) or (self.IteratorIndex == len(self.PastPriceList))):
            return False, 0, 0, 0, 0, 0, 0, 0, 0, 0

        priceInfo = self.PastPriceList[self.IteratorIndex]
        if (fDebug):
            print("GetIteratorCurrentPriceInfo. priceInfo=" + str(priceInfo))

        return True, priceInfo['y'], priceInfo['m'], priceInfo['d'], priceInfo['Cl'], priceInfo['Op'], priceInfo['Lo'], priceInfo['Hi'], priceInfo['Vo'], priceInfo['RSI']
    # End of GetIteratorCurrentPriceInfo




    #####################################################
    #
    # [CStockTicker::GetIteratorExtendedCurrentPriceInfo]
    #
    #####################################################
    def GetIteratorExtendedCurrentPriceInfo(self):
        fDebug = False
        if (fDebug):
            print("GetIteratorCurrentPriceInfo")

        if ((self.IteratorIndex < 0) or (self.IteratorIndex == len(self.PastPriceList))):
            return False, 0, 0, 0, 0, 0, 0, 0, 0, 0

        priceInfo = self.PastPriceList[self.IteratorIndex]
        if (self.IteratorIndex <= 0):
            prevPrice = 0
        else:
            prevPrice = self.PastPriceList[self.IteratorIndex - 1]['Cl']

        return True, prevPrice, priceInfo['EMA12'], priceInfo['EMA26'], priceInfo['MACD'], priceInfo['KStochastic'], priceInfo['DStochastic'], priceInfo['BiggestRecentDropPercent']
    # End of GetIteratorExtendedCurrentPriceInfo






    #####################################################
    #
    # [CStockTicker::PrintDebug]
    #
    #####################################################
    def PrintDebug(self):
        print("\n\n PrintDebug \n\n")

        numEntries = len(self.PastPriceList)
        for index in range(numEntries):
            print(str(index) + ": " + str(self.PastPriceList[index]))
        # End - for index in range(numEntries):
    # End - PrintDebug

# End - CStockTicker






################################################################################
# 
################################################################################
def LoadTickerFromValueDict(tickerSymbol, valueDictList, firstYear):
    fDebug = False
    if (fDebug):
        print("LoadTickerFromValueDict")

    # Make a new empty ticker
    stockTicker = CStockTicker(tickerSymbol)

    # Set latest stock info
    latestDictEntry = valueDictList[len(valueDictList) - 1]
    stockTicker.SetCompanyName(tickerSymbol)
    stockTicker.SetCurrentPrice(latestDictEntry['cl'])
    stockTicker.SetPrevClose(latestDictEntry['cl'])
    stockTicker.SetTodayOpenPrice(latestDictEntry['op'])
    stockTicker.SetTodayLowPrice(latestDictEntry['lo'])
    stockTicker.SetTodayHighPrice(latestDictEntry['hi'])
    stockTicker.SetVolume(latestDictEntry['lo'])

    stockTicker.SetTrailingPE(-1)
    stockTicker.SetForwardPE(-1)
    stockTicker.SetBid(-1)
    stockTicker.SetAsk(-1)
    stockTicker.SetFiftyTwoWeekLow(0)
    stockTicker.SetFiftyTwoWeekHigh(0)
    stockTicker.SetFiftyDayAverage (0)
    stockTicker.SetTwoHundredDayAverage(0)
    stockTicker.SetAvgVolume(0)
    stockTicker.SetPEGRatio(0)

    #######################
    # Set all past info
    for valueDict in valueDictList:
        if ((valueDict['y'] == latestDictEntry['y']) and (valueDict['m'] == latestDictEntry['m']) and (valueDict['d'] == latestDictEntry['d'])):
            break

        # I mean, really, do we need to simulate back to 1930? Let's just skip those.
        if ((firstYear > 0) and (valueDict['y'] < firstYear)):
            continue

        stockTicker.SetPastValues(valueDict['y'], valueDict['m'], valueDict['d'], 
                                valueDict['op'], valueDict['cl'], valueDict['vo'], 
                                valueDict['hi'], valueDict['lo'],
                                valueDict['rsi'], valueDict['ema12'], valueDict['ema26'],
                                valueDict['macd'], valueDict['kStochastic'], valueDict['dStochastic'],
                                valueDict['drop'])
    # for row in hist.itertuples():

    return stockTicker
# End - LoadTickerFromValueDict


