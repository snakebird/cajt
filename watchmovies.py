# -*- coding: UTF-8 -*-
import sys,re,os
import geturl as gethtml
from geturl import PLchar as PLchar

if sys.version_info >= (3,0,0):
# for Python 3
    from cmf3 import parseDOM
    from cmf3 import replaceHTMLCodes
    from urllib.parse import parse_qs, quote, urlencode, quote_plus
    import urllib.parse as urlparse
else:
    # for Python 2
    from cmf2 import parseDOM
    from cmf2 import replaceHTMLCodes
    from urllib import unquote, quote, urlencode, quote_plus
    import urlparse

basurl='https://watch-movies.pl/'
UA= 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'

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

def SelectList(typ):
	if 'gatunek' in typ:
	
		label =["Akcja","Akcja i Przygoda","Animacja","Dokumentalny","Dramat","Familijny","Fantasy","film TV","Historyczny","Horror","Komedia","Kryminał","Muzyczny","Przygodowy","Romans","Sci-Fi","Sci-Fi &amp; Fantasy","Tajemnica","Thriller","Western","Wojenny"]
		value =["https://watch-movies.pl/genre/akcja/page/1","https://watch-movies.pl/genre/akcja-i-przygoda/page/1","https://watch-movies.pl/genre/animacja/page/1","https://watch-movies.pl/genre/dokumentalny/page/1","https://watch-movies.pl/genre/dramat/page/1","https://watch-movies.pl/genre/familijny/page/1","https://watch-movies.pl/genre/fantasy/page/1","https://watch-movies.pl/genre/film-tv/page/1","https://watch-movies.pl/genre/historyczny/page/1","https://watch-movies.pl/genre/horror/page/1","https://watch-movies.pl/genre/komedia/page/1","https://watch-movies.pl/genre/kryminal/page/1","https://watch-movies.pl/genre/muzyczny/page/1","https://watch-movies.pl/genre/przygodowy/page/1","https://watch-movies.pl/genre/romans/page/1","https://watch-movies.pl/genre/sci-fi/page/1","https://watch-movies.pl/genre/sci-fi-fantasy/page/1","https://watch-movies.pl/genre/tajemnica/page/1","https://watch-movies.pl/genre/thriller/page/1","https://watch-movies.pl/genre/western/page/1","https://watch-movies.pl/genre/wojenny/page/1"]
		nazwa = "Wybierz gatunek"
		
	elif 'rok' in typ:
		label =["2020","2019","2018","2017","2016","2015","2014","2013","2012","2011","2010","2009","2008","2007","2006","2005","2004","2003","2002","2001","2000","1999","1998","1997","1996","1995","1994","1993","1992","1991","1990","1989","1988","1987","1985","1984","1983","1982","1981","1980","1979","1978","1977","1976","1975","1974","1973","1971","1969","1967"]
		value =["https://watch-movies.pl/release/2020/page/1","https://watch-movies.pl/release/2019/page/1","https://watch-movies.pl/release/2018/page/1","https://watch-movies.pl/release/2017/page/1","https://watch-movies.pl/release/2016/page/1","https://watch-movies.pl/release/2015/page/1","https://watch-movies.pl/release/2014/page/1","https://watch-movies.pl/release/2013/page/1","https://watch-movies.pl/release/2012/page/1","https://watch-movies.pl/release/2011/page/1","https://watch-movies.pl/release/2010/page/1","https://watch-movies.pl/release/2009/page/1","https://watch-movies.pl/release/2008/page/1","https://watch-movies.pl/release/2007/page/1","https://watch-movies.pl/release/2006/page/1","https://watch-movies.pl/release/2005/page/1","https://watch-movies.pl/release/2004/page/1","https://watch-movies.pl/release/2003/page/1","https://watch-movies.pl/release/2002/page/1","https://watch-movies.pl/release/2001/page/1","https://watch-movies.pl/release/2000/page/1","https://watch-movies.pl/release/1999/page/1","https://watch-movies.pl/release/1998/page/1","https://watch-movies.pl/release/1997/page/1","https://watch-movies.pl/release/1996/page/1","https://watch-movies.pl/release/1995/page/1","https://watch-movies.pl/release/1994/page/1","https://watch-movies.pl/release/1993/page/1","https://watch-movies.pl/release/1992/page/1","https://watch-movies.pl/release/1991/page/1","https://watch-movies.pl/release/1990/page/1","https://watch-movies.pl/release/1989/page/1","https://watch-movies.pl/release/1988/page/1","https://watch-movies.pl/release/1987/page/1","https://watch-movies.pl/release/1985/page/1","https://watch-movies.pl/release/1984/page/1","https://watch-movies.pl/release/1983/page/1","https://watch-movies.pl/release/1982/page/1","https://watch-movies.pl/release/1981/page/1","https://watch-movies.pl/release/1980/page/1","https://watch-movies.pl/release/1979/page/1","https://watch-movies.pl/release/1978/page/1","https://watch-movies.pl/release/1977/page/1","https://watch-movies.pl/release/1976/page/1","https://watch-movies.pl/release/1975/page/1","https://watch-movies.pl/release/1974/page/1","https://watch-movies.pl/release/1973/page/1","https://watch-movies.pl/release/1971/page/1","https://watch-movies.pl/release/1969/page/1","https://watch-movies.pl/release/1967/page/1"]
		nazwa = "Wybierz rok"

	sel = gethtml.selectDialog(nazwa, label)
	if sel>-1:
		kategoria = value[sel]# if sel>-1 else ''
		return kategoria
	else:
		quit()
def splitToSeasons(episodes):
    out={}
    seasons = [x.get('season') for x in episodes]
    for s in set(seasons):
        out['Sezon %02d'%s]=[episodes[i] for i, j in enumerate(seasons) if j == s]
    return out	
	
def getSerial(url):

	html,kuks = gethtml.getRequests(url)
	resultmain = parseDOM(html,'div', attrs={'class': "content"})[0]
	tytul = parseDOM(resultmain,'h1')[0]
	
	genros = parseDOM(resultmain,'div', attrs={'class': "sgeneros"})[0]
	genre = re.findall('rel="tag">([^>]+)<',genros)
	kateg = ','.join([(x.strip()).lower() for x in genre]) if genre else ''
	
	widinfo = parseDOM(html,'div', attrs={'id': "info"})[0]

	opis = parseDOM(widinfo,'p')
	opis = opis[0] if opis else ''

	result = parseDOM(html,'div', attrs={'id': "seasons"})[0]

	sezony = parseDOM(result,'div', attrs={'class': "se\-c"})
	episodes=[]
	for sezon in sezony:
		tytsez = parseDOM(sezon,'span', attrs={'class': "title"})
		ses = re.findall('Season\s*(\d+)',tytsez[0],re.IGNORECASE)
		ses = ses[0] if ses else '0'
		eps = parseDOM(sezon,'li', attrs={'class': "mark\-.+?"})
		for ep in eps:
			tyt2 = parseDOM(ep, 'a')[0] 
			href = parseDOM(ep, 'a', ret='href')[0]  
			episd = parseDOM(ep,'div', attrs={'class': "numerando"})
			epis = re.findall('\-\s*(\d+)',episd[0])
			rys = parseDOM(ep, 'img', ret='src')[0]  
			tyt1 = 'S%02dE%02d'%(int(ses),int(epis[0]))
			tyt = '%s - (%s) %s'%(tytul,tyt1,tyt2)
			episodes.append({'title':PLchar(tyt),'url':PLchar(href),'image':rys,'plot':PLchar(opis),'genre':PLchar(kateg),'season':int(ses),'episode':int(epis[0])})
			
	seasons = splitToSeasons(episodes)
	return seasons

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
			if len(out) > 1:
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

def ListSearch(url,page):	
	d = gethtml.inputDialog(u'Szukaj...')
	fout=[]
	sout=[]
	npage=[]

	if d:
		url=basurl+'?s='+d
		html,kuks = gethtml.getRequests(url)
		
		links = parseDOM(html,'div', attrs={'class': "result\-item"})
		for link in links:
			tytdane = parseDOM(link,'div', attrs={'class': "title"})[0]
			tytul = parseDOM(tytdane, 'a')[0]
			href = parseDOM(link, 'a', ret='href')[0]
			imag = parseDOM(link, 'img', ret='src')[0]
			year = parseDOM(link,'span', attrs={'class': "year"})
			year = year[0] if year else ''
			opis = parseDOM(link, 'p')#[0]
			opis = opis[0] if opis else tytul
			if '/seriale/' in href:
				sout.append({'title':PLchar(tytul),'url':PLchar(href),'image':PLchar(imag),'plot':PLchar(opis),'year':year})
			else:
				fout.append({'title':PLchar(tytul),'url':PLchar(href),'image':PLchar(imag),'plot':PLchar(opis),'year':year})
	return fout,sout,npage
