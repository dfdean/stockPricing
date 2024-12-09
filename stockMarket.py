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
import stockRobot as StockRobot



################################################################################
#
# [RunRobot]
#
################################################################################
def RunRobot(stockTicker, robot, account, numDaysToScan):
    fDebug = False

    if (fDebug):
        print("RunRobot. ")
        print("     numDaysToScan=" + str(numDaysToScan))

    if (numDaysToScan > 0):
        currentYear, currentMonth, currentDay = stockTicker.GetLatestDate()
        year, month, day = StockTicker.GetDateForNumDaysOffset(currentYear, currentMonth, currentDay, numDaysToScan)
        if (fDebug):
            print("RunRobot. ")
            print("     currentYear=" + str(currentYear) + ", currentMonth=" + str(currentMonth) + ", currentDay=" + str(currentDay))
            print("     year=" + str(year) + ", month=" + str(month) + ", day=" + str(day))
        fFoundIt = stockTicker.GotoDate(year, month, day)
    else:
        fFoundIt = stockTicker.GotoFirstDate()
    if (fDebug):
        print("RunRobot. fFoundIt=" + str(fFoundIt))
    if (not fFoundIt):
        print("Error! RunRobot could not find start date")
        return
        

    account.StartRun()
    while (fFoundIt):
        fFoundIt, year, month, day, closePrice, openPrice, lowPrice, highPrice, volume, rsi = stockTicker.GetIteratorCurrentPriceInfo()
        if (not fFoundIt):
            break
        if (fDebug):
            print("RunRobot. year=" + str(year) + ", month=" + str(month) + ", day=" + str(day))
            print("     closePrice=" + str(closePrice) + ", openPrice=" + str(openPrice) + ", lowPrice=" + str(lowPrice))
            print("     highPrice=" + str(highPrice) + ", volume=" + str(volume) + ", rsi=" + str(rsi))

        robot.ProcessNewPrice(stockTicker, account, year, month, day, openPrice, lowPrice, highPrice, closePrice, volume, rsi)

        account.FinishDay(stockTicker, year, month, day, closePrice)
        fFoundIt = stockTicker.GotoNextDate()
    # End - while (fFoundIt):

    account.FinishRun()
# End - RunRobot()



