import torch
import numpy as np
import pandas as pd
import seaborn as sns
from pylab import rcParams
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

from Train import preds, DAYS_TO_PREDICT, scaler ,daily_price,total_price



sns.set(style='whitegrid', palette='muted', font_scale=1.2)

HAPPY_COLORS_PALETTE = ["#01BEFE", "#FFDD00", "#FF7D00", "#FF006D", "#93D30C", "#8F00FF"]

sns.set_palette(sns.color_palette(HAPPY_COLORS_PALETTE))

rcParams['figure.figsize'] = 14, 10
register_matplotlib_converters()

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)






predicted_cases = scaler.inverse_transform(
  np.expand_dims(preds, axis=0)
).flatten()
predicted_index = pd.date_range(
  start=total_price.index[-1],
  periods=DAYS_TO_PREDICT + 1,
  closed='right'
)

predicted_cases = pd.Series(
  data=predicted_cases,
  index=predicted_index
)

print( predicted_cases)
plt.plot(total_price, label='Historical Daily Cases')
plt.plot(predicted_cases, label='Predicted Daily Cases')

plt.figlegend()
plt.show()





