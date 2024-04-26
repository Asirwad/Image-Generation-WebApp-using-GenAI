import json

import streamlit_antd_components as sac
import streamlit as st
from streamlit_lottie import st_lottie

from core.generator import generate_image_locally, generate_image_cloud
from utils.gpu_info_fetcher import get_gpu_info

with st.sidebar:
    selected_tab = sac.menu([
        sac.MenuItem('Home', icon='house-fill'),
        sac.MenuItem('GenAI', icon='box-fill', children=[
            sac.MenuItem('image generation', icon='image'),
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
            sac.MenuItem('github', icon='github', href='https://ant.design/components/menu#menu'),
            sac.MenuItem('linkedin', icon='linkedin', href='https://icons.getbootstrap.com/'),
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

    st.write("Welcome to our Steganography and Super Resolution project! This project combines the power of steganography techniques and super-resolution using deep learning models. Our goal is to hide a secret image within a cover image using advanced convolutional neural networks (CNNs) and then enhance the quality of the hidden image using an Enhanced Super Resolution Generative Adversarial Network (ESRGAN). We also provide an option to encrypt the steg image using various chaos encryption algorithms for added security. Also adding GenAI features like text to image generation.")

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



