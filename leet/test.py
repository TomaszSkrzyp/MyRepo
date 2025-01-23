import requests
from bs4 import BeautifulSoup
brands = ["circle-k-statoil","amic","lotos","lotos-optima","bp","moya", "auchan", "tesco", "carrefour","olkop","leclerc","intermarche","pieprzyk","huzar","total"]
for brand_name in brands:
    url="https://www.autocentrum.pl/stacje-paliw/"+brand_name
    print(url)
    response = requests.get(url)
    #Initialize BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    diesel_price=0; lpg_price=0; pb95_price=0; pb98_price=0
    # Find all station items
    for fuel in soup.find_all('div', class_='last-prices-wrapper'):
        fuel_type = fuel.find('div', class_='fuel-logo').text.strip()
        print(fuel_type)
        if fuel_type=="pb" :
            
            price_element = fuel.find('div', class_='price-wrapper').text.split()[0]
            pb95_price=price_element
        elif fuel_type=="pb+":
            price_element = fuel.find('div', class_='price-wrapper').text.split()[0]
            pb98_price=price_element
        elif fuel_type=="on" or fuel_type=="on+":
            if fuel_type=="on+" and diesel_price!=0:#not taking on+ price if on price is available
                pass
            else:
                price_element = fuel.find('div', class_='price-wrapper').text.split()[0]
                diesel_price=price_element
        elif fuel_type=="lpg" or fuel_type=="lpg+" :
            if fuel_type=="lpg+" and lpg_price!=0:#not taking lpg+ price if lpg price is available
                pass
            else:
                price_element = fuel.find('div', class_='price-wrapper').text.split()[0]
                lpg_price=price_element
    print(diesel_price,lpg_price,pb95_price,pb98_price)
       