

from globals_and_input import avg,INFINITY,get_distance,get_distance_and_go,get_link,geopy,coord_finder,wait_for_word,WebDriverWait,EC,By,cur_fuel



def best_station_availabile(driver,cur_fuel,start,finish,avg):
    usage_sum=INFINITY
    station_name=""
    while("data" not in driver.current_url):
        pass
    start_crd,finish_crd=coord_finder(driver.current_url)
    for i in range(1,5): #3 proby wyboru miejsca wokol ktorego bedziy szukac stacji
        driver.get(station_choice(driver,start_crd,finish_crd,i))
        for k in range(3): #sprawdznie 3 stacji
            station,station_name=scrape_station(driver,k)
            s_g_distance=get_distance_and_go(driver,get_link(start,station))
            print(s_g_distance)
            g_f_distance=get_distance_and_go(driver,get_link(station,finish))
            print(g_f_distance)
            if(s_g_distance+g_f_distance<usage_sum and 1.2*s_g_distance*avg<cur_fuel):#is it the shortest route and will you drive to the station,20% margin of error
                usage_sum=s_g_distance+g_f_distance
                chosen_station=station
                print("SUCCESS")
            else:
                print("this one is a failure")
        if(usage_sum<9999):
            print("not looking anymore")
            break
    
    return s_g_distance,g_f_distance,station,station_name
    
   
  
def scrape_station(driver,k):
    element=WebDriverWait(driver, 10).until(EC.visibility_of_element_located
    ((By.CSS_SELECTOR, "#content-container > div:nth-child(9) > div > div > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1) > div > div > div:nth-child(1) > div:nth-child(1) > div:nth-child("+str(3+2*k)+") > div> a:nth-child(1) ")))
    station_adress=coord_finder(element.get_attribute("href"))
    station_name=element.get_attribute("aria-label")    
    return station_adress,station_name
   


def station_choice(driver,start_crd,finish_crd,i):
   look_around=where_look_around(start_crd,finish_crd,i)
   driver.get("https://www.google.pl/maps/@"+str(look_around[0])+","+str(look_around[1])+",10z")
   wait_for_word("entry",driver)
   return driver.current_url.split("maps")[0]+"maps/search/gas+station"+driver.current_url.split("maps")[1]


def where_look_around(start_crd,finish_crd,iteration):
    
    start_lat=float(start_crd[0]);start_lon=float(start_crd[1])
    finish_lat=float(finish_crd[0]);finish_lon=float(finish_crd[1])
    
    geo_distance=geopy.distance.distance(start_crd,finish_crd).kilometers
   
    reachable_distance=(15-3*iteration)/16*cur_fuel/avg
    print("looking "+str(reachable_distance)+" from the spot")
    ratio=reachable_distance/geo_distance
    print(ratio)
    look_lat=start_lat+(finish_lat-start_lat)*ratio
    look_lon=start_lon+(finish_lon-start_lon)*ratio
    print("looking around",look_lat,look_lon)
    return(look_lat,look_lon)
    #matma do znalezenie lat
    
