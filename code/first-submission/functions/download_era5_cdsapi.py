import cdsapi
from urllib.request import urlopen# start the client

def download_era5_cdsapi(var, days, month, year, dataset="reanalysis-era5-single-levels", product_type='reanalysis', path=''):
    
    client = cdsapi.Client()# dataset you want to read

    if dataset=='reanalysis-era5-single-levels-monthly-means':

        request = {
                  'variable': [var],
                  'product_type': product_type,
                  'year': [year],
                  'month': [month],
                  'time': [
                           '00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00',
                           '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00',
                           '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00',
                           '21:00', '22:00', '23:00'
                          ],
                  'area': ['0', '0', '-90', '360'],
                  'data_format': 'netcdf'
                 }

    else: 
        
        request = {
                  'variable': [var],
                  'product_type': [product_type],
                  'year': [year],
                  'month': [month],
                  'day': [
                      "01", "02", "03",
                      "04", "05", "06",
                      "07", "08", "09",
                      "10", "11", "12",
                      "13", "14", "15",
                      "16", "17", "18",
                      "19", "20", "21",
                      "22", "23", "24",
                      "25", "26", "27",
                      "28", "29", "30",
                      "31"],
                  'time': [
                           '00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00',
                           '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00',
                           '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00',
                           '21:00', '22:00', '23:00'
                          ],
                  'area': [
                           '0', '0', '-90', '360'
                          ],
                  'data_format': 'netcdf'
                 }
        
    print('downloading: ', var, year, month)

    target = path+str(var)+'_'+str(year)+str(month)+'.nc'
    
    fl = client.retrieve(dataset, request, target) # download the file 
    
    # fl.download(path+str(var)+'_'+str(year)+str(month)+'.nc') # load into memory
        
    return