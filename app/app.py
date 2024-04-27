import datetime
import json
import time

from PIL import Image
import streamlit_antd_components as sac
import streamlit as st
from streamlit_lottie import st_lottie
import os
import tempfile
from core_func.text2image.generator import generate_image_locally, generate_image_cloud
from core_func.upscale import upscale_image
from utils.gpu_info_fetcher import get_gpu_info


with st.sidebar:
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
            sac.MenuItem('github', icon='github', href='https://github.com/Asirwad/InvisiCipher'),
        ]),
    ], open_all=False, color='green', size='lg', variant='light')

if selected_tab == 'Home':
    header_col1, header_col2 = st.columns([2.73, 2])
    with header_col1:
        st.title(":green[InvisiCipher] : Deep Learning-Based image Steganography and more")
    with header_col2:
        file = "assets/animation2.json"
        with open(file, 'r') as f:
            data = json.load(f)
        st_lottie(data, width=300)
    sac.menu([sac.MenuItem(type='divider')])

    logo_col, desc_col = st.columns([1, 3])
    with logo_col:
        st.image('assets/logo.png', use_column_width=True)
    with desc_col:
        st.write("This project combines the power of steganography techniques and super-resolution using deep learning models. Our goal is to hide a secret image within a cover image using advanced convolutional neural networks (CNNs) and then enhance the quality of the hidden image using an Enhanced Super Resolution Generative Adversarial Network (ESRGAN). We also provide an option to encrypt the steg image using various chaos encryption algorithms for added security. Also adding GenAI features like text to image generation.")

elif selected_tab == 'image generation':
    st.title("Image Generation using stable Diffusion🪄")

    # Create text input for entering prompt
    prompt = st.text_input("Enter prompt:")

    # select-box for computing platform
    computing_choice = st.selectbox(
        'Which computing platform do you want to use?',
        ('Cloud', 'Local Machine'))

    if computing_choice == 'Local Machine':
        sac.alert(label='GPU Info',
                  description=get_gpu_info(),
                  banner=False,
                  icon=True,
                  closable=True,
                  size='sm',
                  variant='outline',
                  color='gray')
        steps = 10
        if st.toggle('Custom steps'):
            steps = st.number_input(label="Steps",
                                    label_visibility='collapsed',
                                    step=1,
                                    value=10,
                                    min_value=10,
                                    max_value=30)

    # Create generate button
    generate_button = st.button(":green[Generate]")
    if generate_button:
        # Generate image based on prompt
        if prompt:
            image_placeholder = st.empty()
            with image_placeholder:
                with open("assets/animation.json", 'r') as f:
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
        else:
            st.warning("Enter a prompt to generate", icon='⚠️')

    # Create download button
    if 'generated_image' in locals():
        if st.download_button("Download", 'generated_image', file_name=f"{prompt}.png"):
            st.success("Downloaded successfully!")

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
                st.image(low_res_image, width=256, caption=f"Low resolution image\nSize: {uploaded_file.size/1024}kb")
        with col2:
            with high_res_image_placeholder:
                with open("assets/AnimationForSuperRes.json", 'r') as f:
                    data = json.load(f)
                st_lottie(data, width=256)

        if st.button("Upscale", type='primary'):
            progress_placeholder = st.empty()
            progress_placeholder = st.progress(0)
            with col2:
                with high_res_image_placeholder:
                    with open("assets/AnimationProcessing.json", 'r') as f:
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
                    progress_placeholder.progress(i*2)
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
                if st.download_button("Download", 'high_res_image', file_name=f"{uploaded_file.name}"):
                    st.success("Downloaded successfully!")
            else:
                st.error("Upscaling failed. Please check the uploaded image.")

    else:
        st.info("Upload a low-resolution image to see the Super Resolution magic!")
        sac.menu([sac.MenuItem(type='divider')])
        st.write("The Super-Resolution Generative Adversarial Network (SRGAN) is a seminal work that is capable of generating realistic textures during single image super-resolution")
        st.write("ESRGAN achieves consistently better visual quality with more realistic and natural textures than SRGAN")


