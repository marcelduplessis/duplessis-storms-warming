# load function that determines wind direction

import math

def wind_direction(u, v):
    # Ensure that u and v are not both zero to avoid division by zero
    if u == 0 and v == 0:
        return None  # Undefined direction when both components are zero

    # Calculate the wind direction in degrees
    direction_degrees = (math.atan2(v, u) * 180 / math.pi) % 360

    return direction_degrees