import requests
import json
from bs4 import BeautifulSoup

# Function to read the JSON file
def read_json_data(filename='scraped_data.json'):
    try:
        # Open the JSON file and load its content
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Parse the JSON data into a Python object
        return data
    except FileNotFoundError:
        print(f"The file {filename} does not exist.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {filename}.")
        return None


# Function to get the content of a web page
def get_page_content(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract and return the text content of the page
        return soup.get_text()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

# Example usage
data = read_json_data('scraped_data.json')

if data:
    print(f"Total items in JSON: {len(data)}")
    #print(data[:5])  # Print first 5 items for inspection
else:
    print("No data to display.")


for product in data:
    product_title = product["image_alt"]
    product_image_url = product["image_src"]
    product_page_url = product["link"]

    
    content = get_page_content(product)

    if content:
        print("Page Content:")
        print(content[:1000])  # Print the first 1000 characters
