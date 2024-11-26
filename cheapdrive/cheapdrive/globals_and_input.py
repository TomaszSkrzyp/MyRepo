import time
import geopy.distance
import re 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from json.encoder import INFINITY
import re 
from os import read
import time

start="Gawronow 6, 40-750 Katowice".split()
finish="Zlote tarasy, Warszawa".split()
avg=0.078
cur_fuel=13.6
bought_for=6.84
tank=40


def coord_finder(url):
    coords= re.compile(r'\d{2}[.]\d{4,7}/?').findall(url)
    if len(coords)==6:  
        return (coords[3],coords[2]),(coords[5],coords[4])
    elif len(coords)==2:
   
        return (coords[0],coords[1])
    else: 
        print(url)
        raise ValueError('The link provided doesnt contain coord data')

  
   
    print("found station: ",station_adress)
    return station_adress,station_name

def wait_for_word(word,driver):#wait for a word to appear in current url
     while(word not in driver.current_url):
         pass

def get_link(start,finish):
    return "https://www.google.pl/maps/dir/"+"+".join(start)+"/"+"+".join(finish)+"/"+"?entry=ttu"
def get_distance(driver):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#omnibox-directions > div > div:nth-child(2) > div > div > div > div:nth-child(2) > button"))).click()
    driver.refresh()
    wait_for_word("entry",driver)
    distance = WebDriverWait(driver, 10).until(EC.presence_of_element_located
                         ((By.CSS_SELECTOR,"#section-directions-trip-0 > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)"))).text

    distance=distance.replace(",",".").split()
 
    if len(distance[1])==1:
        return float(distance[0])/1000
    return float(distance[0])

def get_distance_and_go(driver,url):#version of get_distance function allowing you to also go to anbother site, given through parameter "url"
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
def print_out(cost_for_trip,cost_for_refill,fuel_left):
    print("you will pay "+str(cost_for_trip)+" for the trip, "+str(cost_for_refill)+" for the refill and still have "+str(fuel_left)+"left")  