# -*- coding: utf-8 -*-
"""Metro Network Analysis.ipynb
"""

#indicate file path for the dataset
filepath = "/content/drive/MyDrive/Delhi-Metro-Network.csv"

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Loading the data
df = pd.read_csv(filepath)
print(df.head())

#Understand the shape of dataset
df.shape

#Get general info about the dataset
df.info()

#check for missing values in the dataframe
df.isna().sum()

#Understand the datatypes
df.dtypes

#The dataframe has a date column that needs to be converted to date time format for easier data processing
def convert_to_datetime(df, date_col):
  """
  This function converts a date column in a pandas DataFrame to datetime format.

  Args:
      df (pandas.DataFrame): The DataFrame containing the date column.
      date_col (str): The name of the column containing dates.

  Returns:
      pandas.DataFrame: The DataFrame with the date column converted to datetime format.
  """
  # Try to infer the date format automatically (recommended)
  try:
    df[date_col] = pd.to_datetime(df[date_col], infer_datetime_format=True)
  except pd.errors.ParserError:
    # If automatic inference fails, handle specific format (optional)
    # Replace '%Y-%m-%d' with your actual date format if needed
    df[date_col] = pd.to_datetime(df[date_col], format='%Y-%m-%d')
  return df

#Apply the function
df = convert_to_datetime(df, "Opening Date")

# Summary statistics
print(df.describe())

"""Examine characteristics of different metro lines, including station count and average distances between stations."""

# Grouping Data by Metro Lines
grouped_lines = df.groupby('Line')

# Calculating Station Count
station_count = grouped_lines['Station Name'].nunique()

# Calculating Average Distances Between Stations
average_distances = grouped_lines['Distance from Start (km)'].mean()

# Visualization
plt.figure(figsize=(10, 6))

# Station Count
plt.subplot(1, 2, 1)
station_count_sorted = station_count.sort_values()
station_count_sorted.plot(kind='bar', color='skyblue')
plt.title('Station Count by Metro Line')
plt.xlabel('Metro Line')
plt.ylabel('Station Count')

# Average Distances Between Stations
plt.subplot(1, 2, 2)
average_distances_sorted = average_distances.sort_values()
average_distances_sorted.plot(kind='bar', color='lightgreen')
plt.title('Average Distance Between Stations by Metro Line')
plt.xlabel('Metro Line')
plt.ylabel('Average Distance (km)')

plt.tight_layout()
plt.show()

"""Analyze the types of station layouts and their distribution across the network."""

# Grouping Data by Station Layout
grouped_layouts = df.groupby('Station Layout')

# Counting the Frequency of Each Station Layout
layout_counts = grouped_layouts.size()

# Counting the Frequency of Each Station Layout and sorting
layout_counts_sorted = layout_counts.sort_values()

# Visualization with sorting
plt.figure(figsize=(8, 6))
layout_counts_sorted.plot(kind='bar', color='skyblue')
plt.title('Distribution of Station Layouts Across the Network (Sorted)')
plt.xlabel('Station Layout')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.show()

"""Create KDE plots for each station layout to visualize the distribution of distances more smoothly."""

# KDE Plot for each Station Layout
plt.figure(figsize=(10, 6))
for layout in df['Station Layout'].unique():
    sns.kdeplot(df[df['Station Layout'] == layout]['Distance from Start (km)'], label=layout)
plt.title('Kernel Density Estimation (KDE) Plot of Distance from Start by Station Layout')
plt.xlabel('Distance from Start (km)')
plt.ylabel('Density')
plt.legend()
plt.show()

# Extracting the opening year from the opening date
df['Opening Year'] = df['Opening Date'].dt.year

# Counting the number of stations opened each year
stations_per_year = df['Opening Year'].value_counts().sort_index()

# Creating a DataFrame from the counted values
dfstations_per_year = stations_per_year.reset_index()
dfstations_per_year.columns = ['Year', 'Number of Stations']

# Creating a bar plot using matplotlib and seaborn
plt.figure(figsize=(10, 6))
sns.barplot(x='Year', y='Number of Stations', data=dfstations_per_year, color='green')

# Customizing the plot
plt.title("Number of Metro Stations Opened Each Year in Delhi")
plt.xlabel("Year")
plt.ylabel("Number of Stations Opened")
plt.xticks(rotation=45)
plt.grid(axis='y')

# Show the plot
plt.show()

import folium

# Defining a color scheme for the metro lines
line_colors = {
    'Red line': 'red',
    'Blue line': 'blue',
    'Yellow line': 'beige',
    'Green line': 'green',
    'Voilet line': 'purple',
    'Pink line': 'pink',
    'Magenta line': 'darkred',
    'Orange line': 'orange',
    'Rapid Metro': 'cadetblue',
    'Aqua line': 'black',
    'Green line branch': 'lightgreen',
    'Blue line branch': 'lightblue',
    'Gray line': 'lightgray'
}

# Create a map centered around Delhi
delhi_map_with_line_tooltip = folium.Map(location=[28.7041, 77.1025], zoom_start=11)

# Adding colored markers for each metro station with line name in tooltip
for index, row in df.iterrows():
    line = row['Line']
    color = line_colors.get(line, 'black')  # Default color is black if line not found in the dictionary
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['Station Name']}",
        tooltip=f"{row['Station Name']}, {line}",
        icon=folium.Icon(color=color)
    ).add_to(delhi_map_with_line_tooltip)

# Displaying the updated map
delhi_map_with_line_tooltip