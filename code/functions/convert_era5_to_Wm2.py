import calendar
import warnings
import numpy as np
import xarray as xr

def convert_era5_to_Wm2(data, var_name, data_freq='hour'):

    """Convert ERA5 data from J m^-2 to W m^-2.
    
    This function takes ERA5 data in Joules per square meter (J m^-2) and converts it to Watts per square meter (W m^-2). The conversion is based on the data frequency, which can be either 'hour' or 'month'.     For hourly data, it divides the values by 3600 to obtain W m^-2, while for monthly data, it accounts for the number of days in each month.
    
    Parameters:
        data (xarray.Dataset): ERA5 data in a dataset format.
        var_name (list): List of variable names to convert.
        data_freq (str, optional): Data frequency, either 'hour' or 'month'. Default is 'hour'.
    
    Returns:
        xarray.Dataset: The converted ERA5 data in W m^-2.
    
    Example Usage:
        converted_data = convert_era5_to_Wm2(era5_dataset, ['variable1', 'variable2'], data_freq='hour')
    """    

    if data_freq == 'hour':
        
        for var in var_name:
            data[var] = (('time', 'latitude', 'longitude'), (data[var] / 3600).data)    
        
    elif data_freq == 'month':

        for var in var_name:

            v = np.ndarray([data.time.size, data.latitude.size, data.longitude.size])

            for m in range(data.time.size):

                year  = data.isel(time=m).time.dt.year.item()
                month = data.isel(time=m).time.dt.month.item()
        
                # Convert monthly data from J m^-2 to W m^-2
                days_in_month = calendar.monthrange(year, month)[1]
                
                v[m] = data[var].isel(time=m).data / (days_in_month * 3600)

            data[var] = (('time', 'latitude', 'longitude'), v)    
    
    else:
        warnings.warn("Data frequency should be either 'hour' or 'month' - nothing changed.")
    
    return data