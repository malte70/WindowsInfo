# -*- coding: utf-8 -*-
#
# file: /setup.py
# part of: Windows Info
# 
# distutils-style setup.py script using cx_Freeze
# 

# cx_Freeze (http://cx-freeze.sf.net) allows easy building of distutils-like
# setup.py scripts capable of building native executables.
from cx_Freeze import setup, Executable

# Main executable which executes the standard (graphical) interface
WindowsInfo_exe = Executable(
	script                = "WindowsInfo.py",
	base                  = "Win32GUI",
	targetName            = "WindowsInfo.exe",
	icon                  = "WindowsInfo.ico"
)

includes = ["wx", "_winreg"]
setup(
	name         = "Windows Info",
	version      = "0.4",
	description  = "Show information like the CD key or the owner of a Windows operating system copy.",
	author       = "Malte Bublitz",
	author_email = "malte70@tuta.io",
	url          = "https://malte70.github.io/WindowsInfo",
	license      = "License :: OSI Approved :: BSD License",
	options      = {"build_exe": {"includes": includes }},
	executables  = [WindowsInfo_exe]
)
