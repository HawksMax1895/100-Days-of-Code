import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇
response = requests.get(URL)
movies_website = response.text

soup = BeautifulSoup(movies_website, "html.parser")
titles = [item.getText() for item in soup.find_all(name="h3", class_="title")]
reversed_titles = list(reversed(titles))

with open("movies.txt", "w", encoding="utf-8") as file:
    for item in reversed_titles:
        file.write(item)
        file.write(item + "\n")

