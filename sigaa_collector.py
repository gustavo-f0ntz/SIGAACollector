from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
from collections import defaultdict
import tkinter as tk
from tkinter import simpledialog


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
# Seleção de navegador e inicialização
# ---------------------

BROWSERS = {
    "1": ("Chrome", "chrome"),
    "2": ("Firefox", "firefox"),
    "3": ("Opera", "opera"),
    "4": ("Opera GX", "opera_gx"),
    "5": ("Brave", "brave"),
}


def init_driver(browser_key):
    if browser_key in ("chrome", "brave"):
        options = webdriver.ChromeOptions()
        if browser_key == "brave":
            brave_path = os.environ.get("BRAVE_PATH")
            if brave_path:
                options.binary_location = brave_path
        options.add_experimental_option("detach", True)
        return webdriver.Chrome(options=options)
    if browser_key == "firefox":
        options = webdriver.FirefoxOptions()
        return webdriver.Firefox(options=options)
    if browser_key in ("opera", "opera_gx"):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        if browser_key == "opera_gx":
            opera_gx_path = os.environ.get("OPERAGX_PATH")
            if opera_gx_path:
                options.binary_location = opera_gx_path
        return webdriver.Opera(options=options)
    raise ValueError("Navegador não suportado")

# ---------------------
# Seleção da instituição e abertura do SIGAA correspondente
# ---------------------

INSTITUTIONS = {
    "1": ("UFERSA", "https://sigaa.ufersa.edu.br/sigaa/verTelaLogin.do"),
    "2": ("UERN", "https://sigaa.uern.br/sigaa/verTelaLogin.do"),
}

root = tk.Tk()
root.withdraw()

inst_choice = None
while inst_choice not in INSTITUTIONS:
    inst_choice = simpledialog.askstring(
        "Instituição",
        "Escolha a instituição:\n1 - UFERSA\n2 - UERN",
    )
    if inst_choice is None:
        print("Seleção cancelada.")
        exit()

browser_choice = None
while browser_choice not in BROWSERS:
    browser_choice = simpledialog.askstring(
        "Navegador",
        "Escolha o navegador:\n1 - Chrome\n2 - Firefox\n3 - Opera\n4 - Opera GX\n5 - Brave",
    )
    if browser_choice is None:
        print("Seleção cancelada.")
        exit()

root.destroy()

inst_name, inst_url = INSTITUTIONS[inst_choice]
driver = init_driver(BROWSERS[browser_choice][1])
print(f"🌐 Abrindo {inst_name}...")
driver.get(inst_url)

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
