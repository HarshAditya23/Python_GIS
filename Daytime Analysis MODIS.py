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

Urban_df = transform(Urban_poi, ['LST_Day_1km'])
Rural_df = transform(Rural_poi, ['LST_Day_1km'])

Urban_df['LST_Day_1km'] = Urban_df['LST_Day_1km'].apply(temperture_conversion)
Rural_df['LST_Day_1km'] = Rural_df['LST_Day_1km'].apply(temperture_conversion)
