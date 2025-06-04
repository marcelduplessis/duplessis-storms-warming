import xarray as xr

def adjust_lon_xr_dataset(ds, lon_name='longitude'):
    
    # whatever name is in the data - lon_name = 'lon'  

    # Adjust lon values to make sure they are within (-180, 180)
    ds['_longitude_adjusted'] = xr.where(
        ds[lon_name] > 180,
        ds[lon_name] - 360,
        ds[lon_name])
    
    # reassign the new coords to as the main lon coords
    # and sort DataArray using new coordinate values
    ds = (
        ds
        .swap_dims({lon_name: '_longitude_adjusted'})
        .sel(**{'_longitude_adjusted': sorted(ds._longitude_adjusted)})
        .drop(lon_name))
    
    ds = ds.rename({'_longitude_adjusted': lon_name})
    
    return ds