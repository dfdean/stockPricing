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
################################################################################
import os
import sys

# WSGI also seems to require the named import style. 
import os
from datetime import datetime
import platform
import importlib

starTimeStr = str(datetime.now().time())

# Must add the current directory to the path before any modules can be loaded
g_DirPath = os.path.dirname(os.path.realpath(__file__))
if g_DirPath not in sys.path:
    sys.path.insert(0, g_DirPath)
#sys.path.append("/var/www/cgi-bin")

import fileTemplate as FileTemplate
import stockTicker as StockTicker
import stockAccount as StockAccount
import stockRobot as StockRobot
import stockMarket as StockMarket
import stockInfo_SP500 as StockInfoSP500

NEWLINE_STR = "\n"

ticker = StockTicker.LoadTickerFromValueDict(StockTicker.SP500_TICKER, StockInfoSP500.g_PriceInfo_SP500, 1990)

numExtremePrices = 10
g_InitialAccountValue = 10000
extremeType = StockTicker.EXTREMES_MAX_PRICES
extremeType = StockTicker.EXTREMES_MIN_PRICES
extremeType = StockTicker.EXTREMES_MAX_PRICE_CHANGES
extremeType = StockTicker.EXTREMES_MAX_PRICE_INCREASES
extremeType = StockTicker.EXTREMES_MAX_PRICE_DECLINES


# numExtremePriceDays, priceList, extremePriceDays, extremePricePrevDays = ticker.GetDaysWithExtremePrices(extremeType, numExtremePrices)

# account = StockAccount.MakeTradingAccount(g_InitialAccountValue)
# robot = StockRobot.MakeSkipDatesRobot(numExtremePriceDays, priceList, extremePriceDays, extremePricePrevDays)
# StockMarket.RunRobot(ticker, robot, account, -1)
# finalValue = account.GetAccountValue()
# print("Final Value: " + str(finalValue))




#######################################
# print("\n\n")
# stopTimeStr = str(datetime.now().time())
# print("Start: " + starTimeStr)
# print("Stop: " + stopTimeStr)




################################################################################
#
# class CWebServerRequestContext
#
# This is a wrapper for the environment. It is independent of WSGI, Flask, Django, or CGI.
################################################################################
class CWebServerRequestContext(object):
    #####################################################
    # Constructor - This method is part of any class
    #####################################################
    def __init__(self, environ):
        self.WSGIEnviron = environ
    # End -  __init__


    #####################################################
    # [CWebServerRequestContext::IsPost]
    #####################################################
    def IsPost(self):
        if ((self.WSGIEnviron is not None) and (self.WSGIEnviron['REQUEST_METHOD'].upper() == 'POST')):
            return True
        return False
    # End - IsPost


    #####################################################
    # [CWebServerRequestContext::GetPostData]
    #####################################################
    def GetPostData(self):
        if ((self.WSGIEnviron is None) or (self.WSGIEnviron['REQUEST_METHOD'].upper() != 'POST')):
            return ""

        input = self.WSGIEnviron['wsgi.input']
        postForm = self.WSGIEnviron.get('wsgi.post_form')
        if ((post_form is not None) and (postForm[0] is input)):
            return postForm[2]

        # This must be done to avoid a bug in cgi.FieldStorage
        self.WSGIEnviron.setdefault('QUERY_STRING', '')
        fs = cgi.FieldStorage(fp=input, environ=self.WSGIEnviron, keep_blank_values=1)
        newInput = InputProcessed('')
        postForm = (newInput, input, fs)
        self.WSGIEnviron['wsgi.post_form'] = postForm
        self.WSGIEnviron['wsgi.input'] = newInput
        return fs
    # End - GetPostData


    #####################################################
    # [CWebServerRequestContext::GetQueryString]
    #####################################################
    def GetQueryString(self):
        if ((self.WSGIEnviron is not None) and (self.WSGIEnviron['REQUEST_METHOD'].upper() == 'POST')):
            return ""

        return self.WSGIEnviron['QUERY_STRING']
    # End - GetQueryString

# End - CWebServerRequestContext








################################################################################
#
# [application]
#
# WSGI looks for a function named "application" in the target file. This is where 
# control initiates.
################################################################################
def application(environ, start_response):
    status = '200 OK'
    textStr = ""

    # Make our wrapper for the environment.
    requestContext = CWebServerRequestContext(environ)

    try:
        reportHTML = FileTemplate.MakeTemplate()
        startimeStr = datetime.today().strftime("%A %B %d, %Y (%H:%M:%S)")
        reportHTML.SetBodyStr("Collected " + startimeStr)

        localDirPath = os.path.dirname(os.path.realpath(__file__))
        localTemplatePath = localDirPath + "/finTech.html"
        textStr = reportHTML.ExpandTemplate(localTemplatePath)

        output = textStr.encode('utf-8')
        contentTypeStr = 'text/html'
    except:
        errStr = "Exception in MakeServerInfoPage. Version 1 textStr=(" + textStr + ")"
        output = errStr.encode('utf-8')
        contentTypeStr = 'text/plain'

    response_headers = [('Content-type', contentTypeStr),
                        ('Content-Length', str(len(output)))]

    start_response(status, response_headers)
    return [output]
# End - application





