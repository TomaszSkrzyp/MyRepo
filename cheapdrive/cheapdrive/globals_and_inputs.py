
from json.encoder import INFINITY
import time
import geopy.distance
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start = "Gawronow 6, 40-750 Katowice".split()
finish = "Zlote tarasy, Warszawa".split()
avg = 0.078  # Average fuel consumption (liters per km)
cur_fuel = 2  # Current fuel in the tank (liters)
bought_for = 6.2  # Fuel price per liter
tank = 40  # Maximum tank capacity (liters)

def coord_finder(url):
    """
    Extracts coordinates from a URL using regex.
    """
    coords = re.compile(r'\d{2}[.]\d{4,7}/?').findall(url)
    if len(coords) == 6:  
        return (coords[3], coords[2]), (coords[5], coords[4])
    elif len(coords) == 2:
        return (coords[0], coords[1])
    else: 
        raise ValueError('The link provided doesn\'t contain coordinate data.')

def wait_for_word(word, driver):
    """
    Waits for a specific word to appear in the current URL.
    """
    while word not in driver.current_url:
        pass

def get_link(start, finish):
    """
    Constructs a Google Maps directions link from start to finish.
    """
    return f"https://www.google.pl/maps/dir/{'+'.join(start)}/{'+'.join(finish)}/?entry=ttu"

def get_distance(driver):
    """
    Retrieves the distance between the start and finish locations using Google Maps.
    """

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "#omnibox-directions > div > div:nth-child(2) > div > div > div > div:nth-child(2) > button"))).click()
    driver.refresh()
    wait_for_word("entry", driver)
    distance_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "#section-directions-trip-0 > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)"))).text
    distance = distance_text.replace(",", ".").split()
    return float(distance[0]) / 1000 if len(distance[1]) == 1 else float(distance[0])

def go_and_get_distance(driver,url):
    """ Version of get_distance function allowing you to also go to anbother site, given through parameter url """
    start_url=driver.current_url
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#omnibox-directions > div > div:nth-child(2) > div > div > div > div:nth-child(2) > button"))).click()
    driver.refresh()
    distance = WebDriverWait(driver, 10).until(EC.presence_of_element_located
                         ((By.CSS_SELECTOR,"#section-directions-trip-0 > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)"))).text

    distance=distance.replace(",",".").split()
 
    driver.get(start_url)
    if len(distance[1])==1:
        return float(distance[0])/1000
    return float(distance[0])

def print_out(cost_for_trip, cost_for_refill, fuel_left):
    """
    Prints the trip cost, refill cost, and remaining fuel.
    """
    print(f"You will pay {cost_for_trip:.2f} for the trip, {cost_for_refill:.2f} for the refill, and still have {fuel_left:.2f} liters left.")
