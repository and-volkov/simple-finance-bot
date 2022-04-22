import os
import sqlite3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import db_queries


graphs_folder = os.path.dirname('graphs')

connection = sqlite3.connect(os.path.join('db', 'finances.db'))
cursor = connection.cursor()

query = db_queries.get_monthly_stats(action='pandas')
df = pd.read_sql(query, connection)

plt.figure(figsize=(10, 7))
plt.grid(True)
plt.title('expenses')
plt.barh(
    df['subcategorie'], df['summary'],
    height=0.7,
    color=mcolors.TABLEAU_COLORS)
plt.show()
