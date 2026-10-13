# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, json

def search_commons(query):
    q = urllib.parse.quote(query)
    url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={q}&gsrnamespace=6&gsrlimit=5&prop=imageinfo&iiprop=url&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'AirFryerCookbook/1.0 (culinary-project)'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            for k, v in pages.items():
                if 'imageinfo' in v and v['imageinfo']:
                    u = v['imageinfo'][0]['url']
                    if any(u.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
                        return u
    except Exception as e:
        print(f"Err {query}: {e}")
        return None
    return None

test_queries = ['Gujiya', 'Handvo', 'Sabudana Vada', 'Aloo Tikki', 'Paneer Tikka', 'Kachori', 'Malai Kofta', 'Shakarpara', 'Besan Ladoo', 'Banana chips']
for q in test_queries:
    print(q, "->", search_commons(q))
