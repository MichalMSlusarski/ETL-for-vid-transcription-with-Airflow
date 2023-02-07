import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 20)

dataset = pd.read_csv(r'C:/Users/mslus/ML-projects-with-Python/ov2_this_week.csv')

# Data for plotting

dataset.plot.scatter(x="display_text_width", y="statuses_count", alpha=0.5)

print(type(dataset))
print(dataset.loc[:, 'display_text_width'])

hist_of_text_width = dataset.hist('display_text_width')

plt.show()
