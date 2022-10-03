import requests
import re
from bs4 import BeautifulSoup as bs
from pytube import YouTube 
from multiprocessing import Pool


videos_data = {
	"links": "",
	"title": "",
	"description": "",
	"thumbnail": "",
}

def mult_proc(i):
	sub_vid = {
	'title': [],
	'thumbnail' : []
	}
	try:
			url = i.replace("?modestbranding=1&&autoplay=1", '')
			url = url.replace("https://youtube.com/embed/", '')
			url = f"https://www.youtube.com/watch?v={url}"
			yt = YouTube(url)
			if title := yt.title:
				sub_vid['title'] = title
			else:
				raise "video unavailabe"
			thumb = yt.thumbnail_url
			sub_vid['thumbnail'] = (thumb)
	except:
			sub_vid['links'].remove(i) if i in videos_data['links'] else 1
			print('video unavailabe!!', url)
	return sub_vid

def generate_data():
	videos_data['links'] = []
	videos_data['title'] = []
	videos_data['description'] = []
	videos_data['thumbnail'] = []

	r = requests.get("https://www.youtube.com").text
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

	

	#print("Enumerating videos_data")

	if __name__ == '__main__':
		i = 0
		while i < len(videos_data['links']):
			p = Pool(processes=8)
			pack = [videos_data['links'][j] for j in range(8)]
			res = p.map(mult_proc, pack)
			p.close() 

			print(333)
			for i in res:
				videos_data['title'].append(i['title'])
				videos_data['thumbnail'].append(i['thumb'])
			i += 8
			break
			exit()
			
	
	"""print(f"links {len(videos_data['links'])}")
	print(f"title {len(videos_data['title'])}")
	print(f"thumbnail {len(videos_data['thumbnail'])}")
	print(f"description {len(videos_data['description'])}")"""

	#	ok	""" THE END """

generate_data()
