import streamlit as st
import re
import pandas as pd

st.set_page_config(page_title="Extrair dados colados do PDF", layout="centered")
st.title("📋 Colar texto do PDF para extrair salários e vínculos")

# Caixa de texto para colar o conteúdo do PDF
texto_pdf = st.text_area("Cole aqui o conteúdo do PDF copiado:", height=400)

if texto_pdf:
    # Quebrar o texto em blocos por sequência ("Seq.")
    blocos = re.split(r"(?=Seq\.\s+\d+)", texto_pdf)

    dados = []

    for bloco in blocos:
        # Encontrar número da sequência (seq.)
        match_seq = re.search(r"Seq\.\s+(\d+)", bloco)
        if not match_seq:
            continue
        seq = match_seq.group(1)

        # Tentar encontrar o Código do Empregador
        match_codigo_emp = re.search(r"C[oó]digo Emp\. Origem do V[ií]nculo:\s*(\d+)", bloco)
        codigo_emp = match_codigo_emp.group(1) if match_codigo_emp else ""

        # Encontrar competências e remunerações no bloco
        matches = re.findall(r"(\d{2}/\d{4})\s+([\d\.]+,[\d]{2})", bloco)
        for competencia, remuneracao in matches:
            try:
                # Limpar e converter remuneração
                remuneracao_float = float(remuneracao.replace(".", "").replace(",", "."))
                dados.append([seq, codigo_emp, competencia, remuneracao_float])
            except ValueError:
                continue

    if dados:
        df = pd.DataFrame(dados, columns=["Seq.", "Código Emp.", "Competência", "Remuneração (R$)"])
        st.success("✅ Dados extraídos com sucesso!")
        st.dataframe(df)

        # Gerar CSV
        csv = df.to_csv(index=False, sep=";", decimal=",", encoding="utf-8-sig")
        st.download_button("📥 Baixar CSV", data=csv, file_name="salarios_extraidos.csv")
    else:
        st.warning("⚠️ Nenhuma competência ou salário foi encontrado no texto colado.")
