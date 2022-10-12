# coding: utf-8
# author: xuxc

import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('test.csv', names=['date', 'temperature'])

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)
ax.plot(data['date'], data['temperature'], label='Temperature')
for tick in ax.get_xticklabels():
    tick.set_rotation(18)
ax.legend(frameon=False)
plt.tight_layout()
plt.show()
