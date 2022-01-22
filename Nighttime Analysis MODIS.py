# Earth Engine Library
import ee
# Library Initialization
ee.Initialize()

# Data Selection
temp = ee.ImageCollection('MODIS/006/MOD11A1')
start_date = '2018-01-01'
end_date = '2020-01-01'

# Band selection and filtering
temp = temp.select('LST_Night_1km', 'QC_Day').filterDate(start_date, end_date)

urban_lon = 77.219159
urban_lat = 28.627522
# Point of Interest Urban
urban_poi = ee.Geometry.Point(urban_lon, urban_lat)

rural_lon = 77.480755
rural_lat = 28.851537
# Point of Interest Rural
rural_poi = ee.Geometry.Point(rural_lon, rural_lat)
