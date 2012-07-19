# -*- coding: utf-8 -*-
#
# file: /WindowsInfo/cli.py
# module: WindowsInfo.cli
# part of: Windows info
#
# Implementation of a command line interface
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

import SysInfo
import sys
import os
import i18n

USAGE_HELP="""
Usage: %(Script)s [/?]
       %(Script)s [/q] [/i:Key[,Key2[,...]]]

Options:
 /?       Display this usage help
 /q       Do not display program information
 /i       Display only the specified keys
 Key[...] Can be one of these:
            ProductName
            Version
            Bits
            ServicePack
            BuildID
            ProductID
            CDKey
            Channel
            Uptime
            Owner
            Organization
 """ % {"Script": os.path.dirname(sys.argv[0])}

class CLIApp(object):
		_InfoToGet     = ["ProductName", "Version", "Bits", "ServicePack", "BuildID", "ProductID", "CDKey", "Channel", "Uptime", "Owner", "Organization"]
		_AvailableInfo = ["ProductName", "Version", "Bits", "ServicePack", "BuildID", "ProductID", "CDKey", "Channel", "Uptime", "Owner", "Organization"]
		info           = None
		info_formatted = ""
		_be_quiet      = False
		_args          = None
		def __init__(self, args=sys.argv):
			self._args = args
			self.loadConfigFromRegistry()
			#self.i18n = i18n.Dirty_i18n(self.__config.lang)
			self.i18n = i18n.Dirty_i18n("german", SysInfo.__WINVER__==SysInfo.__WIN_WINE__)
			self.parse_args()
			self.get_info()
			self._ = self.i18n.getTranslation
			
		def loadConfigFromRegistry(self):
			pass
		def parse_args(self):
			if len(self._args[1:])>0:
				for arg in self._args[1:]:
					if arg.startswith("/i:"):
						self._InfoToGet = arg[3:].split(",")
					elif arg.startswith("/?"):
						self.usage_help()
						sys.exit(0)
					elif arg.startswith("/q"):
						self._be_quiet = True
					elif arg in self._AvailableInfo:
						self._InfoToGet.append(arg)
					else:
						self.error_param(arg)
						sys.exit(1)
			
		def usage_help(self):
			print self.i18n.getTranslation("usage")
			
		def error_param(self, arg):
			print self.i18n.getTranslation("param_error")
			
		def get_info(self):
			self.info = SysInfo.GetInfo()
			
		def FormatInfo(self):
			for key in self._InfoToGet:
				if type(self.info[key]) in [str, unicode]:
					self.info_formatted += key+": "+self.info[key]+"\n"
			
		def run(self):
			self.FormatInfo()
			if not self._be_quiet:
				print self.i18n.getTranslation("version_info")
			print self.info_formatted
		
def main():
	app = CLIApp()
	app.run()
	
if __name__=="__main__":
	main()