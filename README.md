# Dexscreener Soft

A pet project for scraping tokens from Dexscreener and exposing data through FastAPI + PostgreSQL.
Focus: asynchronous scraping, database persistence, and a simple API for querying.

## 🚀 Features

- Scrapes Dexscreener token tables (tickers, age, market cap).
- Persists data into PostgreSQL with duplicate handling.
- REST API with FastAPI for retrieving token data.
- .env configuration for database and runtime settings

## ⚙️ Installation & Run

Clone the repo:

```git clone https://github.com/wfofw/dexscreener_soft```

```cd dexscreener_soft```


Run the batch script (Windows):

```startBAT.bat```


It will create a virtual environment, install dependencies, and launch the project.

Access FastAPI at:
👉 http://127.0.0.1:8000/docs


## 🗄️.env configuration

Example:

- DB_HOST=127.0.0.1 
- DB_PORT=11911 
- DB_NAME=mydb 
- DB_USER=myuser 
- DB_PASSWORD=mypassword 
- CHROME_PORT=55555 


## 📂 Project structure

```
birge_api/
├── fast.py           # FastAPI app
├── start.py          # main scraper runner
├── logger.py         # logging utils
├── config.env        # environment variables (gitignored)
├── requirements.txt  # dependencies
├── start.bat         # launch script
└── .venv/            # virtual environment (gitignored)
```

 ## 🔮 Future development

- Add filtering by liquidity and volume to reduce scam tokens.
- Provide a docker-compose setup (FastAPI + PostgreSQL).
- Integrate CI/CD via GitHub Actions.
- Extract scraper into a standalone worker with a scheduler (e.g. APScheduler).
