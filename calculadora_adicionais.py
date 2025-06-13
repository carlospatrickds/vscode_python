import streamlit as st
from num2words import num2words

st.title("📊 Sistema de Cálculo de Adicionais Trabalhistas")
st.write("Preencha os dados abaixo para calcular os adicionais:")

# Entradas principais
salario_base = st.number_input("Salário Base (R$)", min_value=0.0, step=100.0, format="%.2f")
divisor_jornada = st.number_input("Divisor da Jornada Mensal", min_value=1.0, value=220.0, step=1.0, format="%.0f")
salario_minimo = st.number_input("Salário Mínimo Vigente (R$)", min_value=0.0, value=1412.00, step=10.0, format="%.2f")

# Periculosidade
recebe_periculosidade = st.checkbox("Recebe Periculosidade? (30% do salário base)")
adicional_periculosidade = salario_base * 0.3 if recebe_periculosidade else 0.0

# Insalubridade
grau_insalubridade = st.selectbox("Grau de Insalubridade", ["Nenhum", "10% (Leve)", "20% (Médio)", "40% (Máximo)"])
if grau_insalubridade == "10% (Leve)":
    adicional_insalubridade = salario_minimo * 0.1
elif grau_insalubridade == "20% (Médio)":
    adicional_insalubridade = salario_minimo * 0.2
elif grau_insalubridade == "40% (Máximo)":
    adicional_insalubridade = salario_minimo * 0.4
else:
    adicional_insalubridade = 0.0

# Horas e adicionais
horas_noturnas = st.number_input("Horas Noturnas", min_value=0.0, step=1.0)
horas_50 = st.number_input("Horas Extras 50%", min_value=0.0, step=1.0)
horas_100 = st.number_input("Horas Extras 100%", min_value=0.0, step=1.0)

if st.button("Calcular", key="btn_calcular"):
    operacoes = []

    # Base de cálculo para valor da hora normal
    base_hora = salario_base + adicional_periculosidade + adicional_insalubridade
    operacoes.append(f"Base de cálculo da hora normal = salário base + adicional periculosidade + adicional insalubridade = {salario_base:.2f} + {adicional_periculosidade:.2f} + {adicional_insalubridade:.2f} = {base_hora:.2f}")

    valor_hora_normal = base_hora / divisor_jornada if divisor_jornada > 0 else 0.0
    operacoes.append(f"Valor da hora normal = base de cálculo / divisor jornada = {base_hora:.2f} / {divisor_jornada:.0f} = {valor_hora_normal:.2f}")

    # Adicional noturno (20% sobre hora normal)
    adicional_noturno = horas_noturnas * valor_hora_normal * 0.2
    operacoes.append(f"Adicional noturno = horas noturnas x valor hora normal x 20% = {horas_noturnas:.0f} x {valor_hora_normal:.2f} x 0.2 = {adicional_noturno:.2f}")

    # Horas extras
    valor_hora_50 = valor_hora_normal * 1.5
    operacoes.append(f"Valor da hora extra 50% = valor hora normal x 1.5 = {valor_hora_normal:.2f} x 1.5 = {valor_hora_50:.2f}")
    valor_hora_100 = valor_hora_normal * 2.0
    operacoes.append(f"Valor da hora extra 100% = valor hora normal x 2 = {valor_hora_normal:.2f} x 2 = {valor_hora_100:.2f}")

    total_horas_50 = horas_50 * valor_hora_50
    operacoes.append(f"Total de horas extras 50% = quantidade x valor hora 50% = {horas_50:.0f} x {valor_hora_50:.2f} = {total_horas_50:.2f}")
    total_horas_100 = horas_100 * valor_hora_100
    operacoes.append(f"Total de horas extras 100% = quantidade x valor hora 100% = {horas_100:.0f} x {valor_hora_100:.2f} = {total_horas_100:.2f}")

    # Soma total de adicionais
    total_adicionais = (
        adicional_periculosidade +
        adicional_insalubridade +
        adicional_noturno +
        total_horas_50 +
        total_horas_100
    )
    operacoes.append(f"Total de adicionais = periculosidade + insalubridade + noturno + horas 50% + horas 100% = {adicional_periculosidade:.2f} + {adicional_insalubridade:.2f} + {adicional_noturno:.2f} + {total_horas_50:.2f} + {total_horas_100:.2f} = {total_adicionais:.2f}")

    st.subheader("📝 Detalhamento:")
    st.write(f"🔹 Salário Base: R$ {salario_base:,.2f}")
    st.write(f"🔹 Adicional de Periculosidade: R$ {adicional_periculosidade:,.2f}")
    st.write(f"🔹 Adicional de Insalubridade: R$ {adicional_insalubridade:,.2f}")
    st.write(f"🔹 Base de Cálculo da Hora: R$ {base_hora:,.2f}")
    st.write(f"🔹 Valor da Hora Normal: R$ {valor_hora_normal:,.2f}")

    st.subheader("💰 Cálculos:")
    st.write(f"🌙 Adicional Noturno ({horas_noturnas:.0f}h): R$ {adicional_noturno:,.2f}")
    st.write(f"⏱️ Horas Extras 50% ({horas_50:.0f}h): R$ {total_horas_50:,.2f} (R$ {valor_hora_50:.2f}/hora)")
    st.write(f"⏱️ Horas Extras 100% ({horas_100:.0f}h): R$ {total_horas_100:,.2f} (R$ {valor_hora_100:.2f}/hora)")
    st.success(f"💰 Total de Adicionais: R$ {total_adicionais:,.2f}")

    st.subheader("📑 Histórico de Operações Realizadas")
    for op in operacoes:
        st.write(f"- {op}")