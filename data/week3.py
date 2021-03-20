# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 09:56:12 2021

@author: 马一如
"""

############part 1
name = 'Jonny'
if name == 'Jonny':
    print('Hi Jonny!')
    
######
name = 'Kirsty'

if name == 'Jiawei':        # this will be tested, and is False
    print('Hi Jiawei!') # this will therefore NOT run
    
elif name == 'Kirsty':    # this will be tested, and is True
    print('Hi Kirsty!') # this will therefore run
    
elif name == 'Matt':     # this will NOT be tested, as we already know the answer
    print('Hi Matt!') 
######    
name = 'Jonny'
if name == 'Jiawei':
    print('Hi Jiawei!')
    
elif name == 'Kirsty':
    print('Hi Kirsty!')
    
elif name == 'Matt':
    print('Hi Matt!')
    
else:
    print('I do not know you')
    
###### using spherical of Cosine
from math import sqrt

def distance(x1, y1, x2, y2):
   a=x2-x1
   b=y2-y1
   c=a*a+b*b
   distance = sqrt(c)
   return distance
#distance = Pythagorasdistance(-2.79, 54.04, -2.75, 54.10)
#print(distance)

########part 2
from geopandas import read_file

# read in shapefiles, and show crs info
pop_points = read_file("../../data/gulu/pop_points.shp")
water_points = read_file("../../data/gulu/water_points.shp")
gulu_district = read_file("../../data/gulu/district.shp")
print(pop_points.crs) 
print() 
print(water_points.crs) 
print() 
print(gulu_district.crs) 

#convert to EPSG code
print(pop_points.crs.to_epsg()) 
print(water_points.crs.to_epsg()) 
print(gulu_district.crs.to_epsg()) 

#convert to the same crs
from geopandas import read_file

# read in shapefiles, ensure that they all have the same CRS
pop_points = read_file("../../data/gulu/pop_points.shp")
water_points = read_file("../../data/gulu/water_points.shp").to_crs(pop_points.crs)
gulu_district = read_file("../../data/gulu/district.shp").to_crs(pop_points.crs)

#check the epsg
print(pop_points.crs.to_epsg()) 
print(water_points.crs.to_epsg()) 
print(gulu_district.crs.to_epsg()) 

#claculate population points and wells(complicated)
print(f"population points: {len(pop_points.index)}")
print(f"Initial wells: {len(water_points.index)}")

#claculate population points and wells
from rtree import index
idx = index.Index()
for id, well in water_points.iterrows():
	idx.insert(id, well.geometry.bounds)

#optimising intersections with a spatial index
# get the one and only polygon from the district dataset
polygon = gulu_district.geometry.iloc[0]

# how many rows are we starting with?
print(f"Initial wells: {len(water_points.index)}")
    
# get the indexes of wells that intersect bounds of the district
possible_matches_index = list(idx.intersection(polygon.bounds))
# use those indexes to extract the possible matches from the GeoDataFrame
possible_matches = water_points.iloc[possible_matches_index]
# how many rows are left now? 
print(f"Filtered wells: {len(possible_matches.index)}")

# then search the possible matches for precise matches using the slower but more precise method
precise_matches = possible_matches.loc[possible_matches.within(polygon)]
# how many rows are left now?
print(f"Filtered wells: {len(precise_matches.index)}")
# rebuild the spatial index using the new, smaller dataset
idx = index.Index()
for id, well in precise_matches.iterrows():
	idx.insert(id, well.geometry.bounds)
 

# declare array to store distances
distances = []

# loop through each water source
for id, house in pop_points.iterrows():

	# use the spatial index to get the index of the closest well
	nearest_well_index = list(idx.nearest(house.geometry.bounds, 1))[0]

	# use the spatial index to get the closest well object from the original dataset
	nearest_well = water_points.iloc[nearest_well_index]

	# store the distance to the nearest well
	distances.append(distance(house.geometry.bounds[0], house.geometry.bounds[1],
		nearest_well.geometry.bounds[0], nearest_well.geometry.bounds[1]))

# calculate the mean
mean = round(sum(distances) / len(distances))

# store distance to nearest well
pop_points['nearest_well'] = distances

# output the result
print(f"Minimum distance to water in Gulu District is {round(min(distances))}m.")
print(f"Mean distance to water in Gulu District is {mean}m.")
print(f"Maximum distance to water in Gulu District is {round(max(distances))}m.")

##plot the map
from matplotlib.pyplot import subplots, savefig
# create map axis object
fig, my_ax = subplots(1, 1, figsize=(16, 10))

# remove axes
my_ax.axis('off')

# add title
my_ax.set(title="Distance to Nearest Well, Gulu District, Uganda")

# add the district boundary
gulu_district.plot(
    ax = my_ax,
    color = 'white',
    linewidth = 1,
	edgecolor = 'black',
    )

# plot the locations, coloured by distance to water
pop_points.plot(
    ax = my_ax,
    column = 'nearest_well',
    linewidth = 0,
	markersize = 1,
    cmap = 'RdYlBu_r',
    scheme = 'quantiles',
    legend = 'True',
    legend_kwds = {
        'loc': 'lower right',
        'title': 'Distance to Nearest Well'
        }
    )

# add north arrow
x, y, arrow_length = 0.98, 0.99, 0.1
my_ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
	arrowprops=dict(facecolor='black', width=5, headwidth=15),
	ha='center', va='center', fontsize=20, xycoords=my_ax.transAxes)

# add scalebar
from matplotlib_scalebar.scalebar import ScaleBar
my_ax.add_artist(ScaleBar(dx=1, units="m", location="lower left", length_fraction=0.25))

# save the result
savefig('out/3.png', bbox_inches='tight')
print("done!")