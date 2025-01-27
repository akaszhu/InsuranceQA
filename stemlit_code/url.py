from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin, urlparse
import time
from bs4 import BeautifulSoup
import streamlit as st

def get_all_routes(base_url, login_url, username, password):
    print("😂😂",base_url, login_url, username, password)
    visited_urls = set()
    routes = set()

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def login():
        driver.get(login_url)
        time.sleep(2)  # Wait for the page to load

        # Find the username and password input fields and the login button
        username_field = driver.find_element(By.NAME, 'username')  # Adjust the selector as needed
        password_field = driver.find_element(By.NAME, 'password')  # Adjust the selector as needed
        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')  # Adjust the selector as needed

        # Enter the username and password
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Submit the login form
        login_button.click()
        time.sleep(2)  # Wait for the login to complete

    def crawl(url):
        if url in visited_urls:
            return
        visited_urls.add(url)
        try:
            driver.get(url)
            time.sleep(2)  # Wait for the page to load

            # Parse the page content
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for link in soup.find_all('a', href=True):
                
                href = link.get('href')
                if "logout" in href.lower() or "signout" in href.lower() or ".html" in href.lower() or href in routes:
                    continue

                full_url = urljoin(base_url, href)
                print(full_url,"🍊\n")
                if is_valid_url(full_url):
                    routes.add(full_url)
                    st.write(full_url)
                    crawl(full_url)
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    def is_valid_url(url):
        parsed_url = urlparse(url)
        return bool(parsed_url.netloc) and bool(parsed_url.scheme)

    login()
    crawl(base_url)
    driver.quit()
    return routes
