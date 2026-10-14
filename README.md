
# Pipeline de Dados com IoT e Docker

Projeto desenvolvido para a disciplina Disruptive Architectures: IoT, Big Data e IA, do curso de Análise e Desenvolvimento de Sistemas da UniFECAF.

O objetivo foi criar um pipeline para ler dados de temperatura de sensores IoT, tratar as informações, armazená-las em um banco PostgreSQL e visualizar os resultados em um dashboard.

## Tecnologias utilizadas

- Python e Pandas: leitura e tratamento do CSV
- SQLAlchemy: conexão entre Python e PostgreSQL
- PostgreSQL: armazenamento e consultas SQL
- Docker Compose: execução do banco em contêiner
- Streamlit e Plotly: criação dos gráficos
- Git e GitHub: versionamento do projeto

## Base de dados

Foi utilizada a base pública [Temperature Readings: IoT Devices](https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices), disponível no Kaggle.

O arquivo original possui 97.606 registros. Após o tratamento, permaneceram 97.605 leituras válidas.

A base contém medições realizadas em ambientes internos e externos. Como não há identificação individual de cada dispositivo, as comparações foram feitas por localização do sensor.

O CSV não foi incluído no repositório. Para executar o projeto, é necessário baixá-lo e salvar o arquivo como:

`data/IOT-temp.csv`

## Estrutura do projeto

```text
pipeline-dados-iot/
├── data/
│   └── IOT-temp.csv          # Baixado separadamente
├── sql/
│   └── views.sql
├── src/
│   ├── importar.py
│   └── dashboard.py
├── .env.example
├── .gitignore
├── compose.yaml
├── requirements.txt
└── README.md
```

## Como executar

É necessário ter Python 3.11 ou superior, Git e Docker Desktop instalados.

Os comandos abaixo foram utilizados no Windows, com PowerShell.

### 1. Clonar o repositório

```powershell
git clone https://github.com/GabMasca/pipeline-dados-iot.git
cd pipeline-dados-iot
```

### 2. Criar e ativar o ambiente virtual

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

### 4. Configurar a conexão

```powershell
Copy-Item .env.example .env
```

No arquivo `.env`, definir uma senha local em `POSTGRES_PASSWORD` e usar a mesma senha em `DATABASE_URL`.

A conexão está configurada para a porta `5433`. Caso a senha contenha caracteres especiais, eles precisam estar codificados na URL.

### 5. Baixar os dados

Baixar o arquivo `IOT-temp.csv` no Kaggle e colocá-lo na pasta `data/`.

### 6. Iniciar o PostgreSQL

Abrir o Docker Desktop e executar:

```powershell
docker compose up -d
docker compose ps
```

Aguardar o contêiner do PostgreSQL ficar saudável (`healthy`).

### 7. Importar os dados

```powershell
python src/importar.py
```

Resultado obtido:

```text
Linhas recebidas: 97,606
Linhas válidas após limpeza: 97,605
Sucesso! 97,605 leituras gravadas e 3 views criadas.
```

### 8. Abrir o dashboard

```powershell
python -m streamlit run src/dashboard.py
```

Acessar no navegador:

http://localhost:8501

## Consultas SQL

Foram criadas três views no PostgreSQL:

| View | Finalidade |
|---|---|
| `avg_temp_por_dispositivo` | Calcula a temperatura média e a quantidade de leituras por localização do sensor |
| `leituras_por_hora` | Conta a quantidade de leituras em cada hora do dia |
| `temp_max_min_por_dia` | Mostra as temperaturas mínima e máxima registradas em cada data |

As views são utilizadas diretamente pelo dashboard.

## Dashboard

O dashboard foi desenvolvido com Streamlit e Plotly e apresenta três gráficos.

### Temperatura média por localização do sensor

Esse gráfico permite comparar as medições dos ambientes internos e externos.

### Quantidade de leituras por hora

Mostra a distribuição dos registros ao longo das 24 horas do dia.

### Temperaturas máximas e mínimas por dia

Permite observar a variação entre as temperaturas mais baixas e mais altas registradas a cada dia.

## Testes realizados

Durante o desenvolvimento, foram realizados testes de conexão com o PostgreSQL, leitura do CSV, tratamento dos dados, importação para o banco e visualização dos gráficos.

O script de importação também foi executado duas vezes seguidas para confirmar que a tabela e as views podiam ser recriadas sem erros.

Ao final, os 97.605 registros válidos foram importados e os três gráficos apareceram normalmente no navegador.

## Comandos Git utilizados

Os principais comandos utilizados para organizar e publicar o projeto foram:

```powershell
git init
git branch -M main
git add .
git commit -m "Projeto Pipeline de Dados IoT"
git remote add origin https://github.com/GabMasca/pipeline-dados-iot.git
git push -u origin main
```

O repositório foi posteriormente revisado e teve seu histórico consolidado em um único commit.

## Considerações finais

Com o projeto, foi possível praticar um processo completo de dados, passando pela leitura, limpeza, armazenamento, consultas e visualização.

A atividade ajudou a entender como diferentes ferramentas podem trabalhar juntas. Uma possibilidade de aplicação seria utilizar uma estrutura semelhante para acompanhar temperaturas em ambientes que precisam de monitoramento, como depósitos ou salas de armazenamento.

Os dados utilizados são históricos, mas a estrutura poderia ser adaptada para receber novas leituras no futuro.

## Referências

- [Temperature Readings: IoT Devices — Kaggle](https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices)
- [Docker Compose — Documentação](https://docs.docker.com/compose/)
- [Pandas — Documentação](https://pandas.pydata.org/docs/)
- [PostgreSQL — Documentação](https://www.postgresql.org/docs/16/)
- [SQLAlchemy — Documentação](https://docs.sqlalchemy.org/en/20/)
- [Streamlit — Documentação](https://docs.streamlit.io/)
- [Plotly — Documentação](https://plotly.com/python/)
