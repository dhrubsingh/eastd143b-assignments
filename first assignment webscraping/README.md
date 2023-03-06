# Obtaining data from web assignment

This repository contains all the necessary code required to complete the first assignment for EASTD 143B. The *requirements.txt* file contains all the programming dependencies needed to run this project locally on your computer.

Furthermore, *japan_times_articles.csv* is a file that contains all the scraped data, from January 1, 2023 to February 28, 2023 from [Japan Times](https://www.japantimes.co.jp/) in the "World" category. It's important to note that, because this newspaper puts articles on a paywall, the scraper I wrote is only able to scrape the available pargarpahs before the paywall.

Similarly, *pepoples_daily_articles.csv* is a file that contains all the scraped data, from January 1, 2023 to February 28, 2023 from [People's Daily Online](http://en.people.cn/) in the "World" category. 

The scraping script for both Japan Times and People's Daily Online can be found on *scraper.py* which has comments to help explain the logic and structure for scraping the two different websites. 

It was important to note here, that while scraping for the articles for People's Daily Online, there were several articles not formatted in the same way as most of the articles during this time period. The URLs to these articles can be found in *bad_urls.txt* and the respective scraping script for these specific articles is found in *peoplescraper.py*. I then appended these scraped results to *pepoples_daily_articles.csv* to complete the scraping assignment. 