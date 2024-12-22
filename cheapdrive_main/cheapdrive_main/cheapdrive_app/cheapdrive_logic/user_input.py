
from multiprocessing import Value
from tkinter import CURRENT
from exceptions import AddressError

def print_out(cost_for_trip, cost_for_refill, fuel_left):
        """
        Prints the trip cost, refill cost, and remaining fuel.
        """
        print(f"You will pay {cost_for_trip:.2f} for the trip, {cost_for_refill:.2f} for the refill, and still have {fuel_left:.2f} liters left.")
def how_much(new_fuel_needed, old_fuel_left,tank):
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
def load_other_data():
     # Validate tank size
    while True:
        try:
            tank = float(input("I would also need your fuel tank maximum capacity (in litres): ").replace(",","."))
            if tank > 0:
                break
            print("Fuel tank maximum capacitymust be a positive number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number for tank capacity.")
    #Validate fuel_type
    while True:
        try:
            fuel_type = int(input("Does your vehicle drive on Diesel or PB95. Type in \"0\" for Diesel or \"1\" for PB95:"))
            if fuel_type==0 or fuel_type==1:
                break
            raise ValueError
        except ValueError:
            
            print("Input invalid. Type in \"0\" for Diesel or \"1\" for PB95. Please try again.")
    # Validate current fuel
    while True:
        try:
            current_fuel = float(input("How much is fuel currently in your vehicle (in litres): ").replace(",","."))
            if 0 <= current_fuel <= tank:
                break
            print(f"Current fuel must be between 0 and {tank} liters. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number for current fuel.")
    # Validate fuel usage
    while True:
        try:
            fuel_usage = float(input("What is an average fuel usage for your vehicle (in litres/100km): ").replace(",","."))
            if 0 <= current_fuel <= tank:
                break
            print(f"Fuel usage must be a positive number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number for fuel usage.")
    
    # Validate price per liter
    while True:
        try:
            bought_for = float(input("And price per liter you paid for your last refuel (in zlotys): ").replace(",","."))
            if bought_for > 0:
                break
            print("Price per liter must be a positive number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number for price per liter.")
    return tank,fuel_type,current_fuel,fuel_usage,bought_for


def load_starting_address():
    # Validate starting address
    while True:
        start_address = input("Type in your starting location: ").strip()
        if start_address:
            break
        print("Starting location cannot be empty. Please try again.")
    return start_address

def load_finishing_address():    
    # Validate finishing address
    while True:
        finish_address = input("Type in your finishing location: ").strip()
        if finish_address:
            break
        print("Finishing location cannot be empty. Please try again.")
    return finish_address

def user_refill_decision():
    print("what to do")
