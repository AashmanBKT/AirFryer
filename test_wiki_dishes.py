# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, json, time

def get_wiki_image(title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={urllib.parse.quote(title)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'AirFryerCookbookApp/1.0 (contact@culinary.org)'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data['query']['pages']
            for k, v in pages.items():
                if 'original' in v:
                    return v['original']['source']
    except Exception as e:
        return None
    return None

test_dishes = [
    ('Paratha', 'Paratha'),
    ('Uttapam', 'Uttapam'),
    ('Thepla', 'Thepla'),
    ('Handvo', 'Handvo'),
    ('Bread pizza', 'Bread pizza'),
    ('Kathi roll', 'Kati roll'),
    ('Ragi', 'Finger millet'),
    ('Bhindi', 'Fried okra'),
    ('Makhana', 'Euryale ferox'),
    ('Spring roll', 'Spring roll'),
    ('Aloo tikki', 'Aloo tikki'),
    ('Chicken 65', 'Chicken 65'),
    ('Momo', 'Momo (food)'),
    ('Mathri', 'Mathri'),
    ('Kachori', 'Kachori'),
    ('Potato wedges', 'Potato wedges'),
    ('Seekh kebab', 'Seekh kebab'),
    ('Sweet potato', 'Sweet potato'),
    ('Biryani', 'Biryani'),
    ('Pilaf', 'Pilaf'),
    ('Banana chip', 'Banana chip'),
    ('Laddoo', 'Laddu'),
    ('Chikki', 'Chikki')
]

for name, wiki_title in test_dishes:
    img = get_wiki_image(wiki_title)
    print(f"{name} ({wiki_title}) -> {img}")
    time.sleep(0.1)
