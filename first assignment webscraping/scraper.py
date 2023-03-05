import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv

base_url = 'http://en.people.cn/90777/'
category = 'World'
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 2, 28)


# list of all the urls that are not formatted correctly for People's Daily
bad_urls = []

# list of all the urls that are not formatted correctly for Japan Times
bad_urls_japan = []

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
    with open('peoplesdaily.csv', 'w', newline='', encoding='utf-8') as f:
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


# end: https://www.japantimes.co.jp/news/world/page/4/
# start: https://www.japantimes.co.jp/news/world/page/35/
# collect the links from the Japan Times
def japan_times_links():
    base_url = 'https://www.japantimes.co.jp/news/world/page/'

    links = []
    page = 35

    while page >= 4:
        url = base_url + str(page) + '/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select('#wrapper > section > div > div.padding_block > section > article')
        for article in articles:
            article_link = article.select_one('div.content_col > header > hgroup > p > a')['href']
            links.append(article_link)

        page -= 1
    
    return links

# scrapes through every link in Japan times
def scrape_japan_times_articles(links):
    with open('japan_times_articles.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Text', 'Author', 'Date', 'Time'])

        for url in links:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Check if the article date is within the specified range
            article_date_str = soup.select_one('#wrapper > div > div.main_content.content_styles > article > div:nth-child(3) > div.single-upper-meta > div.meta-right > ul > li:nth-child(1) > time')['datetime']
            article_date = datetime.strptime(article_date_str, '%Y-%m-%dT%H:%M:%S%z')
            if article_date.date() < datetime(2023, 1, 1).date() or article_date.date() > datetime(2023, 2, 28).date():
                continue

            # Get the title of the article
            article_title = soup.select_one('#wrapper > div > div.padding_block.single-title > h1')
            if article_title is not None:
                article_title = article_title.text.strip()
            else:
                bad_urls_japan.append(url)
                continue

            # Get the text content of the article
            article_content = ''
            for p in soup.select('#jtarticle > p'):
                article_content += p.text.strip() + '\n'

            # Get the author of the article
            article_author = soup.select_one('#wrapper > div > div.main_content.content_styles > article > div:nth-child(3) > div.single-upper-meta > div.meta-left > ul > li:nth-child(2) > p')

            if article_author is not None:
                article_author = article_author.text.strip()
            else:
                bad_urls_japan.append(url)
                continue

            # Get the date and time of publication
            article_date_str = article_date.strftime('%Y-%m-%d')
            article_time_str = article_date.strftime('%H:%M:%S%z')

            print(f'read {url}')
            # Write the article information to the CSV file
            writer.writerow([article_title, article_content, article_author, article_date_str, article_time_str])

    print('Article information saved to japan_times_articles.csv')




# scrape2 = all the articles not formatted the usual way for People's Daily
def scrape2(urls):
    with open('bad_urls.txt', 'w') as f:
        for url in urls:
            f.write(url + '\n')

            


"""

# test case Japan times
response = requests.get("https://www.japantimes.co.jp/news/2023/01/01/world/global-new-years-celebrations/")
soup = BeautifulSoup(response.text, 'html.parser')

# Check if the article date is within the specified range
article_date_str = soup.select_one('#wrapper > div > div.main_content.content_styles > article > div:nth-child(3) > div.single-upper-meta > div.meta-right > ul > li:nth-child(1) > time')['datetime']
article_date = datetime.strptime(article_date_str, '%Y-%m-%dT%H:%M:%S%z')



 
# Get the title of the article
article_title = soup.select_one('#wrapper > div > div.padding_block.single-title > h1').text.strip()


# Get the text content of the article
article_content = ''
for p in soup.select('#jtarticle > p'):
    article_content += p.text.strip() + '\n'

# Get the author of the article
article_author = soup.select_one('#wrapper > div > div.main_content.content_styles > article > div:nth-child(3) > div.single-upper-meta > div.meta-left > ul > li:nth-child(2) > p').text.strip()

# Get the date and time of publication
article_date_str = article_date.strftime('%Y-%m-%d')
article_time_str = article_date.strftime('%H:%M')

print(article_author, article_title,  article_content, article_date)

"""







# Scrape People's Daily
#links = people_daily_links()
#scrape_peopledaily(links)
#scrape2(bad_urls)

links2 = japan_times_links()
scrape_japan_times_articles(links2)
