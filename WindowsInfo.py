# -*- coding: utf-8 -*-
#
# file: /WindowsInfo.pyw
# part of: Windows Info
# 
# WindowsInfo GUI; cx_Freeze converts this into WindowsInfo.exe
# 
# Copyright (c) 2012-2017 Malte Bublitz, http://malte70.bplaced.net
# All rights reserved.
# 

__WIN_REAL__ = 0
__WIN_WINE__ = 1

import sys

# Ensure we're running on Windows
if not sys.platform.startswith("win"):
	sys.stderr.write("\n==> FATAL ERROR\n\n")
	sys.stderr.write("As the name implies, WindowsInfo can only be run\n")
	sys.stderr.write("on Windows NT.\n\n")
	sys.exit(1)
	
import wx
import ctypes
import os
import _winreg
import platform
import io
import locale
import webbrowser


class WindowsInfo(object):
	version         = "0.4"
	website         = "https://github.com/malte70/WindowsInfo"
	copyrightInfo   = "(c) 2012-2017 Malte Bublitz"
	developers      = [
		"Malte Bublitz <malte70@tuta.io>, http://malte70.bplaced.net"
	]
	appIcon         = None
	appIconFilename = "WindowsInfo.ico"
	

"""
WindowsInfo's application folder

Either the path of the cloned Git repository, or
the selected installation folder if WindowsInfo was
installed using the InnoSetup-based setup.

If WindowsInfo was frozen by cx_Freeze, __file__ is
not available, but sys.executable.
"""
if getattr(sys, 'frozen', False):
	__WINDOWSINFO_FOLDER__ = os.path.dirname(sys.executable)
else:
	__WINDOWSINFO_FOLDER__ = os.path.dirname(os.path.realpath(__file__))

# Change to application folder
os.chdir(__WINDOWSINFO_FOLDER__)

def GetSystemLanguage():
	"""
	Get System User Interface Language using the
	`locale` module.
	
	Unix systems always have a `$LANG` variable,
	but this weird OS named Windows NT doesn't
	have such neat Features... xD
	Found this solution using `locale.getdefaultlocale()`
	on: https://stackoverflow.com/a/3425316
	"""
	try:
		return locale.getdefaultlocale()[0]
	except NameError:
		return ""
	except TypeError:
		return None
	
""" *************************************
"   * Helper functions                  *
"   ************************************* """
def GetRegistryValue(structure=_winreg.HKEY_LOCAL_MACHINE, key=None, value=None):
	""" get a value from the registry. This makes handling the Registry read-only much easier. """
	RegistryKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, key)
	return _winreg.QueryValueEx(RegistryKey, value)[0]
	
def GetWin32APIVendor():
	if sys.platform != "win32":
		raise ImportError
	try:
		ctypes.windll.kernel32.wine_get_unix_file_name()
		return __WIN_WINE__
	except AttributeError:
		return __WIN_REAL__
	
def DecodeDigitalProductID(ProductID):
	"""
	decode a Windows Digital Product ID to the CD key (a.k.a. serial number)
	based on Decodekey from this extract:
	   https://gist.github.com/877110
	Which seems to not have any Copyright at all.
	Althought it is Copyright 2011 Johnneylee Jack Rollins alias Spaceghost
	"""
	Offset = 52
	i = 28
	PossibleChars = "BCDFGHJKMPQRTVWXY2346789"
	ProductKey = ""
	
	while i >= 0:
		Accumulator = 0
		j = 14
		while j >= 0:
			Accumulator = Accumulator * 256
			d = ProductID[j+Offset]
			if isinstance(d, str):
				d = ord(d)
			Accumulator = d + Accumulator
			ProductID[j+Offset] =  (Accumulator / 24) if (Accumulator / 24) <= 255 else 255 
			Accumulator = Accumulator % 24
			j = j - 1
		i = i - 1
		ProductKey = PossibleChars[Accumulator] + ProductKey
		
		if ((29 - i) % 6) == 0 and i != -1:
			i = i - 1
			ProductKey = "-" + ProductKey
	
	return ProductKey
	
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
	ticks    = ctypes.windll.kernel32.GetTickCount()
	seconds  = ticks/1000
	days     = seconds/60/60/24
	seconds -= days*60*60*24
	hours    = seconds/60/60
	seconds -= hours*60*60
	minutes  = seconds/60
	seconds -= minutes*60
	up = {
		"Days": days,
		"Hours": hours,
		"Minutes": minutes
		}
	up_str = u""
	_DAYS = u" days"
	_DAY = u" day"
	_HOURS = u" hours"
	_HOUR = u" hour"
	_MINUTES = u" minutes"
	_MINUTE = u" minute"
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
	
	return up_str.lstrip(", ")
	
class WindowsInfoMainFrame(wx.Frame):
	def __init__(self, parent, title, parent_app):
		super(WindowsInfoMainFrame, self).__init__(parent, title=title, size=(430,270))
		self._parent = parent_app
		self.InitUI()
		self.Centre()
		self.Show()
		self.LoadInfo()
		
	def readFileContents(self, filename):
		try:
			f = io.open(
				filename,
				mode = "r",
				encoding = "UTF-8"
			)
			fileContents = f.read()
			f.close()
			
			return fileContents
		except IOError:
			return u""
		
	def InitUI(self):
		self.appIcon = wx.EmptyIcon()
		self.appIcon.CopyFromBitmap(
			wx.Bitmap(
				"WindowsInfo.ico",
				wx.BITMAP_TYPE_ANY
			)
		)
		
		self.SetIcon(self.appIcon)
		
		self.InitUI_Menubar()
		self.InitUI_TextCtrl()
		
		self.Bind(wx.EVT_CLOSE,      self.OnExit)
		
		"""
		print "wx.GetFullHostName()              =",wx.GetFullHostName()
		print "wx.GetHomeDir()                   =",wx.GetHomeDir()
		print "wx.GetUserHome()                  =",wx.GetUserHome()
		print "wx.GetUserName()                  =",wx.GetUserName()
		print "wx.GetOsDescription()             =",wx.GetOsDescription()
		"""
		
	def InitUI_Menubar(self):
		self._menuBar  = wx.MenuBar()
		
		self._menuInfo = wx.Menu()
		menuExport     = self._menuInfo.Append(wx.ID_SAVE, "&Export\tCtrl+S", "")
		self._menuInfo.AppendSeparator()
		menuExit       = self._menuInfo.Append(wx.ID_EXIT,  "E&xit\tCtrl+Q",   "")
		self._menuBar.Append(self._menuInfo, "&Info")
		
		self._menuHelp  = wx.Menu()
		menuHelp       = self._menuHelp.Append(wx.ID_HELP,  "&Help\tF1", "")
		menuAbout      = self._menuHelp.Append(wx.ID_ABOUT, "&About",  "")
		self._menuBar.Append(self._menuHelp, "&Help")
			
			
		self.SetMenuBar(self._menuBar)
		
		self.Bind(wx.EVT_MENU,       self.OnExport, menuExport)
		self.Bind(wx.EVT_MENU,       self.OnAbout,  menuAbout)
		self.Bind(wx.EVT_MENU,       self.OnHelp,   menuHelp)
		self.Bind(wx.EVT_MENU,       self.OnExit,   menuExit)
		
	def InitUI_TextCtrl(self):
		font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FIXED_FONT)
		self.tc = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_NO_VSCROLL)
		self.tc.SetFont(font)
		self.tc.SetValue("Loading...")
		self.tc.SetEditable(False)
		self.tc.SetSelection(0,0)
		
		"""
		Set a white background for the TextCtrl, 
		although it's not editable.
		"""
		color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND)
		color = wx.NullColour
		color = "white"
		self.tc.SetBackgroundColour(color)
		
	def OnExport(self, event):
		madeWithFooter = u"\n\n---\nMade with WindowsInfo - " + WindowsInfo.website
		
		filetypes = "Text files (*.txt)|*.txt|All files (*.*)|*.*"
		dialog = wx.FileDialog(
			self,
			"Choose a filename",
			"",
			"",
			filetypes,
			wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
		)
		if dialog.ShowModal() == wx.ID_OK:
			selectedFilename = os.path.join(dialog.GetDirectory(), dialog.GetFilename())
			
			f = io.open(selectedFilename, mode = "w", encoding = "UTF-8", newline = "\r\n")
			f.write(self.tc.GetValue())
			f.write(madeWithFooter)
			f.close()
		
	def OnHelp(self, event):
		readme_html = "README.html"
		webbrowser.open(readme_html)
		
	def OnAbout_AboutBox(self, event):
		"""
		Show WindowsInfo's "About" using a wx.AboutBox
		
		Looks like crap if wxPython uses it's Win32
		backend, which is always the case for us...
		"""
		description = "WindowsInfo shows details about your Windows system, like the runtime, the serial number, or the edition you use."
		license = self.readFileContents("COPYING.md")
		info = wx.AboutDialogInfo()
		
		info.SetIcon(self.appIcon)
		info.SetName("WindowsInfo")
		info.SetVersion(WindowsInfo.version)
		info.SetDescription(description)
		info.SetCopyright(WindowsInfo.copyrightInfo)
		info.SetWebSite(WindowsInfo.website)
		info.SetLicense(license)
		for dev in WindowsInfo.developers:
			info.AddDeveloper(dev)
		
		wx.AboutBox(info)
		
	def OnAbout_MessageDialog(self, event):
		about_title = "About WindowsInfo " + WindowsInfo.version
		about_text  = "WindowsInfo " + WindowsInfo.version + "\n\n"
		about_text += WindowsInfo.copyrightInfo + "\n"
		about_text += WindowsInfo.website
		
		dlg = wx.MessageDialog(
			self,
			about_text,
			about_title,
			wx.OK | wx.ICON_INFORMATION
		)
		dlg.ShowModal()
		dlg.Destroy()
		
	def OnAbout(self, event):
		self.OnAbout_MessageDialog(event)
		
	def OnExit(self, event):
		self.Destroy()
		sys.exit(0)
		
	def LoadInfo(self):
		info = self.GetInfo()
		if info["Win32API"] == "Wine":
			infotext = """%(ProductName)s %(Bits)s %(ServicePack)s
Uses Win32 APIs by: %(Win32API)s

Registered to %(Owner)s (at %(Organization)s)
"""
		else:
			infotext = """%(ProductName)s %(Bits)s %(ServicePack)s
a.k.a. Windows NT %(Version)s

Product key: %(CDKey)s 
{CHANNEL}
Up: %(Uptime)s

Registered to %(Owner)s{ORGANIZATION},
and logged in as %(User)s

The system language is set to %(Language)s.
"""
		if len(info["Organization"]) > 1:
			infotext = infotext.replace("{ORGANIZATION}", " (at %(Organization)s)")
		else:
			infotext = infotext.replace("{ORGANIZATION}", "")
			
		if len(info["Channel"]) > 1:
			infotext = infotext.replace("{CHANNEL}", "Installed from %(Channel)s media\n")
		else:
			infotext = infotext.replace("{CHANNEL}", "")
			
		self.tc.SetValue(infotext % info)
		
	def GetInfo(self):
		# get info available under both wine and real windows
		_Owner              = GetRegistryValue(key="SOFTWARE\Microsoft\Windows NT\CurrentVersion", value="RegisteredOwner")
		_Organization       = GetRegistryValue(key="SOFTWARE\Microsoft\Windows NT\CurrentVersion", value="RegisteredOrganization")
		_ProductName        = GetRegistryValue(key="SOFTWARE\Microsoft\Windows NT\CurrentVersion", value="ProductName")
		_ServicePack        = GetRegistryValue(key="SOFTWARE\Microsoft\Windows NT\CurrentVersion", value="CSDVersion")
		_Bits               = GetBits()
		_Uptime             = GetUptime()
		# WOW64 means we are on a 64bit Windows
		if _Bits == "WOW64":
			_Bits = "64bit"
		if GetWin32APIVendor() == __WIN_WINE__:
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
			else:
				_Channel = "Unknown"
			_User             = unicode(os.environ["USERDOMAIN"])+u"\\"+unicode(os.environ["USERNAME"])
			_Language         = GetSystemLanguage()
	
		# return info as
		if GetWin32APIVendor() ==__WIN_WINE__:
			return {
				"ProductName": _ProductName,
				"ServicePack": _ServicePack,
				"Owner":        _Owner,
				"Organization": _Organization,
				"Win32API":     _Win32API,
				"Bits":         _Bits
				}
		else: #__WINVER__==__WIN_REAL__
			return {
				"ProductName":  _ProductName,
				"ServicePack":  _ServicePack,
				"Version":      _Version,
				"BuildID":      _BuildID,
				"ProductID":    _ProductID,
				"CDKey":        _CDKey,
				"Owner":        _Owner,
				"Organization": _Organization,
				"Uptime":       _Uptime,
				"Bits":         _Bits,
				"Channel":      _Channel,
				"Win32API":     _Win32API,
				"User":         _User,
				"Language":     _Language
			}
		
class WindowsInfoApp(wx.App):
	def getAppIcon(self):
		if WindowsInfo.appIcon == None:
			WindowsInfo.appIcon = wx.EmptyIcon()
			WindowsInfo.appIcon.CopyFromBitmap(
				wx.Bitmap(
					WindowsInfo.appIconFilename,
					wx.BITMAP_TYPE_ANY
				)
			)
		
		return WindowsInfo.appIcon
		
	def __init__(self):
		super(WindowsInfoApp, self).__init__(redirect=False)
		
		"""
		Set WindowsInfo.appIcon - it uses wx.Icon, and this
		class only works if an instance of wx.App was created.
		"""
		WindowsInfo.appIcon = self.getAppIcon()
		
		
	def OnInit(self):
		self.SetAppName("WindowsInfo")
		self.SetVendorName("Malte Bublitz")
		_window_title = "WindowsInfo " + WindowsInfo.version
		_window_title = "WindowsInfo"
		self._frame = WindowsInfoMainFrame(None, _window_title, self)
		self.SetExitOnFrameDelete(True)
		self.SetTopWindow(self._frame)
		return True
		
def main():
	app = WindowsInfoApp()
	app.MainLoop()
	
if __name__=="__main__":
	main()
