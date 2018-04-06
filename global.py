# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 19:12:17 2018

@author: daniel ramírez
"""

import sys; sys.path.insert(1, 'pygplates_rev12_python27_MacOS64') # insert absolute/relative path of the library's folder
import pandas as pd
import pygplates
import os
import errno

# =============================================================================
# Declaring variables
# =============================================================================

reservoir_data = pd.read_csv('giant_oil_and_gas_fields_of_the_world_co_yxz.csv') # reading database
my_reservoir_data = reservoir_data.copy()

periods_age = {'Nan': 0, 'Cretaceous': 105.5, 'Neogene': 12.8, 'Paleogene': 44.5, 'Jurassic': 173, 'Triassic': 226.5,
                'Permian' : 275.5, 'Carboniferous': 329, 'Ordovician': 471.5, 'Ediacaran' : 588 , 'Ectasian' : 1300,
                'Devonian' : 389, 'Cambrian' : 513, 'Silurian' : 431.5} # periods' base map average ages (age_max - age_min)/2

#my_reservoir_data['SYSTEM'].unique() # check what values do you have to make the classification from
periods = pd.Series(my_reservoir_data['SYSTEM'].unique())
periods = periods.dropna()
#my_reservoir_data['AVERAGE_DATE'] = my_reservoir_data['SYSTEM'].map(periods_age) # adding average dates to a new column depending on the dictionary

# =============================================================================
# Rotating continental blocks
# =============================================================================

anchor_plate = 0

for p in periods:
    reconstruction_time = periods_age[p]
    if periods_age[p] < 410:
        input_feature_filename = 'tectonic_data/Matthews_etal_GPC_2016_ContinentalPolygons.gpmlz'
        input_rotation_filename = 'tectonic_data/Matthews_etal_GPC_2016_410-0Ma_GK07.rot'
    elif periods_age[p] > 410 and periods_age[p] <= 541: # There's no suitable data for Late Paleozoic and reservoirs at this time aren't that important either so we skip it
        continue
    else:
        input_feature_filename = 'tectonic_data/Neoproterozoic_shapes.gpml'
        input_rotation_filename = 'tectonic_data/Neoproterozoic_rotations.rot'
    output_reconstructed_feature_filename = 'reconstructions/' + str(p) + '/' + str(p) + '.shp'
    if not os.path.exists(os.path.dirname(output_reconstructed_feature_filename)):
        try:
            os.makedirs(os.path.dirname(output_reconstructed_feature_filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    pygplates.reconstruct(input_feature_filename, input_rotation_filename, output_reconstructed_feature_filename, reconstruction_time, anchor_plate)

# =============================================================================
# Transforming actual coordinates into paleographic coordinates
# =============================================================================

for p in periods:
    reconstruction_time = periods_age[p]
    if periods_age[p] < 410:
        input_feature_filename = pygplates.FeatureCollection('tectonic_data/Matthews_etal_GPC_2016_ContinentalPolygons.gpmlz')
        input_rotation_filename = pygplates.RotationModel('tectonic_data/Matthews_etal_GPC_2016_410-0Ma_GK07.rot')
    elif periods_age[p] > 410 and periods_age[p] <= 541:
        continue
    else:
        input_feature_filename = pygplates.FeatureCollection('tectonic_data/Neoproterozoic_shapes.gpml')
        input_rotation_filename = pygplates.RotationModel('tectonic_data/Neoproterozoic_rotations.rot')
    output_reconstructed_feature_filename = 'reconstructions/' + str(p) + '/' + str(p) + '_points' + '.shp'
    if not os.path.exists(os.path.dirname(output_reconstructed_feature_filename)):
        try:
            os.makedirs(os.path.dirname(output_reconstructed_feature_filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    df_temp = my_reservoir_data[my_reservoir_data.SYSTEM == p] # making the following manual iteration quicker by reducing data set size
    point_features = []
    for index, row in df_temp.iterrows():
        point = pygplates.PointOnSphere(float(row.LAT_DD),float(row.LON_DD))
        point_feature = pygplates.Feature()
        point_feature.set_geometry(point)
        point_feature.set_shapefile_attribute('MMBOE', row.EUR_MMBOE)
        point_feature.set_shapefile_attribute('Region', row.REG_NAME)
        point_feature.set_shapefile_attribute('Lithology', row.RSVR_LITH1)
        point_features.append(point_feature)
    partitioned_point_features = pygplates.partition_into_plates(input_feature_filename, input_rotation_filename, point_features)
    pygplates.reconstruct(partitioned_point_features, input_rotation_filename, output_reconstructed_feature_filename, reconstruction_time)


