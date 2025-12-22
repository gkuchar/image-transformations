import streamlit as st

st.title('Transform By Gaming')
st.write(
    "Upload a new image or select one from the collections to begin transforming it. "
    "Play various games to affect the image in various ways!"
    )

if "caption_text" not in st.session_state:
    st.session_state.caption_text = ""

image_slot = st.empty()
caption_slot = st.empty()

uploaded_file = st.file_uploader(
    "Upload new image:",
    type=["jpg", "png", "jpeg"],
    )

if uploaded_file:
    with caption_slot:
        st.session_state.caption_text = st.text_input(
            'Give your image a caption (optional)'
            )
    with image_slot:
        st.image(uploaded_file, caption=st.session_state.caption_text)
    
    





