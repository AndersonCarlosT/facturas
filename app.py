import streamlit as st
import pdfplumber
import json

st.set_page_config(page_title="Estructura de PDF", layout="wide")

st.title("🔍 Analizador de estructura de PDF (facturas)")

uploaded_file = st.file_uploader("Sube tu PDF", type=["pdf"])

if uploaded_file is not None:
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            st.success(f"📄 PDF cargado correctamente. Total de páginas: {len(pdf.pages)}")
            
            for page_num, page in enumerate(pdf.pages, start=1):
                st.subheader(f"📄 Página {page_num}")
                
                # Extraer datos estructurados
                page_data = page.extract_words()  # lista de diccionarios por palabra
                page_text = page.extract_text()   # texto plano
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Texto plano:**")
                    st.text(page_text)
                
                with col2:
                    st.write("**Estructura JSON-like (palabras con posiciones):**")
                    st.json(page_data)
                    
    except Exception as e:
        st.error(f"❌ Error al procesar el PDF: {e}")
else:
    st.info("Por favor, sube un archivo PDF para analizar.")
