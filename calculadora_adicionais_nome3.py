import streamlit as st
import re
from num2words import num2words
from datetime import datetime

salarios_minimos = {
    "01/2018": 100.00, "02/2018": 954.00, "03/2018": 954.00, "04/2018": 954.00, "05/2018": 954.00, "06/2018": 954.00,
    "07/2018": 954.00, "08/2018": 954.00, "09/2018": 954.00, "10/2018": 954.00, "11/2018": 954.00, "12/2018": 954.00,
    "01/2019": 50.00, "02/2019": 998.00, "03/2019": 998.00, "04/2019": 998.00, "05/2019": 998.00, "06/2019": 998.00,
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

def format_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_real_sem_rs(valor):
    return "{:,.2f}".format(valor).replace(",", "X").replace(".", ",").replace("X", ".")

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

if st.button("Calcular", key="btn_calcular"):
    operacoes = []

    base_hora = salario_base + adicional_periculosidade + adicional_insalubridade
    operacoes.append(
        f"Base de cálculo da hora normal = salário base + adicional periculosidade + adicional insalubridade = "
        f"{format_real_sem_rs(salario_base)} + {format_real_sem_rs(adicional_periculosidade)} + {format_real_sem_rs(adicional_insalubridade)} = "
        f"{format_real_sem_rs(base_hora)}"
    )

    valor_hora_normal = base_hora / divisor_jornada if divisor_jornada > 0 else 0.0
    operacoes.append(
        f"Valor da hora normal = base de cálculo / divisor jornada = {format_real_sem_rs(base_hora)} / {divisor_jornada:.0f} = {format_real_sem_rs(valor_hora_normal)}"
    )

    adicional_noturno = horas_noturnas * valor_hora_normal * 0.2
    operacoes.append(
        f"Adicional noturno = horas noturnas x valor hora normal x 20% = {horas_noturnas:.0f} x {format_real_sem_rs(valor_hora_normal)} x 0.2 = {format_real_sem_rs(adicional_noturno)}"
    )

    valor_hora_50 = valor_hora_normal * 1.5
    operacoes.append(
        f"Valor da hora extra 50% = valor hora normal x 1.5 = {format_real_sem_rs(valor_hora_normal)} x 1.5 = {format_real_sem_rs(valor_hora_50)}"
    )
    valor_hora_100 = valor_hora_normal * 2.0
    operacoes.append(
        f"Valor da hora extra 100% = valor hora normal x 2 = {format_real_sem_rs(valor_hora_normal)} x 2 = {format_real_sem_rs(valor_hora_100)}"
    )

    total_horas_50 = horas_50 * valor_hora_50
    operacoes.append(
        f"Total de horas extras 50% = quantidade x valor hora 50% = {horas_50:.0f} x {format_real_sem_rs(valor_hora_50)} = {format_real_sem_rs(total_horas_50)}"
    )
    total_horas_100 = horas_100 * valor_hora_100
    operacoes.append(
        f"Total de horas extras 100% = quantidade x valor hora 100% = {horas_100:.0f} x {format_real_sem_rs(valor_hora_100)} = {format_real_sem_rs(total_horas_100)}"
    )

    total_adicionais = (
        adicional_periculosidade +
        adicional_insalubridade +
        adicional_noturno +
        total_horas_50 +
        total_horas_100
    )
    operacoes.append(
        f"Total de adicionais = periculosidade + insalubridade + noturno + horas 50% + horas 100% = "
        f"{format_real_sem_rs(adicional_periculosidade)} + {format_real_sem_rs(adicional_insalubridade)} + {format_real_sem_rs(adicional_noturno)} + "
        f"{format_real_sem_rs(total_horas_50)} + {format_real_sem_rs(total_horas_100)} = {format_real_sem_rs(total_adicionais)}"
    )

    st.subheader("📝 Detalhamento:")
    st.write(f"🔹 Salário Base: {format_real(salario_base)}")
    st.write(f"🔹 Adicional de Periculosidade: {format_real(adicional_periculosidade)}")
    st.write(f"🔹 Adicional de Insalubridade: {format_real(adicional_insalubridade)}")
    st.write(f"🔹 Base de Cálculo da Hora: {format_real(base_hora)}")
    st.write(f"🔹 Valor da Hora Normal: {format_real(valor_hora_normal)}")

    st.subheader("💰 Cálculos:")
    st.write(
        f"🌙 Adicional Noturno ({horas_noturnas:.0f}h): {format_real(adicional_noturno)}"
    )
    st.write(
        f"⏱️ Horas Extras 50% ({horas_50:.0f}h): {format_real(total_horas_50)} ({format_real(valor_hora_50)}/hora)"
    )
    st.write(
        f"⏱️ Horas Extras 100% ({horas_100:.0f}h): {format_real(total_horas_100)} ({format_real(valor_hora_100)}/hora)"
    )
    st.success(f"💰 Total de Adicionais: {format_real(total_adicionais)}")

    st.subheader("📑 Histórico de Operações Realizadas")
    for op in operacoes:
        st.write(f"- {op}")
