from geopandas import read_file
from pyproj import Geod
from rtree import index

# load the shapefile of countries - this gives a table of 12 columns and 246 rows (one per country)
world = read_file("ne_10m_admin_0_countries.shp")
# print a list of all of the columns in the shapefile
# print(world.columns)
# print(world.head())
# print(type(world))

idx = index.Index()
for id,country in world.iterrows():
	idx.insert(id, country.geometry.bounds)

#country = world.ISO_A3
#country_list = list(country)

#try:
#    while True:
#        country_list.remove('-99')
#except Exception:
#    pass
# print(list(country))
g = Geod(ellps='WGS84')
#cumulative_len = []

country_distance_list = []

for id,country in world.iterrows:
    #for j in world.iterrows:
        #if i != j:
            country1 = world.loc[(world.ISO_A3 == i)]
            country1_geom = country1.geometry.iloc[0]

            country2 = world.loc[(world.ISO_A3 == j)]
            country2_geom = country2.geometry.iloc[0]

            # border = idx.intersection(country2_geom)
            cumulative_length = 0
            # print(type(border))
            try:
                for segment in list(border):
                    azF, azB, distance = g.inv(segment.coords[0][0], segment.coords[0][1], segment.coords[1][0],
                                               segment.coords[1][1])
                    cumulative_length += distance
                print(cumulative_length)
                # cumulative_len.append(cumulative_length)
                print(i)
                print(j)
                triple=[cumulative_length,i,j]
                country_distance_list.append(triple)
            except TypeError:
                pass

# print(type(cumulative_len))
# cumulative_length_list = []


# cumulative_len.sort()
country_distance_list.sort()
sorted(country_distance_list, key=lambda x:x[0])
# print(cumulative_len[0])
print(country_distance_list[0])
