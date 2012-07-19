# -*- coding: utf-8 -*-
#
# module: WindowsInfo.checkUpdate
# part of: Windows Info
#
# Simple update mechanism
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

import urllib2

class VersionNumber(object):
	_major    = 0
	_minor    = 0
	_revision = 0
	def __init__(self, major, minor, revision=0):
		self._major    = major
		self._minor    = minor
		self._revision = revision
		
	def __repr__(self):
		return '<VersionNumber '+str(self._major)+'.'+str(self._minor)+'.'+str(self._revision)+'>'
		
	def __str__(self):
		return str(self._major)+'.'+str(self._minor)+'.'+str(self._revision)
		
	def setVersion(self, major=None, minor=None, revision=None):
		if major    != None: self._major    = major
		if minor    != None: self._minor    = minor
		if revision != None: self._revision = revision
		
class Update(object):
	_oldVersion = VersionNumber(0, 0, 0)
	_newVersion = VersionNumber(0, 0, 0)
	_releaseNotes = ""
	def __init__(self, oldVersion=None, newVersion=None):
		self._oldVersion = oldVersion
		self._newVersion = newVersion
		
	def __repr__(self):
		return '<Update '+str(self._oldVersion)+'=>'+str(self._newVersion)+'>'
		
	def getOldVersion(self):
		return self._oldVersion
		
	def setOldVersion(self, oldVersion):
		if isinstance(oldVersion, VersionNumber):
			self._oldVersion = oldVersion
		else:
			raise TypeError
		
	def getNewVersion(self):
		return self._newVersion
		
	def setNewVersion(self, newVersion):
		if isinstance(newVersion, VersionNumber):
			self._newversion = newVersion
		else:
			raise TypeError
		
	def getReleaseNotes(self):
		return self._releaseNotes
		
	def setReleaseNotes(self, releaseNotes):
		self._releaseNotes = releaseNotes
	
class UpdateCheck(object):
	url = None
	
	def __init__(self):
		pass
		
	def setUpdateDescriptionURL(self, url):
		self._url = url
		
	def 