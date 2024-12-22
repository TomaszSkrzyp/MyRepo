import googlemaps
import os
def adress_to_route(start, finish):
    """
    Constructs a Google Maps directions link from start to finish.
    """
    return f"https://www.google.pl/maps/dir/{'+'.join(start)}/{'+'.join(finish)}/?entry=ttu"