# duplessis-storms-warming
Code using in "Storms regulate Southern Ocean summer warming"

### Figures

- `figure-1.ipnyb`
- `figure-2.ipynb`

### Data processing 

#### Slocum glider 

Slocum processing done in `slocum_processing_main.ipynb` and follow these steps:

1. Runs `process-slocum-mat-to-nc.py`, which:
	- Reads in the data processed by the GEOMAR toolbox: `soscexstorm2_final_1sec_v2.mat`
	- Converts the .mat dictionary format to an xarray dataset and saves the data as `slocum_processed.nc`

#### Storm tracking

Original storm track position were obtained from https://github.com/jlodise/JGR2022_ExtratropicalCycloneTracker and processed into a single netcdf file using `process-loidse_storm_centers.ipnyb`

#### ERA5

1. Download the ERA5 data using `download_era5_data.ipynb` which downloads and saves hourly files of the required ERA5 data
2. Convert the hourly ERA5 files in daily means using `era5_hourly_to_daily.ipynb` which is done to make down the line processing more efficient
3. Calculate the storm statisitics using the daily ERA5 files in this order:
	- Remove data where sea ice concentration is above 15%
	- Identify median storm and interstorm periods for a each season
	- Calculate total storm and interstorm days in a each sesaon
	- Calculate the mean wind speed and fluxes for storm and interstorm periods
	- Save the netcdf file as `era5_storm_interstorm_periods_1981_2023_DJF.nc`
