import streamlit as st
import re
from num2words import num2words
from fpdf import FPDF
from datetime import datetime
import io

salarios_minimos = {
    "01/2018": 954.00, "02/2018": 954.00, "03/2018": 954.00, "04/2018": 954.00, "05/2018": 954.00, "06/2018": 954.00,
    "07/2018": 954.00, "08/2018": 954.00, "09/2018": 954.00, "10/2018": 954.00, "11/2018": 954.00, "12/2018": 954.00,
    "01/2019": 998.00, "02/2019": 998.00, "03/2019": 998.00, "04/2019": 998.00, "05/2019": 998.00, "06/2019": 998.00,
    "07/2019": 998.00, "08/2019": 998.00, "09/2019": 998.00, "10/2019": 998.00, "11/2019": 998.00, "12/2019": 998.00,
    "01/2020": 1039.00, "02/2020": 1045.00, "03/2020": 1045.00, "04/2020": 1045.00, "05/2020": 1045.00, "06/2020": 1045.00,
    "07/2020": 1045.00, "08/2020": 1045.00, "09/2020": 1045.00, "10/2020": 1045.00, "11/2020": 1045.00, "12/2020": 1045.00,
    "01/2021": 1100.00, "02/2021": 1100.00, "03/2021": 1100.00, "04/2021": 1100.00, "05/2021": 1100.00, "06/2021": 1100.00,
    "07/2021": 1100.00, "08/2021": 1100.00, "09/2021": 1100.00, "10/2021": 1100.00, "11/2021": 1100.00, "12/2021": 1100.00,
    "01/2022": 1212.00, "02/2022": 1212.00, "03/2022": 1212.00, "04/2022": 1212.00, "05/2022": 1212.00, "06/2022": 1212.00,
    "07/2022": 1212.00, "08/2022": 1212.00, "09/2022": 1212.00, "10/2022": 1212.00, "11/2022": 1212.00, "12/2022": 1212.00,
    "01/2023": 1302.00, "02/2023": 1302.00, "03/2023": 1302.00, "04/2023": 1302.00, "05/2023": 1320.00, "06/2023": 1320.00,
    "07/2023": 1320.00, "08/2023": 1320.00, "09/2023": 1320.00, "10/2023": 1320.00, "11/2023": 1320.00, "12/2023": 1320.00,
    "01/2024": 1412.00, "02/2024": 1412.00, "03/2024": 1412.00, "04/2024": 1412.00, "05/2024": 1412.00, "06/2024": 1412.00,
    "07/2024": 1412.00, "08/2024": 1412.00, "09/2024": 1412.00, "10/2024": 1412.00, "11/2024": 1412.00, "12/2024": 1412.00,
    "01/2025": 1518.00, "02/2025": 1518.00, "03/2025": 1518.00, "04/2025": 1518.00, "05/2025": 1518.00, "06/2025": 1518.00,
    "07/2025": 1518.00, "08/2025": 1518.00, "09/2025": 1518.00, "10/2025": 1518.00, "11/2025": 1518.00, "12/2025": 1518.00,
}

st.title("📊 Sistema de Cálculo de Adicionais Trabalhistas")
st.write("Preencha os dados abaixo para calcular os adicionais:")

nome = st.text_input("Nome da pessoa analisada")
competencia = st.text_input("Competência (MM/AAAA)")

competencia_valida = bool(re.match(r"^(0[1-9]|1[0-2])/[0-9]{4}$", competencia))
salario_minimo_vigente = salarios_minimos.get(competencia) if competencia_valida else None

if competencia and not competencia_valida:
    st.warning("Digite a competência no formato MM/AAAA.")
elif competencia_valida and salario_minimo_vigente is None:
    st.info("Competência não encontrada na tabela. Digite o salário mínimo manualmente.")

if nome and competencia:
    st.success(f"Analisando {nome} para a competência {competencia}")

salario_base = st.number_input("Salário Base (R$)", min_value=0.0, step=100.0, format="%.2f")
divisor_jornada = st.number_input("Divisor da Jornada Mensal", min_value=1.0, value=220.0, step=1.0, format="%.0f")

if competencia_valida and salario_minimo_vigente:
    salario_minimo = st.number_input("Salário Mínimo Vigente (R$)", min_value=0.0, value=salario_minimo_vigente, step=10.0, format="%.2f")
else:
    salario_minimo = st.number_input("Salário Mínimo Vigente (R$)", min_value=0.0, value=0.0, step=10.0, format="%.2f")

recebe_periculosidade = st.checkbox("Recebe Periculosidade? (30% do salário base)")
adicional_periculosidade = salario_base * 0.3 if recebe_periculosidade else 0.0

grau_insalubridade = st.selectbox("Grau de Insalubridade", ["Nenhum", "10% (Leve)", "20% (Médio)", "40% (Máximo)"])
if grau_insalubridade == "10% (Leve)":
    adicional_insalubridade = salario_minimo * 0.1
elif grau_insalubridade == "20% (Médio)":
    adicional_insalubridade = salario_minimo * 0.2
elif grau_insalubridade == "40% (Máximo)":
    adicional_insalubridade = salario_minimo * 0.4
else:
    adicional_insalubridade = 0.0

horas_noturnas = st.number_input("Horas Noturnas", min_value=0.0, step=1.0)
horas_50 = st.number_input("Horas Extras 50%", min_value=0.0, step=1.0)
horas_100 = st.number_input("Horas Extras 100%", min_value=0.0, step=1.0)

