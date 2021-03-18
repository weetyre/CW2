from geopandas import read_file
from pyproj import Geod

# load the shapefile of countries - this gives a table of 12 columns and 246 rows (one per country)
world = read_file("ne_10m_admin_0_countries.shp")
# print a list of all of the columns in the shapefile
# print(world.columns)
# print(world.head())
# print(type(world))

country = world.ISO_A3
country_list = list(country)
try:
    while True:
        country_list.remove('-99')
except Exception:
    pass
# print(list(country))
g = Geod(ellps='WGS84')
for i in country_list:
    for j in country_list:
        if i != j:
            country1 = world.loc[(world.ISO_A3 == i)]
            country1_geom = country1.geometry.iloc[0]

            country2 = world.loc[(world.ISO_A3 == j)]
            country2_geom = country2.geometry.iloc[0]

            border = country1_geom.intersection(country2_geom)
            cumulative_length = 0
            # print(type(border))
            try:
                for segment in list(border):
                    azF, azB, distance = g.inv(segment.coords[0][0], segment.coords[0][1], segment.coords[1][0],
                                               segment.coords[1][1])
                    cumulative_length += distance
                print(cumulative_length)
                print(i)
                print(j)
            except TypeError:
                pass

print(type(cumulative_length))
# cumulative_length_list = []

cumulative_length_list = [cumulative_length]
final_list=cumulative_length_list.sort_values(by )
