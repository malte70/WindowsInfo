# -*- coding: utf-8 -*-
#
# file: /setup.py
# part of: Windows Info
# 
# distutils-style setup.py script using cx_Freeze
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

# cx_Freeze (http://cx-freeze.sf.net) allows easy building of distutils-like
# setup.py scripts capable of building native executables.
from cx_Freeze import setup, Executable

# Main executable which executes the standard (graphical) interface
WindowsInfo_exe = Executable(
    script = "WindowsInfo.pyw",
    targetName = "WindowsInfo.exe",
    base = "Win32GUI",
    compress = True,
    copyDependentFiles = True,
    appendScriptToExe = False,
    appendScriptToLibrary = False,
    icon = "WindowsInfo.ico"
    )

setup(
        name         = "Windows Info",
        version      = "0.3",
        description  = "Show information like the CD key or the owner of a Windows operating system copy.",
        author       = "Malte Bublitz",
        author_email = "me@malte-bublitz.de",
        url          = "http://windowsinfo.malte-bublitz.de",
		  download_url = "http://windowsinfo.malte-bublitz.de/download/",
		  license      = "License :: OSI Approved :: BSD License",
        executables  = [WindowsInfo_exe]
        )
