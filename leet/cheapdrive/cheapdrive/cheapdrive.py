import re
import geopy
def coord_finder(url):
    data=url.split("data")[1]
    coords= re.compile(r'\d{2}[.]\d{4,6}/?').findall(data)
    return (coords[1],coords[0]),(coords[3],coords[2])
def where_look_around(start_crd,finish_crd):
    start_lat=start_crd[0].split(".");start_lon=start_crd[1].split(".")
    finish_lat=finish_crd[0].split(".");finish_lon=finish_crd[1].split(".")
    print(start_lat,start_lon,finish_lat,finish_lon)
def scrape_station(url):
   start_coord,finish_coord=coord_finder(url)
print(float("50.672"))