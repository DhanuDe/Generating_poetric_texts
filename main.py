import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Activation
from tensorflow.keras.optimizers import RMSprop


filepath = 'shakespeare.txt'
with open(filepath, "rb") as file:
    shakespeare_text = file.read()

shakespeare_text = shakespeare_text.decode(encoding="utf-8").lower()
print(shakespeare_text[0:9])





