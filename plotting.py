# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 13:02:40 2018

@author: daniel ramírez
"""

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
import pandas as pd

# =============================================================================
# Declaring variables
# =============================================================================

reservoir_data = pd.read_csv('giant_oil_and_gas_fields_of_the_world_co_yxz.csv') # reading database
my_reservoir_data = reservoir_data.copy()

periods = pd.Series(my_reservoir_data['SYSTEM'].unique())
periods = periods.dropna()

periods_age = {'Nan': 0, 'Cretaceous': 105.5, 'Neogene': 12.8, 'Paleogene': 44.5, 'Jurassic': 173, 'Triassic': 226.5,
                'Permian' : 275.5, 'Carboniferous': 329, 'Ordovician': 471.5, 'Ediacaran' : 588 , 'Ectasian' : 1300,
                'Devonian' : 389, 'Cambrian' : 513, 'Silurian' : 431.5}

periods_color = {'Cretaceous': '#88C86F', 'Neogene': '#FEDF2A', 'Paleogene': '#F9AA6E', 'Jurassic': '#01BAEA', 'Triassic': '#9050A1',
                'Permian' : '#E76549', 'Carboniferous': '#66AEB2', 'Ordovician': '#08A88D', 'Ediacaran' : '#FED886' , 'Ectasian' : '#fcd19e',
                'Devonian' : '#ce9d5b', 'Cambrian' : '#8dab76', 'Silurian' : '#b4dec9'} # Colors after ICS


# =============================================================================
# Plotting maps
# =============================================================================

for p in periods:

    if periods_age[p] > 410 and periods_age[p] <= 541:
        continue

    fig = plt.figure(figsize=(14,10))
    ax_map = fig.add_axes([0,0,0.9,1.0])
    m = Basemap(projection='robin', lon_0=0, resolution='c', ax=ax_map)

    #m.drawmeridians(range(0, 360, 10), linewidth=0.1) # when exporting to .pdf, linewidths don't hold
    #m.drawparallels(range(-90, 90, 10), linewidth=0.1)

    shp_info = m.readshapefile('reconstructions/' + str(p)+'/'+str(p), 'shp', drawbounds=True ,color='w') # rotated continental blocks

    for nshape,seg in enumerate(m.shp):
        poly = Polygon(seg,facecolor= periods_color[p],edgecolor='k',alpha=0.5)
        ax_map.add_patch(poly)

    reservoirs_info = m.readshapefile('reconstructions/' + str(p)+'/'+str(p)+'_points', 'reservoirs') # point layer with reservoir data


    for info, reservoir in zip(m.reservoirs_info, m.reservoirs):
        # Subclassification after lithology
        if info['Lithology'] == 'CARBONATE': color='blue'
        elif info['Lithology'] == 'SANDSTONE': color='yellow'
        else: color='purple'
        # Subclassification after MMBOE values
        if float(info['MMBOE']) < 500:
            markersize = 3; alpha=1
        elif float(info['MMBOE']) >= 500 and float(info['MMBOE']) < 800:
            markersize = 5; alpha=0.8
        elif float(info['MMBOE']) >= 800 and float(info['MMBOE']) < 1000:
            markersize = 7; alpha=0.5
        elif float(info['MMBOE']) >= 1000 and float(info['MMBOE']) < 2000:
            markersize = 9; alpha=0.5
        elif float(info['MMBOE']) >= 2000 and float(info['MMBOE']) < 10000:
            markersize = 12; alpha=0.5
        elif float(info['MMBOE']) >= 10000 and float(info['MMBOE']) < 100000:
            markersize = 16; alpha=0.5;
        else:
            markersize = 22; alpha=0.5; label='MMBOE >= 100000'
        m.plot(reservoir[0], reservoir[1], marker='o', color=color, markersize=markersize, markeredgewidth=0.0, alpha=alpha)

    # Making the legend entries
    m.plot(int(), int(), marker='o', color='k', markersize = 3, fillstyle ='none', linestyle="None", label='MMBOE < 500')
    m.plot(int(), int(), marker='o', color='k', markersize = 5, fillstyle ='none', linestyle="None", label='500 <= MMBOE < 800')
    m.plot(int(), int(), marker='o', color='k', markersize = 7, fillstyle ='none', linestyle="None", label='800 <= MMBOE < 1000')
    m.plot(int(), int(), marker='o', color='k', markersize = 9, fillstyle ='none', linestyle="None", label='1000 <= MMBOE < 2000')
    m.plot(int(), int(), marker='o', color='k', markersize = 12, fillstyle ='none', linestyle="None", label='2000 <= MMBOE < 10000')
    m.plot(int(), int(), marker='o', color='k', markersize = 16, fillstyle ='none', linestyle="None", label='10000 <= MMBOE < 100000')
    m.plot(int(), int(), marker='o', color='k', markersize = 22, fillstyle ='none', linestyle="None", label='MMBOE >= 100000')

    m.plot(int(), int(), marker='o', color='yellow', markersize = 14, linestyle="None", markeredgewidth=0.0, label= 'Sandstone Reservoirs')
    m.plot(int(), int(), marker='o', color='blue', markersize = 14, linestyle="None", markeredgewidth=0.0, label='Carbonate Reservoirs')
    m.plot(int(), int(), marker='o', color='purple', markersize = 14, linestyle="None", markeredgewidth=0.0, label='Other lithologies / Not defined')

    plt.legend(title= 'Estimated Ultimate Recovery (MMBOE)', labelspacing=1.2)

    if periods_age[p] < 410:
        plt.title(str(p) + ' - ' + str(periods_age[p]) + ' Ma' + ' (after Matthews & others (2016))', fontsize=20)
    else:
        plt.title(str(p) + ' - ' + str(periods_age[p]) + ' Ma' + ' (after Merdith & others (2017))', fontsize=20)

    fig.savefig('reconstructions/' + str(p) + '/' +str(p) + '_map.pdf', papertype='A4', edgecolor='k')
