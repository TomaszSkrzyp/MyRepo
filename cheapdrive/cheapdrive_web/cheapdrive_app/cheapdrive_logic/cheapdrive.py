from turtle import distance
from api_calls import route_to_distance
from globals_and_inputs import *
from getting_station import best_station_available
import requests
import re
from bs4 import BeautifulSoup
from hello import hello_user
from input_manager import other_input_manager
from  distance_manager import need_refill 
from input_manager import other_input_manager


def calculate(s_f_distance, avg, cur_fuel, bought_for, start, finish, driver):
    """
    Calculates the costs and remaining fuel for a trip. 
    Handles cases where refueling is or isn't necessary.
    """
    s_f_usage = s_f_distance * avg
    if cur_fuel - s_f_usage > 0:
        print(f"You have enough fuel. At the end, you will have {cur_fuel - s_f_usage:.2f} liters left. Do you want to refill anyway? (Yes/No)")
        if input().strip().lower() != "yes":
            return bought_for * s_f_usage, 0, cur_fuel - s_f_usage
    return calc_problem(cur_fuel, start, finish, driver, bought_for, avg)

def calc_problem(cur_fuel, start, finish, driver, bought_for, avg):
        """
        Finds the best fuel station and calculates the cost of refueling and the trip.
        """
        
        s_g_distance, g_f_distance, station_address, station_name = best_station_available(driver, start, finish, avg)
        new_price = get_price(driver, station_address, station_name)
       
        driver.quit()
        s_g_usage = avg * s_g_distance
        old_fuel_left = cur_fuel - s_g_usage
        new_fuel_needed = max(avg * g_f_distance - old_fuel_left, 0)
        tanked_fuel = how_much(new_fuel_needed, old_fuel_left)
        
        cost_for_trip = (s_g_usage * bought_for) + ((cur_fuel - s_g_usage) * bought_for) + ((g_f_distance - (old_fuel_left / avg)) * avg * new_price)
        cost_for_refill = tanked_fuel * new_price
        fuel_left = tanked_fuel + old_fuel_left - avg * g_f_distance
        
        return cost_for_trip, cost_for_refill, fuel_left,station_address


def get_price(driver,station_adress,station_name):
        """
        Retrieves the price of fuel from a specific fuel station.
        """
        fuel_sites = {
            "ORLEN":"orlen","Orlen": "orlen", "Moya": "moya", "AMIC": "amic", "bp": "bp",
            "Circle": "circle-k", "Shell": "shell", "Lotos": "lotos"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        adress="+".join([i.replace(",","") for i in station_adress.split() if "-" not in i]) #removing postal code from the adress since the search engine on the site i'm using doesn't work well with the full adress 
        session = requests.Session()
        session.headers.update(headers)
        url = f"https://cena-paliw.pl/?s="+adress
        response = session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            site_href = soup.find('header', 'search-entry-header clr').find('a',href=True)['href']
        except:
            site_href=None 
        if site_href is not None:
           
       
            driver.get(site_href)
            price=WebDriverWait(driver, 10).until(EC.presence_of_element_located ((By.CSS_SELECTOR,"#create_tables > tbody > tr > td.cell_index_1-1 > div"))).text.split(" ")
           
            return float(price[0].replace(",","."))
        for key, value in fuel_sites.items():
        
            if key in station_name:
                url = f"https://cena-paliw.pl/grupa/{value}/"
                driver.get(url)
                price=WebDriverWait(driver, 10).until(EC.presence_of_element_located ((By.CSS_SELECTOR,"#create_tables > tbody > tr > td.cell_index_1-1 > div"))).text.split(" ")
              
                return float(price[0].replace(",","."))
            else:
                continue
        url = "https://cena-paliw.pl/grupa/circle-k/"
        driver.get(url)
        price=WebDriverWait(driver, 10).until(EC.presence_of_element_located ((By.CSS_SELECTOR,"#create_tables > tbody > tr > td.cell_index_1-1 > div"))).text.split(" ")

        return float(price[0].replace(",","."))

def main():
    """
    The main function that orchestrates the fuel cost calculation process.
    """
    start,finish, distance=hello_user()
    tank,fuel_type,current_fuel,fuel_usage,bought_for=other_input_manager()
    if not need_refill(distance,current_fuel,fuel_usage):
        print("hell yeah styknie")
    else:
        print(":(") 
    

if __name__ == "__main__":
    main()
