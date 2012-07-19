# -*- coding: utf-8 -*-
#
# module: WindowsInfo.i18n
# part of Windows info
#
# quick'n'dirty i18n
#  A very dirty internationalization solution
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

USAGE_HELP_EN = """
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
"""
PARAM_ERROR_EN = """
You told me to do '%s'. But I don't know what you mean by that.
If you run '%s /?', I'll tell you what I can do.
"""
VERSION_INFO_EN = """
Windows Info 0.2.1
------------------
Copyright (c) 2012 Malte Bublitz, https://malte-bublitz.de

I found out the following:
"""
ABOUTBOX_EN = """
<html>
	<body bgcolor="#fff8dc" style="padding: 0;">
		<center>
			<table bgcolor="#deb887" width="100%%" cellspacing="0"
cellpadding="0" border="1">
				<tr>
					<td align="center">
						<h1>Windows Info 0.2.1</h1>
					</td>
				</tr>
			</table>
			<p>
				<b>Windows Info</b> displays useful information about your
				Windows system, like the exact version or the CD Key.
			</p>
			<p>
				<b>Windows Info</b> is brought to you by <b>Malte Bublitz</b>.
			</p>
		</center>
	</body>
</html>
"""
INFOTEXT_EN = """%(ProductName)s %(Bits)s %(ServicePack)s
a.k.a. Windows NT %(Version)s

Product key: %(CDKey)s 
Installed from %(Channel)s media

Up: %(Uptime)s

Registered to %(Owner)s (at %(Organization)s),
and logged in as %(User)s
"""
INFOTEXT_WINE_EN = """%(ProductName)s %(Bits)s %(ServicePack)s
Uses Win32 APIs by: %(Win32API)s

Registered to %(Owner)s (at %(Organization)s)
"""
USAGE_HELP_DE = u"""
Benutzung: WindowsInfo.CLI.exe [/?]
           WindowsInfo.CLI.exe [/q] [/i:Eigenschaft[,Eigenschaft2[,...]]]
           
Optionen:
 /?       Zeigt diesen Hilfetext an.
 /q       Keine Programminformationen anzeigen
 /i       Nur gewählte Informationen anzeigen
 Eigenschaft[...] Kann eine (oder durch Kommata separiert auch mehrere)
                  der Folgenden sein:
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
"""
PARAM_ERROR_DE = u"""
Ich habe dich leider nicht verstanden.
Wenn Du '%s /?' ausführst, werde ich Dir sagen, was ich alles kann.
"""
VERSION_INFO_DE = """
Windows Info 0.2.1
------------------
Copyright (c) 2012 Malte Bublitz, https://malte-bublitz.de

Folgendes habe ich herausgefunden:
"""
ABOUTBOX_DE = """
<html>
	<body bgcolor="#fff8dc" style="padding: 0;">
		<center>
			<table bgcolor="#deb887" width="100%%" cellspacing="0"
cellpadding="0" border="1">
				<tr>
					<td align="center">
						<h1>Windows Info 0.2.1</h1>
					</td>
				</tr>
			</table>
			<p>
				<b>Windows Info</b> zeigt n&uuml;tzliche Informationen &uuml;ber Dein
				Windows-System an, wie z.B. die exakte Version oder den CD-Schl&uuml;ssel.
			</p>
			<p>
				<b>Windows Info</b> wurde zu Dir gebracht von <b>Malte Bublitz</b>.
			</p>
		</center>
	</body>
</html>
"""
INFOTEXT_DE = u"""%(ProductName)s %(Bits)s %(ServicePack)s
alias Windows NT %(Version)s

Produktschlüssel: %(CDKey)s 
Installiert von einem %(Channel)s-Medium

Laufzeit: %(UptimeGerman)s

Lizensiert an %(Owner)s (bei %(Organization)s),
und angemeldet als %(User)s
"""
INFOTEXT_WINE_DE = """%(ProductName)s %(Bits)s %(ServicePack)s
Nutzt die Win32-APIs von: %(Win32API)s

Lizensiert an %(Owner)s (bei %(Organization)s)
"""

class Dirty_i18n(object):
	__language = "english"
	__is_wine = False
	__translations = {
	                  "english": {
	                              "usage": USAGE_HELP_EN,
	                              "param_error": PARAM_ERROR_EN,
	                              "version_info": VERSION_INFO_EN,
	                              "about": "About...",
	                              "aboutbox": ABOUTBOX_EN,
	                              "infotext": INFOTEXT_EN,
	                              "file": "&File",
	                              "exit": "E&xit\tCtrl+Q",
	                              "view": "&View",
	                              "view_normal": "&Normal\tF2",
	                              "view_detail": "&Detailed\tF3",
	                              "view_refresh": "&Refresh\tF5",
	                              "help": "&?",
	                              "help_topics": "&Help\tF1",
	                              "help_about": "About...\tCtrl+F1",
	                              "error_wow64_title": "Error: This is WOW64!",
	                              "error_wow64": "This is a 64-bit Windows. Please use the 64-bit version of WindowsInfo."
	                             },
	                  "german": {
	                              "usage": USAGE_HELP_DE,
	                              "param_error": PARAM_ERROR_DE,
	                              "version_info": VERSION_INFO_DE,
	                              "about": u"Über...",
	                              "aboutbox": ABOUTBOX_DE,
	                              "infotext": INFOTEXT_DE,
	                              "file": "&Datei",
	                              "exit": "Beenden\tCtrl+Q",
	                              "view": "&Anzeige",
	                              "view_normal": "&Normal\tF2",
	                              "view_detail": "&Detailiert\tF3",
	                              "view_refresh": "&Aktualisieren\tF5",
	                              "help": "&?",
	                              "help_topics": "&Hilfe\tF1",
	                              "help_about": u"Über...\tCtrl+F1",
	                              "error_wow64_title": "Fehler: Dies ist WOW64!",
	                              "error_wow64": "Dies ist eine 64-Bit-Version von Windows. Bitte die 64-Bit-Version von WindowsInfo nutzen."
	                            }
	                 }
	def __init__(self, language, is_wine):
		self.__language = language
		self.__is_wine = is_wine
		if self.__is_wine:
			self.__translations["english"]["infotext"] = INFOTEXT_WINE_EN
			self.__translations["german"]["infotext"] = INFOTEXT_WINE_DE
		
	def getTranslation(self, id):
		return self.__translations[self.__language][id]
		