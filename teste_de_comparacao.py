# Testando diferença entre = e ==
profissao = input("Digite a profissão do cliente: ")

# Comparação SEM .lower()
if profissao == "desempregado":
    print("✅ Comparação sem .lower() deu certo!")
else:
    print("❌ Comparação sem .lower() FALHOU!")

# Comparação COM .lower()
if profissao.lower() == "desempregado":
    print("✅ Comparação com .lower() deu certo!")
else:
    print("❌ Comparação com .lower() FALHOU!")

