import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

# Define the search query
search_query = input("Please enter the company name: ")
page = 1

BASE_URL = "https://www.trustpilot.com/"


df = pd.DataFrame(columns=['COMPANY_NAME', 'TRUSTSCORE', 'REVIEW_COUNT', 'LOCATION', 'WEBSITE_URL', 'REVIEWS'])

# print(len(data))
# input("press any key to continue")

while True:
    url = f"search?experiment=c&page={page}&query={search_query}"

    response = requests.get(BASE_URL+url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    data = soup.find_all('script', id='__NEXT_DATA__')  
    
    json_data = json.loads(data[0].text)

    company_details = json_data['props']['pageProps']['businessUnits']
    if len(company_details) == 0:
        break

    for company in company_details:
        name = company['displayName']
        reviews = company['numberOfReviews']
        rating = company['trustScore']
        location = company['location'].get('country', None)
        website_url = company['contact']['website']

        df = pd.concat([df, pd.DataFrame([[name, rating, reviews, location, website_url]], columns=['COMPANY_NAME', 'TRUSTSCORE', 'REVIEW_COUNT', 'LOCATION', 'WEBSITE_URL'])], ignore_index=True)

    # print(df)

    data2 = soup.find_all('a', class_='link_internal__7XN06 link_wrapper__5ZJEx styles_linkWrapper__UWs5j')
    # print(data2)
    # input("press any key to continue")

    if len(data2) > 0:
        for datum in data2:
            review_url = datum['href']
            # print(review_url, "review_url########################")
            # input("press any key to continue")
            
            response = requests.get(BASE_URL + review_url)

            soup = BeautifulSoup(response.text, 'html.parser')

            data = soup.find_all('script', id='__NEXT_DATA__')

            json_data = json.loads(data[0].text)

            website_url  =json_data['props']['pageProps']['businessUnit']['websiteUrl']
            print("Getting reviews for: ", website_url)
            
            reviews = json_data['props']['pageProps']['reviews']
            
            review_data = {}
            lst = []
            for review in reviews:
                review_text = review['text']
                rating = review['rating']
                experienced_on = review['dates']['experiencedDate']
                author = review['consumer']['displayName']
                country = review['consumer']['countryCode']
                review_data = {'author': author, 'rating': rating, 'review_text': review_text, 'experienced_on': experienced_on, 'country': country}
                lst.append(review_data)
            
            df['REVIEWS'] = df.apply(lambda x: lst if x['WEBSITE_URL'] == website_url else x['REVIEWS'], axis=1)
            # print(df)
            # input("press any key to continue")
    
    page += 1

df.to_csv('trustpilot.csv', index=False)



