

from globals_and_input import *

from getting_station import best_station_availabile

def driver_setup():
    chrome_options = Options()
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    new_driver = webdriver.Chrome(options=chrome_options)
    return new_driver

def go_through_cookies(driver):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "form:nth-child(2) > div > div > button"))).click()
    
def main(start,finish):
    driver=driver_setup()
    link=get_link(start,finish)
    driver.get(link)
    go_through_cookies(driver)
    s_f_distance=get_distance(driver)
    print(s_f_distance)
    
    cost_for_trip,cost_for_refill,fuel_left=calculate(s_f_distance,avg,cur_fuel,bought_for,start,finish,driver)
    print_out(cost_for_trip,cost_for_refill,fuel_left)
    

    
def calculate(s_f_distance,avg,cur_fuel,bought_for,start,finish,driver):
    s_f_usage=s_f_distance*avg
    if cur_fuel-s_f_usage>0:#enough fuel
        print("you have nough fuel. at the end you will have "+str(cur_fuel-s_f_usage)+" liters of fuel left. DO you want to refill anyway?")
        if input()!="Yes":
            return bought_for*s_f_usage,0,cur_fuel-s_f_usage
        #do dodania- guiowa zgoda
        
        
    cost_for_trip,cost_for_refill,fuel_left=calc_problem(cur_fuel,start,finish,driver,bought_for,avg)
    return cost_for_trip,cost_for_refill,fuel_left     

def calc_problem(cur_fuel,start,finish,driver,bought_for,avg):
    
    s_g_distance,g_f_distance,station_loc,station_name= best_station_availabile(driver,cur_fuel,start,finish,avg)
    new_price=get_price(station_name,driver)
    s_g_usage=avg*s_g_distance
    old_fuel_left=cur_fuel-s_g_usage
    new_fuel_needed=max(avg*g_f_distance-(cur_fuel-s_g_usage),0)#in case no new fuel was used
    
    tanked_fuel=how_much(new_fuel_needed,old_fuel_left)
    cost_for_trip=s_g_usage*bought_for+(cur_fuel-s_g_usage)*bought_for+(g_f_distance-(cur_fuel-s_g_usage)/avg)*avg*new_price
    cost_for_refill=tanked_fuel*new_price
    fuel_left=tanked_fuel+cur_fuel-avg*g_f_distance
    return cost_for_trip,cost_for_refill,fuel_left  
   






def how_much(new_fuel_needed,old_fuel_left):
    minimum=max(new_fuel_needed,0) #in case no new fuel was used
    maximum=tank-old_fuel_left
    print("how much you wanna: you need"+str(minimum ))
    
    return int(input())
    
def get_price(station,driver):
    fuel_sites={"Orlen":"orlen","orlen":"orlen","Moya":"moya","AMIC":"amic","bp":"bp","Circle":"circle-k","Shell":"shell","Lotos":"lotos"}
    
    for v in fuel_sites.keys():
        if v in station:
            driver.get("https://cena-paliw.pl/grupa/"+fuel_sites[v]+"/")
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.fc-consent-root > div.fc-dialog-container > div.fc-dialog.fc-choice-dialog > div.fc-footer-buttons-container > div.fc-footer-buttons > button.fc-button.fc-cta-consent.fc-primary-button"))).click()
   
            price=WebDriverWait(driver, 10).until(EC.presence_of_element_located ((By.CSS_SELECTOR,"#create_tables > tbody > tr > td.cell_index_1-1 > div"))).text.split(" ")
            print (float(price[0].replace(",",".")))
            return float(price[0].replace(",","."))
    driver.get("https://cena-paliw.pl/grupa/circle-k/")
    price=WebDriverWait(driver, 10).until(EC.presence_of_element_located ((By.CSS_SELECTOR,"#create_tables > tbody > tr > td.cell_index_1-1 > div"))).text.split(" ")
    print(float(price[0].replace(",",".")))
    return float(price[0].replace(",","."))
  
            
    
        

    

main(start,finish)
