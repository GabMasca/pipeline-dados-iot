from pathlib import Path
import os
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine

BASE = Path(__file__).resolve().parents[1]
load_dotenv(BASE / ".env")
st.set_page_config(page_title="Temperaturas IoT", layout="wide")
st.title("Dashboard de Temperaturas IoT")
st.caption("Fonte: Temperature Readings: IoT Devices (Kaggle). Dados históricos de 2018.")
url = os.getenv("DATABASE_URL")
if not url:
    st.error("Configure DATABASE_URL no arquivo .env")
    st.stop()

@st.cache_resource
def db():
    return create_engine(url, pool_pre_ping=True)

@st.cache_data(ttl=60)
def consultar(view):
    permitidas = {"avg_temp_por_dispositivo", "leituras_por_hora", "temp_max_min_por_dia"}
    if view not in permitidas:
        raise ValueError("View não permitida")
    with db().connect() as conn:
        return pd.read_sql(f'SELECT * FROM {view}', conn)

try:
    media = consultar("avg_temp_por_dispositivo")
    horas = consultar("leituras_por_hora")
    dias = consultar("temp_max_min_por_dia")
except Exception:
    st.error("Não foi possível carregar as views. Confira a conexão com o banco e execute a importação dos dados.")
    st.stop()

st.subheader("1. Temperatura média por localização do sensor")
st.plotly_chart(px.bar(media, x="tipo_sensor", y="avg_temp", color="tipo_sensor", text="avg_temp",
                       labels={"tipo_sensor":"Sensor", "avg_temp":"Temperatura média (°C)"}), use_container_width=True)
st.subheader("2. Quantidade de leituras por hora")
st.plotly_chart(px.line(horas, x="hora", y="contagem", markers=True,
                        labels={"hora":"Hora do dia", "contagem":"Número de leituras"}), use_container_width=True)
st.subheader("3. Temperaturas máximas e mínimas por dia")
long = dias.melt(id_vars="data", value_vars=["temp_min", "temp_max"], var_name="medida", value_name="temperatura")
st.plotly_chart(px.line(long, x="data", y="temperatura", color="medida",
                        labels={"data":"Data", "temperatura":"Temperatura (°C)", "medida":"Medida"}), use_container_width=True)
st.caption("Observação: 'Interno' e 'Externo' são categorias de medição, não IDs individuais de aparelhos.")
