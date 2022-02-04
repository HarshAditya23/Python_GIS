"""
Created on Thu Jan 27 20:18:13 2022

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
Temp = Temp.select('LST_Night_1km', 'QC_Night').filterDate(Start_date, End_date)

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
        ).get('LST_Night_1km').getinfo()
Urban_min = Temp.min().sample(Urban_poi, Scale).first(
        ).get('LST_Night_1km').getinfo()
Urban_max = Temp.max().sample(Urban_poi, Scale).first(
        ).get('LST_Night_1km').getinfo()

# Temperature in degree celcius
print('Mean nighttime LST at Urban POI:', round(Urban_poi * 0.02 - 273.15,
                                                2), '°C')
print('Minimum nighttime LST at Urban POI:', round(Urban_poi * 0.02 - 273.15,
                                                   2), '°C')
print('Maximum nighttime LST at Urban POI:', round(Urban_poi * 0.02 - 273.15,
                                                   2), '°C')

# Mean, Min and Max temperature of Rural POI
Rural_mean = Temp.mean().sample(Rural_poi, Scale).first(
        ).get('LST_Night_1km').getInfo()
Rural_min = Temp.mean().sample(Rural_poi, Scale).first(
        ).get('LST_Night_1km').getInfo()
Rural_max = Temp.mean().sample(Rural_poi, Scale).first(
        ).get('LST_Night_1km').getInfo()

# Temperature in degree celcius
print('Mean nighttime LST at Rural POI:', round(Rural_poi * 0.02 - 273.15,
                                                2), '°C')
print('Minimum nighttime LST at Rural POI:', round(Rural_poi * 0.02 - 273.15,
                                                   2), '°C')
print('Maximum nighttime LST at Rural POI:', round(Rural_poi * 0.02 - 273.15,
                                                   2), '°C')

Urban_df = Temp.getRegion(Urban_poi, Scale).getInfo()
Rural_df = Temp.getRegion(Rural_poi, Scale).getInfo()

Urban_df = transform(Urban_poi, ['LST_Night_1km'])
Rural_df = transform(Rural_poi, ['LST_Night_1km'])

Urban_df['LST_Night_1km'] = Urban_df['LST_Night_1km'].apply(
        temperture_conversion)
Rural_df['LST_Night_1km'] = Rural_df['LST_Night_1km'].apply(
        temperture_conversion)

Urban_df['UTFVI'] = Urban_df['LST_Night_1km'].apply(utfvi_calculation)
Rural_df['UTFVI'] = Rural_df['LST_Night_1km'].apply(utfvi_calculation)

# Urban data to csv
Urban_df.to_csv('data_urban.csv', index=False)
# Rural data to csv
Rural_df.to_csv('data_rural.csv', index=False)

fig, ax = plt.subplots(figsize=(14, 6))
ax.scatter(Urban_df['nighttime'], Urban_df['LST_Night_1km'],
           c='black', alpha=0.2, label='Urban (data)')
ax.scatter(Rural_df['nighttime'], Rural_df['LST_Night_1km'],
           c='green', alpha=0.35, label='Rural (data)')

lst_img = Temp.mean()
lst_img = lst_img.select('LST_Night_1km').multiply(0.02)
lst_img = lst_img.select('LST_Night_1km').add(-273.15)
roi = Urban_poi.buffer(1e6)
# Heat map for daytime
url = lst_img.getThumbUrl({'min': 10, 'max': 30, 'dimensions': 512,
                           'palette': ['blue', 'yellow', 'orange', 'red']})

response = requests.get("url")
file = open("image.png", "wb")
file.write(response.content)
file.close()

plt.imshow(mpimg.imread('image.png'))
