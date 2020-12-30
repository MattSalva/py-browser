import requests

from bs4 import BeautifulSoup

index = int(input())
link = input()

r = requests.get(link)

parsed = BeautifulSoup(r.content, 'html.parser')

subs = parsed.find_all('h2')

print(subs[index].text)
