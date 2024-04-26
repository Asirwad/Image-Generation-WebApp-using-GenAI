import streamlit as st
from streamlit_option_menu import option_menu
from utils.gpu_info_fetcher import get_gpu_info
from generator import generate_image_cloud, generate_image_locally
import streamlit_antd_components as sac


st.title("Image Generation using stable Diffusion")

# Create text input for entering prompt
prompt = st.text_input("Enter prompt:")

# selectbox for computing platform
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
    if st.toggle('Custom steps'):
        steps = st.number_input(label="Steps",
                                label_visibility='collapsed',
                                step=1,
                                value=10,
                                min_value=10,
                                max_value=30)


# Create generate button
generate_button = st.button("Generate")
if generate_button:
    # Generate image based on prompt
    if prompt:
        with st.spinner('Generating..'):
            if computing_choice == 'Local Machine':
                generated_image = generate_image_locally(prompt=prompt, steps=steps)
            else:
                generated_image = generate_image_cloud(prompt=prompt)

        # Display generated image
        st.image(generated_image, caption='Generated Image', use_column_width=True)
    else:
        st.warning("Enter a prompt to generate", icon='⚠️')

# Create download button
if 'generated_image' in locals():
    if st.button("Download"):
        # Save the image
        save_path = "generated_image.png"  # Default save path
        generated_image.save(save_path)
        st.success(f"Image saved to: {save_path}")



