import requests
from selenium import webdriver
import time

def test_requests_get(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    return end_time - start_time

def test_selenium_get(url):
    start_time = time.time()
    driver = webdriver.Chrome()
    driver.get(url)
    end_time = time.time()
    driver.quit()
    return end_time - start_time

if __name__ == "__main__":
    url = "http://wikipedia.com"
    requests_time = test_requests_get(url)
    selenium_time = test_selenium_get(url)
    
    print(f"requests.get took {requests_time} seconds")
    print(f"selenium took {selenium_time} seconds")
