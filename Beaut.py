import requests
from bs4 import BeautifulSoup as b
https://www.mathematichka.ru/ege/problems/problem_B10P1.html
URL = ""
r = requests.get(URL)
soup = b(r.text, 'html.parser')
a = [i.text for i in soup.find_all('div', class_='Problem')]

# with open("rr.txt", "w", encoding="UTF-8") as f:
#     for i in a:
#         f.write(i)
with open("rr.txt", "r", encoding="UTF-8") as f:
    for i in f.readlines():
        print(i)