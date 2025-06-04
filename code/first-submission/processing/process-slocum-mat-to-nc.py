import numpy as np
import xarray as xr
from tqdm import tqdm
from datetime import datetime
import scipy.io
import os

print(os.getcwd())

sl = scipy.io.loadmat('../../../data/slocum/soscexstorm2_final_1sec_v2.mat')

# Assuming you have the variables available
tim = sl['time_datenum'].squeeze()
chl = sl['chlorophyll'].squeeze()
lat = sl['latitude'].squeeze()
lon = sl['longitude'].squeeze()
pre = sl['pressure'].squeeze()
sal = sl['salinity'].squeeze()
tem = sl['temperature'].squeeze()
u = sl['u'].squeeze()
v = sl['v'].squeeze()

# Initialize empty arrays
time = np.array([])  
chlorophyll = np.array([])  
latitude = np.array([])  
longitude = np.array([])   
pressure = np.array([])  
salinity = np.array([])  
temperature = np.array([])  
u_velocity = np.array([])  
v_velocity = np.array([])  
profile = np.array([])  
dive = np.array([])  
p = 0
d = -0.5

# For each iteration, add the variables of the profiles to the arrays
for s in tqdm(range(tim.size)):
    p = p + 1
    d = d + 0.5
    dive = np.append(dive, np.tile(d, tim[s].size))
    profile = np.append(profile, p)
    time = np.append(time, tim[s])
    chlorophyll = np.append(chlorophyll, chl[s])
    latitude = np.append(latitude, lat[s])
    longitude = np.append(longitude, lon[s])
    pressure = np.append(pressure, pre[s])
    salinity = np.append(salinity, sal[s])
    temperature = np.append(temperature, tem[s])
    u_velocity = np.append(u_velocity, u[s])
    v_velocity = np.append(v_velocity, v[s])

# Create an xarray dataset with time as the coordinate
ds = xr.Dataset({
    'chlorophyll': (['time'], chlorophyll),
    'latitude': (['time'], latitude),
    'longitude': (['time'], longitude),
    'pressure': (['time'], pressure),
    'salinity': (['time'], salinity),
    'temperature': (['time'], temperature),
    'dive': (['time'], dive),
    'u': (['profile'], u_velocity),
    'v': (['profile'], v_velocity)
}, coords={'time': time, 'profile': profile})

# You can add attributes to the variables or dataset if needed
ds['chlorophyll'].attrs['units'] = 'some unit'
ds.attrs['description'] = 'Slocum dataset with raw variables, no processing applied'

print(ds)

# Save the dataset to a netCDF file with the creation date appended
date_str = datetime.now().strftime('%Y%m%d')
output_filename = f'slocum_processed.nc'
ds.to_netcdf('../../../data/slocum/' + output_filename)
print(f'Dataset saved as {output_filename}')
