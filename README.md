<h1 align="center">
  InvisiCipher : Deep Learning-Based image Steganography and more
</h1>

<p align="center">
  <img src="app/assets/logo.png" alt="Project Logo" width="100">
</p>

<p align="center">
  <strong>Hide secrets, enhance images!</strong>
</p>

## Overview

Welcome to our Steganography and Super Resolution project! This project combines the power of steganography techniques and super-resolution using deep learning models. Our goal is to hide a secret image within a cover image using advanced convolutional neural networks (CNNs) and then enhance the quality of the hidden image using an Enhanced Super Resolution Generative Adversarial Network (ESRGAN). We also provide an option to encrypt the steg image using various chaos encryption algorithms for added security.

## Features

✨ **Interactive Hiding**: Utilize our intuitive hide network powered by CNNs to embed secret images within cover images effortlessly.

🔒 **Secure Encryption**: Choose from multiple chaos encryption algorithms such as AES, Blowfish to encrypt your steg image and protect your secrets.

🌟 **Enhanced Super Resolution**: Witness the magic of our ESRGAN model as it enhances the resolution and quality of the hidden image, revealing every detail.

🎨 **Easy-to-Use**: Our project provides a user-friendly interface and simple scripts to perform hiding, encryption, decryption, and image enhancement with just a few lines of code.

🪄 **Text-to-image**: Fast image generation from text prompts using transformers and diffusers .

## Project Architecture

The project architecture consists of the following components:

1. **Prepare Network**: A CNN-based network that prepares the secret image for hiding by extracting essential features and encoding it.

2. **Hide Network**: Another CNN-based network that embeds the prepared secret image within the cover image, producing the steg image.

3. **Chaos Encryption**: Choose between AES encryption, Blowfish encryption to secure your steg image.

4. **Chaos Decryption**: Decrypt the encrypted steg image using the corresponding decryption algorithm to retrieve the steg image.

5. **Reveal Network**: A CNN-based network that extracts the secret image from the steg image by decoding the hidden information.

6. **ESRGAN**: Our Enhanced Super Resolution Generative Adversarial Network (ESRGAN) model enhances the quality and resolution of the extracted secret image.

7. **Stable Diffusion pipeline** : Fast image generation from text prompts using transformers and diffusers .

## Getting Started

To get started with our project, follow these steps:

1. **Clone the Repository**: `git clone https://github.com/Asirwad/Image-Generation-WebApp-using-GenAI.git`

2. **Install Dependencies**: Install the required dependencies by running `pip install -r requirements.txt`.

3. **Run**: Run the streamlit app using `cd app` , `streamlit run app.py`

## Welcome screen

<p align="center">
  <img src="https://github.com/Asirwad/Image-Generation-WebApp-using-GenAI/assets/85600836/1ff82cfe-d50a-428d-a2a5-839ce7c3de2b" alt="Welcome" width="1000">
</p>

## Image hide

<p align="center">
  <img src="https://github.com/Asirwad/Image-Generation-WebApp-using-GenAI/assets/85600836/a4d09263-264b-42c1-a964-f36565706932" alt="Image hide" width="1000">
</p>

## Image reveal

<p align="center">
  <img src="https://github.com/Asirwad/Image-Generation-WebApp-using-GenAI/assets/85600836/044b5c19-a540-488c-a64e-dc13aa81879a" alt="Image reveal" width="1000">
</p>

## Super resolution

<p align="center">
  <img src="https://github.com/Asirwad/Image-Generation-WebApp-using-GenAI/assets/85600836/cf356a2e-2461-46f8-bc02-b61d56806cee" alt="Super resolution" width="1000">
</p>

## image generation

<p align="center">
  <img src="https://github.com/Asirwad/Image-Generation-WebApp-using-GenAI/assets/85600836/01368d58-75bb-4893-89d7-4fcacedf2d92" alt="Super resolution" width="1000">
</p>

## Contributing

We welcome contributions from the open source community. If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## Acknowledgements

We would like to acknowledge the following resources and libraries used in this project:

- <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Tensorflow_logo.svg/1915px-Tensorflow_logo.svg.png" alt="TensorFlow" width="26" align="center"> TensorFlow: [↗️](https://www.tensorflow.org/)
- <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/PyTorch_logo_icon.svg/1200px-PyTorch_logo_icon.svg.png"
 alt="PyTorch" width="25" align="center"> PyTorch: [↗️](https://pytorch.org/)
- <img src="https://github.com/Asirwad/Image-Generation-WebApp-using-GenAI/assets/85600836/ffa4e4e4-4f16-46c0-939e-bf28ba04de84"
 alt="Streamlit" width="50" align="center"> Streamlit: [↗️](https://streamlit.io/)

## Contact

For any questions or inquiries, please contact us at [asirwadsali@gmail.com](mailto:asirwadsali@gmail.com).
