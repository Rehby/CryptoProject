import torch
import numpy as np
import pandas as pd
import seaborn as sns
from pylab import rcParams
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

from Predictor import CryptoPredictor
from Train import train_model



sns.set(style='whitegrid', palette='muted', font_scale=1.2)

HAPPY_COLORS_PALETTE = ["#01BEFE", "#FFDD00", "#FF7D00", "#FF006D", "#93D30C", "#8F00FF"]

sns.set_palette(sns.color_palette(HAPPY_COLORS_PALETTE))

rcParams['figure.figsize'] = 14, 10
register_matplotlib_converters()

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
DAYS_TO_PREDICT=12
num_epochs = 60
seq_length = 12
ticker="BTC-USD"

model = CryptoPredictor(
  n_features=1,
  n_hidden=80,
  seq_len=seq_length,
  n_layers=2
)
model, trn, tst,preds,total_price,scaler = train_model(
  model,
  num_epochs,
  seq_length,
  ticker
)


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





