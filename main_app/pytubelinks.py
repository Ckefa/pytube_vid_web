#!/usr/bin/env python3

import re
from time import time
import requests
from pytube import YouTube
import asyncio


videos_data = {
	"title": [],
    "links": [],
	"thumbnail": [],
}


async def get_title(url) -> {'title': str, 'thumb': str}:
    res = {'title': None, 'link':None, 'thumb': None}
    try:
        yt = YouTube(url)
        if yt.title and yt.thumbnail_url:
            res['link'] = url
            res['title'] = yt.title
            res['thumb'] = yt.thumbnail_url
            return res
        else:
            raise ValueError("Video unavailable")
    except Exception as e:
        print(f'Video unavailable!! {url}: {e}')
    return None

async def fetch_data(url="https://www.youtube.com"):
    tasks = []
    resp = requests.get(url)
    text = resp.text

    pattern = r"watch\?v=.{11}"
    matches = re.findall(pattern, text)

    if matches:
        temp = list(set(matches))
        for i, url in enumerate(temp):
            task = asyncio.create_task(get_title(url))
            tasks.append(task)
        
        for i, task in enumerate(tasks):
            res = await task
            if res.get('link') and res.get('title') and res.get('thumb'):
                videos_data['links'].append(res.get('link'))
                videos_data["title"].append(res.get('title'))
                videos_data['thumbnail'].append(res.get('thumb'))
            

    else:
        print("No video links found.")

if __name__ == "__main__":
    a = time()
    asyncio.run(fetch_data())
    b = time()
    print(videos_data)
    print(f"Time: {b - a}")
