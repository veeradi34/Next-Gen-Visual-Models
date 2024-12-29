# -*- coding: utf-8 -*-
"""Autoencodersassignment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Y7GLEUB1qUIjQivKp9Vbqe2ci9SyJWQa
"""

import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import matplotlib.pyplot as plt

def load_data():
    (x_train, _), (x_test, _) = tf.keras.datasets.mnist.load_data()
    x_train = x_train.astype('float32') / 255.
    x_test = x_test.astype('float32') / 255.
    x_train = x_train.reshape((len(x_train), 28, 28, 1))
    x_test = x_test.reshape((len(x_test), 28, 28, 1))
    return x_train, x_test

class Sampling(layers.Layer):
    def call(self, inputs):
        z_mean, z_log_var = inputs
        batch = tf.shape(z_mean)[0]
        dim = tf.shape(z_mean)[1]
        epsilon = tf.random.normal(shape=(batch, dim))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon

def create_vanilla_vae(latent_dim=2):
    encoder_inputs = layers.Input(shape=(28, 28, 1))
    x = layers.Flatten()(encoder_inputs)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dense(256, activation='relu')(x)
    z_mean = layers.Dense(latent_dim)(x)
    z_log_var = layers.Dense(latent_dim)(x)
    z = Sampling()([z_mean, z_log_var])
    encoder = models.Model(encoder_inputs, [z_mean, z_log_var, z])

    decoder_inputs = layers.Input(shape=(latent_dim,))
    x = layers.Dense(256, activation='relu')(decoder_inputs)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dense(784, activation='sigmoid')(x)
    decoder_outputs = layers.Reshape((28, 28, 1))(x)
    decoder = models.Model(decoder_inputs, decoder_outputs)

    return encoder, decoder

def create_vae_encoder_ed(latent_dim=2):
    encoder_inputs = layers.Input(shape=(28, 28, 1))
    x = layers.Flatten()(encoder_inputs)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dense(512, activation='relu')(x)
    z_mean = layers.Dense(latent_dim)(x)
    z_log_var = layers.Dense(latent_dim)(x)
    z = Sampling()([z_mean, z_log_var])
    encoder = models.Model(encoder_inputs, [z_mean, z_log_var, z])

    decoder_inputs = layers.Input(shape=(latent_dim,))
    x = layers.Dense(256, activation='relu')(decoder_inputs)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dense(784, activation='sigmoid')(x)
    decoder_outputs = layers.Reshape((28, 28, 1))(x)
    decoder = models.Model(decoder_inputs, decoder_outputs)

    return encoder, decoder

def create_vae_decoder_ed(latent_dim=2):
    encoder_inputs = layers.Input(shape=(28, 28, 1))
    x = layers.Flatten()(encoder_inputs)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dense(256, activation='relu')(x)
    z_mean = layers.Dense(latent_dim)(x)
    z_log_var = layers.Dense(latent_dim)(x)
    z = Sampling()([z_mean, z_log_var])
    encoder = models.Model(encoder_inputs, [z_mean, z_log_var, z])

    decoder_inputs = layers.Input(shape=(latent_dim,))
    x = layers.Dense(128, activation='relu')(decoder_inputs)
    x = layers.Dense(64, activation='relu')(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dense(784, activation='sigmoid')(x)
    decoder_outputs = layers.Reshape((28, 28, 1))(x)
    decoder = models.Model(decoder_inputs, decoder_outputs)

    return encoder, decoder

def create_vae_both_ed(latent_dim=2):
    encoder_inputs = layers.Input(shape=(28, 28, 1))
    x = layers.Flatten()(encoder_inputs)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dense(512, activation='relu')(x)
    z_mean = layers.Dense(latent_dim)(x)
    z_log_var = layers.Dense(latent_dim)(x)
    z = Sampling()([z_mean, z_log_var])
    encoder = models.Model(encoder_inputs, [z_mean, z_log_var, z])

    decoder_inputs = layers.Input(shape=(latent_dim,))
    x = layers.Dense(128, activation='relu')(decoder_inputs)
    x = layers.Dense(64, activation='relu')(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dense(784, activation='sigmoid')(x)
    decoder_outputs = layers.Reshape((28, 28, 1))(x)
    decoder = models.Model(decoder_inputs, decoder_outputs)

    return encoder, decoder

class VAE(tf.keras.Model):
    def __init__(self, encoder, decoder, **kwargs):
        super(VAE, self).__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder

    def train_step(self, data):
        with tf.GradientTape() as tape:
            z_mean, z_log_var, z = self.encoder(data)
            reconstruction = self.decoder(z)
            reconstruction_loss = tf.reduce_mean(
                tf.reduce_sum(
                    tf.keras.losses.binary_crossentropy(data, reconstruction),
                    axis=(1, 2, 3)
                )
            )
            kl_loss = -0.5 * tf.reduce_mean(
                tf.reduce_sum(
                    1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var),
                    axis=1
                )
            )
            total_loss = reconstruction_loss + kl_loss

        grads = tape.gradient(total_loss, self.trainable_weights)
        self.optimizer.apply_gradients(zip(grads, self.trainable_weights))

        return {
            "loss": total_loss,
            "reconstruction_loss": reconstruction_loss,
            "kl_loss": kl_loss,
        }

def train_vae(vae, x_train, epochs=10, batch_size=128):
    vae.compile(optimizer=tf.keras.optimizers.Adam())
    history = vae.fit(x_train, x_train,
                     epochs=epochs,
                     batch_size=batch_size)
    return history

def plot_results(models, x_test, n=10):
    plt.figure(figsize=(20, 4*len(models)))
    for idx, (name, vae) in enumerate(models.items()):
        ax = plt.subplot(len(models), 2, 2*idx + 1)
        for i in range(n):
            ax.imshow(x_test[i].reshape(28, 28), cmap='gray')
        ax.set_title(f'Original - {name}')

        ax = plt.subplot(len(models), 2, 2*idx + 2)
        z_mean, _, _ = vae.encoder.predict(x_test[:n])
        reconstructed = vae.decoder.predict(z_mean)
        for i in range(n):
            ax.imshow(reconstructed[i].reshape(28, 28), cmap='gray')
        ax.set_title(f'Reconstructed - {name}')
    plt.show()

def main():
    x_train, x_test = load_data()

    vae_architectures = {
        'Vanilla VAE': create_vanilla_vae(),
        'Encoder-ED VAE': create_vae_encoder_ed(),
        'Decoder-ED VAE': create_vae_decoder_ed(),
        'Both-ED VAE': create_vae_both_ed()
    }

    trained_models = {}
    histories = {}

    for name, (encoder, decoder) in vae_architectures.items():
        print(f"\nTraining {name}...")
        vae = VAE(encoder, decoder)
        history = train_vae(vae, x_train, epochs=10)
        trained_models[name] = vae
        histories[name] = history.history

    plt.figure(figsize=(12, 6))
    for name, history in histories.items():
        plt.plot(history['loss'], label=f'{name} - Loss')
    plt.title('Training Loss Comparison')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    plot_results(trained_models, x_test)

if __name__ == "__main__":
    main()
