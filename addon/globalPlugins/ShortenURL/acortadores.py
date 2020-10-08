# -*- coding: utf-8 -*-
# Copyright (C) 2020 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import urllib.request, urllib.parse
import json

class AcortameShortener :
	def __init__(self, *args, **kwargs):
		self.name = "acorta.me"

	def _shorten (self, url):
		api = urllib.request.urlopen("https://acorta.me/api.php?action=shorturl&format=simple&url=" + urllib.parse.quote(url))
		if api.code == 200:
			text = api.read().decode('utf-8')
			return text

class ClckruShortener :
	def __init__ (self, *args, **kwargs):
		self.name = "clck.ru"

	def _shorten (self, url):
		api = urllib.request.urlopen("http://clck.ru/--?url=" + urllib.parse.quote(url))
		if api.code == 200:
			text = api.read().decode('utf-8')
			return text

class IsgdShortener :
	def __init__ (self, *args, **kwargs):
		self.name = "Is.gd"

	def _shorten (self, url):
		opener = urllib.request.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		api = opener.open("http://is.gd/api.php?longurl=" + urllib.parse.quote(url))
		if api.code == 200:
			text = api.read().decode('utf-8')
			return text

class RelinkShortener:
	def __init__(self, *args, **kwargs):
		self.name = "rel.ink"

	def _shorten(self, url):
		data = urllib.parse.urlencode({"url": url}).encode()
		response = urllib.request.Request("https://rel.ink/api/links/", data=data)
		opener = urllib.request.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		resp = opener.open(response)
		if resp.code == 201:
			text = json.loads(resp.read().decode('utf-8'))
			return "https://rel.ink/" + text["hashid"]

class TinyurlShortener :
	def __init__(self, *args, **kwargs):
		self.name = "TinyURL.com"

	def _shorten (self, url):
		api = urllib.request.urlopen("http://tinyurl.com/api-create.php?url=" + urllib.parse.quote(url))
		if api.code == 200:
			text = api.read().decode('utf-8')
			return text

