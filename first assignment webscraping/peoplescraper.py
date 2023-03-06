import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv


titles = []

with open("bad_urls.txt", "r") as file:
    lines = file.readlines()
    for url in lines:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the title
        title = soup.find('h1').text.strip()

        # Extract the author name and date/time
        author_name = soup.find("div", class_="origin cf").get_text().split("(")[1].split(")")[0]
        date = soup.select_one('div.main > div.w860.d2txtCon.cf > div.origin.cf > span').text.strip()

        # Extract the content
        # find all p elements under /html/body/div[1]/div[3]/div[2]


        # find all p elements under body > div.main > div.w860.d2txtCon.cf
        p_elements = soup.select("body > div.main > div.w860.d2txtCon.cf p")

        # combine p elements into a single string
        content = ""
        for p in p_elements:
            content += p.get_text().strip() + "\n"

        # Print the results
        print('Title:', title)
        print('Author:', author_name)
        print('Datetime:', date)
        print('Content:', content)

        titles.append(title)

print(titles)
print(len(titles))



"""
response = requests.get('http://en.people.cn/90777//n3/2023/0217/c90000-10208985.html')
soup = BeautifulSoup(response.text, 'html.parser')


# Extract the title
title = soup.find('h1').text.strip()

# Extract the author name and date/time
author_name = soup.find("div", class_="origin cf").get_text().split("(")[1].split(")")[0]
date = soup.select_one('div.main > div.w860.d2txtCon.cf > div.origin.cf > span').text.strip()


# Extract the content
# find all p elements under /html/body/div[1]/div[3]/div[2]


# find all p elements under body > div.main > div.w860.d2txtCon.cf
p_elements = soup.select("body > div.main > div.w860.d2txtCon.cf p")

# combine p elements into a single string
content = ""
for p in p_elements:
    content += p.get_text().strip() + "\n"

# Print the results
print('Title:', title)
print('Author:', author_name)
print('Datetime:', date)
print('Content:', content)
"""