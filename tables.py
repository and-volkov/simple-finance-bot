import os
import sqlite3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import db_queries


class GraphStatistic:
    def __init__(self):
        self.action = 'pandas'
        self.graph_folder = os.path.dirname('graphs/')
        self.queries_dict = {
            'GraphToday': db_queries.get_today_stats(self.action),
            'GraphWeek': db_queries.get_weekly_stats(self.action),
            'GraphMonth': db_queries.get_monthly_stats(self.action),
            'GraphAllTime': db_queries.get_top_ten_stats(self.action)
        }

        self.connection = sqlite3.connect(os.path.join('db', 'finances.db'))

    def create_plot(self, query_name):
        df = pd.read_sql(
            self.queries_dict[query_name],
            self.connection
        )

        fig = plt.figure(figsize=(8, 4))
        plt.grid(True)
        plt.title('expenses')
        plt.barh(
            df['subcategorie'], df['summary'],
            height=0.7,
            color=mcolors.TABLEAU_COLORS)
        fig.savefig(os.path.join(self.graph_folder, 'output.png'))
