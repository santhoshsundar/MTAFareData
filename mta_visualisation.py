import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


bar_width = .6
year = [yr for yr in range(2010, 2018)]
month = [mth for mth in range(1, 13)]


# Import CSV file
df = pd.read_csv('MTA_Fare_Data.csv')


# Change string date to date date
df['From Date'] = pd.to_datetime(df['From Date'])
df['To Date'] = pd.to_datetime(df['To Date'])

# Create year and month column

df['year'] = df['From Date'].dt.year
df['month'] = df['From Date'].dt.month

# Calculate Total value for each row

column = df.columns.values.tolist()
column.remove('From Date')
column.remove('To Date')
column.remove('Remote Station ID')
column.remove('Station')
column.remove('year')
df['total'] = df[column].sum(axis=1)

# Setting and Sorting Index

df.set_index(['year', 'month'], inplace=True)
df.sort_index(inplace=True)

# Total MTA Swipe Count for all year


def total_swipe_count():
    df.reset_index(inplace=True)
    df.set_index(['year', 'month'], inplace=True)
    df.sort_index(inplace=True)
    group_by_year = df.groupby(by=['year'])['total'].sum()
    group_by_year = group_by_year[1:]
    xindex = range(len(group_by_year))
    ax = plt.subplot()
    group_by_year = group_by_year / (1000000)
    plt.bar(xindex, group_by_year, width=bar_width)
    plt.xlabel('Year', fontsize=15)
    plt.ylabel('Count(Million)', fontsize=15)
    plt.xticks(xindex, year, fontsize=10, rotation=30)
    plt.title('Total MTA Card Swipe Number')
    plt.show()

# Top 10 Busiest MTA Railway Station for a year


def busiest_mta_station(year):
    df.reset_index(inplace=True)
    df.set_index(['year', 'month'], inplace=True)
    df.sort_index(inplace=True)
    df1 = df.loc[year]
    group_by_station = df1.groupby(by=['Station'])['total'].sum().sort_values(ascending=False)
    group_by_station = group_by_station[0:11]
    group_by_station_index = list(group_by_station.index)
    group_by_station_index = [names for index, names in enumerate(group_by_station_index) if index <11]
    ax = plt.subplot()
    y_pos = np.arange(len(group_by_station))
    values_range = [value for value in np.arange(0, 40, 5)]
    plt.barh(y_pos, group_by_station)
    ax.invert_yaxis()
    ax.set_yticks(y_pos)
    ax.set_yticklabels(group_by_station_index)
    ax.set_xticklabels(values_range)
    plt.xlabel('Annual Average Swipe Count(Million)', fontsize=10)
    ax.set_title('Top 10 Busiest MTA Railway Station'+" " + year)
    plt.show()

# Station count in all year


def station_count_year(station):
    look_station = station
    df.reset_index(inplace=True)
    df.set_index(['Station', 'year', 'month'], inplace=True)
    df.sort_index(inplace=True, ascending=True)
    groupby_station_year = df.groupby(by='year')['total'].sum()
    groupby_station_year = groupby_station_year[1:]
    xindex = range(len(groupby_station))
    ax = plt.subplot()
    groupby_station_year = groupby_station_year / (1000000)
    plt.bar(xindex, groupby_station_year, width=bar_width)
    plt.xlabel('Year', fontsize=15)
    plt.ylabel('Count(Million)', fontsize=15)
    plt.xticks(xindex, year, fontsize=10, rotation=30)
    plt.title(look_station)
    plt.show()

# Station with fare type in all year


def station_fare_type_year(station, fare_type):
    df.reset_index(inplace=True)
    df.set_index(['Station', 'year', 'month'], inplace=True)
    df.sort_index(inplace=True, ascending=True)
    look_station = station
    fare_type = fare_type
    df2 = df.loc[(slice(look_station), slice(None), slice(None)), :]
    groupby_fare_type = df2.groupby(by='year')[fare_type].sum()
    groupby_fare_type = groupby_fare_type[1:]
    xindex = range(len(groupby_fare_type))
    ax = plt.subplot()
    groupby_fare_type = groupby_fare_type / (1000000)
    plt.bar(xindex, groupby_fare_type, width=bar_width)
    plt.xlabel('Year', fontsize=15)
    plt.ylabel('Count(Million)', fontsize=15)
    plt.xticks(xindex, year, fontsize=10, rotation=30)
    plt.title(fare_type + " " + 'Swipe Count')
    plt.show()


# Station with fare type in months of particular year


def station_fare_type_month(station, fare_type, year):
    df.reset_index(inplace=True)
    df.set_index(['Station', 'year', 'month'], inplace=True)
    df.sort_index(inplace=True, ascending=True)
    look_station = station
    fare_type = fare_type
    yr = year
    df3 = df.loc[(slice(look_station), slice(yr), slice(None)), :]
    groupby_fare_type_month = df3.groupby(by='month')[fare_type].sum()
    xindex = range(len(groupby_fare_type_month))
    ax = plt.subplot()
    groupby_fare_type_month = groupby_fare_type_month / (1000000)
    plt.bar(xindex, groupby_fare_type_month, width=bar_width)
    plt.xlabel('Month', fontsize=15)
    plt.ylabel('Count(Million)', fontsize=15)
    plt.xticks(xindex, month, fontsize=10, rotation=30)
    plt.title(fare_type + " " + "Swipe Count")
    plt.show()
