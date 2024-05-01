import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import imageio


def normalize_batch(images):
    return (images - np.array([0.485, 0.456, 0.406])) / np.array([0.229, 0.224, 0.225])


def denormalize_batch(images, should_clip=True):
    images = (images * np.array([0.229, 0.224, 0.225])) + np.array([0.485, 0.456, 0.406])

    if should_clip:
        images = np.clip(images, 0, 1)
    return images


def hide_image(cover_image_in, secret_image_in):
    model = load_model("C:/Users/asirw/PycharmProjects/InvisiCipher/app/models/DEEP_STEGO/models/hide.h5")

    print("secret image size : ", secret_image_in.size)
    print("cover image size : ", cover_image_in.size)

    # Resize if image to 224px*224px
    if secret_image_in.size != (224, 224):
        secret_image_in = secret_image_in.resize((224, 224))
        print("secret_image was resized to 224px * 224px")
    if cover_image_in.size != (224, 224):
        cover_image_in = cover_image_in.resize((224, 224))
        print("cover_image was resized to 224px * 224px")

    secret_image_in = np.array(secret_image_in).reshape(1, 224, 224, 3) / 255.0
    cover_image_in = np.array(cover_image_in).reshape(1, 224, 224, 3) / 255.0

    steg_image_out = model.predict([normalize_batch(secret_image_in), normalize_batch(cover_image_in)])

    steg_image_out = denormalize_batch(steg_image_out)
    steg_image_out = np.squeeze(steg_image_out) * 255.0
    steg_image_out = np.uint8(steg_image_out)

    # imageio.imsave('C:/Users/asirw/PycharmProjects/InvisiCipher/app/steg_image.png', steg_image_out)
    # print("Saved steg image to steg_image.png")

    return steg_image_out


def reveal_image(stego_image_filepath):
    model = load_model("C:/Users/asirw/PycharmProjects/InvisiCipher/app/models/DEEP_STEGO/models/reveal.h5", compile=False)

    stego_image = Image.open(stego_image_filepath).convert('RGB')

    # Resize the image to 224px*224px
    if stego_image.size != (224, 224):
        stego_image = stego_image.resize((224, 224))
        print("stego_image was resized to 224px * 224px")

    stego_image = np.array(stego_image).reshape(1, 224, 224, 3) / 255.0

    secret_image_out = model.predict([normalize_batch(stego_image)])

    secret_image_out = denormalize_batch(secret_image_out)
    secret_image_out = np.squeeze(secret_image_out) * 255.0
    secret_image_out = np.uint8(secret_image_out)

    imageio.imsave("C:/Users/asirw/PycharmProjects/InvisiCipher/app/secret_out.png", secret_image_out)
    print("Saved revealed image to secret_out.png")

    return


