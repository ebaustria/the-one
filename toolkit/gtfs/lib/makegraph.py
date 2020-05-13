import pandas as pd
from datetime import datetime, timedelta
from pandas import DataFrame
import matplotlib.pyplot as plt


class Graph:

    def make_graph(self, routes: DataFrame, services, trips):

        start_date = str(services.at[0, 'start_date'])

        start_date = datetime.strptime(start_date, '%Y%m%d')

        end_date = start_date + timedelta(days=7)

        day_list = []
        delta = timedelta(days=1)
        current_date = start_date

        while current_date < end_date:
            day_list.append(current_date)
            current_date += delta

        eligible_trips = pd.merge(
            trips[['route_id', 'service_id']],
            routes[['route_id', 'route_short_name']],
            on=['route_id']
        )

        pd.options.display.max_columns = None

        eligible_trips = pd.merge(
            eligible_trips,
            services[['service_id', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']],
            on=['service_id']
        )

        pd.options.display.max_columns = None

        placeholder = []
        placeholder_value = 0

        for date in day_list:
            placeholder.append(placeholder_value)
            placeholder_value += 1

        total_trips = {'Days': day_list}
        for r in routes['route_short_name']:
            total_trips[r] = placeholder

        graph_df = pd.DataFrame(total_trips, columns=total_trips.keys())

        days_df = graph_df['Days'].dt.day_name()

        for column, days in graph_df.items():
            if column != graph_df.columns[0]:
                comparison_df = eligible_trips.loc[eligible_trips['route_short_name'] == column]
                days.index = days_df
                for i, day in days.iteritems():
                    index = i
                    index = index.lower()
                    for d, t in comparison_df.items():
                        if d == index:
                            index = days_df.index[day]
                            day = t.sum()
                            graph_df.at[index, column] = day

        graph_df = graph_df.drop(columns='Days')
        graph_df.index = days_df
        graph = graph_df.plot.line(grid=True, title='Number of Daily Trips by Line', figsize=(10, 7))
        graph.set_ylabel('Number of Trips')
        plt.show()
