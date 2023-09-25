import requests
from bs4 import BeautifulSoup
import csv
import json

# Define the search query
search_query = "nestle"

# Initialize lists to store data
discussion_data = []

# Define a function to scrape discussions
def scrape_discussions(search_query):
    page = 1
    while True:
        url = f"https://www.trustpilot.com/search?experiment=c&page={page}&query={search_query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        # input("press any key to continue")

        # Extract discussion data
        discussions = soup.find_all("a", class_="link_internal__7XN06 link_wrapper__5ZJEx styles_linkWrapper__UWs5j")
        # print(discussions)
        # input("press any key to continue")
        if not discussions:
            break

        for discussion in discussions:
            print(discussion)
            input("press any key to continue")
            # Extract company name
            company = discussion.find("p", class_="typography_heading-xs__jSwUz typography_appearance-default__AAY17 styles_displayName__GOhL2").text
            print(company, "company########################")
            input("press any key to continue")

            # Extract rating
            rating = soup.find("span", class_="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_trustScore__8emxJ").text
            print(rating, "rating########################")
            input("press any key to continue")

            # Extract reviews
            reviews = soup.find("p", class_="typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_ratingText__yQ5S7").text
            print(reviews, "reviews########################")
            input("press any key to continue")

            # Store the data in a dictionary
            discussion_info = {
                "Date": date,
                "Title": title,
                # Add other attributes as needed
            }
            discussion_data.append(discussion_info)

        page += 1

# Call the function to start scraping
scrape_discussions(search_query)

# Save the data to a CSV file
with open('trustpilot_discussions.csv', 'w', newline='') as csvfile:
    fieldnames = discussion_data[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for discussion_info in discussion_data:
        writer.writerow(discussion_info)

# Save the data to a JSON file
with open('trustpilot_discussions.json', 'w') as jsonfile:
    json.dump(discussion_data, jsonfile, indent=4)


