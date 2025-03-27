from bs4 import BeautifulSoup
import requests

response = requests.get(url="https://news.ycombinator.com/news")
yc_webpage = response.text

soup = BeautifulSoup(yc_webpage, "html.parser")
articles = soup.select(".titleline a")
article_texts = []
article_links = []
for article_tag in articles:
    article_text = article_tag.getText()
    article_link = article_tag.get("href")
    article_texts.append(article_text)
    article_links.append(article_link)
print(article_texts)
print(article_links)
article_upvotes = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]
print(article_upvotes)

index_max = article_upvotes.index(max(article_upvotes))
article_max = article_texts[index_max]
link_max = article_links[index_max]
print(article_max)
print(link_max)
print(index_max)

# from soupsieve import select_one
#
# with open("website.html") as file:
#     contents = file.read()
#
# soup = BeautifulSoup(contents, 'html.parser')
# print(soup.title)
# print(soup.title.name)
# print(soup.title.string)
#
# #print(soup.prettify())
#
# print(soup.a)
# print(soup.p)
# print(soup.li)
#
# all_anchor_tags = soup.find_all(name="a")
# print(all_anchor_tags)
#
# all_paragraphs_tags = soup.find_all(name="p")
# print(all_paragraphs_tags)
#
# for tag in all_anchor_tags:
#     # print(tag.getText())
#     print(tag.get("href"))
#
# heading = soup.find(name="h1", id="name")
# print(heading)
#
# section_heading = soup.find(name="h3", class_="heading")
# print(section_heading.getText)
# print(section_heading.name)
# print(section_heading.get("class"))
#
# company_url = soup.select_one(selector="p a")
# print(company_url)
#
# name = soup.select_one(selector="#name")
# print(name)
#
# heading_class = soup.select(selector=".heading")
# print(heading_class)

