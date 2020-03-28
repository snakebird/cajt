# -*- coding: UTF-8 -*-
import sys,re,os
import geturl as gethtml
from geturl import PLchar as PLchar

from cmf3 import parseDOM
from cmf3 import replaceHTMLCodes
from urllib.parse import parse_qs, quote, urlencode, quote_plus
import urllib.parse as urlparse

from pprint import pprint

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'

def ListContent(url,page):
	
	if '/page/' in url:
		nturl = re.sub('page\/\\d+','page/%d'%(int(page)+1),url)
		url = re.sub('page\/\\d+','page/%d'%int(page),url)
	else:
		nturl = url + 'page/%d' %(int(page)+1)
		url = url + 'page/%d' %int(page)
		
	html,kuks = gethtml.getRequests(url)
	npage=[]
	fout=[]
	sout=[]
	
	try:
		pagination = parseDOM(html,'div', attrs={'class': "pagination"})[0]
		if pagination.find( '/page/%d' %(int(page)+1))>-1:
			npage.append({'title':'Następna strona','url':nturl,'image':'','plot':'','page':int(page)+1})
	except:
		pass

	result = parseDOM(html,'div', attrs={'id': "archive-content"})
	result =result[0] if result else html
	links = parseDOM(result,'article', attrs={'id': "post\-.+?"})
	
	for link in links:
		href = parseDOM(link, 'a', ret='href')[0]
		imag = parseDOM(link, 'img', ret='src')[0]
		try:
			tytul = (parseDOM(link, 'h4')[0]).strip(' ')
		except:
			tytul = (parseDOM(link, 'h3')[0]).strip(' ')
		
		if '<h2>' in tytul:
			tytul = (tytul.split('<h2>')[0]).strip(' ')
		opis = parseDOM(link,'div', attrs={'class': "texto"})
		opis = opis[0] if opis else tytul
		genre = re.findall('rel="tag">([^>]+)<',link)
		kateg = ','.join([(x.strip()).lower() for x in genre]) if genre else ''
		metad = parseDOM(link,'div', attrs={'class': "metadata"})
		jak = parseDOM(link,'span', attrs={'class': "quality"})
		jak = jak[0] if jak else ''
		if metad:
			try:
				if'IMDb:' in metad[0]:
					if '/movies/' in 	href:
						if 'view' in metad[0]:
							imdb,year,czas,wysw = re.findall('>([^<]+)<\/span>',metad[0])
						else:
							imdb,year,czas = re.findall('>([^<]+)<\/span>',metad[0])
					else:
						if 'view' in metad[0]:
							imdb,year,wysw = re.findall('>([^<]+)<\/span>',metad[0])
						else:
							imdb,year = re.findall('>([^<]+)<\/span>',metad[0])
				else:
					if '/movies/' in 	href:
						if 'view' in metad[0]:
							year,czas,wysw = re.findall('>([^<]+)<\/span>',metad[0])
						else:
							year,czas = re.findall('>([^<]+)<\/span>',metad[0])
					else:
						if 'view' in metad[0]:
							year,wysw = re.findall('>([^<]+)<\/span>',metad[0])
						else:
							year = re.findall('>([^<]+)<\/span>',metad[0])
			except:
				imdb=''
				year=''
				czas=''
				wysw=''
		else:
			year=''
			try:
				year = re.findall('<span>(.+?)<\/span><\/div>',link)[0]
			except:
				year = '' 
			imdb=''
			czas=''
			wysw=''
		if '/movies/' in 	href:
			fout.append({'title':PLchar(tytul),'url':PLchar(href),'image':PLchar(imag),'plot':PLchar(opis),'year':year,'code':PLchar(jak),'genre':PLchar(kateg)})	
		else:
			sout.append({'title':PLchar(tytul),'url':PLchar(href),'image':PLchar(imag),'plot':PLchar(opis),'year':year,'code':PLchar(jak),'genre':PLchar(kateg)})

	return fout,sout,npage

def getVideo(url):
	out=[]
	html,kuks = gethtml.getRequests(url)
	stream_url=''
	
	result = parseDOM(html,'div', attrs={'id': "playeroptions"})
	if result:
		result=result[0]
		videos = re.findall("<li id=(.+?)<\/li",result,re.DOTALL+re.IGNORECASE)
		for vid in videos:
			
			dpost = re.findall('data\-post="([^"]+)',vid)[0]
			dtype = re.findall('data\-type="([^"]+)',vid)[0]
			dnume = re.findall('data\-nume="([^"]+)',vid)[0]
			host = re.findall('"server">([^<]+)<',vid)[0]
			data = 'action=doo_player_ajax&post=%s&nume=%s&type=%s'%(dpost,dnume,dtype)
			out.append({'href':data,'host':host})
	
		if out:
			if len(out) > 100:
				u = [ x.get('href') for x in  out]
				h = [ x.get('host') for x in  out]
				sel = gethtml.selectDialog("Źródło", h)
				data = out[sel].get('href') if sel>-1 else ''
			else:
				data = out[0].get('href')
			if data:
				headers = {
					'User-Agent': UA,
					'Accept': '*/*',
					'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
					'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
					'X-Requested-With': 'XMLHttpRequest',
					'Origin': 'https://watch-movies.pl',
					'Connection': 'keep-alive',
					'Referer': url,
					'TE': 'Trailers',}

				posturl = 'https://watch-movies.pl/wp-admin/admin-ajax.php'
				html,kuks = gethtml.getRequests(posturl,data=data,headers=headers)
				stream_url = parseDOM(html, 'iframe', ret='src')#[0] 
				stream_url = stream_url[0] if stream_url else ''
			else:
				return stream_url,'quit'
	return stream_url,True


# a, b, c = ListContent('https://watch-movies.pl/release/2020/page/1', 1)

# vid, x = getVideo('https://watch-movies.pl/movies/upadek-grace/')
# pprint(vid)
