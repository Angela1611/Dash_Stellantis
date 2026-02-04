import streamlit as st
import base64
import os
import pandas as pd

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

def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        # Ensure 'Documento' is treated as string for comparison and remove any leading/trailing spaces
        if 'Documento' in df.columns:
            df['Documento'] = df['Documento'].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None

def main():
    st.set_page_config(page_title="Dashboard RFC", layout="centered")
    
    # Path to the background image
    image_path = "stellantis.jpeg"
    excel_path = "ROSTER2.xlsx"
    
    if os.path.exists(image_path):
        set_png_as_page_bg(image_path)
    else:
        st.warning(f"Image not found at {image_path}. Please ensure 'stellantis.jpeg' is in the same directory.")

    st.title("User Dashboard")
    
    # Create the RFC input field
    rfc_input = st.text_input("RFC", placeholder="Ingrese su RFC aquí")
    
    if st.button("Ingresar"):
        if rfc_input:
            if os.path.exists(excel_path):
                df = load_data(excel_path)
                if df is not None:
                    # Clean input rfc
                    clean_rfc = rfc_input.strip()
                    
                    # Lookup
                    # specific check for column existence to avoid crash
                    if 'Documento' in df.columns and 'Nombre' in df.columns:
                        result = df[df['Documento'] == clean_rfc]
                        
                        if not result.empty:
                            nombre = result.iloc[0]['Nombre']
                            st.success(f"Nombre encontrado: {nombre}")
                        else:
                            st.error("RFC no encontrado.")
                    else:
                        st.error("El archivo Excel no tiene las columnas requeridas: 'Documento' y 'Nombre'.")
            else:
                st.error(f"No se encontró el archivo de datos: {excel_path}")
        else:
            st.warning("Por favor ingrese un RFC.")

if __name__ == "__main__":
    main()
