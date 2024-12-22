from input_manager import adress_input_manager,other_input_manager

from output import visit_message


def hello_user():
    visit_message()
    start="";finish=""
    distance=adress_input_manager(start,finish)
    return start, finish, distance
def vehicle_data():
    return other_input_manager()

