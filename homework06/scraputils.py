import requests  # type: ignore
from bs4 import BeautifulSoup


def extract_news(parser):
    """Extract news from a given web page"""

    news_list = []

    athing = parser.find_all(class_="athing")
    subtext = parser.find_all(class_="subtext")

    for i in range(len(athing)):
        author = subtext[i].find(class_="hnuser")
        comments = subtext[i].find_all("a")[-1].text.split()[0]
        points = subtext[i].find(class_="score")
        title = athing[i].find(class_="titlelink").text
        url = athing[i].find(class_="titlelink")["href"]
        one_article = {
            "author": author.text if author else "None",
            "comments": int(comments) if comments.isdigit() else 0,
            "points": int(points.string.split()[0]) if points else 0,
            "title": title,
            "url": url if "http" in url else "https://news.ycombinator.com/" + url,
        }
        news_list.append(one_article)
        # print(one_article)

    # print(news_list)
    return news_list


def extract_next_page(parser):
    """Extract next page URL"""
    return parser.find(class_="morelink")["href"]


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


# url = "https://news.ycombinator.com/news?p=1"
# response = requests.get(url)
# soup = BeautifulSoup(response.text, "html.parser")
# news_list = extract_news(soup)

# news_list = get_news("https://news.ycombinator.com/", n_pages=2)
