import json
import requests
from bs4 import BeautifulSoup

def get_articles(page_number):
    url = f"https://mises.org/wire?page={page_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []

    for article in soup.find_all('article'):
        title = article.find('h3')
        if title:
            title = title.text.strip()
        else:
            title = None

        tags = article.find('div', class_='article-tags')
        if tags:
            tags_value = [tag.text.strip() for tag in tags.find_all('a')]
        else:
            tags_value = None

        description = article.find('div', class_='text-base')
        if description:
            description = description.text.strip()
        else:
            description = None

        url = article.find('a')['href'] if article.find('a') else None

        articles.append({
            'title': title,
            'tags': tags_value,
            'description': description,
            'url': url  
        })

    return articles

def save_articles_to_json(articles):
    with open('mises_articles.json', 'w') as json_file:
        json.dump(articles, json_file, indent=4)

all_articles = []
for page_number in range(0, 12001):
    print(f"Scraping page {page_number}...")
    articles = get_articles(page_number)
    all_articles.extend(articles)

print("Writing articles to JSON file...")
save_articles_to_json(all_articles)
print("Articles have been saved to mises_articles.json.")
