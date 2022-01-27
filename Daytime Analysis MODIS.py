"""
Created on Thu Jan 27 18:18:13 2022

@author: gaurh
"""

# Earth Engine Library
import ee
from temperature import transform
from temperature import temperture_conversion
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
        ).get('LST_Day_1km').getinfo()
Rural_min = Temp.mean().sample(Rural_poi, Scale).first(
        ).get('LST_Day_1km').getinfo()
Rural_max = Temp.mean().sample(Rural_poi, Scale).first(
        ).get('LST_Day_1km').getinfo()

# Temperature in degree celcius
print('Mean daytime LST at Rural POI:', round(Rural_poi * 0.02 - 273.15, 2),
      '°C')
print('Minimum daytime LST at Rural POI:', round(Rural_poi * 0.02 - 273.15, 2),
      '°C')
print('Maximum daytime LST at Rural POI:', round(Rural_poi * 0.02 - 273.15, 2),
      '°C')

Urban_df = transform(Urban_poi, ['LST_Day_1km'])
Rural_df = transform(Rural_poi, ['LST_Day_1km'])

Urban_df['LST_Day_1km'] = Urban_df['LST_Day_1km'].apply(temperture_conversion)
Rural_df['LST_Day_1km'] = Rural_df['LST_Day_1km'].apply(temperture_conversion)
