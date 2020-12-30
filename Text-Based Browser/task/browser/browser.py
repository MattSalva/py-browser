import os
import sys
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore, init

init(autoreset=True)

# nytimes_com = '''
# This New Liquid Is Magnetic, and Mesmerizing

# Scientists have created “soft” magnets that can flow
# and change shape, and that could be a boon to medicine
# and robotics. (Source: New York Times)


# Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

# Jessica Wade has added nearly 700 Wikipedia biographies for
#  important female and minority scientists in less than two
#  years.

# '''

# bloomberg_com = '''
# The Space Race: From Apollo 11 to Elon Musk

# It's 50 years since the world was gripped by historic images
#  of Apollo 11, and Neil Armstrong -- the first man to walk
#  on the moon. It was the height of the Cold War, and the charts
#  were filled with David Bowie's Space Oddity, and Creedence's
#  Bad Moon Rising. The world is a very different place than
#  it was 5 decades ago. But how has the space race changed since
#  the summer of '69? (Source: Bloomberg)


# Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

# Twitter and Square Chief Executive Officer Jack Dorsey
#  addressed Apple Inc. employees at the iPhone maker’s headquarters
#  Tuesday, a signal of the strong ties between the Silicon Valley giants.
# '''

# write your code here
# init la variable que recibe los argumentos
args = sys.argv
# se guarda el argument [1] que es el dir_name siendo [0] el file name
dir_name = args[1]

# se crea el dir con el argumento, si ya existe no tira error por eso el exist_ok=True
os.makedirs(dir_name, exist_ok=True)

# se crea la estructura de historial de paginas con deque() vacio
history = deque()


# se llena el historial con una página ya en cache
def in_cache(filename):
    with open(dir_name + '/' + filename) as f:
        print(f.read())
    history.append(filename)


# se agrega la nueva pagina a la lista de paginsa y al historial
def new_site(content, filename):
    print(content)
    with open(dir_name + '/' + filename, 'w') as f:
        f.write(content)
        history.append(filename)


# Loop para ingresar paginas (funcionamiento de la app constante hasta que el user salga)
while True:
    sitename = input('Write domain')

    if sitename == 'exit':
        break

    elif sitename == 'back':
        if history:
            history.pop()
            # ultimo elemento de history es len(history) - 1
            in_cache(history[len(history) - 1])

    # Chequea si es una url valida (cantidad de .)
    elif sitename.find('.') < 0:
        print('Error: Incorrect URL')

    else:

        if sitename.find('https://') < 0:
            site = requests.get('https://' + sitename)
        else:
            site = requests.get(sitename)

        site.encoding = 'utf-8'
        # Guarda el filename (nytimes.com => nytimes)
        filename = sitename.split('.')[0]

        parsed_site = BeautifulSoup(site.content, 'html.parser')
        sitetext = ''
        tags = ['p', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title']
        for tag in parsed_site.find_all():
            if tag.name in tags and tag.name == 'a':
                sitetext += (Fore.BLUE + tag.get_text())
            elif tag.name in tags:
                sitetext += tag.get_text()

        if os.path.exists(os.path.join(dir_name, filename)):
            in_cache(filename)
        else:
            new_site(sitetext, filename)

        # # Chequea si existe el site en el path, si existe lo agrega al historial y muestra, sino crea el file, agrega al historial y muestra
        # if sitename == 'nytimes.com':
        #     if os.path.exists(dir_name + '/' + filename):
        #         in_cache(filename)
        #     else:
        #         new_site(nytimes_com, 'nytimes')

        # elif sitename == 'bloomberg.com':
        #     if os.path.exists(dir_name + '/' + filename):
        #         in_cache(filename)
        #     else:
        #         new_site(bloomberg_com, 'bloomberg')

        # else:
        #print('Error: Incorrect URL')