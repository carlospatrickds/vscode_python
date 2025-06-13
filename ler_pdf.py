import fitz  # PyMuPDF

# Caminho do seu PDF
caminho_pdf = "exemplo.pdf"  # substitua pelo nome real do seu arquivo

# Abre o PDF
doc = fitz.open(caminho_pdf)

# Percorre todas as páginas e imprime o texto
for pagina in doc:
    texto = pagina.get_text()
    print(texto)
    print("-" * 50)  # separador entre páginas

doc.close()

import fitz
import re  # módulo de expressões regulares

caminho_pdf = "exemplo.pdf"

doc = fitz.open(caminho_pdf)

# Lista pra guardar valores encontrados
valores_encontrados = []

for pagina in doc:
    texto = pagina.get_text()

    # Expressão regular para valores em reais tipo "R$ 1.234,56"
    valores = re.findall(r'R\$ ?\d{1,3}(?:\.\d{3})*,\d{2}', texto)

    valores_encontrados.extend(valores)

doc.close()

# Mostra os valores encontrados
print("Valores encontrados no PDF:")
for valor in valores_encontrados:
    print(valor)

import fitz  # PyMuPDF
import re

caminho_pdf = "sahhhhhhhhhhhhh.pdf"
doc = fitz.open(caminho_pdf)

valores_encontrados = []

for pagina in doc:
    texto = pagina.get_text()
    
    # Expressão regular para valores como R$ 1.412,00
    encontrados = re.findall(r'R\$ ?[\d\.]+,\d{2}', texto)
    
    valores_encontrados.extend(encontrados)

doc.close()

print("💰 Valores encontrados:")
for v in valores_encontrados:
    print(v)
