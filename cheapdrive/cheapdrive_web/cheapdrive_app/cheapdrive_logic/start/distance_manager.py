from user_input import load_other_data

def need_refill(distance,current_fuel,fuel_usage):
    if (distance*fuel_usage/100)<(current_fuel):
        return False
    else:
        return True
        