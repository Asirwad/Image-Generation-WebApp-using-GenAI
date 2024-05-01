import datetime
import io
import json
import time

from PIL import Image
import streamlit_antd_components as sac
import streamlit as st
from streamlit_lottie import st_lottie
import os
from core_func.text2image.generator import generate_image_locally, generate_image_cloud
from core_func import aes, blowfish
from core_func.upscale import upscale_image
from core_func import stego_cnn
from utils.gpu_info_fetcher import get_gpu_info

st.set_page_config(page_title="Invisicipher",
                   page_icon="assets/icon.ico",
                   )

with st.sidebar:
    logo_and_name_placeholder = st.empty()
    with logo_and_name_placeholder:
        st.image("assets/InvisiCipherLogoAndName.gif", clamp=True)
    selected_tab = sac.menu([
        sac.MenuItem('Home', icon='house-fill'),
        sac.MenuItem('GenAI', icon='box-fill', children=[
            sac.MenuItem('image generation', icon='image'),
            sac.MenuItem('super resolution', icon='feather')
        ]),
        sac.MenuItem('Security', icon='safe', children=[
            sac.MenuItem('encryption', icon='lock'),
            sac.MenuItem('decryption', icon='unlock')
        ]),
        sac.MenuItem('Steganography', icon='search', children=[
            sac.MenuItem('image hide', icon='stickies-fill'),
            sac.MenuItem('image reveal', icon='textarea-resize')
        ]),

        sac.MenuItem(type='divider'),
        sac.MenuItem('Connect', type='group', children=[
            sac.MenuItem('desktopApp repo', icon='github', href='https://github.com/Asirwad/InvisiCipher'),
            sac.MenuItem('webApp repo', icon='github',
                         href='https://github.com/Asirwad/Image-Generation-WebApp-using-GenAI'),
        ]),
    ], open_all=False, color='green', size='md', variant='light')

if selected_tab == 'Home':
    header_col1, logo_col = st.columns([3, 1])
    with header_col1:
        st.title(":green[InvisiCipher] : Deep Learning-Based image Steganography and more")
    with logo_col:
        st.image('assets/logo.png', use_column_width=True)
    sac.menu([sac.MenuItem(type='divider')])

    illustration_col, desc_col = st.columns([1, 2])
    with illustration_col:
        with open("assets/lottie/Animation2.json", 'r') as f:
            data = json.load(f)
        st_lottie(data, width=235)
    with desc_col:
        st.write(
            "This project combines the power of steganography techniques and super-resolution using deep learning models. Our goal is to hide a secret image within a cover image using advanced convolutional neural networks (CNNs) and then enhance the quality of the hidden image using an Enhanced Super Resolution Generative Adversarial Network (ESRGAN). We also provide an option to encrypt the steg image using various chaos encryption algorithms for added security. Also adding GenAI features like text to image generation.")

elif selected_tab == 'image generation':
    st.title("Image Generation using :green[stable Diffusion]🪄")
    sac.menu([sac.MenuItem(type='divider')])

    prompt = st.text_input("Enter a prompt", placeholder="eg: A field of pumpkins ready for harvest")

    computing_choice = st.selectbox(
        'Which computing platform do you want to use?',
        ('Cloud', 'Local Machine'))

    if computing_choice == 'Local Machine':
        sac.alert(label='GPU Info',
                  description=get_gpu_info(),
                  banner=False,
                  icon=True,
                  closable=False,
                  size='sm',
                  variant='outline',
                  color='green')
        steps = 10
        if st.toggle('Custom steps'):
            steps = st.number_input(label="Steps",
                                    label_visibility='collapsed',
                                    step=1,
                                    value=10,
                                    min_value=10,
                                    max_value=30)

    # Create generate button
    generate_button = st.button("Generate", use_container_width=True, type='primary')
    if generate_button:
        # Generate image based on prompt
        if prompt:
            image_placeholder = st.empty()
            with image_placeholder:
                with open("assets/lottie/animation.json", 'r') as f:
                    data = json.load(f)
                loading_animation = st_lottie(data, width=300)
            with st.spinner('Generating..'):
                if computing_choice == 'Local Machine':
                    generated_image = generate_image_locally(prompt=prompt, steps=steps)
                else:
                    generated_image = generate_image_cloud(prompt=prompt)

            # Display generated image
            image_placeholder.empty()
            st.image(generated_image, width=256)

            if 'generated_image' in locals():
                buffer = io.BytesIO()
                generated_image.save(buffer, format="JPEG")
                image_bytes = buffer.getvalue()
                if st.download_button("Download", image_bytes, file_name=f"{prompt.replace(' ', '_')}.jpg"):
                    st.success("Downloaded successfully!")
        else:
            st.warning("Enter a prompt to generate", icon='⚠️')

elif selected_tab == 'super resolution':
    st.title("Image super-resolution using :green[Enhanced Super-resolution GAN🪶]")

    uploaded_file = st.file_uploader("Upload a low resolution Image", type=['jpg', 'png'])
    if uploaded_file is not None:
        sac.menu([sac.MenuItem(type='divider')])
        low_res_image = Image.open(uploaded_file)
        col1, col2 = st.columns([1, 1])
        with col1:
            low_res_image_placeholder = st.empty()
        with col2:
            high_res_image_placeholder = st.empty()
        with col1:
            with low_res_image_placeholder:
                st.image(low_res_image, width=256, caption=f"Low resolution image\nSize: {uploaded_file.size / 1024}kb")
        with col2:
            with high_res_image_placeholder:
                with open("assets/lottie/AnimationForSuperRes.json", 'r') as f:
                    data = json.load(f)
                st_lottie(data, width=256)

        if st.button("Upscale", type='primary', use_container_width=True):
            progress_placeholder = st.empty()
            progress_placeholder = st.progress(0)
            with col2:
                with high_res_image_placeholder:
                    with open("assets/lottie/AnimationProcessing.json", 'r') as f:
                        data = json.load(f)
                    st_lottie(data, width=256)
            # Save the uploaded file temporarily
            original_filename = uploaded_file.name
            temp_folder = 'temps'
            if not os.path.exists(temp_folder):
                os.mkdir(temp_folder)
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            image_filepath = os.path.join(temp_folder, f"{timestamp}_{original_filename}")
            image = Image.open(uploaded_file)
            image.save(image_filepath)

            with st.spinner("In progress.."):
                for i in range(1, 25):
                    progress_placeholder.progress(i * 2)
                    time.sleep(0.1)
                high_res_image_filepath = upscale_image(image_filepath)
                progress_placeholder.progress(100)

            # Check if upscale_image returned a valid path
            if high_res_image_filepath:
                high_res_image = Image.open(high_res_image_filepath)
                with col2:
                    high_res_image_placeholder.empty()
                    st.image(high_res_image, width=256, caption=f"high resolution image")
                    progress_placeholder.empty()
                # Optionally, delete the temporary file after successful processing
                os.remove(image_filepath)
                buffer = io.BytesIO()
                high_res_image.save(buffer, "PNG")
                high_res_image_bytes = buffer.getvalue()
                if st.download_button("Download", high_res_image_bytes, file_name=f"{uploaded_file.name}"):
                    st.success("Downloaded successfully!")
            else:
                st.error("Upscaling failed. Please check the uploaded image.")

    else:
        st.info("Upload a low-resolution image to see the Super Resolution magic!")
        sac.menu([sac.MenuItem(type='divider')])
        st.write(
            "The Super-Resolution Generative Adversarial Network (SRGAN) is a seminal work that is capable of generating realistic textures during single image super-resolution")
        st.write(
            "ESRGAN achieves consistently better visual quality with more realistic and natural textures than SRGAN")

elif selected_tab == 'encryption':
    st.title("Image encryption using :green[AES] and :green[Blowfish]🔐")
    sac.menu([sac.MenuItem(type='divider')])

    selected_algorithm = st.selectbox("Select the encryption algorithm", options=(None, 'AES', 'Blowfish'))
    enc_key = st.text_input(label="Enter the encryption key", placeholder="key here..", type="password", value='')
    uploaded_file = st.file_uploader("Upload image to be encrypted", type=['jpg', 'png'])

    image_placeholder = st.empty()
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        with image_placeholder:
            st.image(image, caption="Image to be encrypted", width=256)

        # Save the uploaded file temporarily
        original_filename = uploaded_file.name
        temp_folder = 'temps'
        if not os.path.exists(temp_folder):
            os.mkdir(temp_folder)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        image_filepath = os.path.join(temp_folder, f"{timestamp}_{original_filename}")
        image = Image.open(uploaded_file)
        image.save(image_filepath)

        enc_filepath = ""
        if st.button("Encrypt", type='primary', use_container_width=True):
            with st.spinner("Working on it..."):
                progress_placeholder = st.empty()
                if enc_key != '':
                    if selected_algorithm == 'AES':
                        with image_placeholder:
                            with open("assets/lottie/AnimationProcessing.json", 'r') as f:
                                data = json.load(f)
                            st_lottie(data, width=256)
                        progress_placeholder = st.progress(0)
                        for i in range(1, 50):
                            progress_placeholder.progress(i * 2)
                            time.sleep(0.1)
                        enc_filepath = aes.encrypt(image_filepath, key=enc_key)
                        progress_placeholder.progress(100)
                        progress_placeholder.empty()
                    elif selected_algorithm == 'Blowfish':
                        with image_placeholder:
                            with open("assets/lottie/AnimationProcessing.json", 'r') as f:
                                data = json.load(f)
                            st_lottie(data, width=256)
                        progress_placeholder = st.progress(0)
                        for i in range(1, 50):
                            progress_placeholder.progress(i * 2)
                            time.sleep(0.1)
                        enc_filepath = blowfish.encrypt(image_filepath, key=enc_key)
                        progress_placeholder.progress(100)
                        progress_placeholder.empty()
                    else:
                        st.warning("Select an algorithm to continue")
                else:
                    st.warning("Enter a valid key")

        if enc_filepath != "":
            image_placeholder.empty()
            st.success("Encryption successful")
            os.remove(image_filepath)
            image = None
            with open(enc_filepath, 'rb') as f:
                if st.download_button("Download", f, file_name=uploaded_file.name + '.enc'):
                    st.success("Downloaded!")
            os.remove(enc_filepath)
elif selected_tab == 'decryption':
    st.title("Image decryption using :green[AES] and :green[Blowfish]🔓")
    sac.menu([sac.MenuItem(type='divider')])

    selected_algorithm = st.selectbox("Select the decryption  algorithm", options=[None, 'AES', 'Blowfish'])
    dec_key = st.text_input(label="Enter the decryption key", placeholder="key here..", type="password", value='')
    uploaded_file = st.file_uploader("Upload image to be encrypted", type=['enc'])

    image_placeholder = st.empty()
    button_placeholder = st.empty()
    with button_placeholder:
        if st.button("Decrypt", use_container_width=True, type='primary'):
            if selected_algorithm is None or dec_key == '' or uploaded_file is None:
                st.warning("All fields are required", icon='ℹ️')
            else:
                # Save the uploaded file temporarily
                original_filename = uploaded_file.name
                temp_folder = 'temps'
                if not os.path.exists(temp_folder):
                    os.mkdir(temp_folder)
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                enc_file_filepath = os.path.join(temp_folder, f"{timestamp}_{original_filename}")
                buffer = uploaded_file.getvalue()
                with open(enc_file_filepath, 'wb') as f:
                    f.write(buffer)
                button_placeholder.empty()
                with image_placeholder:
                    with open("assets/lottie/AnimationProcessing.json", 'r') as f:
                        data = json.load(f)
                    st_lottie(data, width=256)
                progress_placeholder = st.progress(0)
                for i in range(1, 50):
                    progress_placeholder.progress(i * 2)
                    time.sleep(0.1)
                image_placeholder.empty()
                progress_placeholder.empty()
                result, decrypted_image_filepath = aes.decrypt(enc_file_filepath, dec_key) if selected_algorithm == 'AES' else blowfish.decrypt(enc_file_filepath, dec_key)
                if result == -1:
                    st.error('Wrong key or algorithm', icon='❌')
                else:
                    with image_placeholder:
                        st.image(decrypted_image_filepath)
                    button_placeholder.empty()
                    dec_image = Image.open(decrypted_image_filepath)
                    buffer = io.BytesIO()
                    dec_image.save(buffer, "PNG")
                    dec_image_bytes = buffer.getvalue()
                    with button_placeholder:
                        st.download_button('Download',
                                           type='primary',
                                           use_container_width=True,
                                           file_name=original_filename + '.png',
                                           data=dec_image_bytes)

elif selected_tab == 'image hide':
    st.title("Image steganography hide using :green[STEGO CNN]🔍")
    sac.menu([sac.MenuItem(type='divider')])

    cover_fileupload_col, secret_fileupload_col = st.columns([2, 2])
    with cover_fileupload_col:
        uploaded_cover_file = st.file_uploader("Upload cover image", type=['png'])
    with secret_fileupload_col:
        uploaded_secret_file = st.file_uploader("Upload secret image", type=['png'])

    cover_col, secret_col, steg_col = st.columns([1, 1, 1])
    with cover_col:
        cover_placeholder = st.empty()
    with secret_col:
        secret_placeholder = st.empty()
    with steg_col:
        steg_placeholder = st.empty()
    with cover_col:
        with cover_placeholder:
            with open("assets/lottie/AnimationForStegoImageUpload.json", 'r') as f:
                st_lottie(json.load(f), width=256)
    with secret_col:
        with secret_placeholder:
            with open("assets/lottie/AnimationForStegoImageUpload.json", 'r') as f:
                st_lottie(json.load(f), width=256)
    with steg_col:
        with steg_placeholder:
            with open("assets/lottie/AnimationForStegnoHideProcessing.json", 'r') as f:
                st_lottie(json.load(f), width=256)

    if uploaded_cover_file is not None:
        with cover_placeholder:
            with cover_col:
                cover_placeholder.empty()
                st.image(Image.open(uploaded_cover_file), caption="Cover image")

    if uploaded_secret_file is not None:
        with secret_placeholder:
            with secret_col:
                secret_placeholder.empty()
                st.image(Image.open(uploaded_secret_file), caption='Secret image')

    sac.alert(label='GPU Info',
              description=get_gpu_info(),
              banner=False,
              icon=True,
              closable=False,
              size='xs',
              variant='outline',
              color='green',
              radius='lg')
    button_placeholder = st.empty()
    with button_placeholder:
        hide_button = st.button("Hide image", type='primary', use_container_width=True)
    if hide_button:
        if uploaded_secret_file is not None and uploaded_cover_file is not None:
            # TODO: solve the animation and steg image stacking issue
            # with steg_placeholder:
            #   with steg_col:
            #       steg_placeholder.empty()
            #       with open("assets/lottie/AnimationProcessing.json", 'r') as f:
            #           st_lottie(json.load(f), width=256)
            progress_placeholder = st.empty()
            progress_placeholder = st.progress(0)
            with st.spinner("Working on it.."):
                for i in range(1, 24):
                    progress_placeholder.progress(i * 2)
                    time.sleep(0.1)
                cover_image = Image.open(uploaded_cover_file).convert('RGB')
                secret_image = Image.open(uploaded_secret_file).convert('RGB')
                steg_image = stego_cnn.hide_image(cover_image, secret_image)
                steg_image = Image.fromarray(steg_image)
                print(type(steg_image))
                for i in range(25, 50):
                    progress_placeholder.progress(i * 2)
                    time.sleep(0.1)
            progress_placeholder.progress(100)
            progress_placeholder.empty()
            button_placeholder.empty()
            steg_placeholder.empty()
            steg_placeholder.image(steg_image, caption='steg image')

            buffer = io.BytesIO()
            steg_image.save(buffer, "PNG")
            steg_image_bytes = buffer.getvalue()
            with button_placeholder:
                if st.download_button(label='Download', data=steg_image_bytes, file_name='steg_image.png', type='primary', use_container_width=True):
                    st.info("Downloaded successfully!")

        else:
            st.warning("All fields are required", icon='⚠️')


