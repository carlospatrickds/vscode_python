# Coletando dados do usuário
nome = input("Digite o nome do cliente: ")
idade = int(input("Digite a idade do cliente: "))
renda = float(input("Digite a renda mensal do cliente (em R$): "))
profissao = input("Digite a profissão do cliente: ")

# Exibindo os dados
print("\n📄 Ficha do Cliente")
print("Nome:", nome)
print("Idade:", idade, "anos")
print("Renda: R$", renda)
print("Profissão:", profissao)

# Analisando perfil
print("\n🔎 Análise de Perfil:")

# Regra 1 – Benefício por renda
if renda < 2000:
    print("✅ Pode ter direito ao benefício por baixa renda.")
else:
    print("❌ Não se enquadra no critério de renda.")

# Regra 2 – Idoso
if idade >= 60:
    print("👵 Cliente é considerado idoso.")
else:
    print("🧒 Cliente não é idoso.")

if profissao.lower() == "desempregado" and renda == 0.0:
    print("🚨 Situação crítica detectada!")
else:
    print("🧑 Cliente possui emprego.")


