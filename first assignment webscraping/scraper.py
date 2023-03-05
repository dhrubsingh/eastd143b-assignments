import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv

base_url = 'http://en.people.cn/90777/'
category = 'World'
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 2, 28)

# end at index6.html
# start from  index47.html

# collect links from People's Daily
def people_daily_links():

    # url:date
    links = {}
    # Iterate over pages until the end date is reached
    page = 47
    while page >= 6:
        url = base_url + 'index{}.html'.format(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all article links on the page
        article_list = soup.find('ul', {'class': 'foreign_list8 cf'})
        if article_list is None:
            print('No article list found on page: ' + url)
            break

        for li in article_list.find_all('li'):
            article_url = base_url + li.a['href']
            article_date_str = li.find('span').text.strip()
            article_date = datetime.strptime(article_date_str, '%Y-%m-%d %H:%M')

            # Exclude articles published on 2023-03-01
            if article_date.date() == datetime(2023, 3, 1).date():
                continue
            
            print(f'URL: {article_url} and date: {article_date}')
            if article_date < start_date:
                # If the article date is before the start date, we're done
                break

            """
            elif article_date <= end_date and category in article_url:
                # If the article date is within the specified range and category, add the link to the list
                print(article_url)
                links.append(article_url)
            """

            links[article_url] = article_date

        
        # Decrement the page number
        page -= 1

        if page < 6:
            break

    return links



def scrape_articles(links):
    with open('articles.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Text', 'Author', 'Date', 'Time'])

        for url in links:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            article_title = soup.select_one('body > div.main > div.w860.d2txtCon.cf > h1')
            if article_title is not None:
                article_title = article_title.text.strip()
            else:
                print("Bad url", url)
                article_title  = article_title = "None"

            article_author = soup.select_one('body > div.main > div.w860.d2txtCon.cf > div.origin.cf > a')
            if article_author is not None:
                article_author = article_author.text.strip()
            else:
                print("Bad url", url)
                article_author = "None"

            article_content = ""

            if soup.select('body > div.main > div.w860.d2txtCon.cf > p') is not None:
                for p in soup.select('body > div.main > div.w860.d2txtCon.cf > p'):
                    article_content += p.text.strip() + "\n"
            else:
                print("Bad url", url)
                article_content = "None"
            
            # Get the date and time of publication
            date = links[url]

            # Write the article information to the CSV file
            writer.writerow([article_title, article_content, article_author, date])

    print('Article information saved to articles.csv')


"""
response = requests.get("http://en.people.cn/n3/2023/0303/c90000-10215655.html")
soup = BeautifulSoup(response.text, 'html.parser')

article_title = soup.select_one('body > div.main > div.w860.d2txtCon.cf > h1').text.strip()
author_name = soup.select_one('body > div.main > div.w860.d2txtCon.cf > div.origin.cf > a').text.strip()
content = ""
for p in soup.select('body > div.main > div.w860.d2txtCon.cf > p'):
    content += p.text.strip() + "\n"


print('Title:', article_title)
print('Author/Title:', author_name)
print('Content:', content)

"""




# Scrape People's Daily
#scrape_articles(people_daily_links())

links = people_daily_links()
scrape_articles(links)




"""
Working code for scraping 1 page
url = 'http://en.people.cn/n3/2023/0103/c90000-10191194.html'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Get the title of the article
title = soup.find('h1').text.strip()

# Get the text content of the article
text = ''
for p in soup.find_all('p'):
    if p.text.strip():
        text += p.text.strip() + '\n'
    

# Get the author(s) of the article
author = soup.find('div', {'class': 'origin cf'}).find('a').text.strip()

# Get the date and time of publication
datetime_str = soup.find('div', {'class': 'origin cf'}).find('span').text.strip()
datetime_parts = datetime_str.split(',')
time = datetime_parts[0]
date = datetime_parts[1].strip()

# Print the scraped information
#print('Title:', title)
#rint('Text:', text)
print('Author(s):', author)
print('Date:', date)
print('Time:', time)
"""






"""
Notes: 

for China Daily, we want to go from http://en.people.cn/90777/index38.html up until the most recent index



def scrape_peoples_daily():
    base_url = 'http://en.people.cn/'
    url = base_url + 'index.html'
    category = 'World'
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 2, 28)

    articles = []
    page = 1
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        article_list = soup.find('ul', {'class': 'list_14'})
        if article_list is None:
            print('Error: no article list found on page: ' + url)
            break

        for li in article_list.find_all('li'):
            article_url = base_url + li.a['href']
            article_date_str = li.find('span').text.strip()
            article_date = datetime.strptime(article_date_str, '%Y-%m-%d %H:%M:%S')
            if article_date < start_date:
                return articles
            elif article_date <= end_date and category in article_url:
                article = scrape_article(article_url)
                if article:
                    articles.append(article)

        next_page = soup.find('a', {'class': 'next_page'})
        if not next_page:
            break
        page += 1
        url = base_url + 'channel' + category + '/index{}.html'.format(page)

    return articles


def scrape_japan_times():
    base_url = 'https://www.japantimes.co.jp/'
    url = base_url + 'category/world/'
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 2, 28)

    articles = []
    page = 1
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        article_list = soup.find('div', {'class': 'article-list'})
        for article in article_list.find_all('article'):
            article_url = article.a['href']
            article_date_str = article.find('time')['datetime']
            article_date = datetime.fromisoformat(article_date_str[:-6])
            if article_date < start_date:
                return articles
            elif article_date <= end_date:
                article = scrape_article(article_url)
                if article:
                    articles.append(article)

        next_page = soup.find('a', {'class': 'pagination-next'})
        if not next_page:
            break
        page += 1
        url = base_url + 'category/world/page/{}'.format(page)

    return articles

def scrape_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1', {'class': 'news_title'}).text.strip()

    author = soup.find('div', {'class': 'autor'}).text.strip()

    article_date_str = soup.find('span', {'class': 'date'}).text.strip()
    article_date = datetime.strptime(article_date_str, '%Y-%m-%d %H:%M:%S')

    content = ''
    for p in soup.find_all('div', {'class': 'box_con'}):
        for tag in p.contents:
            if tag.name == 'p':
                content += tag.text.strip() + ' '

    if content:
        return {'title': title, 'author': author, 'date': article_date, 'content': content}
    else:
        return None
    
def save_to_csv(articles, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'author', 'date', 'content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article in articles:
            writer.writerow(article)

#peoples_daily_articles = scrape_peoples_daily()
#save_to_csv(peoples_daily_articles, 'peoples_daily_articles.csv')

japan_times_articles = scrape_japan_times()
save_to_csv(japan_times_articles, 'japan_times_articles.csv')

"""