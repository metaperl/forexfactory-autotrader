import requests


url = 'https://www.forexfactory.com/ratmach'
r = requests.get(url, allow_redirects=True)

open('ratmach.html', 'wb').write(r.content)
