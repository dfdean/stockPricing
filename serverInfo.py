#!/usr/bin/python3
#####################################################################################
# 
# Copyright (c) 2020-2024 Dawson Dean
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
#####################################################################################
#
# For debugging, look at:
#   tail /var/log/httpd/error_log
#
# Some handy web sites:
# https://www.thepythoncode.com/article/get-hardware-system-information-python
#####################################################################################
import os
from datetime import datetime
import platform
import importlib

import socket

# This is supported on some machines, but not all.
SUPPORT_PSUTILS = False
#import psutil

g_GPUList = []
CHECK_GPUS = False
if (CHECK_GPUS):
    #g_GPUList = [torch.cuda.device(i) for i in range(torch.cuda.device_count())]
    pass

import fileTemplate as FileTemplate



################################################################################
#
# [CheckIfPythonModuleIsInstalled]
#
################################################################################
g_PipList = ""
def CheckIfPythonModuleIsInstalled(moduleName):
    global g_PipList

    try:
        if (importlib.import_module(moduleName) is not None):
            return "True"
    except Exception:
        pass

    # Lazily read in the list of all modules installed with Pip
    if (g_PipList == ""):
        stream = os.popen('pip list')
        g_PipList = stream.read().lower()

    if (moduleName.lower() in g_PipList):
        return "True"

    return "False"
# End - CheckIfPythonModuleIsInstalled



################################################################################
#
# [AddSubsectionToTable]
#
################################################################################
def AddSubsectionToTable(tableStr, nameStr):
    #tableStr += "<tr><td></td></tr>\n"
    tableStr += "<tr><td><b><u><h4>" + nameStr + "</h4></u></b></td></tr>\n"
    return tableStr
# End - AddSubsectionToTable




################################################################################
#
# [AddNameValueToTable]
#
################################################################################
def AddNameValueToTable(tableStr, nameStr, valueStr):
    tableStr += "<tr><td>" + nameStr + "</td><td>" + str(valueStr) + "</td></tr>\n"
    return tableStr
# End - AddNameValueToTable





################################################################################
#
# [MakeServerInfoTable]
#
################################################################################
def MakeServerInfoTable():
    infoTableStr = ""

    ###########################################
    infoTableStr = AddSubsectionToTable(infoTableStr, "Server")
    infoTableStr = AddNameValueToTable(infoTableStr, "MachineName", platform.node())
    infoTableStr = AddNameValueToTable(infoTableStr, "OS", platform.system())
    infoTableStr = AddNameValueToTable(infoTableStr, "OS Version", platform.platform())
    infoTableStr = AddNameValueToTable(infoTableStr, "Server Local Time", datetime.now())
    infoTableStr = AddNameValueToTable(infoTableStr, "Extension Dir", os.path.dirname(os.path.realpath(__file__)))
    try:
        hostname = socket.gethostname()    
        IPAddr = socket.gethostbyname(hostname)
    except:
        hostname = " "
        IPAddr = " "
    infoTableStr = AddNameValueToTable(infoTableStr, "Hostname", hostname)
    infoTableStr = AddNameValueToTable(infoTableStr, "IP Address", IPAddr)

    ###########################################
    infoTableStr = AddSubsectionToTable(infoTableStr, "Hardware")
    infoTableStr = AddNameValueToTable(infoTableStr, "Processor", platform.processor())
    infoTableStr = AddNameValueToTable(infoTableStr, "Machine", platform.machine())
    infoTableStr = AddNameValueToTable(infoTableStr, "System", platform.system())
    if (SUPPORT_PSUTILS):
        #infoTableStr = AddNameValueToTable(infoTableStr, "Physical cores", psutil.cpu_count(logical=False))
        #infoTableStr = AddNameValueToTable(infoTableStr, "Total cores", psutil.cpu_count(logical=True))
        pass
    # This seems to be blocked when running as a web server CGI
    #cpufreq = psutil.cpu_freq()
    #infoTableStr += "<br>Max Frequency</td><td>" + str(cpufreq.max) + "Mhz")
    if (CHECK_GPUS):
        infoTableStr = AddNameValueToTable(infoTableStr, "Num GPUs", len(g_GPUList))
    memSize = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')  # e.g. 4015976448
    memSize = memSize / (1024 * 1024 * 1024)
    memSize = round(memSize, 2)
    infoTableStr = AddNameValueToTable(infoTableStr, "Phys Mem size", str(memSize) + "Gb")
    #infoTableStr += str(pwd.getpwuid(os.getuid()))


    ###########################################
    infoTableStr = AddSubsectionToTable(infoTableStr, "Web Server")
    try:
        infoTableStr = AddNameValueToTable(infoTableStr, "Web Server Software", os.environ["SERVER_SOFTWARE"])
    except Exception:
        pass
    try:
        infoTableStr = AddNameValueToTable(infoTableStr, "Web Server Name", os.environ["SERVER_NAME"])
    except Exception:
        pass
    try:
        infoTableStr = AddNameValueToTable(infoTableStr, "Web Server CGI Script", os.environ["SCRIPT_FILENAME"])
    except Exception:
        pass


    ###########################################
    infoTableStr = AddSubsectionToTable(infoTableStr, "Python")
    infoTableStr = AddNameValueToTable(infoTableStr, "Python Version", platform.python_version())
    infoTableStr = AddNameValueToTable(infoTableStr, "PyTorch Installed", CheckIfPythonModuleIsInstalled("torch"))
    infoTableStr = AddNameValueToTable(infoTableStr, "psutil Installed", CheckIfPythonModuleIsInstalled("psutil"))
    infoTableStr = AddNameValueToTable(infoTableStr, "gputils Installed", CheckIfPythonModuleIsInstalled("gputils"))
    infoTableStr = AddNameValueToTable(infoTableStr, "GPUtil Installed", CheckIfPythonModuleIsInstalled("GPUtil"))
    infoTableStr = AddNameValueToTable(infoTableStr, "scipy Installed", CheckIfPythonModuleIsInstalled("scipy"))
    infoTableStr = AddNameValueToTable(infoTableStr, "numpy Installed", CheckIfPythonModuleIsInstalled("numpy"))
    infoTableStr = AddNameValueToTable(infoTableStr, "importlib Installed", CheckIfPythonModuleIsInstalled("importlib"))


    ###########################################
    infoTableStr = AddSubsectionToTable(infoTableStr, "Requesting Client")
    try:
        #clientIPAddr = str(html.escape(os.environ["REMOTE_ADDR"]))
        #clientUserAgent = str(html.escape(os.environ["HTTP_USER_AGENT"]))
        clientIPAddr = str(os.environ["REMOTE_ADDR"])
        clientUserAgent = str(os.environ["HTTP_USER_AGENT"])
    except Exception:
        clientIPAddr = ""
        clientUserAgent = ""
    infoTableStr = AddNameValueToTable(infoTableStr, "IP Address", clientIPAddr)
    infoTableStr = AddNameValueToTable(infoTableStr, "User Agent", clientUserAgent)


    return infoTableStr
# End - MakeServerInfoTable





################################################################################
#
# [MakeServerInfoPage]
#
################################################################################
def MakeServerInfoPage(requestContext):
    startimeStr = datetime.today().strftime("%A %B %d, %Y (%H:%M:%S)")
    reportHTML = FileTemplate.MakeTemplate()
    reportHTML.SetBodyStr("Collected " + startimeStr)

    try:
        infoTableStr = MakeServerInfoTable()
        reportHTML.SetTableStr(infoTableStr)
    except:
        pass

    localDirPath = os.path.dirname(os.path.realpath(__file__))
    localTemplatePath = localDirPath + "/serverInfoTemplate.html"
    reportStr = reportHTML.ExpandTemplate(localTemplatePath)

    return reportStr
# End - MakeServerInfoPage




