"""
Created on Thu Jan 27 18:18:13 2022

@author: gaurh
"""

# Earth Engine Library
import ee
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from temperature import transform
from temperature import temperture_conversion
from temperature import utfvi_calculation
# Library Initialization
ee.Initialize()

# Data Selection
Temp = ee.ImageCollection('MODIS/006/MOD11A1')
Start_date = '2018-01-01'
End_date = '2020-01-01'

# Band selection and filtering
Temp = Temp.select('LST_Day_1km', 'QC_Day').filterDate(Start_date, End_date)

Urban_lon = 77.219159
Urban_lat = 28.627522
# Point of Interest Urban
Urban_poi = ee.Geometry.Point(Urban_lon, Urban_lat)

Rural_lon = 77.480755
Rural_lat = 28.851537
# Point of Interest Rural
Rural_poi = ee.Geometry.Point(Rural_lon, Rural_lat)
# Resolution in meters

Scale = 1000

# Mean, Min and Max temperature of Urban POI
Urban_mean = Temp.mean().sample(Urban_poi, Scale).first(
        ).get('LST_Day_1km').getinfo()
Urban_min = Temp.min().sample(Urban_poi, Scale).first(
        ).get('LST_Day_1km').getinfo()
Urban_max = Temp.max().sample(Urban_poi, Scale).first(
        ).get('LST_Day_1km').getinfo()

# Temperature in degree celcius
print('Mean daytime LST at Urban POI:', round(Urban_poi * 0.02 - 273.15, 2),
      '°C')
print('Minimum daytime LST at Urban POI:', round(Urban_poi * 0.02 - 273.15, 2),
      '°C')
print('Maximum daytime LST at Urban POI:', round(Urban_poi * 0.02 - 273.15, 2),
      '°C')

# Mean, Min and Max temperature of Rural POI
Rural_mean = Temp.mean().sample(Rural_poi, Scale).first(
        ).get('LST_Day_1km').getInfo()
Rural_min = Temp.mean().sample(Rural_poi, Scale).first(
        ).get('LST_Day_1km').getInfo()
Rural_max = Temp.mean().sample(Rural_poi, Scale).first(
        ).get('LST_Day_1km').getInfo()

# Temperature in degree celcius
print('Mean daytime LST at Rural POI:', round(Rural_poi * 0.02 - 273.15, 2),
      '°C')
print('Minimum daytime LST at Rural POI:', round(Rural_poi * 0.02 - 273.15, 2),
      '°C')
print('Maximum daytime LST at Rural POI:', round(Rural_poi * 0.02 - 273.15, 2),
      '°C')

Urban_df = Temp.getRegion(Urban_poi, Scale).getInfo()
Rural_df = Temp.getRegion(Rural_poi, Scale).getInfo()

Urban_df = transform(Urban_poi, ['LST_Day_1km'])
Rural_df = transform(Rural_poi, ['LST_Day_1km'])

Urban_df['LST_Day_1km'] = Urban_df['LST_Day_1km'].apply(temperture_conversion)
Rural_df['LST_Day_1km'] = Rural_df['LST_Day_1km'].apply(temperture_conversion)

Urban_df['UTFVI'] = Urban_df['LST_Day_1km'].apply(utfvi_calculation)
Rural_df['UTFVI'] = Rural_df['LST_Day_1km'].apply(utfvi_calculation)

# Urban data to csv
Urban_df.to_csv('data_urban.csv', index=False)
# Rural data to csv
Rural_df.to_csv('data_rural.csv', index=False)

lst_img = Temp.mean()
lst_img = lst_img.select('LST_Day_1km').multiply(0.02)
lst_img = lst_img.select('LST_Day_1km').add(-273.15)
roi = Urban_poi.buffer(1e6)
# Heat map for daytime
url = lst_img.getThumbUrl({'min': 10, 'max': 30, 'dimensions': 512,
                           'palette': ['blue', 'yellow', 'orange', 'red']})

response = requests.get("url")
file = open("image.png", "wb")
file.write(response.content)
file.close()

plt.imshow(mpimg.imread('image.png'))
