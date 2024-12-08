from globals_and_inputs import avg, get_distance, get_link, geopy, coord_finder, cur_fuel
import requests
from json import INFINITY
def best_station_available(start, finish, avg):
    """
    Identifies the best fuel station based on the shortest distance and available fuel.
    """
    usage_sum = INFINITY
    station_name = ""
    start_crd, finish_crd = coord_finder(get_link(start, finish))
    
    for i in range(1, 5):  # Attempt to find a station across four search zones
        for k in range(3):  # Check three stations per zone
            station, station_name = scrape_station(i, k)
            s_g_distance = get_distance(get_link(start, station))
            g_f_distance = get_distance(get_link(station, finish))
            
            if s_g_distance + g_f_distance < usage_sum and 1.2 * s_g_distance * avg < cur_fuel:
                usage_sum = s_g_distance + g_f_distance
                chosen_station = station
                print("SUCCESS")
            else:
                print("This station is not suitable.")
        if usage_sum < 9999:
            print("Stopping search after finding a suitable station.")
            break
    
    return s_g_distance, g_f_distance, station, station_name
"""
def scrape_station(driver, k):
   
    Scrapes station address and name from Google Maps.
   
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, f"#content-container > div:nth-child(9) > div > div > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1) > div > div > div:nth-child(1) > div:nth-child(1) > div:nth-child({3 + 2 * k}) > div > a:nth-child(1)")
    ))
    station_address = coord_finder(element.get_attribute("href"))
    station_name = element.get_attribute("aria-label")
    return station_address, station_name
def station_choice(driver, start_crd, finish_crd, i):
   
    Returns the search link for gas stations around a calculated mid-point.
   
    look_around = where_look_around(start_crd, finish_crd, i)
    driver.get(f"https://www.google.pl/maps/@{look_around[0]},{look_around[1]},10z")
    wait_for_word("entry", driver)
    return driver.current_url.split("maps")[0] + "maps/search/gas+station" + driver.current_url.split("maps")[1]
    
"""
def scrape_station(zone, k):
    """
    Scrapes station address and name from Google Maps.
    """
    # Simulate scraping with dummy data
    station_address = ("52.2297", "21.0122")
    station_name = f"Station {zone}-{k}"
    return station_address, station_name

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
