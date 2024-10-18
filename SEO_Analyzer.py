#import requests
from bs4 import BeautifulSoup
import nltk
import sys
from nltk.tokenize import word_tokenize
from _datetime import datetime
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import os
os.chmod('/mount/src/stream/chromedriver', 0o755)
def Analyze(url):
    '''if (len(sys.argv) < 1):
        print("URL not found")
    else:
        url = sys.argv[1]'''
    nltk.download('stopwords')
    nltk.download('punkt')
    #url = "https://blog.qima.com/saso/importing-fashion-saudi-arabia"
    #url = input("Enter URL: ")

    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    # Initialize the webdriver (make sure you have the correct driver installed)
    driver = webdriver.Chrome(options=options, executable_path=r'/mount/src/stream/chromedriver')  # Or webdriver.Firefox(), etc.

    # Navigate to the website
    driver.get(url)

    # Wait for a specific element to load (optional, but often helpful)
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    # Get the page source after JavaScript execution (if any)
    html_content = driver.page_source

    # Parse the HTML content with BeautifulSoup
    # page, resources = ghost.wait_for_page_loaded()

    """if response.history:
        for resp in response.history:
            print(resp.status_code, resp.url)
    if response.status_code == 200 or response.status_code == 302 or response.status_code == 301\
        or response.status_code ==307 or response.status_code == 308 or response.status_code == 400:
        print(response.request.headers['User Agent'])"""

#        soup2 = BeautifulSoup(response.content, 'html.parser')
#        soup = BeautifulSoup(soup2.prettify(), 'html.parser')
    soup = BeautifulSoup(html_content, 'html.parser')
    bad = []
    CurrentTime = datetime.today()
    Seconds = CurrentTime.timestamp()
    print("Processing...")
    with open('SEOAnalysis.txt', 'w', encoding='utf-8') as SEOData:
            meta_tags = soup.find_all('meta')
            title = soup.find('title').get_text()
            SEOData.write("TITLE \n")
            SEOData.write(title + '\n')
            metadata = {}
            for tag in meta_tags:
                if "name" in tag.attrs:
                    metadata[tag.attrs["name"]] = tag.attrs["content"]
            print("Title:", title)
            print("Metadata:")
            SEOData.write("METADATA \n")
            for key, value in metadata.items():
                print(f"{key}: {value}")
                SEOData.write(f"{key}: {value} \n")

            # Grab the Headings
            hs = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
            h_tags = []
            print("Headers:")
            SEOData.write("HEADERS\n")
            for h in soup.find_all(hs):
                print(f"{h.name}-->{h.text.strip()}")
                SEOData.write(f"{h.name}-->{h.text.strip()}\n")
                h_tags.append(h.name)
            if 'h1' not in h_tags:
                bad.append("No H1 found!")

            # Extract keywords
            # Grab the text from the body of html
            body = soup.find('body').text

            # Extract all the words in the body and lowercase them in a list
            words = [i.lower() for i in word_tokenize(body)]

            # Grab a list of English stopwords
            sw = nltk.corpus.stopwords.words('english')
            new_words = []

            # Put the tokens which are not stopwords and are actual words (no punctuation) in a new list
            for i in words:
                if i not in sw and i.isalpha():
                    new_words.append(i)

                # Extract the fequency of the words and get the 10 most common ones
                freq = nltk.FreqDist(new_words)
                keywords = freq.most_common(10)

            # Print the results
            print("Keywords:\n")
            SEOData.write("Top 10 KEYWORDS repetition \n")
            for w in keywords:
                print(w)
                SEOData.write(str(w)+'\n')
    print("File successfully generated")

"""else:
#        print(response.status_code)
"""
