from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service(r"C:\chromedriver-win64\chromedriver.exe")  # Path to chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://laam.pk/nodes/women-gharara-182"
driver.get(url)

# Wait for JavaScript to load
driver.implicitly_wait(10)

# Locate the element using class name
try:
    product_list_container = driver.find_element(By.CLASS_NAME, "product_list_container")
    print("Element found:", product_list_container.find_elements(By.CLASS_NAME, "w-full"))  # Prints the content of the element
except:
    print("Element not found.")

driver.quit()
