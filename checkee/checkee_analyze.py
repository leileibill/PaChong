import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt


def load_main_table_data():
    # load main table from csv
    file_name = 'data/checkee_main_table.csv'
    df = pd.read_csv(file_name)

    month = df.loc[:, 'Month'][::-1]
    total = np.array(df.loc[:, 'Total'], dtype=np.float)[::-1]
    clear = np.array(df.loc[:, 'Clear'], dtype=np.float)[::-1]

    # waiting durations before clear
    duration = np.array(df.loc[1:, 'Ave. Waiting Days for Complete Cases'], dtype=np.float)[::-1]

    # ratio of cleared cases over total number of cases
    ratio = np.divide(clear, total)

    return (month, duration, clear)


## Process monthly data
def load_and_process_month(month):
    # month = '2019-01'
    file_name = 'data/checkee_' + month + '.csv'
    df = pd.read_csv(file_name)

    # remove rows with waiting days fewer than 8
    df = df.drop(df.index[df['Waiting Day(s)'] < 8]).reset_index(drop=True)

    durations = df.loc[:, 'Waiting Day(s)']
    status = df.loc[:, 'Status']
    check_dates = df.loc[:, 'Check Date']
    complete_dates = df.loc[:, 'Complete Date']

    consolidated_dates = check_dates.unique()

# total number of cases

# get only cleared cases
# df_cleared = df.loc[df['Status'] == 'Clear']

# consolidated_clear = len(df_cleared)
# consolidated_average = np.array(df_cleared.groupby('Check Date').mean()['Waiting Day(s)'])

# grouped = df.groupby('Check Date')

    print(consolidated_dates)

    consolidated_ratio = []
    consolidated_clear = []
    consolidated_pending = []
    consolidated_reject = []
    consolidated_total = []
    consolidated_average = []
    consolidated_median = []

    for date in consolidated_dates:
        matched_index = [i for i, x in (check_dates == date).iteritems() if x]
        matched_status = status[matched_index]
        matched_durations = durations[matched_index]

        total = len(matched_index)
        clear = sum(matched_status == 'Clear')
        pending = sum(matched_status == 'Pending')
        reject = sum(matched_status == 'Reject')
        ratio = clear / total

        average = sum(matched_durations[matched_status == 'Clear']) / max(clear, 1)
        # median = np.percentile(matched_durations[matched_status == 'Clear'], 50)
        median = 0

        consolidated_ratio.append(ratio)
        consolidated_clear.append(clear)
        consolidated_pending.append(pending)
        consolidated_reject.append(reject)
        consolidated_total.append(total)
        consolidated_average.append(average)
        consolidated_median.append(median)

    return np.array(consolidated_dates), np.array(consolidated_ratio), np.array(consolidated_total), \
            np.array(consolidated_clear), np.array(consolidated_pending), np.array(consolidated_reject), \
            np.array(consolidated_average), np.array(consolidated_median)


## Process data by clear dates
def load_and_process_by_clear_dates():

    file_name = 'data/checkee_by_clear_dates' + '.csv'
    df = pd.read_csv(file_name, dtype={'Waiting Day(s)': np.float64})

    # remove rows with waiting days fewer than 8
    df = df.drop(df.index[df['Waiting Day(s)'] < 8]).reset_index(drop=True)

    complete_dates = df.loc[:, 'Complete Date']

    consolidated_dates = complete_dates.unique()

    print(consolidated_dates)

    consolidated_total = np.zeros(len(consolidated_dates))
    for i, date in enumerate(consolidated_dates):
        consolidated_total[i] = len(complete_dates.index[complete_dates == date])

    return np.array(consolidated_dates), np.array(consolidated_total)

## Process data by clear dates
def load_and_process_by_category():

    file_name = 'data/checkee_by_clear_dates' + '.csv'
    df = pd.read_csv(file_name, dtype={'Waiting Day(s)': np.float64})

    # remove rows with waiting days fewer than 8
    df = df.drop(df.index[df['Waiting Day(s)'] < 8]).reset_index(drop=True)

    # remove rows with waiting days higher than 90
    df = df.drop(df.index[df['Waiting Day(s)'] > 90]).reset_index(drop=True)

    df_embassy = df.groupby('US Consulate').mean()

    df_visa = df.groupby('Visa Type').mean()

    return df_embassy, df_visa
