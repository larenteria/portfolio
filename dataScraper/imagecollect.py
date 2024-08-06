"""

This script collects images from Google Image Search based on a search query.

Credits: 
    The building blocks of this code was inspired and tweaked from the following source: 
        https://oxylabs.io/blog/how-to-scrape-google-images
"""

import hashlib
import io
import os
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pathlib import Path
from PIL import Image
import base64
from urllib.parse import urljoin, quote

""" CHANGE THESE GLOBAL VARIABLES """

# The variable for the search query
    # Example: "roger federer playing tennis" (Try changing it!)
images_of = "roger federer playing tennis"

"""END OF GLOBAL VARIABLES"""

# Make the Google Image search URL
query = quote(images_of)
URL = f"https://www.google.com/search?q={query}&tbm=isch"

# Create a folder based on the search query in the same repo as this script
folder_name = f"{images_of.replace(' ', '_')}_images"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Instantiate WebDriver
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get(URL)

# Wait for the images to load (max 10 sec)
try:
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img")))
except Exception as err:
    print(f"Error waiting for images to load: {err}")
    driver.quit()

# Get the page content
content = driver.page_source
soup = BeautifulSoup(content, "html.parser")
driver.quit()

# Get the URL of the images
def gets_url(tag, attribute, source):
    results = []
    for img in soup.findAll(tag, attrs={attribute: True}):
        url = img.get(source)
        if url and url not in results:
            # Make sure the URL is complete
            url = urljoin(URL, url)
            results.append(url)
    return results

# Save the images
def save_image(image_content, file_path):
    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert("RGB")
        image.save(file_path, "PNG", quality=80)
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    returned_results = gets_url("img", "src", "src")
    for b in returned_results:
        try:
            # Handle base64 image
            if b.startswith("data:image"):  
                
                base64_data = b.split(",")[1]
                image_content = base64.b64decode(base64_data)
            # Handle normal URL
            else:    
                image_content = requests.get(b).content
            
            file_path = Path(folder_name, hashlib.sha1(image_content).hexdigest()[:10] + ".png")
            save_image(image_content, file_path)
        except Exception as e:
            print(f"Error processing image {b}: {e}")
