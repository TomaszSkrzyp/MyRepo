def print_route_parameters(distance, duration):
    """Prints distance and duration in a user-friendly format on one line.

    Args:
        distance: Distance in kilometers.
        duration: Duration in seconds.
    """

    remaining_time = duration
    time_measures = []
    time_measures_displayed=0
    if (remaining_time>=86400) & (time_measures_displayed<2):  # 1 day = 86400 seconds
        days = remaining_time // 86400
        time_measures.append(f"{days} {'day' if days == 1 else 'days'}")
        remaining_time %= 86400
        time_measures_displayed+=1

    if (remaining_time>= 3600) & (time_measures_displayed<2):  # 1 hour = 3600 seconds
        hours = remaining_time // 3600
        time_measures.append(f"{hours} {'hour' if hours == 1 else 'hours'}")
        remaining_time %= 3600
        
        time_measures_displayed+=1

    if (remaining_time>= 60) & (time_measures_displayed<2):  # 1 minute = 60 seconds
        minutes = remaining_time // 60
        time_measures.append(f"{minutes} {'minute' if minutes == 1 else 'minutes'}")
        remaining_time %= 60
        
        time_measures_displayed+=1

    if (remaining_time>0) & (time_measures_displayed<1):
        time_measures.append("1 minute")
            
        time_measures_displayed+=1

    print(f"Distance of this route: {round(distance)} kilometers, Duration: {' '.join(time_measures)}")
print_route_parameters(4000,1740234)