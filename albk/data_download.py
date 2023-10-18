import numpy as np
import requests
import os
import json
import csv

# Define the Google Static Maps API base URL
base_url = "https://maps.googleapis.com/maps/api/staticmap?"

# Your Google Maps API Key
api_key = "AIzaSyBgJJgNv8-MSaR1R8yKEHQadis4kputx2I"

# Specify the delta values for latitude and longitude shifts
delta_lat = 0.0020  # Adjust this value for latitude granularity
delta_lon = 0.0025  # Adjust this value for longitude granularity

bottom_left_lon = 76.85
top_right_lon = 77.64

bottom_left_lat = 28.20
top_right_lat = 28.99

#For fixing the values 
updated_bottom_left_lon = 76.85
updated_bottom_left_lat = 28.20

lat_grid = np.arange(updated_bottom_left_lat, top_right_lat, delta_lat)
lon_grid = np.arange(updated_bottom_left_lon, top_right_lon, delta_lon)
Lat, Lon = np.meshgrid(lat_grid, lon_grid)
coords = np.vstack((Lat.flatten(), Lon.flatten())).T

consecutive_failures = 0
if(os.path.exists("index.npy")):
    current_index = np.load("index.npy")
else:
    current_index = 94785

# Directory to save the images
output_directory = "entire_NCR"

# Create the directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Create a CSV file to save image names and coordinates
csv_filename = os.path.join("entire_NCR.csv")

# Loop through the coordinates
for index, (lat, lon) in enumerate(coords):
    if index <= current_index:
        continue

    params = {
        "center": f"{lat},{lon}",
        "zoom": 17,
        "size": "256x276",
        "maptype": "satellite",
        "key": api_key,
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        consecutive_failures = 0
        filename = os.path.join(output_directory, f"{round(lat,4)}_{round(lon,4)}.png")

        with open(filename, "wb") as img_file:
            img_file.write(response.content)

        # Save image information to the CSV file
        with open(csv_filename, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([f"{round(lat,4)}_{round(lon,4)}.png", round(lat,4), round(lon,4)])

        print(f"Saved image {filename}")
    else:
        consecutive_failures += 1
        if consecutive_failures >= 10:
            # Save the index of the last successful image
            np.save("index.npy", index - 10)
            break
        