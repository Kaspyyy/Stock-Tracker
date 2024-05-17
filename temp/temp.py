from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import requests

# List of symbols
symbols = ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "TSLA", "GOOG", "BRK.B", 
           "META", "UNH", "XOM", "LLY", "JPM", "JNJ", "V", "PG", "MA", "AVGO", 
           "HD", "CVX", "MRK", "ABBV", "COST", "PEP", "ADBE"]

# Base URL
base_url = "https://www.investopedia.com/markets/quote?tvwidgetsymbol="

# Directory to save images
image_directory = "stock_logos"
os.makedirs(image_directory, exist_ok=True)

# Initialize Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Function to download image
def download_image(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            file.write(response.content)

# Iterate over symbols
for symbol in symbols:
    try:
        url = base_url + symbol
        driver.get(url)
        time.sleep(3)  # Wait for the page to load

        # Find the image element
        img_element = driver.find_element(By.CLASS_NAME, 'tv-circle-logo')

        # Extract image URL
        image_url = img_element.get_attribute('src')
        image_path = os.path.join(image_directory, f"media/stock_icon/{symbol}.svg")

        # Download image
        download_image(image_url, image_path)
        print(f"Downloaded logo for {symbol}")

    except Exception as e:
        print(f"Error retrieving logo for {symbol}: {e}")

# Close the WebDriver
driver.quit()
