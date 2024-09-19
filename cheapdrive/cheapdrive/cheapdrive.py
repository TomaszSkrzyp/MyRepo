from hmac import new
from json.encoder import INFINITY
from pickle import FALSE
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import geopy.distance






start="Gawronow 6, 40-750 Katowice".split()
finish="Zlote tarasy, Warszawa".split()
avg=0.078
cur_fuel=13.6
bought_for=6.84
tank=40

def driver_setup():
    chrome_options = Options()
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    new_driver = webdriver.Chrome(options=chrome_options)
    return new_driver
   

def get_link(start,finish):
    return "https://www.google.pl/maps/dir/"+"+".join(start)+"/"+"+".join(finish)+"/"+"?entry=ttu"
def get_triple_link(start,gas,finish):
    return "https://www.google.pl/maps/dir/"+"+".join(start)+"/"+"+".join(finish)+"/"+"?entry=ttu"

def go_through_cookies(driver):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "form:nth-child(2) > div > div > button"))).click()
    
def main(start,finish):
    driver=driver_setup()
    link=get_link(start,finish)
    driver.get(link)
    go_through_cookies(driver)
    #do dodania: lepsze zliczanie spalania
    s_f_distance=get_distance(driver)
    print(s_f_distance)
    cost_for_trip,cost_for_refill,fuel_left=calculate(s_f_distance,avg,cur_fuel,bought_for,start,finish,driver)
    print_out(cost_for_trip,cost_for_refill,fuel_left)
    
def print_out(cost_for_trip,cost_for_refill,fuel_left):
    print("you will pay "+str(cost_for_trip)+" for the trip, "+str(cost_for_refill)+" for the refill and still have "+str(fuel_left)+"left")  
    
def calculate(s_f_distance,avg,cur_fuel,bought_for,start,finish,driver):
    s_f_usage=s_f_distance*avg
    if cur_fuel-s_f_usage>0:#enough fuel
        print("you have nough fuel. at the end you will have "+str(cur_fuel-s_f_usage)+" liters of fuel left. DO you want to refill anyway?")
        if input()!="Yes":
            return bought_for*s_f_usage,0,cur_fuel-s_f_usage
        #do dodania- guiowa zgoda
        
        
    cost_for_trip,cost_for_refill,fuel_left=calc_prob(cur_fuel,start,finish,driver,bought_for,avg)
    return cost_for_trip,cost_for_refill,fuel_left     

def calc_prob(cur_fuel,start,finish,driver,bought_for,avg):
    
    s_g_distance,g_f_distance,new_price= refill(driver,cur_fuel,start,finish,avg)
    s_g_usage=avg*s_g_distance
    tanked_fuel=how_much(g_f_distance,avg,cur_fuel-s_g_usage)
    new_fuel_used=max(avg*g_f_distance-(cur_fuel-s_g_usage),0)#in case no new fuel was used
    
    cost_for_trip=s_g_usage*bought_for+(cur_fuel-s_g_usage)*bought_for+(g_f_distance-(cur_fuel-s_g_usage)/avg)*avg*new_price
    cost_for_refill=tanked_fuel*new_price
    fuel_left=tanked_fuel+cur_fuel-new_fuel_used
   


def get_distance(driver):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#omnibox-directions > div > div:nth-child(2) > div > div > div > div:nth-child(2) > button"))).click()
    
    distance = WebDriverWait(driver, 10).until(EC.presence_of_element_located
                         ((By.CSS_SELECTOR,"#section-directions-trip-0 > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)"))).text
    distance=distance.replace(",",".")
    distance=distance.split()
  
    if len(distance[1])==1:
        return float(distance[0])/1000
    return float(distance[0])


def refill(driver,cur_fuel,start,finish,avg):
    get_url = station_choice(cur_fuel,avg,driver)
    fuel_sites={}
    usage_sum=INFINITY 
    for i in range(3):
        driver.get(get_url)
        station=scrape_station(i)
        s_g_distance=get_distance(get_link(start,station))
        
        g_f_distance=get_distance(get_link(station,finish))
       
        
        if(s_g_distance+g_f_distance<usage_sum and s_g_distance*avg<cur_fuel):#is it the shortest route and will you drive to the station
            usage_sum=s_g_distance+g_f_distance
            chosen_station=station
        
    new_price=get_price(station)
    return s_g_distance,g_f_distance,new_price




def coord_finder(url):
    
    coords= re.compile(r'\d{2}[.]\d{4,6}/?').findall(url)
    
    return (coords[3],coords[2]),(coords[5],coords[4])

def where_look_around(start_crd,finish_crd,iteration):
    start_lat=float(start_crd[0]);start_lon=float(start_crd[1])
    finish_lat=float(finish_crd[0]);finish_lon=float(finish_crd[1])
    geo_distance=geopy.distance.distance(start_crd,finish_crd).kilometers
    reachable_distance=min(pow(0.75,iteration)*cur_fuel/avg,0.75*geo_distance)
    ratio=reachable_distance/geo_distance
    look_lat=start_lat+(finish_lat-start_lat)*ratio
    look_lon=start_lon+(finish_lon-start_lon)*ratio
    print(look_lat,look_lon)
    return(look_lat,look_lon)
    #matma do znalezenie lat
    
   
    
def station_choice(cur_fuel,avg,driver):
   while "data" not in driver.current_url:
       pass
   url=driver.current_url
   
   start_coord,finish_coord=coord_finder(url)
   look_around=where_look_around(start_coord,finish_coord,1)
   driver.get("https://www.google.pl/maps/@"+str(look_around[0])+","+str(look_around[1])+",10z")
   while "entry" not in driver.current_url:
       pass
   print(driver.current_url.split("maps")[0]+"maps/search/gas+station"+driver.current_url.split("maps")[1])
   return driver.current_url.split("maps")[0]+"maps/search/gas+station"+driver.current_url.split("maps")[1]


    
   
   

def how_much(g_f_distance,avg_g_f,old_fuel_left):
    minimum=max(g_f_distance*avg_g_f-old_fuel_left,0) #in case no new fuel was used
    maksimum=tank-old_fuel_left
    print("how much you wanna")
    new_fuel=10
    return new_fuel
    
    
def get_price(station,driver):
    fuel_prices={}
    for v in station:
        if v in fuel_prices:
            driver.get(fuel_prices[v])
            station=WebDriverWait(driver, 10).until(EC.presence_of_element_located
                         ((By.CSS_SELECTOR,"CENKA PB 95")))
            
            
    
        

    

main(start,finish)
