import ee #Earth Engine Library
ee.initialize #Library Initialization

temp = ee.ImageCollection('MODIS/006/MOD11A1') #Data Selection
start_date = '2018-01-01'
end_date = '2020-01-01'

temp = temp.select()