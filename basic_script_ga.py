import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

Driver_path = r'C:\chromedriver-win64\chromedriver.exe'

# Function to initialize the Selenium WebDriver and perform auto-scrolling
def get_full_page_content_with_selenium(url):
    # Set up the Chrome WebDriver
    chrome_options = Options()
    #chrome_options.add_argument('--headless')  # Run in headless mode (optional)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Ensure you have chromedriver installed and set the correct path
    service = Service(Driver_path)  # Update with your chromedriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Open the URL
        driver.get(url)
        
        # Scroll down to the bottom of the page
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)  # Scroll to the bottom
            time.sleep(7)  # Wait for the page to load more content
            
            # Calculate new scroll height and compare with last height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # Exit the loop if no new content is loaded
            last_height = new_height
        
        # Get the page source after scrolling
        page_source = driver.page_source
        return page_source
    
    finally:
        driver.quit()

# Function to extract data from the page content
def extract_data_from_page(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    main_image_divs = soup.find_all('div', class_='item main-image')
    
    data = []
    
    for main_image_div in main_image_divs:
        # Extract the anchor tag and its href
        anchor_tag = main_image_div.find('a')
        image_tag = main_image_div.find('img')
        
        # Get the link and image details
        dedicated_link = anchor_tag['href'] if anchor_tag else None
        image_src = image_tag['data-owlsrc'] if image_tag else None
        image_alt = image_tag['alt'] if image_tag else None

        x = {
            'link': dedicated_link,
            'image_src': image_src,
            'image_alt': image_alt
        }

        data.append(x)
    
    return data

# Function to save data to a JSON file
def save_data_to_json(data, filename='scraped_data.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

# Example usage
url = 'https://www.gulahmedshop.com/women'
page_content = get_full_page_content_with_selenium(url)
data = extract_data_from_page(page_content)

# Save data to JSON file
save_data_to_json(data)

print(f"Total items scraped: {len(data)}")
print(data[:5])  # Print first 5 items for inspection
