import requests
from bs4 import BeautifulSoup
from os import mkdir

# url_input = input("Input the URL: ")
url_input = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page="
num_of_pages = int(input()) + 1
type_of_art = input()


for page in range(1, num_of_pages):
    mkdir(f"Page_{page}")

    r = requests.get(f"{url_input}{page}")
    soup = BeautifulSoup(r.content, "html.parser")

    articles = soup.find_all("article")
    for art in articles:

        span = art.find("span", {"data-test": "article.type"})

        if span.text.strip() == type_of_art:
            a = art.find("a", {"data-track-action": "view article", "data-track-label": "link"})
            title = a.text.strip().replace(" ", "_")
            title = "".join(["" if letter in "!\"#$%&'()*+,-./:;<=>?@[\]^`{|}~" else letter for letter in title])

            link = a.get("href")
            print(span.text, title, link)
            r = requests.get(f"https://www.nature.com{link}")

            soup = BeautifulSoup(r.content, "html.parser")

            content = soup.find("div", {"class": "c-article-body main-content"})
            content = bytes(content.text, encoding="utf-8")

            with open(f"Page_{page}/{title}.txt", "wb") as file:
                file.write(content)
