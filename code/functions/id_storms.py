import numpy as np

def id_storms(ds, wind_var='ws'):

    # Identify storms by taking the wind speed as 10 m/s or larger for 8 hours or more

    storm_locs = np.arange(ds.time.size)[ds[wind_var]>10]  # Find the indices where wind speed is greater than 10 m/s

    # Finding consecutive groups

    consecutive_storm_locs = np.split(storm_locs, np.where(np.diff(storm_locs) != 1)[0] + 1)  # Split the indices into groups where consecutive indices differ by 1

    # Merging groups with a difference of two or less indices

    merged_groups = [consecutive_storm_locs[0]]  # Initialize with the first group

    for group in consecutive_storm_locs[1:]:
        if group[0] - merged_groups[-1][-1] <= 8:  # If the difference between the first index of the current group and the last index of the last group is less than or equal to 8
            merged_groups[-1] = np.concatenate((merged_groups[-1], group))  # Merge the current group with the last group
        else:
            merged_groups.append(group)  # Otherwise, add the current group as a new group

    merged_storms = []
    
    for i in range(len(merged_groups)):
        if len(merged_groups[i]) > 12:  # If the length of the group is greater than 12
            merged_storms.append(merged_groups[i])  # Add the group to the list of merged storms

    # Append the indices of the merged storms to the storms_idx array

    storms_idx = np.array([])

    for s in range(len(merged_storms)):
        storms_idx = np.append(storms_idx, merged_storms[s])  

    # Initialize an array of zeros with the same size as the time dimension

        storms = np.zeros(ds.time.size)  

    # Set the indices corresponding to storms to 1

    storms[storms_idx.astype(int)]=1  

    # Add the storms array to the dataset as a new variable

    ds['storms'] = (('time'), storms)  

    ds['storms'].attrs['long_name'] = 'Boolean value for the presence of storm conditions (>10 m/s winds for 8 consecutive hours). 0 = non storm, 1 = storm.'  # Add a long_name attribute to the storms variable

    return ds, merged_storms