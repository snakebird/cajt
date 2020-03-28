# -*- coding: UTF-8 -*-
import sys,re,os
import requests
# import xbmcgui

import cloudscraper

PY3 = sys.version_info >= (3,0,0)
UA= 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'
_cfscrapex = cloudscraper.create_scraper(interpreter='native', browser={'custom': UA})

# dialog = xbmcgui.Dialog()

TIMEOUT=15
sess  = requests.Session()

headers = {
    'User-Agent': UA,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',}
	
# def selectDialog(heading,list):
#     return dialog.select(heading, list)
	
# def inputDialog(heading,type=xbmcgui.INPUT_ALPHANUM):
#     return dialog.input(heading, type=xbmcgui.INPUT_ALPHANUM)
	
	
def getRequests(url,data={},headers=headers):
	if not data:
		resp = sess.get(url, headers = headers, verify=False)
		kuks =''.join(['%s=%s;'%(c.name, c.value) for c in sess.cookies])
		if resp.status_code == 503:
			resp = _cfscrapex.get(url)
			kuks =''.join(['%s=%s;'%(c.name, c.value) for c in _cfscrapex.cookies])
		html = resp.text
	else:
		resp = sess.post(url, headers = headers, data=data,verify=False)
		kuks =''.join(['%s=%s;'%(c.name, c.value) for c in sess.cookies])
		if resp.status_code == 503:
			resp = _cfscrapex.post(url, headers = headers, data=data)
			kuks =''.join(['%s=%s;'%(c.name, c.value) for c in _cfscrapex.cookies])
		html = resp.text
	# if PY3:
	# 	html = html.decode(encoding='utf-8', errors='strict')
	html = html.replace("\'",'"')
	return html,kuks

def PLchar(char):
	if type(char) is not str:
		char=char.encode('utf-8')
	char = char.replace('\\u0105','\xc4\x85').replace('\\u0104','\xc4\x84')
	char = char.replace('\\u0107','\xc4\x87').replace('\\u0106','\xc4\x86')
	char = char.replace('\\u0119','\xc4\x99').replace('\\u0118','\xc4\x98')
	char = char.replace('\\u0142','\xc5\x82').replace('\\u0141','\xc5\x81')
	char = char.replace('\\u0144','\xc5\x84').replace('\\u0144','\xc5\x83')
	char = char.replace('\\u00f3','\xc3\xb3').replace('\\u00d3','\xc3\x93')
	char = char.replace('\\u015b','\xc5\x9b').replace('\\u015a','\xc5\x9a')
	char = char.replace('\\u017a','\xc5\xba').replace('\\u0179','\xc5\xb9')
	char = char.replace('\\u017c','\xc5\xbc').replace('\\u017b','\xc5\xbb')
	char = char.replace('&#8217;',"'")
	char = char.replace('&#8211;',"-")	
	char = char.replace('&#8230;',"...")	
	char = char.replace('&#8222;','"').replace('&#8221;','"')	
	char = char.replace('[&hellip;]',"...")
	char = char.replace('&#038;',"&")	
	char = char.replace('&#039;',"'")
	char = char.replace('&quot;','"').replace('&oacute;','ó').replace('&rsquo;',"'")
	char = char.replace('&nbsp;',".").replace('&amp;','&').replace('&eacute;','e')
	return char	