
from api_calls import route_to_distance
from exceptions import AddressError
from user_input import load_starting_address,load_finishing_address,load_other_data

def adress_input_manager(start,finish):
    start,finish=load_starting_address(),load_finishing_address()
    while True:
        try:
            distance=route_to_distance(start,finish)  
            print("No address errors found.")
            return distance
        except AddressError as e:
            print(f"Address error: ")
            if(e.address_type=="origin"):
                start=load_starting_address()
            
            elif(e.address_type=="origin"):
                finish=load_finishing_address()
            else:
                start,finish=load_starting_address(),load_finishing_address()
#returns parameters: tank,fuel_type,current_fuel,fuel_usage,bought_for
def other_input_manager():
    return load_other_data()
   
        
