import numpy as np
import torch

from Predictor import CryptoPredictor
from sklearn.preprocessing import MinMaxScaler
from  DataProcessing import  get_data, create_sequences



preds = []
DAYS_TO_PREDICT=12
num_epochs = 60
seq_length = 12

daily_price,total_price=get_data("BTC-USD")

scaler = MinMaxScaler()
scaler = scaler.fit(np.expand_dims(daily_price, axis=1))
all_data = scaler.transform(np.expand_dims(daily_price, axis=1))
X_all, y_all = create_sequences(all_data, seq_length)

X_all = torch.from_numpy(X_all).float()
y_all = torch.from_numpy(y_all).float()

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