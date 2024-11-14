import requests
import json
from bs4 import BeautifulSoup
import os

# Path to the text file that stores the image ID
ID_FILE_PATH = '.gul-ahmed-data/image_id_iterator.txt'

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
    
def download_image(image_url, save_path):
    try:
        # Send a GET request to fetch the image
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Open a file in binary write mode and save the image
        with open(save_path, 'wb') as file:
            file.write(response.content)
        
        print(f"Image successfully downloaded and saved as {save_path}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the image: {e}")


# Function to read the current image ID from the text file
def get_current_image_id():
    if os.path.exists(ID_FILE_PATH):
        # Read the current ID from the file
        with open(ID_FILE_PATH, 'r', encoding='utf-8') as f:
            return int(f.read().strip())  # Return the ID as an integer
    else:
        # If the file doesn't exist, start with ID 1
        return 0

# Function to update the image ID in the text file
def update_image_id(new_id):
    with open(ID_FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(str(new_id))  # Write the new ID to the file

# Function to get the next image ID
def get_next_image_id():
    current_id = get_current_image_id()
    next_id = current_id + 1
    update_image_id(next_id)
    return next_id


# Function to get the content of a web page
def get_page_content(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract and return the text content of the page
        return soup

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

# Example usage
data = read_json_data('scraped_intermediate_info.json')

if data:
    print(f"Total items in JSON: {len(data)}")
    #print(data[:5])  # Print first 5 items for inspection
else:
    print("No data to display.")


# Initialize an empty list to hold data for the DataFrame
product_data = []

for product in data:
    product_title = product["image_alt"]
    product_image_url = product["image_src"]
    product_page_url = product["link"]

    # Extract image type
    img_type = product_image_url.split(".")[-1].split('?')[0]

    # Generate the file name and save path
    save_path = f"./gul-ahmed-data/images/image{get_current_image_id()}.{img_type}"

    # Download the image
    download_image(product_image_url, save_path)

    # Fetch the product page content
    content = get_page_content(product_page_url)

    # Extract product description
    product_description = content.find('div', class_="product attribute description").find('p').get_text()

    # Find the table with class 'data table additional-attributes'
    table = content.find('table', class_='data table additional-attributes')

    # Extract all rows in the table
    rows = table.find_all('tr')

    # Create an empty dictionary to store the product info
    product_info = {}

    # Iterate through each row and extract the label and corresponding data
    for row in rows:
        label = row.find('th')
        data = row.find('td')
        
        if label and data:
            label_text = label.get_text(strip=True)  # Get text from the label (th)
            data_text = data.get_text(strip=True)    # Get text from the data (td)
            product_info[label_text] = data_text

    # Prepare a dictionary with all product information for DataFrame
    product_dict = {
        'product_title': product_title,
        'product_image_url': product_image_url,
        'product_page_url': product_page_url,
        'product_description': product_description,
        **product_info  # Add the additional product attributes from the table
    }

    # Append the dictionary to the list for DataFrame
    product_data.append(product_dict)

    # Optionally update the image ID after each iteration
    update_image_id(get_current_image_id() + 1)