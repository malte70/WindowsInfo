# -*- coding: utf-8 -*-
#
# module: WindowsInfo.gui
# part of Windows Info
#
# wxPython-based GUI
#  Default interface since version 0.2.
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

import webbrowser
import wx
import wx.html
import SysInfo
import sys
import os
import _winreg
winreg = _winreg
import i18n

class AboutBox(wx.Dialog):
	def __init__(self, parent, title, htmlpage):
		wx.Dialog.__init__(self, parent, -1, title,)
		html = wx.html.HtmlWindow(self, -1, size=(420, -1))
		if "gtk2" in wx.PlatformInfo:
			html.SetStandardFonts()
		html.SetPage(htmlpage)
		ir = html.GetInternalRepresentation()
		html.SetSize( (ir.GetWidth()+25, ir.GetHeight()+25) )
		self.SetClientSize(html.GetSize())
		self.CentreOnParent(wx.BOTH)
		
class WindowsInfoFrame(wx.Frame):
	def __init__(self, parent, title, parent_app):
		super(WindowsInfoFrame, self).__init__(parent, title=title, size=(430,270))
		self.parent = parent_app
		
		self.i18n = i18n.Dirty_i18n( self.parent.getConfig("language"), SysInfo.__WINVER__==SysInfo.__WIN_WINE__ )
		self.InitUI()
		self.Centre()
		self.Show()
		self.LoadInfo()
		self.OnViewNormal(None)
		
	def InitUI(self):
		#self.SetIcon(wx.Icon("C:\Users\Malte\Documents\WindowsInfo\\build\\exe.win-amd64-2.7\WindowsInfo.exe",wx.BITMAP_TYPE_ICO))
		self.SetIcon(wx.Icon(sys.executable,wx.BITMAP_TYPE_ICO))
		
		menuBar = wx.MenuBar()
		filemenu = wx.Menu()
		menuExit = filemenu.Append(wx.ID_EXIT, self.i18n.getTranslation("exit"), "")
		menuBar.Append(filemenu, self.i18n.getTranslation("file"))
		viewmenu = wx.Menu()
		ID_VIEW_NORMAL = wx.NewId()
		ID_VIEW_DETAILS = wx.NewId()
		menuViewNormal  = viewmenu.Append(wx.NewId(), self.i18n.getTranslation("view_normal"),  "", kind=wx.ITEM_RADIO)
		menuViewDetails = viewmenu.Append(wx.NewId(), self.i18n.getTranslation("view_detail"),  "", kind=wx.ITEM_RADIO)
		viewmenu.AppendSeparator()
		menuViewRefresh = viewmenu.Append(wx.NewId(), self.i18n.getTranslation("view_refresh"))
		menuBar.Append(viewmenu, self.i18n.getTranslation("view"))
		helpmenu = wx.Menu()
		menuHelp = helpmenu.Append(wx.ID_HELP, self.i18n.getTranslation("help_topics"))
		menuAbout = helpmenu.Append(wx.ID_ABOUT, self.i18n.getTranslation("help_about"))
		menuBar.Append(helpmenu, self.i18n.getTranslation("help"))
		self.SetMenuBar(menuBar)
		
		font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FIXED_FONT)
		
		self.tc = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		self.tc.SetFont(font)
		self.tc.SetValue("Loading...")
		self.tc.SetEditable(False)
		self.tc.SetSelection(0,0)
		
		self.Bind(wx.EVT_MENU,       self.OnExit,        menuExit)
		self.Bind(wx.EVT_MENU_RANGE, self.OnViewNormal,  menuViewNormal)
		self.Bind(wx.EVT_MENU_RANGE, self.OnViewDetails, menuViewDetails)
		self.Bind(wx.EVT_MENU,       self.OnViewRefresh, menuViewRefresh)
		self.Bind(wx.EVT_MENU,       self.OnHelp,        menuHelp)
		self.Bind(wx.EVT_MENU,       self.OnAbout,       menuAbout)
		
	def OnExport(self, e):
		pass
		
	def OnExit(self, e):
		self.Close()
		
	def OnHelp(self, e):
		webbrowser.open( os.path.join(self.parent.getConfig("path"),"Help.html") )
		
	def OnAbout(self, e):
		box = AboutBox(self, self.parent.i18n.getTranslation("about"), self.parent.i18n.getTranslation("aboutbox"))
		box.ShowModal()
		box.Destroy()
		
	def LoadInfo(self):
		self.info = SysInfo.GetInfo()
		
	def OnViewNormal(self, e):
		self.tc.SetValue(self.i18n.getTranslation("infotext")  % self.info)
		
	def OnViewDetails(self, e):
		formatted_info = ""
		for key in self.info.keys(): #["ProductName", "Version", "Bits", "ServicePack", "BuildID", "ProductID", "CDKey", "Channel", "Uptime", "Owner", "Organization"]:
			if type(self.info[key]) in [str, unicode]:
				formatted_info += key+": "+self.info[key]+"\n"
		self.tc.SetValue(formatted_info)
		
	def OnViewRefresh(self, e):
		self.LoadInfo()
		self.OnViewNormal(None)
		
class WindowsInfoApp(wx.App):
	def __init__(self):
		super(WindowsInfoApp, self).__init__(redirect=False)
		try:
			print SysInfo.GetBits()
			self.loadConfigFromRegistry()
			self.i18n = i18n.Dirty_i18n( self.getConfig("language"), SysInfo.__WINVER__==SysInfo.__WIN_WINE__  )
		except WindowsError:
			wx.MessageBox( "This is a 64-bit Windows. Please use the 64-bit version of WindowsInfo.", "Error: This is WOW64!", wx.CLOSE|wx.ICON_ERROR)
			sys.exit(1)
		
	def OnInit(self):
		frame = WindowsInfoFrame(None, "Windows Info", self)
		self.SetAppName("Windows Info")
		self.SetExitOnFrameDelete(True)
		self.SetTopWindow(frame)
		self.SetVendorName("Malte Bublitz")
		return True
		
	def loadConfigFromRegistry(self):
		RegKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Malte Bublitz\WindowsInfo")
		# the following isn't flexible, but the windows registry sucks, so this
		# is the best I can do.
		self.config = {
		               "language": winreg.QueryValueEx(RegKey, "InstalledLanguage")[0],
		               "path": winreg.QueryValueEx(RegKey, "Path")[0]
		              }
	def getConfig(self, id):
		self.loadConfigFromRegistry()
		return self.config[id]
		
def main():
	app = WindowsInfoApp()
	app.MainLoop()
	
if __name__=="__main__":
	main()
	
run = main