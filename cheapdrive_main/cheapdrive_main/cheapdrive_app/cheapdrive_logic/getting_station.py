from globals_and_inputs import avg, get_distance,go_and_get_distance, geopy, coord_finder, cur_fuel,WebDriverWait,By,INFINITY,EC,wait_for_word
import requests
import time

def best_station_available(driver,start, finish, avg):
    """
    Identifies the best fuel station based on the shortest distance and available fuel.
    """
    usage_sum = INFINITY
    wait_for_word("data",driver)
    start_crd, finish_crd = coord_finder(driver.current_url)
    chosen_station=[]
    
    for i in range(1, 5):  # Attempt to find a station across four search zones
        driver.get(station_choice(driver,start_crd,finish_crd,i))
        for k in range(3):  # Check three stations per zone
            station_adress,station_crd, station_name = scrape_station(driver, k)
            s_g_distance = go_and_get_distance(driver,get_link(start_crd,station_crd))
            g_f_distance = go_and_get_distance(driver,get_link(station_crd, finish_crd))
         
            if s_g_distance + g_f_distance < usage_sum and 1.2 * s_g_distance * avg < cur_fuel:
                usage_sum = s_g_distance + g_f_distance
                
                chosen_station = [station_adress,station_name]
                
        if usage_sum < 9999:
            print("Stopping search after finding a suitable station.")
            break
    
    return s_g_distance, g_f_distance, chosen_station[0],chosen_station[1]

def scrape_station(driver,k):
    
    element=WebDriverWait(driver, 10).until(EC.visibility_of_element_located
    ((By.CSS_SELECTOR, "#content-container > div:nth-child(9) > div > div > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1) > div > div > div:nth-child(1) > div:nth-child(1) > div:nth-child("+str(3+2*k)+") > div> a:nth-child(1) ")))
    
    station_coord=coord_finder(element.get_attribute("href"))
    station_name=element.get_attribute("aria-label") 
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element)).click()
    station_adress = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "#content-container > div:nth-child(9)>div>div>div:nth-child(1)>div:nth-child(2)>div>div:nth-child(1)>div>div>div:nth-child(9)>div:nth-child(3)>button>div>div:nth-child(2)>div:nth-child(1)"))).text

    return station_adress,station_coord,station_name
   


def station_choice(driver,start_crd,finish_crd,i):
   look_around=where_look_around(start_crd,finish_crd,i)
   driver.get("https://www.google.pl/maps/@"+str(look_around[0])+","+str(look_around[1])+",10z")
   wait_for_word("entry",driver)
   return driver.current_url.split("maps")[0]+"maps/search/gas+station"+driver.current_url.split("maps")[1]


def where_look_around(start_crd, finish_crd, iteration):
    """
    Calculates a mid-point to search for gas stations based on trip distance and fuel capacity.
    """
    start_lat, start_lon = map(float, start_crd)
    finish_lat, finish_lon = map(float, finish_crd)
    
    geo_distance = geopy.distance.distance(start_crd, finish_crd).kilometers
    reachable_distance = (15 - 3 * iteration) / 16 * cur_fuel / avg
    
    ratio = reachable_distance / geo_distance
    look_lat = start_lat + (finish_lat - start_lat) * ratio
    look_lon = start_lon + (finish_lon - start_lon) * ratio
    return look_lat, look_lon
