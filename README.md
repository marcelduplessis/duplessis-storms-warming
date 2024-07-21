# duplessis-storms-warming
Code using in "Storms regulate Southern Ocean summer warming"

### Data processing 

#### ERA5

1. Download the ERA5 data using `download_era5_data.ipynb` which downloads and saves hourly files of the required ERA5 data
2. Convert the hourly ERA5 files in daily means using `era5_hourly_to_daily.ipynb` which is done to make down the line processing more efficient
3. Calculate the storm statisitics using the daily ERA5 files in this order:
	- Remove data where sea ice concentration is above 15%
	- Identify median storm and interstorm periods for a each season
	- Calculate total storm and interstorm days in a each sesaon
	- Calculate the mean wind speed and fluxes for storm and interstorm periods
	- Save the netcdf file as `era5_storm_interstorm_periods_1981_2023_DJF.nc`
