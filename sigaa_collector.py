from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os

# Configura o navegador (Chrome)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # Deixa o navegador aberto depois de rodar
driver = webdriver.Chrome(options=options)

# Cria a pasta de output se não existir
if not os.path.exists("output"):
    os.makedirs("output")

print("🔵 Abra o SIGAA, faça login e acesse a tela de matrícula com disciplinas + horários.")
input("⚡ Pressione ENTER aqui quando estiver na tela certa...")

# CAPTURANDO O MAPEAMENTO DE DISCIPLINAS (Código -> Nome)

print("📝 Coletando disciplinas e códigos...")

# Localiza a tabela de disciplinas
disciplinas_rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'listagem')]//tbody//tr")

codigo_nome_disciplina = {}

for row in disciplinas_rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) >= 1:
        texto_disciplina = cols[0].text.strip()
        if " - " in texto_disciplina:
            codigo = texto_disciplina.split(" - ")[0].strip()
            nome = " - ".join(texto_disciplina.split(" - ")[1:]).split("-")[0].strip()
            codigo_nome_disciplina[codigo] = nome

print(f"✅ Disciplinas capturadas: {len(codigo_nome_disciplina)}")


# CAPTURANDO A GRADE DE HORÁRIOS

print("📝 Coletando horários da grade...")

# Localiza a tabela de horários
horarios_rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'formulario')]//tbody//tr")

# Mapeamento das colunas para dias da semana
dias_da_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']

dados_finais = []

# Vamos percorrer cada linha da tabela
for index, row in enumerate(horarios_rows):
    cols = row.find_elements(By.TAG_NAME, "td")
    
    if len(cols) < 7:
        continue  # Pula linhas que não têm todas as colunas

    horario_faixa = cols[0].text.strip()

# Só tenta separar se realmente existir um " - " no texto
    if " - " in horario_faixa:
        hora_inicio, hora_fim = horario_faixa.split(" - ")

        for i in range(1, 7):  # de Segunda até Sábado
            codigo_disciplina = cols[i].text.strip()
            if codigo_disciplina and codigo_disciplina != "---":
                dados_finais.append({
                    "Codigo": codigo_disciplina,
                    "Dia": dias_da_semana[i-1],
                    "Hora Inicio": hora_inicio,
                    "Hora Fim": hora_fim
                })
    else:
        # Se não tem formato correto, ignora a linha
        continue


    for i in range(1, 7):  # De 1 a 6 porque a primeira coluna é o horário
        codigo_disciplina = cols[i].text.strip()

        if codigo_disciplina and codigo_disciplina != "---":
            dados_finais.append({
                "Codigo": codigo_disciplina,
                "Dia": dias_da_semana[i-1],  # Ajusta índice porque lista começa no 0
                "Hora Inicio": hora_inicio,
                "Hora Fim": hora_fim
            })


# ORGANIZANDO E SALVANDO EM CSV

print("💾 Montando CSV final...")

# Lista para armazenar as linhas finais
linhas_csv = []

for dado in dados_finais:
    codigo = dado['Codigo']
    nome_disciplina = codigo_nome_disciplina.get(codigo, "Desconhecido")
    
    linhas_csv.append({
        "Subject": nome_disciplina,
        "Location": "",  # (vamos pensar se puxamos o local depois!)
        "Day": dado['Dia'],
        "Period": "",  # (periodo tipo manhã, tarde, noite — vamos inferir depois se quiser)
        "Start Time": dado['Hora Inicio'],
        "End Time": dado['Hora Fim']
    })

# Criar DataFrame
df = pd.DataFrame(linhas_csv)

# Salvar CSV
df.to_csv('output/subjects_schedule.csv', index=False, encoding='utf-8-sig')

print("✅ Arquivo 'subjects_schedule.csv' gerado com sucesso!")
