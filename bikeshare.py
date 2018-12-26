import time
import calendar
import pandas as pd
import numpy as np
import sys


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city

    while True:
        city = input("\nWould you like to see data for Chicago, New York City, or Washington? \n").lower()
        if city.title() not in ('Chicago', 'New York City', 'Washington'):
            print("Sorry, I did not understand your answer.")
        else:
            print("Ok, let's take a look at {}'s bikeshare data.".format(city.title()))
            break


    # Get user input for month

    while True:
        month = input("\nWhich month would you like to see data for? January, February, March, April, May, June, or all months? \n").lower()
        if month.title() not in ('January', 'February', 'March', 'April', 'May', 'June', 'All'):
            print("Sorry, I did not understand you.")
        else:
            print("Great, we'll focus on {}. What a lovely time of year.".format(month.title()))
            break

    # Get user input for day of week
    while True:
        day = input("\nWhich day of the week would you like to see data for? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all days? \n").lower()
        if day.title() not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All'):
            print("Sorry, I did not understand you.")
        else:
            print("Ok, {} it is. Let's take a look at the data.".format(day.title()))
            break

    print('-'*40)
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
# Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

# Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

# Extract month and day of week from Start Time to create new column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

# Filter by month if applicable
    if month != 'all':
    # use the index of the months list to get the correspondeing int
        months = ['january', 'february', 'march', 'april', 'may','june']
        month = months.index(month) + 1
    # Filter by month to create the new dataframe
        df = df[df['month'] == month]
# Filter by day of week if applicable
    if day != 'all':
    # filter by day of week to create a new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    # Convert the Start TIme column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month from Start Time column and create new column
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print("Most common month: ", calendar.month_name[popular_month])


    # Display the most common day of week

    # Extract day of week from Start Time column and create new column
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # find most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]

    print("Most common day of week: ", popular_day_of_week)

    # Display the most common start hour

    # Extract hour from Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]

    print("Most common start hour: ", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    print("The most common station to start a trip: ", popular_start_station)

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    print("The most common station to end a trip: ", popular_end_station)

    # Display most frequent combination of start station and end station trip
    df['station_combo'] = "From: " + df['Start Station'] +" to " + df['End Station']
    popular_station_combo = df['station_combo'].mode()[0]

    print("Most frequent combination of stations to start and end a trip: ", popular_station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time in minutes
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time: {} minutes.".format(total_travel_time/60))

    # Display mean travel time in minutes
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time: {} minutes.".format(mean_travel_time/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # Display counts of user types
    if df.columns.isin(['User Type']).any():
        user_types = df['User Type'].value_counts()
        print(user_types)
    else:
        print('There is no User Type data for this dataset.')


    # Display counts of gender
    if df.columns.isin(['Gender']).any():
        user_gender = df['Gender'].value_counts()
        print(user_gender)
    else:
        print('There is no Gender data for this dataset.')


    # Display earliest, most recent, and most common year of birth
    if df.columns.isin(['Birth Year']).any():
        earliest_birth_year = df['Birth Year'].min()
        print("The oldest subscriber of the bikeshare service was born in {}.".format(earliest_birth_year))

        most_recent_birth_year = df['Birth Year'].max()
        print("The youngest subscriber of the bikeshare service was born in {}.".format(most_recent_birth_year))

        common_birth_year = df['Birth Year'].mode()[0]
        print("The most common birth year of the bikeshare's subscribers is {}.".format(common_birth_year))
    else:
        print('There is no Birth Year data for this dataset.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Display raw data
        # Set counter to zero
        x = 0
        # Set view_raw_data to something other than 'No'
        view_raw_data = ''
        while view_raw_data != "no":
            view_raw_data = input("\nWould you like to take a look at some of the raw data? Type yes or no. \n").lower()
            if view_raw_data != "no":
                print(df.iloc[x:x+5])
                x = x+5

# If user does not want to see more data, allow the user to restart or exit the program
        # Set restart to something other than 'No'
        restart = ''

        while restart != "no":
            restart = input("\nWould you like to restart the program? Enter yes or no.\n").lower()
            if restart != "no":
                print("\nEnjoy. Perhaps try a different city.\n")
                main()
        if restart == "no":
            print("\nGoodbye!\n")
            sys.exit(0)



if __name__ == "__main__":
    main()
