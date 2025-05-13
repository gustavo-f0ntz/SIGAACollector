from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
from collections import defaultdict

# ---------------------
# Função auxiliar: Detecta o turno com base no horário de início
# ---------------------
def detectar_turno(hora_inicio):
    hora, minuto = map(int, hora_inicio.split(":"))
    if 7 <= hora < 12:
        return "MANHÃ"
    elif 13 <= hora < 18:
        return "TARDE"
    elif 18 <= hora <= 22:
        return "NOITE"
    else:
        return "Unknown"

# ---------------------
# Inicialização do navegador
# ---------------------
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # Deixa o navegador aberto depois
driver = webdriver.Chrome(options=options)

# Garantir pasta de saída
if not os.path.exists("output"):
    os.makedirs("output")

print("🔵 Abra o SIGAA, faça login e acesse a tela de matrícula com disciplinas + horários.")
input("⚡ Pressione ENTER aqui quando estiver na tela certa...")

# ---------------------
# Coletar disciplinas (código, nome e local)
# ---------------------
print("📝 Coletando disciplinas e códigos...")

disciplinas_rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'listagem')]//tbody//tr")

codigo_nome_disciplina = {}

for row in disciplinas_rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) >= 3:
        texto_disciplina = cols[0].text.strip()
        local_disciplina = cols[2].text.strip()
        if " - " in texto_disciplina:
            codigo = texto_disciplina.split(" - ")[0].strip()
            nome = " - ".join(texto_disciplina.split(" - ")[1:]).split("-")[0].strip()
            codigo_nome_disciplina[codigo] = {
                "nome": nome,
                "local": local_disciplina
            }

print(f"✅ Disciplinas capturadas: {len(codigo_nome_disciplina)}")

# ---------------------
# Coletar horários da tabela de grade
# ---------------------
print("🕒 Coletando horários da grade...")

horarios_rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'formulario')]//tbody//tr")

dias_da_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']

dados_finais = []

for row in horarios_rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) < 7:
        continue

    horario_faixa = cols[0].text.strip()

    if " - " not in horario_faixa:
        continue

    hora_inicio, hora_fim = horario_faixa.split(" - ")

    for i in range(1, 7):  # De Segunda até Sábado
        codigo_disciplina = cols[i].text.strip()
        if codigo_disciplina and codigo_disciplina != "---":
            dados_finais.append({
                "Codigo": codigo_disciplina,
                "Dia": dias_da_semana[i - 1],
                "Hora Inicio": hora_inicio,
                "Hora Fim": hora_fim
            })

# ---------------------
# Agrupar por código e dia
# ---------------------
agrupador = defaultdict(list)

for dado in dados_finais:
    key = (dado['Codigo'], dado['Dia'])
    agrupador[key].append((dado['Hora Inicio'], dado['Hora Fim']))

# ---------------------
# Montar o CSV final
# ---------------------
print("💾 Montando CSV final...")

linhas_csv = []

for (codigo, dia), horarios in agrupador.items():
    info = codigo_nome_disciplina.get(codigo, {"nome": "Unknown", "local": "Unknown"})
    horarios.sort()
    hora_inicio = horarios[0][0]
    hora_fim = horarios[-1][1]

    linhas_csv.append({
        "DISCIPLINA": info['nome'],
        "LOCAL DE AULA": info['local'],
        "DIA": dia,
        "TURNO": detectar_turno(hora_inicio),
        "HORÁRIO INICIAL": hora_inicio,
        "HORÁRIO FINAL": hora_fim
    })

df = pd.DataFrame(linhas_csv)
df.to_csv('output/subjects_schedule.csv', index=False, encoding='utf-8-sig')

print("✅ Arquivo 'subjects_schedule.csv' gerado com sucesso!")
