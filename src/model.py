# src/model.py

from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, TimeDistributed
from tensorflow.keras.models import Model

def build_seq2seq(vocab_size: int, max_len: int, embed_dim=64, units=128):
    enc_input = Input(shape=(max_len,))
    enc_emb = Embedding(vocab_size, embed_dim, mask_zero=True)(enc_input)
    _, h, c = LSTM(units, return_state=True)(enc_emb)

    dec_input = Input(shape=(max_len-1,))
    dec_emb = Embedding(vocab_size, embed_dim, mask_zero=True)(dec_input)
    dec_out, _, _ = LSTM(units, return_sequences=True, return_state=True)(dec_emb, initial_state=[h,c])
    dec_out = TimeDistributed(Dense(vocab_size, activation="softmax"))(dec_out)

    model = Model([enc_input, dec_input], dec_out)
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model