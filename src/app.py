import streamlit as st
import numpy as np
from PIL import Image
from io import BytesIO

# App Title and Description
st.title(':yellow[5-Prong] Image Transformation')
st.write(
    "Upload an image and transform it with five powerful tools: vertical stretch, "
    "horizontal stretch, 90-degree rotation, vertical flip, and horizontal flip. "
    "Download your transformed image or add it to The Collection when you're done!"
)

st.divider()

col1, col2, col3, col4, col5 = st.columns(5) # Transformation Buttons

# Set inital session_state variables
if "caption_text" not in st.session_state:
    st.session_state.caption_text = ""

if "rotation_direction" not in st.session_state:
    st.session_state.rotation_direction = None

if "hstretch_factor" not in st.session_state:
    st.session_state.hstretch_factor = None

if "vstretch_factor" not in st.session_state:
    st.session_state.vstretch_factor = None

if "perform_rotation" not in st.session_state:
    st.session_state.perform_rotation = False

if "perform_hstretch" not in st.session_state:
    st.session_state.perform_hstretch = False

if "perform_vstretch" not in st.session_state:
    st.session_state.perform_vstretch = False

if "current_image" not in st.session_state:
    st.session_state.current_image = None

image_slot = st.empty()
caption_slot = st.empty()

save_col, download_col = st.columns(2) # Save and Download Buttons

section_divide_slot = st.empty()

uploaded_file = st.file_uploader(
    "Upload new image:",
    type=["jpg", "png", "jpeg"],
    )

st.divider()
st.subheader("The Collection")


# Transformation and Save/Download Buttons appear once file uploaded
if uploaded_file:
    with caption_slot:
        st.session_state.caption_text = st.text_input(
            'Give your image a caption (optional)'
            )
    # Only update session image on new image uploaded
    if "uploaded_file_id" not in st.session_state or st.session_state.uploaded_file_id != uploaded_file.file_id:
        with image_slot:
            st.image(uploaded_file, caption=st.session_state.caption_text)
            pil_image = Image.open(uploaded_file)
            st.session_state.current_image = np.array(pil_image)
            st.session_state.uploaded_file_id = uploaded_file.file_id
    with save_col:
        save_button = st.button('Save Image To The Collection', use_container_width=True)
    with download_col:
        if st.session_state.current_image is not None:
            img = Image.fromarray(st.session_state.current_image.astype('uint8'), 'RGB')
            buf = BytesIO()
            img.save(buf, format='PNG')
            byte_data = buf.getvalue()
            filename = "transformed_image.png" if st.session_state.caption_text == "" else st.session_state.caption_text + ".png"
            
            st.download_button(
                label='Download Image',
                data=byte_data,
                file_name=filename,
                mime="image/png",
                use_container_width=True
            )
    with section_divide_slot:
        st.divider()
    with col1:
        vstretch_button = st.button('Verticle Stretch', use_container_width=True)
    with col2:
        hstretch_button = st.button('Horizontal Stretch', use_container_width=True)
    with col3:
        rotate_button = st.button('Rotate', use_container_width=True)
    with col4:
        vflip_button = st.button('Flip Vertically', use_container_width=True)
    with col5:
        hflip_vbutton = st.button('Flip Horizontally', use_container_width=True)

    # Rerender image on screen with new image and caption
    def update_image():
        with image_slot:
            st.image(st.session_state.current_image, st.session_state.caption_text)

    # Dialog to recieve rotation direction from user input
    @st.dialog("Rotate Clockwise or Counterclockwise by 90 degrees?")
    def direction():
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clockwise"):
                st.session_state.rotation_direction = True
                st.session_state.perform_rotation = True
                st.rerun()
        
        with col2:
            if st.button("Counterclockwise"):
                st.session_state.rotation_direction = False
                st.session_state.perform_rotation = True
                st.rerun()

    # Dialog to recieve verticle stretch magnitude from user input
    @st.dialog("Vertical Stretch Factor")
    def get_vstretch_factor():
        factor = st.number_input("Enter stretch factor:", min_value=1, max_value=5, value=2)
        if st.button("Apply"):
            st.session_state.vstretch_factor = factor
            st.session_state.perform_vstretch = True
            st.rerun()
    
    # Dialog to recieve horizontal stretch magnitude from user input
    @st.dialog("Horizontal Stretch Factor")
    def get_hstretch_factor():
        factor = st.number_input("Enter stretch factor:", min_value=1, max_value=5, value=2)
        if st.button("Apply"):
            st.session_state.hstretch_factor = factor
            st.session_state.perform_hstretch = True
            st.rerun()

    # Image transormation functions
    def stretch_vertically(image, factor=2):
        # Check if resulting image would be too large
        new_height = image.shape[0] * factor
        if new_height > 10000:  # Limit to 10000 pixels
            st.error(f"Image would be too large ({new_height} pixels tall). Maximum is 10000 pixels.")
            return image
        return np.repeat(image, factor, axis=0)

    def stretch_horizontally(image, factor=2):
        # Check if resulting image would be too large
        new_width = image.shape[1] * factor
        if new_width > 10000:  # Limit to 10000 pixels
            st.error(f"Image would be too large ({new_width} pixels wide). Maximum is 10000 pixels.")
            return image
        return np.repeat(image, factor, axis=1)

    def rotate_image(image, clockwise):
        if clockwise:
            return np.rot90(image, k=1)
        else:
            return np.rot90(image, k=-1)

    def mirror_vertically(image):
        return np.flip(image, axis=0)
        
    def mirror_horizontally(image):
        return np.flip(image, axis=1)
    
    # Transformarion Button Logic
    if vstretch_button:
        # Open dialog to get verticle stretch magnitude from user
        get_vstretch_factor()
    # Check if we need to perform vstretch (after dialog closes)
    if st.session_state.perform_vstretch:
        st.session_state.current_image = stretch_vertically(
            st.session_state.current_image, 
            st.session_state.vstretch_factor
        )
        # Clear the flags after use
        st.session_state.vstretch_factor = None
        st.session_state.perform_vstretch = False
    elif hstretch_button:
        # Open dialog to get horizonal stretch magnitude from user
        get_hstretch_factor()
    if st.session_state.perform_hstretch:
        st.session_state.current_image = stretch_horizontally(
            st.session_state.current_image, 
            st.session_state.hstretch_factor
        )
        # Clear the flags after use
        st.session_state.hstretch_factor = None
        st.session_state.perform_hstretch = False
    elif rotate_button:
        # Open dialog to get direction from user
        direction()
    # Check if we need to perform rotation (after dialog closes)
    if st.session_state.perform_rotation:
        st.session_state.current_image = rotate_image(
            st.session_state.current_image, 
            st.session_state.rotation_direction
        )
        # Clear the flags after use
        st.session_state.rotation_direction = None
        st.session_state.perform_rotation = False
    elif vflip_button:
        st.session_state.current_image = mirror_vertically(st.session_state.current_image)
    elif hflip_vbutton:
        st.session_state.current_image = mirror_horizontally(st.session_state.current_image)
    
    # Always update image each time the script is ran
    update_image()

    





