# Code used in "Storms regulate Southern Ocean summer warming"

Datasets are located at:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12779502.svg)](https://doi.org/10.5281/zenodo.12779502)

## Figures

- `figure-1.ipnyb`
- `figure-2.ipynb`
- `figure-3.ipynb`

## Datasets 

### Slocum glider 

The primary datasets used are `slocum_gridded.nc`, `slocum_sst_median_10m.nc`, `slocum_epsilon.nc` and `slocum_xld.nc`

#### Processing steps:

1. Slocum processing done in `slocum_processing_main.ipynb` and follow these steps:

	- Runs `process-slocum-mat-to-nc.py`, which:
		- Reads in the data processed by the GEOMAR toolbox: `soscexstorm2_final_1sec_v2.mat`
		- Converts the .mat dictionary format to an xarray dataset and saves the data as `slocum_processed.nc`
	- Removes pressure and temeprature values that are below -5 (erroneous data)
	- Saves the data `slocum_processed_L2.nc` and dissipation and xld data as and `slocum_epsilon.nc` and `slocum_xld.nc`
	- Calculates the Slocum SST, by:
		- Filter out profiles where the minimum depth is below 10 m (keeps 99.78% of data)
		- Finds the median value between 0.5 m and 10 m for each profile
		- Save the data as `slocum_sst_median_10m.nc`

2. Grid the Slocum data to 1 m depth intervals in `slocum_gridding.ipynb` to make `slocum_gridded.nc`

### Storm tracking

Original storm track position were obtained from https://github.com/jlodise/JGR2022_ExtratropicalCycloneTracker and processed into a single netcdf file using `process-loidse_storm_centers.ipnyb`

### ERA5

1. Download the ERA5 data using `download_era5_data.ipynb` which downloads and saves hourly files of the required ERA5 data
2. Convert the hourly ERA5 files in daily means using `era5_hourly_to_daily.ipynb` which is done to make down the line processing more efficient
3. Calculate the storm statisitics using the daily ERA5 files in this order:
	- Remove data where sea ice concentration is above 15%
	- Identify median storm and interstorm periods for a each season
	- Calculate total storm and interstorm days in a each sesaon
	- Calculate the mean wind speed and fluxes for storm and interstorm periods
	- Save the netcdf file as `era5_storm_interstorm_periods_1981_2023_DJF.nc`

### Cloud Top Pressure

The MODIS Level-2 Cloud product was obtained from `http://dx.doi.org/10.5067/MODIS/MYD06_L2.061`. The raw `.hdf` files were processed into a daily composite using `process-modis-CTP.ipynb`. The final data containing the MODIS cloud top pressure for 4 January is saved as `modis_ctt_ctp.nc`.