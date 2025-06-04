# Import the xarray library and alias it as 'xr'
import xarray as xr
import numpy as np

# Define a function named 'function' that calculates relative humidity (RH) and adds it to an input xarray dataset
def convert_dp_to_rh(era5_ds):
    # Extract dew point temperature (Dp) values from the input dataset
    Dp = era5_ds.d2m.values - 273.15 # dew point temperature

    # Extract air temperature (T) values from the input dataset, and convert to Kelvin
    T = era5_ds.t2m.values - 273.15# temperature in kelvin
    
    # Calculate relative humidity (RH) using the formula and add it to the input dataset
    era5_ds['rh'] = (('time'),
                     100 * (np.exp((17.625 * Dp) / (243.04 + Dp)) / np.exp((17.625 * T) / (243.04 + T))))
    
    # Return the input dataset with the 'rh' variable added
    return era5_ds
