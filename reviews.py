import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

# Define the search query
search_query = "nestle"

BASE_URL = "https://www.trustpilot.com"

url = f"/search?experiment=c&page=1&query={search_query}"

response = requests.get(BASE_URL + url)
soup = BeautifulSoup(response.text, 'html.parser')

data = soup.find_all('a', class_='link_internal__7XN06 link_wrapper__5ZJEx styles_linkWrapper__UWs5j')
# print(data)
# input("press any key to continue")

if len(data) > 0:
    for datum in data:
        review_url = datum['href']
        # print(review_url, "review_url########################")
        # input("press any key to continue")
        
        response = requests.get(BASE_URL + review_url)

        soup = BeautifulSoup(response.text, 'html.parser')

        data = soup.find_all('script', id='__NEXT_DATA__')

        json_data = json.loads(data[0].text)

        website_url  =json_data['props']['pageProps']['businessUnit']['websiteUrl']
        
        reviews = json_data['props']['pageProps']['reviews']
        for review in reviews:
            review_text = review['text']
            rating = review['rating']
            experienced_on = review['dates']['experiencedDate']
            author = review['consumer']['displayName']
            country = review['consumer']['countryCode']