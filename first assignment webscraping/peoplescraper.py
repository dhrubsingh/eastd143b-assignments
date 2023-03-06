import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv


titles = []

with open("bad_urls.txt", "r") as file, open("peoples_daily_articles.csv", "a", newline="", encoding="utf-8") as csv_file:
    # create CSV writer object
    fieldnames = ["Title", "Text", "Author", "Date and Time"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    lines = file.readlines()
    for url in lines:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the title
        title = soup.find('h1').text.strip()

        # Extract the author name and date/time
        author_name = soup.find("div", class_="origin cf").get_text().split("(")[1].split(")")[0]
        date = soup.select_one('div.main > div.w860.d2txtCon.cf > div.origin.cf > span').text.strip()
        date_time_obj = datetime.strptime(date, '%H:%M, %B %d, %Y')
        date_time_str = date_time_obj.strftime('%Y-%m-%d %H:%M:%S')
       
        # find all p elements under body > div.main > div.w860.d2txtCon.cf
        p_elements = soup.select("body > div.main > div.w860.d2txtCon.cf p")

        # combine p elements into a single string
        content = ""
        for p in p_elements:
            content += p.get_text().strip() + "\n"

        # Write the article information to CSV file
        writer.writerow({"Title": title, "Text": content, "Author": author_name, "Date and Time": date_time_str})