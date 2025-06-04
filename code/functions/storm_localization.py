from glob import glob
import numpy as np
import xarray as xr
from adjust_lon_xr_dataset import adjust_lon_xr_dataset
import gsw
import pandas as pd
from scipy.interpolate import griddata
from joblib import Parallel, delayed


def convert_longitude(longitude):
    if longitude < 0:
        return longitude + 360
    else:
        return longitude

def read_era5_dataset(name, year):
    print(f'reading in era5 dataset for {name} {year}')
    data_directory_in = f'/home/mduplessis/data/era5/DJF_1981_2024_{name[0]}/*.nc'
    file_list = sorted(glob(data_directory_in))
    
    year_str = str(year)
    next_year_str = str(year + 1)
    months = [f'{year_str}12.nc', f'{next_year_str}01.nc', f'{next_year_str}02.nc']
    
    # choose only the files that are dec, jan or feb
    filtered_files = [file for file in file_list if any(file.endswith(month) for month in months)]
    
    ds = xr.open_mfdataset(filtered_files)
    ds = ds.sel(latitude=slice(-30, -90)).load()

    ds_adjusted = adjust_lon_xr_dataset(ds)

    return ds, ds_adjusted

def select_data_by_year(ds, year):
    """
    Selects a portion of the cyclone center data based on the given year.

    Parameters:
    ds (xarray.Dataset): The dataset to select data from.
    year (int): The year to select data for.

    Returns:
    xarray.Dataset: The dataset containing data for the specified year.
    """
    print(f'Selecting storm data for year {year}')
    return ds.isel(TIME=((ds.TIME >= np.datetime64(f'{year}-12-01')) & (ds.TIME < np.datetime64(f'{year+1}-03-01'))))

def process_storm_data(var, ds, ds_adjusted, storm_ds, storm_id):
    # print(f'Processing data for storm {storm_id} of {storm_ds.STORM_ID.size}')

    new_x = np.arange(-1000, 1050, 50)
    new_y = np.arange(-1000, 1050, 50)

    ds_storm = storm_ds.isel(TIME=storm_ds.STORM_ID == storm_id)

    which_lon_grid = np.ndarray([ds_storm.TIME.size])
    lons = np.ndarray([ds_storm.TIME.size, 241])
    lats = np.ndarray([ds_storm.TIME.size, 81])

    # ds_final = xr.Dataset()

    for time_idx in range(ds_storm.TIME.size):
        cyclone = ds_storm.isel(TIME=time_idx)  # choose one cyclone position at a time

        ref_lat = np.round(cyclone.LATITUDE.values, 2)

        if (cyclone.LONGITUDE >= 145) or (cyclone.LONGITUDE < -145):            
            ref_lon = np.round(convert_longitude(cyclone.LONGITUDE.values), 2)

            ds_ = ds.sel(time=cyclone.TIME.values,
                         latitude=slice(np.round(ref_lat) + 10, np.round(ref_lat) - 10),
                         longitude=slice(np.round(ref_lon) - 30, np.round(ref_lon) + 30))
            
            which_lon_grid[time_idx] = 1  # give a value that represents a grid of 0 to 360

        else:
            ref_lon = np.round(cyclone.LONGITUDE.values, 2)

            ds_ = ds_adjusted.sel(time=cyclone.TIME.values,
                                  latitude=slice(np.round(ref_lat) + 10, np.round(ref_lat) - 10),
                                  longitude=slice(np.round(ref_lon) - 30.0, np.round(ref_lon) + 30))
            
            which_lon_grid[time_idx] = 0  # give a value that represents a grid of -180 to 180

        lats = ds_.latitude.values
        lons = ds_.longitude.values

        # longitude to distance interpolation
        dist_from_lon = np.zeros([81, 241])

        for j, lt in enumerate(lats):
            for i, ln in enumerate(lons):
                dist_from_lon[j, i] = gsw.distance([ln, ref_lon], [lt, lt])[0] / 1000

            dist_from_lon[j][lons < ref_lon] = -dist_from_lon[j][lons < ref_lon]

        # latitude to distance interpolation
        dist_from_lat = np.zeros(lats.size)

        for j, lt in enumerate(lats):
            dist_from_lat[j] = gsw.distance([lons[0], lons[0]], [lt, ref_lat])[0] / 1000

        dist_from_lat[lats < ref_lat] = -dist_from_lat[lats < ref_lat]

        for v in var:
            new_data = np.zeros([81, new_x.size])
            final_data = np.zeros([new_x.size, new_y.size])

            data = ds_[v]

            for j in range(lats.size):
                new_data[j, :] = griddata(dist_from_lon[j], data[j], new_x)

            for i in range(new_x.size):
                final_data[:, i] = griddata(dist_from_lat, new_data[:, i], new_y)

            ds_var = xr.Dataset(
                {v: (['time', 'x', 'y'], final_data[np.newaxis, :, :]),
                 'pressure': (['time'], [cyclone.PRESSURE_MIN.data]),
                 'storm_id': (['time'], [cyclone.STORM_ID.data]),
                 },
                coords={
                    'x': ('x', new_x),
                    'y': ('y', new_y),
                    'time': ('time', [pd.to_datetime(cyclone.TIME.data)]),
                    'lon': ('time', [ref_lon]),
                    'lat': ('time', [ref_lat]),                
                }
            )
    
            if 'ds_final' in locals() and isinstance(ds_final, xr.Dataset):
                ds_final = xr.concat([ds_final, ds_var], dim='time')

            else:
                ds_final = ds_var 

    ## Example padding logic (adjust as needed)
    max_time_length = 300  # Define a maximum length for the time dimension
    time_length = ds_final.time.size
    #
    if time_length < max_time_length:
        pad_width = max_time_length - time_length
        pad_values = {dim: (0, pad_width) for dim in ds_final.dims if dim == 'time'}
        ds_final = ds_final.pad(pad_values, constant_values=0)           
    
    return ds_final

def process_storms(names, vars, storms_ds, year, storm_id=None):
    """
    Function to process all storms for a given year or a specific storm.
    Args:
    name: str
        Name of the dataset to be used. Options: '2m_temperature', 'winds', 'sea_ice_cover'
    var: str
        Variable to be processed. Options: 't2m', 'u10', 'v10', 'siconc'
    storms_ds: xarray.Dataset
        Dataset containing the storms data
    year: int
        Year to be processed
    storm_id: int
        Storm ID to be processed. If None, all storms for the year will be processed

    Returns:
    ds_all: xarray.Dataset
        Dataset containing the processed data
    """

    #def read_and_merge_datasets(names, year):
    #    datasets = [read_era5_dataset(name, year) for name in names]
    #    era5_ds_all = xr.merge([ds[0] for ds in datasets])
    #    era5_ds_adjusted_all = xr.merge([ds[1] for ds in datasets])
    #    return era5_ds_all, era5_ds_adjusted_all

    # era5_ds_all, era5_ds_adjusted_all = read_and_merge_datasets(names, year)

    era5_ds_all, era5_ds_adjusted_all = read_era5_dataset(names, year)
    
    ds_storms_year = select_data_by_year(storms_ds, year)

    def rename_valid_time_to_time(ds):
        if 'valid_time' in ds:
            ds = ds.rename({'valid_time': 'time'})
        return ds
    
    era5_ds_all = rename_valid_time_to_time(era5_ds_all)
    era5_ds_adjusted_all = rename_valid_time_to_time(era5_ds_adjusted_all)

    def process_single_storm(storm):
        return process_storm_data(vars, era5_ds_all, era5_ds_adjusted_all, ds_storms_year, storm)

    if storm_id is None:
        print(f'No storms provided, using all storms for the year {year}. Total number of storms: {len(np.unique(ds_storms_year.STORM_ID.values))}')
        storm_ids = np.unique(ds_storms_year.STORM_ID.values)

        # Use parallel processing to handle multiple storms simultaneously
        results = Parallel(n_jobs=-1, backend='loky')(delayed(process_single_storm)(storm) for storm in storm_ids)
        ds_all = xr.concat(results, dim='time', join='outer')

    else:
        storm = storm_id
        ds_all = process_single_storm(storm)

    return ds_all