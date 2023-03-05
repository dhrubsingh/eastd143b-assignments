import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv

base_url = 'http://en.people.cn/90777/'
category = 'World'
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 2, 28)


# list of all the urls that are not formatted correctly
bad_urls = []

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

            links[article_url] = article_date

        # Decrement the page number
        page -= 1

        if page < 6:
            break

    return links


def scrape_peopledaily(links):
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
                bad_urls.append(url)
                continue

            article_author = soup.select_one('body > div.main > div.w860.d2txtCon.cf > div.origin.cf > a')
            if article_author is not None:
                article_author = article_author.text.strip()
            else:
                bad_urls.append(url)
                continue

            article_content = ""

            if soup.select('body > div.main > div.w860.d2txtCon.cf > p') is not None:
                for p in soup.select('body > div.main > div.w860.d2txtCon.cf > p'):
                    article_content += p.text.strip() + "\n"
            else:
                bad_urls.append(url)
                continue
                
            
            # Get the date and time of publication
            date = links[url]

            # Write the article information to the CSV file
            writer.writerow([article_title, article_content, article_author, date])

    print('Article information saved to articles.csv')


# scrape2 = all the articles not formatted the usual way for People's Daily
def scrape2(urls):
    with open('bad_urls.txt', 'w') as f:
        for url in urls:
            f.write(url + '\n')

# Scrape People's Daily
links = people_daily_links()
scrape_peopledaily(links)
scrape2(bad_urls)
