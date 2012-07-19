# -*- coding: utf-8 -*-
# 
# file: WindowsInfo/gui_messagebox.py
# part of: Windows Info
# 
# graphical user interface based on MessagwBoxW function from user32.dll
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
import ctypes
MessageBoxW = ctypes.windll.user32.MessageBoxW

def run():
	_info = SysInfo.GetInfo()
	ctypes.windll.user32.MessageBoxW(
			0,
			"""%(ProductName)s %(Bits)s %(ServicePack)s
a.k.a. Windows NT %(Version)s

Product key: %(CDKey)s 
Installed from %(Channel)s media

Up: %(Uptime)s

Registered to %(Owner)s (%(Organization)s)
""" % _info,
			u'Windows Info',
			0
		)

if __name__=="__main__":
	run()
