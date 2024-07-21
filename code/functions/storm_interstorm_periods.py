from adjust_lon_xr_dataset import adjust_lon_xr_dataset
from storm_interstorm_id import storm_interstorm_id
from tqdm.notebook import tqdm
import xarray as xr
import numpy as np
import time

def calc_periods(file_list):
    
    years = np.arange(2012, 2023, 1)
    
    storm_period = np.ndarray([years.size, 361, 1440])
    interstorm_period = np.ndarray([years.size, 361, 1440])    

    for y in tqdm(range(years.size)):
    
        year = years[y]

        print(year)
    
        D = str(year) + '12.nc'
        J = str(year+1) + '01.nc'
        F = str(year+1) + '02.nc'
        
        # choose only the files that are dec, jan or feb
        filtered_files = [file for file in file_list if file.endswith(D) or file.endswith(J) or file.endswith(F)]
        
        # load them into xarray
        ds = xr.open_mfdataset(filtered_files, engine='netcdf4')
        
        # load the dataset
        ds = ds.load()
        
        # as this stage - resample the data to daily resolution, then do the calculations and adjust longitudes
        
        ds_1D = ds.resample(time='1D').mean()
        
        # calculate the wind speed
        ds_1D['ws'] = (('time', 'latitude', 'longitude'), np.sqrt(ds_1D['u10'].data**2 + ds_1D['v10'].data**2))
        
        # Adjust the longitudes to be -180 to 180
        ds_1D = adjust_lon_xr_dataset(ds_1D)
        
        # determine the storm and interstorm periods
        
        for i, ln in enumerate(ds_1D.longitude.data):
        
            for ii, lt in enumerate(ds_1D.latitude.data):
        
                wind_speed_data = ds_1D['ws'].sel(longitude=ln, latitude=lt).data
                
                storm_indices, interstorm_indices = storm_interstorm_id(wind_speed_data, threshold=10)
        
                storm_period[y, ii, i] = np.median([len(s) for s in storm_indices])
                interstorm_period[y, ii, i] = np.median([len(s) for s in interstorm_indices])

    return storm_period, interstorm_period
