import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Activation
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.models import load_model


filepath = 'shakespeare.txt'
with open(filepath, "rb") as file:
    shakespeare_text = file.read()

shakespeare_text = shakespeare_text.decode(encoding="utf-8").lower()

characters = sorted(set(shakespeare_text))
char_to_index = dict((c, i) for i, c in enumerate(characters))
index_to_char = dict((i, c) for i, c in enumerate(characters))

SEQ_LENGTH = 40
STEP_SIZE = 5

sentences = []
next_characters = []

for i in range(0, len(shakespeare_text) - SEQ_LENGTH, STEP_SIZE):
    sentences.append(shakespeare_text[i:i + SEQ_LENGTH])
    next_characters.append(shakespeare_text[i + SEQ_LENGTH])

x = np.zeros((len(sentences), SEQ_LENGTH, len(characters)), dtype=np.bool_)
y= np.zeros((len(sentences),len(characters)),dtype=np.bool_)

for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t,char_to_index[char]] = 1
    y[i, char_to_index[next_characters[i]]] = 1


# model = Sequential()
# model.add(LSTM(120,input_shape=(SEQ_LENGTH,len(characters))))
# model.add(Dense(len(characters)))
# model.add(Activation('softmax'))
#
# model.compile(loss='categorical_crossentropy', optimizer=RMSprop(learning_rate=0.01), metrics=['accuracy'])
#
#
# model.fit(x, y, batch_size=256, epochs=5)
#
# model.save('shakespearemodel.h5')


model = load_model("shakespearemodel.h5")


def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1,preds,1)
    return np.argmax(probas)


def generate_text(length,temperature ):
    start_index = random.randint(0,len(sentences)-SEQ_LENGTH-1)
    generated = ''
    sentence  = shakespeare_text[start_index:start_index+SEQ_LENGTH]
    generated += sentence
    for i in range(length):
        x = np.zeros((1,SEQ_LENGTH,len(characters)))
        for t, char in enumerate(sentence):
            x[0, t, char_to_index[char]] = 1

        predictions = model.predict(x,verbose= 0)[0]
        next_index = sample(predictions,temperature)
        next_character = index_to_char[next_index]
        generated += next_character
        sentence = sentence[1:] + next_character
    return generated

print('------------temp 0.2 -----------')
print(generate_text(300, temperature=0.2))
print('------------temp 0.4 -----------')
print(generate_text(300, temperature=0.4))
print('------------temp 0.6 -----------')
print(generate_text(300, temperature=0.6))
print('------------temp 0.8 -----------')
print(generate_text(300, temperature=0.8))
print('------------temp 1.0 -----------')
print(generate_text(300, temperature=1.0))