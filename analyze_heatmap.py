
import datetime

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("arena.results.csv", index_col=0)

f, ax = plt.subplots(figsize=(8, 4))
plt.title("Performance Results", fontsize=18)
ax = sns.heatmap((df*100).astype(int), annot=True, fmt="d", cmap='BuGn', linewidth=0.30)
ax.set_xlabel('Player 1')
ax.set_ylabel('Player 2')
plt.yticks(rotation=0) 
# ax = sns.heatmap((df*100).astype(int), annot=True, fmt="d", cmap='RdBu', linewidth=0.30)

fig = ax.get_figure()
fig.savefig('www/performance_results.png')

print('Written Heatmap', datetime.datetime.now().isoformat())