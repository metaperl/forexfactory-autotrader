from bs4 import BeautifulSoup

with open('page.html') as p:
    html = p.read()

soup = BeautifulSoup(html, 'html.parser')

# print(soup.prettify())

for a in soup.find_all('a'):
    href = a.get('href')
    if href and 'list-ticket' in href:
        span = a.contents[1]
        print(a)
        print(span.contents[0])
        symbol, direction, price = span.contents[0].split()
        print(f"{symbol}, {direction}, {price}")
        

