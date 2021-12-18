import torch
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import seaborn as sns
from pylab import rcParams
import matplotlib.pyplot as plt
from matplotlib import rc
from sklearn.preprocessing import MinMaxScaler
from pandas.plotting import register_matplotlib_converters
from Predictor import CryptoPredictor



sns.set(style='whitegrid', palette='muted', font_scale=1.2)

HAPPY_COLORS_PALETTE = ["#01BEFE", "#FFDD00", "#FF7D00", "#FF006D", "#93D30C", "#8F00FF"]

sns.set_palette(sns.color_palette(HAPPY_COLORS_PALETTE))

rcParams['figure.figsize'] = 14, 10
register_matplotlib_converters()

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)

preds = []
DAYS_TO_PREDICT=12
num_epochs = 60
# df = pd.read_csv('data/LTC-USD.csv')
# daily_price = df["Close"]
# daily_price.index = pd.to_datetime(df["Date"])

def get_data(crypt):
    df = pd.read_csv(f"data/{crypt}.csv")
     # df = pd.read_csv('data/LTC-USD.csv')
    daily_price = df["Close"]
    daily_price.index = pd.to_datetime(df["Date"])
    return  daily_price







def create_sequences(data, seq_length):
    xs = []
    ys = []

    for i in range(len(data)-seq_length-1):
        x = data[i:(i+seq_length)]
        y = data[i+seq_length]
        xs.append(x)
        ys.append(y)

    return np.array(xs), np.array(ys)



def train_model(
        model,
        train_data,
        train_labels,
        test_data=None,
        test_labels=None
):
    loss_fn = torch.nn.MSELoss(reduction='sum')

    optimiser = torch.optim.Adam(model.parameters(), lr=1e-3)


    train_hist = np.zeros(num_epochs)
    test_hist = np.zeros(num_epochs)

    for t in range(num_epochs):
        model.reset_hidden_state()

        y_pred = model(X_all)

        loss = loss_fn(y_pred.float(), y_all)
        DAYS_TO_PREDICT = 12
        if all_data is not None:
            with torch.no_grad():
                test_seq = X_all[:1]
                preds.clear()
                for _ in range(DAYS_TO_PREDICT):
                    y_test_pred = model(test_seq)
                    pred = torch.flatten(y_test_pred).item()
                    preds.append(pred)
                    new_seq = test_seq.numpy().flatten()
                    new_seq = np.append(new_seq, [pred])
                    new_seq = new_seq[1:]
                    test_seq = torch.as_tensor(new_seq).view(1, seq_length, 1).float()


            if t % 1 == 0:
                print(f'Epoch {t} train loss: {loss.item()}')



        train_hist[t] = loss.item()

        optimiser.zero_grad()

        loss.backward()

        optimiser.step()

    return model.eval(), train_hist, test_hist



daily_price=get_data("BTC-USD")

scaler = MinMaxScaler()
scaler = scaler.fit(np.expand_dims(daily_price, axis=1))
all_data = scaler.transform(np.expand_dims(daily_price, axis=1))
seq_length = 12
X_all, y_all = create_sequences(all_data, seq_length)

X_all = torch.from_numpy(X_all).float()
y_all = torch.from_numpy(y_all).float()



model = CryptoPredictor(
  n_features=1,
  n_hidden=80,
  seq_len=seq_length,
  n_layers=2
)
model, train_hist, _ = train_model(
  model,
  X_all,
  y_all
)







predicted_cases = scaler.inverse_transform(
  np.expand_dims(preds, axis=0)
).flatten()
predicted_index = pd.date_range(
  start=daily_price.index[-1],
  periods=DAYS_TO_PREDICT + 1,
  closed='right'
)

predicted_cases = pd.Series(
  data=predicted_cases,
  index=predicted_index
)

print( predicted_cases)
plt.plot(daily_price, label='Historical Daily Cases')
plt.plot(predicted_cases, label='Predicted Daily Cases')

plt.figlegend()
plt.show()





