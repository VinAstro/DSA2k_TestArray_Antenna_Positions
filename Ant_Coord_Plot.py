#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 09:55:51 2025

@author: vinand
"""
import numpy as np
import matplotlib.pyplot as plt
from pyproj import Transformer
from matplotlib.patches import Rectangle, ConnectionPatch

# Antenna coordinates (longitude, latitude)
antenna_coords = [
    (-118.28085914, 37.2333311),    # Antenna 09
    (-118.28085968, 37.23345725),   # Antenna 08
    (-118.28077818, 37.23339358),   # Antenna 07
    (-118.28070317, 37.23331983),   # Antenna 06
    (-118.28069784, 37.23345807),   # Antenna 03
    (-118.294838294, 37.2314483819) # Antenna 01
]

# Updated antenna numbers according to your specification
antenna_num = ['09', '08', '07', '06', '03', '01']

# Use Antenna 07 (index 2) as the origin/center for our projection
center_lon, center_lat = antenna_coords[2]  # Antenna 07 coordinates
transformer = Transformer.from_crs(
    "EPSG:4326",  # WGS84
    f"+proj=tmerc +lat_0={center_lat} +lon_0={center_lon} +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs",
    always_xy=True
)

# Convert to local Cartesian coordinates (in meters)
x_coords = []
y_coords = []

for lon, lat in antenna_coords:
    x, y = transformer.transform(lon, lat)
    x_coords.append(x)
    y_coords.append(y)

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

# Plot 1: All antennas (left plot)
ax1.scatter(x_coords, y_coords, color='red', s=100, marker='^')

# Only label Antenna 01 (which is the last one, index 5) on the left plot
ax1.annotate(f'Ant {antenna_numbers[5]}', (x_coords[5], y_coords[5]), 
             textcoords="offset points", xytext=(0, 10), ha='center')

# Draw a solid square around the clustered antennas
cluster_x = [x for i, x in enumerate(x_coords) if i != 5]  # All but antenna 01
cluster_y = [y for i, y in enumerate(y_coords) if i != 5]
cluster_center_x = np.mean(cluster_x)
cluster_center_y = np.mean(cluster_y)

# Calculate the size for a perfect square
max_dist = max([max([abs(x - cluster_center_x) for x in cluster_x]), 
                max([abs(y - cluster_center_y) for y in cluster_y])])
                
# Make the square larger with a scaling factor
square_half_size = max_dist * 3.0  # Large scaling factor for a bigger square

# Create the square
square = Rectangle(
    (cluster_center_x - square_half_size, cluster_center_y - square_half_size),
    2 * square_half_size, 2 * square_half_size,
    fill=False, linewidth=2, color='black', alpha=0.7
)
ax1.add_patch(square)

# Add grid, labels, and title for the left plot
ax1.grid(True)
ax1.set_xlabel('East-West Distance (meters)')
ax1.set_ylabel('North-South Distance (meters)')
ax1.set_title('Antenna Locations')

# Plot 2: Zoomed in on the cluster (right plot)
# Extract just the cluster coordinates (all but antenna 01)
x_cluster = [x_coords[i] for i in range(len(x_coords)) if i != 5]
y_cluster = [y_coords[i] for i in range(len(y_coords)) if i != 5]
cluster_numbers = [antenna_numbers[i] for i in range(len(antenna_numbers)) if i != 5]

# Plot and label the clustered antennas
ax2.scatter(x_cluster, y_cluster, color='red', s=100, marker='^')
for i, (x, y, num) in enumerate(zip(x_cluster, y_cluster, cluster_numbers)):
    ax2.annotate(f'Ant {num}', (x, y), textcoords="offset points", 
                xytext=(0, 10), ha='center')

# Add grid, labels, and title for the right plot
ax2.grid(True)
ax2.set_xlabel('East-West Distance (meters)')
ax2.set_title('Zoomed View of Clustered Antennas')

# # Add origin information
# origin_text = f'Origin (0,0) corresponds to:\nLongitude: {center_lon}\nLatitude: {center_lat}'
# props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# ax1.text(0.05, 0.05, origin_text, transform=ax1.transAxes, fontsize=9,
#         verticalalignment='bottom', bbox=props)

# Add solid connecting lines between the square and the zoomed view
con1 = ConnectionPatch(
    xyA=(cluster_center_x - square_half_size, cluster_center_y), 
    coordsA=ax1.transData,
    xyB=(ax2.get_xlim()[0], (ax2.get_ylim()[0] + ax2.get_ylim()[1])/2), 
    coordsB=ax2.transData,
    color="black", linewidth=2, alpha=0.7
)
fig.add_artist(con1)

con2 = ConnectionPatch(
    xyA=(cluster_center_x + square_half_size, cluster_center_y), 
    coordsA=ax1.transData,
    xyB=(ax2.get_xlim()[1], (ax2.get_ylim()[0] + ax2.get_ylim()[1])/2), 
    coordsB=ax2.transData,
    color="black", linewidth=2, alpha=0.7
)
fig.add_artist(con2)

plt.tight_layout()
plt.savefig('antenna_map_final.png', dpi=300, bbox_inches='tight')
plt.show()
