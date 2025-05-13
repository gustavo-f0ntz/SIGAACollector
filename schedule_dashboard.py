import streamlit as st
import pandas as pd

st.set_page_config(page_title="SIGAA Schedule", layout="wide")

st.title("📚 Visualizador de Horários - SIGAACollector")

# Carregar o CSV
df = pd.read_csv("output/subjects_schedule.csv")

# ✅ DEBUG opcional (pode remover depois)
# st.write("🧾 Colunas disponíveis:", df.columns.tolist())

# Filtros
dias = df["DIA"].unique()
turnos = df["TURNO"].unique()

col1, col2 = st.columns(2)
with col1:
    filtro_dia = st.multiselect("📅 Filtrar por dia da semana", dias, default=list(dias))
with col2:
    filtro_turno = st.multiselect("🕒 Filtrar por turno", turnos, default=list(turnos))

# Aplicar filtros
df_filtrado = df[(df["DIA"].isin(filtro_dia)) & (df["TURNO"].isin(filtro_turno))]

# Exibir resultado
st.dataframe(df_filtrado, use_container_width=True)
