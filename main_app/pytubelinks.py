import requests
import re
from bs4 import BeautifulSoup as bs
from pytube import YouTube 
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed


videos_data = {
	"links": "",
	"title": "",
	"description": "",
	"thumbnail": "",
}

def mult_proc(i):
	val = ["", ""]
	try:
		url = i.replace("?modestbranding=1&&autoplay=1", '')
		url = url.replace("https://youtube.com/embed/", '')
		url = f"https://www.youtube.com/watch?v={url}"
		yt = YouTube(url)
                #pass
		if yt.title:
			val[0] = yt.title
		else:
			raise "video unavailabe"
		thumb = yt.thumbnail_url
		val[1] = thumb
	except:
		if i in videos_data['links']:
			videos_data['links'].remove(i) 
		print('video unavailabe!!', url)
		return [None, None]
	return val

def generate_data():
	videos_data['links'] = []
	videos_data['title'] = []
	videos_data['description'] = []
	videos_data['thumbnail'] = []

	r = requests.get("https://www.youtube.com", stream=True).text
	soup = bs(r, 'lxml')
	cont = soup.find_all("script")

	ind = [len(str(v)) for i,v in enumerate(cont)]
	#print(len(ind))

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

	j = 0
	L = len(videos_data['links'])
	with ThreadPoolExecutor() as tpe: 
		pack = [videos_data['links'][k] for k in range(L)]
		futures = tpe.map(mult_proc, pack)

		for i in futures:
			if i[0]:
				videos_data['title'].append(i[0])
			if i[1]:
				videos_data["thumbnail"].append(i[1])

	print("Done!!!")
	print(len(videos_data['title']), "videos rendered")
	
	
#generate_data()
#	ok	""" THE END """

