import matplotlib.pyplot as plt
import numpy as np

# noinspection PyUnresolvedReferences
import matplotlib.backends.backend_qt5agg

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
x = np.array([1, 2, 3, 4, 5])
y = np.array([3, 3, 4, 3, 1])
ax.plot(x, y, 'o-', label='plot1')
ax.legend(frameon=False)
plt.show()
