import numpy

def storm_interstorm_id(wind_speed_data, threshold=10):
    storm_indices = []
    interstorm_indices = []

    in_storm_period = False
    in_interstorm_period = False

    for i, speed in enumerate(wind_speed_data):
        if speed >= threshold:
            if not in_storm_period:
                storm_start = i
                in_storm_period = True
                if in_interstorm_period:
                    interstorm_indices.append(list(range(interstorm_start, i)))
                    in_interstorm_period = False
            elif in_interstorm_period:
                interstorm_indices.append(list(range(interstorm_start, i)))
                in_interstorm_period = False
        else:
            if in_storm_period:
                storm_indices.append(list(range(storm_start, i)))
                in_storm_period = False
            if not in_interstorm_period:
                interstorm_start = i
                in_interstorm_period = True

    if in_storm_period:
        storm_indices.append(list(range(storm_start, len(wind_speed_data))))
    if in_interstorm_period:
        interstorm_indices.append(list(range(interstorm_start, len(wind_speed_data))))

    return storm_indices, interstorm_indices