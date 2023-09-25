import requests

search_query = "nestle"

# Define the URL you want to access
url = "https://www.trustpilot.com/search?experiment=c&page=4&query=nestle"


try:
    # Send a GET request to the URL
    response = requests.get(url)
    print(response.status_code)
    print(response.text)
    input("press any key to continue")

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the content of the response
        print(response.text)
    else:
        print(f"Failed to fetch the URL. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {str(e)}")



