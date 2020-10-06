#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import urllib.request, urllib.parse, urllib.error
import json

class AcortameShortener ():
	def __init__(self, *args, **kwargs):
		self.name = "acorta.me"
		super(AcortameShortener, self).__init__(*args, **kwargs)

	def _shorten (self, url):
		answer = url
		api = requests.get ("https://acorta.me/api.php?action=shorturl&format=simple&url=" + urllib.parse.quote(url))
		if api.status_code == 200:
			answer = api.text
		return answer

class ClckruShortener ():
	def __init__ (self, *args, **kwargs):
		self.name = "clck.ru"
		super(ClckruShortener, self).__init__(*args, **kwargs)

	def _shorten (self, url):
		answer = url
		api = requests.get ("http://clck.ru/--?url=" + urllib.parse.quote(url))
		if api.status_code == 200:
			answer = api.text
		return answer

class IsgdShortener ():
	def __init__ (self, *args, **kwargs):
		self.name = "Is.gd"
		super(IsgdShortener, self).__init__(*args, **kwargs)

	def _shorten (self, url):
		answer = url
		api = requests.get ("http://is.gd/api.php?longurl=" + urllib.parse.quote(url))
		if api.status_code == 200:
			answer = api.text
		return answer

class RelinkShortener():
	def __init__(self, *args, **kwargs):
		self.name = "rel.ink"
		super(RelinkShortener, self).__init__(*args, **kwargs)

	def _shorten(self, url):
		response = requests.post('https://rel.ink/api/links/', data={"url": url})
		if response.status_code == 201:
			data = json.dumps(response.json())
			output = json.loads(data)
			output = 'https://rel.ink/' + str(output['hashid'])
		else:
			return response.status_code
		return output

class TinyurlShortener ():
	def __init__(self, *args, **kwargs):
		self.name = "TinyURL.com"
		super(TinyurlShortener, self).__init__(*args, **kwargs)

	def _shorten (self, url):
		answer = url
		api = requests.get ("http://tinyurl.com/api-create.php?url=" + urllib.parse.quote(url))
		if api.status_code == 200:
			answer = api.text
		return answer
