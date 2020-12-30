import requests

from bs4 import BeautifulSoup

chapter = int(input())
site = str(input())

r = requests.get(site)

soup = BeautifulSoup(r.content, 'html.parser')
anchors = soup.find_all('a')

print(anchors[chapter-1].get('href'))
