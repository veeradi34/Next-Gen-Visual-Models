We know that a VAE normally consists of an encoder-decoder architecture. The encoder is the part of the model with layers with consecutively lesser no. of neurons (for eg. [200, 100, 50, ..]) and the decoder has layers with increasing number of neurons. The encoder is said to downsample i.e. reduce the dimensionality of the input, turning it into a somewhat condensed form; and the decoder is said to upsample (expand the dimensions)

<div align="center">
  <img src="https://raw.githubusercontent.com/shoryasethia/Next-Gen-Visual-Models/main/Week3/Assignment/vae-architecture.webp" alt="VAE Architecture">
</div>

### A. Knowing this, write a VAE:

1. much like the one in the tutorial with an encoder(left) and decoder(right) - basic vanilla VAE implementation
2. where the encoder (left) is replaced with an encoder-decoder architecture (both downsampling-upsampling)
3. where the decoder (right) is replaced with an encoder-decoder architecture (both downsampling-upsampling)
4. where both sides - encoder and decoder - are replaced with encoder-decoder architecture

### B. Compare results of accuracy and output images across all 3 parts of A and comment on which architecture is the best

Some examples of encoder-decoder architectures are included for reference:

An encoder-decoder architecture is one where a decoder is attached right after the encoder

It would have layers with decreasing size, reach a minimum , followed by layers of increasing size.

While coding, these layers can be dense, convolutional or any other layers you feel would be right

<div align="center">
  <img src="https://raw.githubusercontent.com/shoryasethia/Next-Gen-Visual-Models/main/Week3/Assignment/segnet.webp" alt="segnet-architecture">
</div>
<div align="center">
  <img src="https://raw.githubusercontent.com/shoryasethia/Next-Gen-Visual-Models/main/Week3/Assignment/encoder-decoder.webp" alt="encoder-decoder-architecture">
</div>

