import streamlit as st
import pdfplumber
import re
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Extractor de Factor", layout="wide")
st.title("📄 Extractor de 'Factor:' en PDFs de facturas")

uploaded_files = st.file_uploader(
    "Sube tus facturas PDF",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    resultados = []

    for uploaded_file in uploaded_files:
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                factor_valor = None
                
                for page in pdf.pages:
                    texto = page.extract_text()
                    if texto:
                        match = re.search(r"Factor:([0-9]+\.[0-9]+)", texto)
                        if match:
                            factor_valor = match.group(1)
                            break  # Como solo hay uno por PDF, paramos aquí

                if factor_valor:
                    resultados.append({
                        "Archivo PDF": uploaded_file.name,
                        "Factor": float(factor_valor)
                    })
                else:
                    resultados.append({
                        "Archivo PDF": uploaded_file.name,
                        "Factor": "No encontrado"
                    })
        except Exception as e:
            st.error(f"Error procesando {uploaded_file.name}: {e}")

    if resultados:
        df = pd.DataFrame(resultados)
        st.subheader("📊 Resultados extraídos")
        st.dataframe(df)

        # Generar Excel para descargar
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        output.seek(0)

        st.download_button(
            label="⬇️ Descargar resultados en Excel",
            data=output,
            file_name="factores_extraidos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
