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

        file_name = 'data/checkee_' + month + '.csv'
        df = pd.read_csv(file_name)

        # remove unqualified 
        rows_to_drop = []
        for index, row in df.iterrows():
            if float(row['Waiting Day(s)']) < 7:
                rows_to_drop.append(index)

        df = df.drop(df.index[rows_to_drop]).reset_index(drop=True)
        df.to_csv('test.csv')

        durations = df.loc[:, 'Waiting Day(s)'][::-1]
        status = df.loc[:, 'Status'][::-1]
        check_dates = df.loc[:, 'Check Date'][::-1]
        complete_dates = df.loc[:, 'Complete Date'][::-1]

        current_day = ''
        consolidated_dates = []
        for ii in range(len(check_dates)):
            day = check_dates[ii]
            if current_day != day:
                consolidated_dates.append(day)
                current_day = day

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


# for i, check_date in enumerate(check_dates):
#     if i == len(check_dates):
#         break
#     else:
#         if same_day[-1] == check_dates[i+1]:
#             same_day.append(check_dates[i])
            


# ratio of cleared cases over total number cases, day by day

# fig, ax = plt.subplots()

# ax.bar(month, np.multiply(ratio, 100))

# ax.set(xlabel='Month', ylabel='Percentage that cleared', title='Clear/Total')
# ax.grid()

# fig.set_size_inches(16, 9)
# fig.savefig("checkee_main_page.png", dpi=300)