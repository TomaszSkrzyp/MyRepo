from globals_and_inputs import *
from getting_station import best_station_available
import requests
import re
from bs4 import BeautifulSoup

def driver_setup():
    """
    Sets up and returns a Selenium WebDriver with pre-configured options.
    """
    chrome_options = Options()
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    new_driver = webdriver.Chrome(options=chrome_options)
    return new_driver

def go_through_cookies(driver):
    """
    Accepts cookies on the website if the cookie banner is present.
    """
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "form:nth-child(2) > div > div > button")
    )).click()

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
        print(new_price)
        driver.quit()
        s_g_usage = avg * s_g_distance
        old_fuel_left = cur_fuel - s_g_usage
        new_fuel_needed = max(avg * g_f_distance - old_fuel_left, 0)
        tanked_fuel = how_much(new_fuel_needed, old_fuel_left)
        
        cost_for_trip = (s_g_usage * bought_for) + ((cur_fuel - s_g_usage) * bought_for) + ((g_f_distance - (old_fuel_left / avg)) * avg * new_price)
        cost_for_refill = tanked_fuel * new_price
        fuel_left = tanked_fuel + old_fuel_left - avg * g_f_distance
        
        return cost_for_trip, cost_for_refill, fuel_left

def how_much(new_fuel_needed, old_fuel_left):
        """
        Prompts the user to input the amount of fuel they want to buy.
           """
        minimum = max(new_fuel_needed, 0)
        maximum = tank - old_fuel_left
        print(f"How much fuel do you want to refill? You need at least {minimum:.2f} liters.")
        new_fuel=input()
        while float(new_fuel)>maximum or float(new_fuel)<minimum:
            print("Wrong input. Try again!!!") 
            new_fuel=input()
            
        return float(new_fuel)

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
        print(url)
        response = session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(url)
        try:
            site_href = soup.find('header', 'search-entry-header clr').find('a',href=True)['href']
        except:
            site_href=None 
        if site_href is not None:
            print(site_href)
       
            driver.get(site_href)
            price=WebDriverWait(driver, 10).until(EC.presence_of_element_located ((By.CSS_SELECTOR,"#create_tables > tbody > tr > td.cell_index_1-1 > div"))).text.split(" ")
            print (float(price[0].replace(",",".")))
            return float(price[0].replace(",","."))
        for key, value in fuel_sites.items():
            print(station_name)
            if key in station_name:
                url = f"https://cena-paliw.pl/grupa/{value}/"
                driver.get(url)
                price=WebDriverWait(driver, 10).until(EC.presence_of_element_located ((By.CSS_SELECTOR,"#create_tables > tbody > tr > td.cell_index_1-1 > div"))).text.split(" ")
                print (float(price[0].replace(",",".")))
                return float(price[0].replace(",","."))
            else:
                continue
        print("Station brand unknown, using data for Circle-k") 
        url = "https://cena-paliw.pl/grupa/circle-k/"
        driver.get(url)
        price=WebDriverWait(driver, 10).until(EC.presence_of_element_located ((By.CSS_SELECTOR,"#create_tables > tbody > tr > td.cell_index_1-1 > div"))).text.split(" ")
        print (float(price[0].replace(",",".")))
        return float(price[0].replace(",","."))

def main(start, finish):
    """
    The main function that orchestrates the fuel cost calculation process.
    """
    driver = driver_setup()
    link = get_link(start, finish)
    driver.get(link)
    go_through_cookies(driver)
    s_f_distance = get_distance(driver)
    print(f"Total distance from start to finish: {s_f_distance:.2f} km")
    cost_for_trip, cost_for_refill, fuel_left = calculate(s_f_distance, avg, cur_fuel, bought_for, start, finish, driver)
    print_out(cost_for_trip, cost_for_refill, fuel_left)

if __name__ == "__main__":
    main(start, finish)
