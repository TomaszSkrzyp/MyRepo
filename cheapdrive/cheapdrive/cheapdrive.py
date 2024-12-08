from globals_and_inputs import *
from getting_station import best_station_available

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
    Rejects cookies on the website if the cookie banner is present.
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
    s_g_distance, g_f_distance, station_loc, station_name = best_station_available(driver, cur_fuel, start, finish, avg)
    new_price = get_price(station_name, driver)
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
    return float(input().strip())

def get_price(station, driver):
    """
    Retrieves the price of fuel from a specific fuel station.
    """
    fuel_sites = {
        "Orlen": "orlen", "Moya": "moya", "AMIC": "amic", "bp": "bp",
        "Circle": "circle-k", "Shell": "shell", "Lotos": "lotos"
    }
    for key, value in fuel_sites.items():
        if key in station:
            driver.get(f"https://cena-paliw.pl/grupa/{value}/")
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.fc-cta-consent.fc-primary-button")
            )).click()
            price = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#create_tables > tbody > tr > td.cell_index_1-1 > div")
            )).text.split(" ")[0]
            return float(price.replace(",", "."))
    driver.get("https://cena-paliw.pl/grupa/circle-k/")
    price = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "#create_tables > tbody > tr > td.cell_index_1-1 > div")
    )).text.split(" ")[0]
    return float(price.replace(",", "."))

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
