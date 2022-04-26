import numpy as np
import torch
import  streamlit as st
import time
from neuralnetwork.Predictor import CryptoPredictor

from  neuralnetwork.DataProcessing import  get_data, secData

preds = []

def train_model(
        model,
        num_epochs=None,
        seq_length=12,
        ticker="",
        DAYS_TO_PREDICT=1):
    total_price, daily_price = get_data(ticker)
    X_all, y_all, scaler=secData(daily_price,seq_length)

    loss_fn = torch.nn.MSELoss(reduction='mean')

    optimiser = torch.optim.Adam(model.parameters(), lr=1e-3)
    train_hist = np.zeros(num_epochs)
    test_hist = np.zeros(num_epochs)
    my_bar = st.progress(0)

    for t in range(num_epochs):

        model.reset_hidden_state()

        y_pred = model(X_all)

        loss = loss_fn(y_pred.float(), y_all)
        if daily_price is not None:
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
                my_bar.progress(t/(num_epochs-1))



        train_hist[t] = loss.item()

        optimiser.zero_grad()
        loss.backward()
        optimiser.step()
    my_bar.empty()
    return model.eval(), train_hist, test_hist, preds,total_price, daily_price,scaler
   