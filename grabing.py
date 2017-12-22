from bs4 import BeautifulSoup
from urllib.request import urlopen
import random
import requests

def find_news(case):
	links=[];
	if case=="Наука":
		html_doc = urlopen('https://ukr.media/science/').read()
		soup = BeautifulSoup(html_doc,"lxml")
 
		for link in soup.find_all('a'):
			rep=link.get('href');
			#print(rep)
			if rep.find("science")>0:
				if rep.find("?")<0 and len(rep)>26:
					links.append(rep);				
	elif case=="Спорт":
		html_doc = urlopen('https://sportarena.com/lenta/').read()
		soup = BeautifulSoup(html_doc,"lxml")
 
		for link in soup.find_all('a'):
			rep=str(link.get('href'));
			#print(rep)
			if rep.find("instagram")<0 and rep.find("youtube")<0 and rep.find("telegram")<0 and rep.find("twitter")<0 and rep.find("facebook")<0 and rep.find("wp-login")<0 and rep.find("viber")<0 and rep.find("mailto")<0 and rep.find("tag")<0 and rep.find("contacts")<0 and rep.find("vk.com")<0:
				#print(rep)
				if rep.find("sportarena")>0 and len(rep)>=65:
					#print(rep)
					links.append(rep);
	elif case=="Политика":
		html_doc = urlopen('http://ru.golos.ua/show_articles_list/type/news/category/politika').read()
		soup = BeautifulSoup(html_doc,"lxml")
 
		for link in soup.find_all('a'):
			rep=str(link.get('href'));
			#print(rep)
			if rep.find("politika")>0 and rep.find("show")<0:
				#print(rep)
				links.append(rep);		
	elif case=="Культура":
		html_doc = urlopen('http://www.unn.com.ua/uk/news/culture').read()
		soup = BeautifulSoup(html_doc,"lxml")
 
		for link in soup.find_all('a'):
			rep=str(link.get('href'));
			#print(rep)
			if rep.find("news")>0 and len(rep)>25 and rep.find("instagram")<0 and rep.find("darkoyu")<0:
				#print(rep)
				links.append('http://www.unn.com.ua'+str(rep));
			#	if rep.find("?")<0 and len(rep)>26:
			#		links.append(rep);	
	else:
		return "Не знаю что ты хочешь"		
	#print(links)
	return links[random.randint(0,len(links)-1)]
	
def get_story(tipe):
	if tipe=="ItHappens":
		html = urlopen('http://ithappens.me/').read()
		soup = BeautifulSoup(html,"lxml")

		story_list=[]
	
		for link in soup.find_all('a'):
			story=link.get('href')
			if story.find("story")>0 and story.find(".com")<0 and story.find("add")<0 and story.find(".me")<0:
				story_list.append(story)

		html_doc = urlopen('http://ithappens.me/'+story_list[random.randint(1,len(story_list))]).read()
		soup = BeautifulSoup(html_doc,"lxml")
	

		list_of_story=""
		for text in soup.find_all("p"):
			#text_list.append(text)
			#txt=text.get("content-text")
			text=str(text)
			if text.find("span")<0:
			
				text=text.replace("<p>","")
				text=text.replace("</p>","")
				list_of_story+=text
		return list_of_story;
	elif tipe=="Bash.im":
		headers = {
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
				}
		html = requests.get('http://bash.im/random', headers=headers)
		soup = BeautifulSoup(html.text,"lxml")

		story_list=[]


		for link in soup.find_all('div',{"class":"text"}):
			story_list.append(str(link));
	
	
		story=story_list[random.randint(1,len(story_list))]


		story=story.replace("<br/>","\n")
		story=story.replace('<div class="text">',"")			
		story=story.replace("</div>","\n")
		return story;
		
def get_music():
	headers = {
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
				}
	html = requests.get('http://www.fakemusicgenerator.com/', headers=headers)
	soup = BeautifulSoup(html.text,"lxml")

	music_list=[]
	
	for link in soup.find_all('a'):
		story=link.get('href')
		if story.find("download")>0:
			music_list.append(story)
	
	href='http://www.fakemusicgenerator.com'+music_list[random.randint(1,len(music_list)-1)]
	#print(href)
	music = requests.get(href, headers=headers,stream=True)
	
	#print(music)
	name="";
	name=href[href.find("artist")+len("artist")+1:href.find("track")-1]
	name+=" - "+href[href.find("track")+len("track")+1:href.find("type")-1]+".mp3"
	name=name.replace("+"," ")
	with open(name,"wb") as code:
		music_file=code.write(music.content)
	return name;

def get_comics():
	headers = {
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
				}
	html = requests.get('https://xkcd.ru/random/', headers=headers)
	soup = BeautifulSoup(html.text,"lxml")

	story_true=""
	
	list_of_html=[]
	
	for link in soup.find_all('a'):
		story=link.get('href')
		if story.find("random")>0:
			story_true=story
			break;
			
	for link in soup.find_all('h1'):
		link=str(link)
		link=link.replace("<h1>","")
		link=link.replace("</h1>","")
		list_of_html.append(link)
	
	for link in soup.find_all('div',{"class":"comics_text"}):
		link=str(link)
		link=link.replace('<div class="comics_text">',"")
		link=link.replace("</div>","")
		list_of_html.append(link)
			#story_list.append(str(link));
	
	story_true=story_true[8:len(story_true)-1]
	link='https://xkcd.ru/i/'+story_true+'_v1.png'
	pic=requests.get(link, headers=headers)
	with open(story_true+'.png',"wb") as code:
		img_file=code.write(pic.content)
	list_of_html.append(story_true+'.png')
	return list_of_html;
