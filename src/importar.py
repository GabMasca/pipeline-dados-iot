from pathlib import Path
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parents[1]
load_dotenv(BASE / ".env")
url = os.getenv("DATABASE_URL")
if not url:
    raise RuntimeError("Configure DATABASE_URL no arquivo .env (veja .env.example).")

csv_file = BASE / "data" / "IOT-temp.csv"
if not csv_file.is_file():
    raise FileNotFoundError(f"Baixe o CSV do Kaggle e salve em {csv_file}")

raw = pd.read_csv(csv_file)
required = {"id", "room_id/id", "noted_date", "temp", "out/in"}
if not required.issubset(raw.columns):
    raise ValueError(f"Colunas ausentes: {sorted(required - set(raw.columns))}. Recebidas: {list(raw.columns)}")

print(f"Linhas recebidas: {len(raw):,}")
df = raw.rename(columns={
    "id": "leitura_id", "room_id/id": "ambiente",
    "noted_date": "data_leitura", "temp": "temperatura",
    "out/in": "tipo_sensor",
})
df["data_leitura"] = pd.to_datetime(df["data_leitura"], format="%d-%m-%Y %H:%M", errors="coerce")
df["temperatura"] = pd.to_numeric(df["temperatura"], errors="coerce")
df["tipo_sensor"] = df["tipo_sensor"].astype("string").str.strip().str.lower().map({"in": "Interno", "out": "Externo"})
df = df.dropna(subset=["leitura_id", "data_leitura", "temperatura", "tipo_sensor"])
df = df.drop_duplicates(subset=["leitura_id"])
print(f"Linhas válidas após limpeza: {len(df):,}")
if df.empty:
    raise ValueError("Nenhuma leitura válida após limpeza.")

engine = create_engine(url, pool_pre_ping=True)

sql = (BASE / "sql" / "views.sql").read_text(encoding="utf-8")

with engine.begin() as connection:
    # As views precisam ser removidas antes de substituir a tabela.
    for view in ("avg_temp_por_dispositivo", "leituras_por_hora", "temp_max_min_por_dia"):
        connection.execute(text(f"DROP VIEW IF EXISTS {view}"))

    df.to_sql(
        "temperature_readings",
        connection,
        if_exists="replace",
        index=False,
        chunksize=2000,
        method="multi"
    )

    for statement in sql.split(";"):
        statement = "\n".join(
            linha for linha in statement.splitlines()
            if linha.strip() and not linha.strip().startswith("--")
        ).strip()

        if statement:
            connection.execute(text(statement))

    count = connection.execute(
        text("SELECT COUNT(*) FROM temperature_readings")
    ).scalar_one()

print(f"Sucesso! {count:,} leituras gravadas e 3 views criadas.")
