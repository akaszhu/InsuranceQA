from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def scrape_pages(base_url, login_url, username, password, urls):
    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Open the login URL
    driver.get(login_url)

    # Wait for the page to load
    time.sleep(3)

    # Find the username and password input fields and the login button
    username_field = driver.find_element(By.NAME, 'username')  # Adjust the selector as needed
    password_field = driver.find_element(By.NAME, 'password')  # Adjust the selector as needed
    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')  # Adjust the selector as needed

    # Enter the username and password
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Submit the login form
    login_button.click()

    # Wait for the login process to complete
    time.sleep(5)

    # Dictionary to store the scraped data
    scraped_data = {}

    # Loop through each URL and scrape data
    for url in urls:
        # Navigate to the target page
        driver.get(url)

        # Wait for the page to load
        time.sleep(3)

        # Scrape the entire HTML content of the page
        html_content = driver.page_source

        # Store the scraped HTML content in the dictionary
        scraped_data[url] = html_content

    # Close the WebDriver
    driver.quit()

    # Return the collected data
    return scraped_data[urls[0]]
