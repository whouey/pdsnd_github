import time
import pandas as pd
import numpy as np
from datetime import datetime as dt
from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype
import calendar

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    while not city:
        input_str = input(
            '\nPlease input a city name among chicago, new york city and washington.\n').lower()

        if input_str in CITY_DATA:
            city = input_str
        else:
            print(
                'The city name dosen\'t supported or can\'t be recognized. Please try again.')

    # get user input for month (all, january, february, ... , june)
    month = None
    while not month:
        input_str = input(
            '\nPlease input a month name, or `all` for all month.\n').lower()

        if input_str.capitalize() in ['All', *calendar.month_name[1:], *calendar.month_abbr[1:]]:
            month = input_str
        else:
            print('The month name can\'t be recognized, please try again.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = None
    while not day:
        input_str = input(
            '\nPlease input a day name, or `all` for all weekdays.\n').lower()

        if input_str.capitalize() in ['All', *calendar.day_name, *calendar.day_abbr]:
            day = input_str
        else:
            print('The day name can\'t be recognized, please try again.')

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    if city not in CITY_DATA:
        raise ValueError

    # refine data types
    df = pd.read_csv(f'./{CITY_DATA[city]}')

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # filter by month
    if month != 'all':
        month = month.capitalize()
        if month in calendar.month_name:
            month = dt.strptime(month, '%B').month
        elif month in calendar.month_abbr:
            month = dt.strptime(month, '%b').month
        else:
            raise ValueError

        df = df[(df['Start Time'].dt.month == month)
                | (df['End Time'].dt.month == month)]

    # filter by weekday
    if day != 'all':
        day = day.capitalize()
        if day in calendar.day_name:
            day = dt.strptime(day, '%A').weekday()
        elif day in calendar.day_abbr:
            day = dt.strptime(day, '%a').weekday()
        else:
            raise ValueError

        df = df[(df['Start Time'].dt.weekday == day)
                | (df['End Time'].dt.weekday == day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    assert is_datetime64_any_dtype(df['Start Time'].dtype)

    # display the most common month
    most_common_month = \
        calendar.month_name[df['Start Time'].dt.month.mode()[0]]

    print(f'The most common month is {most_common_month}')

    # display the most common day of week
    most_common_day = \
        calendar.day_name[df['Start Time'].dt.weekday.mode()[0]]
    print(f'The most common day is {most_common_day}')

    # display the most common start hour
    most_common_hour = df['Start Time'].dt.hour.mode()[0]
    print(f'The most common hour is {most_common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print(f'The most commonly used start station is "{start_station}"')

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print(f'The most commonly used end station is "{end_station}"')

    # display most frequent combination of start station and end station trip
    trip_stations = \
        df[['Start Station', 'End Station']] \
        .value_counts().reset_index() \
        .loc[0, ['Start Station', 'End Station']]
    print(
        f'The most frequent trip is from "{trip_stations[0]}" to "{trip_stations[1]}".')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    assert is_numeric_dtype(df['Trip Duration'].dtype)

    # display total travel time
    print(f"The total travel time is {df['Trip Duration'].sum():.0f} seconds")

    # display mean travel time
    print(
        f"The average travel time is {df['Trip Duration'].mean():.2f} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    assert is_numeric_dtype(df['Birth Year'].dtype)

    # Display counts of user types
    print('The counts of user types:')
    print(df['User Type'].value_counts())

    # Display counts of gender
    print('\n\nThe counts of gender:')
    print(df['Gender'].value_counts())
    print()

    # Display earliest, most recent, and most common year of birth
    print(f"The earliest year of birth is {df['Birth Year'].min():.0f}.")
    print(f"The latest year of birth is {df['Birth Year'].max():.0f}.")
    print(
        f"The most common year of birth is {df['Birth Year'].mode()[0]:.0f}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    """
    This is the main module of the file, it does:
    1. retrieve and filter data the user specified
    2. show the data by a page of 5 if requested
    3. show analytics of the data
    4. go back to 1. if the user like to
    """
    while True:
        # get user inputs
        city, month, day = get_filters()

        # load and filter
        try:
            df = load_data(city, month, day)
        except:
            print('Load data failed, please try again.')
            continue

        # show the raw data if requested
        show_raw_data = input(
            '\nWould you like to checkout the raw data? Enter yes or no. (default to no)\n').lower()
        if show_raw_data == 'yes' or show_raw_data == 'y':
            page = 0
            while True:
                df_page = df.iloc[page * 5:(page + 1) * 5, :]

                print(
                    f'Showing the data [{(page * 5) + 1}:{(page + 1) * 5}] out of {df.shape[0]}')
                print(df_page)

                page += 1

                if page * 5 >= df.shape[0]:
                    print('\nThere is no more data to show.')
                    break

                cont = input(
                    '\nContinue to next page? Enter yes or no. (default to no)\n').lower()
                if cont != 'yes' and cont != 'y':
                    break
            print('-' * 40)

        # do analytics
        try:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        except Exception as e:
            print('Something went wrong while analyzing the data, the error is:\n')
            print(e)

        # ask if restart
        restart = input(
            '\nWould you like to restart? Enter yes or no. (default to no)\n')
        if restart.lower() not in {'yes', 'y'}:
            break


if __name__ == "__main__":
    main()
