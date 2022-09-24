import requests,re
from bs4 import BeautifulSoup as bs
from pytube import YouTube 

videos_data = {
	"links": [],
	"title": [],
	"description": [],
	"thumbnail": [],
}

r = requests.get("https://www.youtube.com").text
soup = bs(r, 'lxml')
cont = soup.find_all("script")

ind = [len(str(v)) for i,v in enumerate(cont)]
cont = cont[ind.index(max(ind))]
jsn_text = re.search("var ytInitialData = (.+)[,;](1)",str(cont)).group(1)

cont = jsn_text

for ind, ch in enumerate(cont):
	if ch == 'v' and cont[ind+5] == 'I':
		posl= cont[ind+10:ind+21]
		if len(posl) == 11 and '"' not in posl and '/' not in posl and '\\' not in posl:
			klkl = f"https://youtube.com/embed/{str(posl)}?modestbranding=1&&autoplay=1"
			if klkl not in videos_data["links"]:
				videos_data["links"].append(klkl)
			
print("Enumerating videos_data")
for i in videos_data["links"]:
	try:
		url = i.replace("?modestbranding=1&&autoplay=1", '')
		url = url.replace("https://youtube.com/embed/", '')
		url = f"https://www.youtube.com/watch?v={url}"
		yt = YouTube(url)
		if title := yt.title:
			videos_data["title"].append(title)
		else:
			raise "video unavailabe"
		thumb = yt.thumbnail_url
		videos_data["thumbnail"].append(thumb)
	except:
		videos_data['links'].remove(i)
		print('video unavailabe!!', url)

print(f"links {len(videos_data['links'])}")
print(f"title {len(videos_data['title'])}")
print(f"thumbnail {len(videos_data['thumbnail'])}")
print(f"description {len(videos_data['description'])}")	

#		""" THE END """
