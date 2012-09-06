# -*- coding: utf-8 -*-
#
# file: src/SysInfo.py
# part of: Windows Info
#
# core logic responsible for getting the information from the Windows registry.
#
# Copyright © 2012 Malte Bublitz. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR
# AND/OR CONTRIBUTORS OF WindowsInfo BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 

import sys
import ctypes, os, platform, _winreg
GetTickCount = ctypes.windll.kernel32.GetTickCount
winreg = _winreg

__WINVER__   = None
__WIN_REAL__ = 0
__WIN_WINE__ = 1
# check if running on Windows or wine, if not, exit.
if sys.platform != "win32":
	raise ImportError
try:
	ctypes.windll.kernel32.wine_get_unix_file_name()
	__WINVER__ = __WIN_WINE__
except AttributeError:
	__WINVER__ = __WIN_REAL__

def GetRegistryValue(structure=winreg.HKEY_LOCAL_MACHINE, key=None, value=None):
	""" get a value from the registry. This makes handling the Registry read-only much easier. """
	RegistryKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key)
	try:
		return winreg.QueryValueEx(RegistryKey, value)[0]
	except WindowsError:
		return ""
	
def DecodeDigitalProductID(ProductID):
	"""
	decode a Windows Digital Product ID to the CD key (a.k.a. serial number)
	based on Decodekey from this extract:
	   https://gist.github.com/877110
	Which seems to not have any Copyright at all.
	Althought it is Copyright 2011 Johnneylee Jack Rollins alias Spaceghost
	"""
	rpkOffset = 52
	i = 28
	szPossibleChars = "BCDFGHJKMPQRTVWXY2346789"
	szProductKey = ""
	
	while i >= 0:
		dwAccumulator = 0
		j = 14
		while j >= 0:
			dwAccumulator = dwAccumulator * 256
			d = ProductID[j+rpkOffset]
			if isinstance(d, str):
				d = ord(d)
			dwAccumulator = d + dwAccumulator
			ProductID[j+rpkOffset] =  (dwAccumulator / 24) if (dwAccumulator / 24) <= 255 else 255 
			dwAccumulator = dwAccumulator % 24
			j = j - 1
		i = i - 1
		szProductKey = szPossibleChars[dwAccumulator] + szProductKey
		
		if ((29 - i) % 6) == 0 and i != -1:
			i = i - 1
			szProductKey = "-" + szProductKey
	
	return szProductKey
	
def GetBits():
	"""
	Detect if running on a 32-Bit or 64-Bit OS. (Intel/AMD-only)
	Support for WOW64-detection
	return: (32bit|64bit|WOW64)
	"""
	arch = platform.architecture()[0]
	if arch == "32bit" and ("PROGRAMFILES(X86)" in os.environ):
		return "WOW64"
	else:
		return arch
	
def GetUptime():
	""" Get the system uptime using ctypes kernel32.dll interface """
	ticks    = GetTickCount()
	seconds  = ticks/1000
	days     = seconds/60/60/24
	seconds -= days*60*60*24
	hours    = seconds/60/60
	seconds -= hours*60*60
	minutes  = seconds/60
	seconds -= minutes*60
	return {
		"Days": days,
		"Hours": hours,
		"Minutes": minutes,
		"Seconds": seconds
		}
	
def format_uptime(up, language="english"):
	up_str = u""
	if language == "german":
		_DAYS = u" Tage"
		_DAY = u" Tag"
		_HOURS = u" Stunden"
		_HOUR = u" Stunde"
		_MINUTES = u" Minuten"
		_MINUTE = u" Minute"
		_SECONDS = u" Sekunden"
		_SECOND = u" Sekunde"
	else:
		_DAYS = u" days"
		_DAY = u" day"
		_HOURS = u" hours"
		_HOUR = u" hour"
		_MINUTES = u" minutes"
		_MINUTE = u" minute"
		_SECONDS = u" seconds"
		_SECOND = u" second"
	if up["Days"]      > 1:
		up_str += ", " + unicode(up["Days"])    + _DAYS
	elif up["Days"]    > 0:
		up_str += ", " + unicode(up["Days"])    + _DAY
	if up["Hours"]     > 1:
		up_str += ", " + unicode(up["Hours"])   + _HOURS
	elif up["Hours"]   > 0:
		up_str += ", " + unicode(up["Hours"])   + _HOUR
	if up["Minutes"]   > 1:
		up_str += ", " + unicode(up["Minutes"]) + _MINUTES
	elif up["Minutes"] > 0:
		up_str += ", " + unicode(up["Minutes"]) + _MINUTE
	if up["Seconds"]   > 1:
		up_str += ", " + unicode(up["Seconds"]) + _SECONDS
	elif up["Seconds"] > 0:
		up_str += ", " + unicode(up["Seconds"]) + _SECOND
	return up_str.lstrip(", ")

def GetInfo():
	# get info available under both wine and real windows
	_Owner              = GetRegistryValue(key="SOFTWARE\Microsoft\Windows NT\CurrentVersion", value="RegisteredOwner")
	_Organization       = GetRegistryValue(key="SOFTWARE\Microsoft\Windows NT\CurrentVersion", value="RegisteredOrganization")
	_ProductName        = GetRegistryValue(key="SOFTWARE\Microsoft\Windows NT\CurrentVersion", value="ProductName")
	_ServicePack        = GetRegistryValue(key="SOFTWARE\Microsoft\Windows NT\CurrentVersion", value="CSDVersion")
	_Bits             = GetBits()
	_Uptime           = GetUptime()
	# WOW64 means we are on a 64bit Windows
	if _Bits == "WOW64":
		_Bits = "64bit"
	if __WINVER__ == __WIN_WINE__:
		_Win32API         = "Wine"
	else:
		_ProductName      = GetRegistryValue(key="SOFTWARE\Microsoft\Windows NT\CurrentVersion", value="ProductName")
		_ServicePack      = GetRegistryValue(key="SOFTWARE\Microsoft\Windows NT\CurrentVersion", value="CSDVersion")
		_DigitalProductID = GetRegistryValue(key="SOFTWARE\Microsoft\Windows NT\CurrentVersion", value="DigitalProductID")
		_CDKey            = DecodeDigitalProductID( list( _DigitalProductID ) )
		_ProductID        = GetRegistryValue(key="SOFTWARE\Microsoft\Windows NT\CurrentVersion", value="ProductID")
		_Version          = GetRegistryValue(key="SOFTWARE\Microsoft\Windows NT\CurrentVersion", value="CurrentVersion")
		_BuildID          = GetRegistryValue(key="SOFTWARE\Microsoft\Windows NT\CurrentVersion", value="BuildLab")
		_Win32API         = "Microsoft Windows NT"
		# Channel ID (Detect OEM, Retail)
		# see: http://wiki.lunarsoft.net/wiki/Product_IDs
		_Channel = ""
		if _ProductID.split("-")[1]=="OEM":
			_Channel = "OEM"
		elif _ProductID.split("-")[1]=="335":
			_Channel = "Retail"
		elif _ProductID.split("-")[1]=="770":
			_Channel = "Retail"
		elif 640<=int(_ProductID.split("-")[1])<=652 or _ProductID.split("-")[1]=="270":
			_Channel = "Volume License"
		_User             = unicode(os.environ["USERDOMAIN"])+u"\\"+unicode(os.environ["USERNAME"])
	
	# return info as
	if __WINVER__==__WIN_WINE__:
		return {
			"ProductName": _ProductName,
			"ServicePack": _ServicePack,
			"Owner": _Owner,
			"Organization": _Organization,
			"Win32API": _Win32API,
			"Bits": _Bits
			}
	else: #__WINVER__==__WIN_REAL__
		return {
			"ProductName": _ProductName,
			"ServicePack": _ServicePack,
			"Version": _Version,
			"BuildID": _BuildID,
			"ProductID": _ProductID,
			"CDKey": _CDKey,
			"Owner": _Owner,
			"Organization": _Organization,
			"RawUptime": _Uptime,
			"Uptime": format_uptime(_Uptime),
			"UptimeGerman": format_uptime(_Uptime, "german"),
			"Bits": _Bits,
			"Channel": _Channel,
			"Win32API": _Win32API,
			"User": _User
			}
