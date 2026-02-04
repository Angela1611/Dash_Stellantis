import streamlit as st
import base64
import os

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/jpeg;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Dashboard RFC", layout="centered")
    
    # Path to the background image
    # Assuming the image is in the same directory as the script
    image_path = "stellantis.jpeg"
    
    if os.path.exists(image_path):
        set_png_as_page_bg(image_path)
    else:
        st.warning(f"Image not found at {image_path}. Please ensure 'stellantis.jpeg' is in the same directory.")

    st.title("User Dashboard")
    
    # Create the RFC input field
    rfc_input = st.text_input("RFC", placeholder="Ingrese su RFC aquí")
    
    if rfc_input:
        st.write(f"RFC Ingresado: {rfc_input}")

if __name__ == "__main__":
    main()
