# Project Outline: E-commerce RAG System with Dashboards

## Objective

To build a Retrieval-Augmented Generation (RAG) system using FastAPI and React that allows users to query product recommendations based on the Global Power Plants & Renewable Energy Data , alongside helpful dashboards for insights.

<!-- ## Table of Content
*Installation and setup* -->

## Architecture

    React (Vite)
    ↓
    FastAPI
    ↓
    RAG Pipeline  ←→  ChromaDB (vector store)
    ↓
    Siemens Embeddings (bge-m3)
    ↓
    Siemens LLM 
    Reranker   (qwen3-reranker-0.6b)

## Models

| Role       | Model                         |
| ---------- | ----------------------------- |
| Embedding  | bge-m3                        |
| Generation | ministral-3-14b-instruct-2512 |
| Reranking  | qwen3-reranker-0.6b           |

## Siemens API Resources

| Resource              | URL                                                                                      |
| --------------------- | -------------------------------------------------------------------------                |
| API Key Generation    |[my.siemens.com](https://my.siemens.com/#/main/keys)                                      |
| LLM API Documentation | [LLM API DOC](https://developer.internal.siemens.com/code-siemens-com/llm/overview.html) |

## Tech Stack

- Frontend : React with libraries for visualization (Recharts or Chart.js).
- Backend :  Python , FastAPI , Pandas Library
- Vector DB : ChromaDB  

## Getting Started

### Step 1 — Download datasets

| File                   | Source                                                                                                          | Save as                                  |
| ---------------------- | ------------------------------------------------------------------------------                                  | ---------------------------------------- |
| Global Power Plants    | [Kaggle -Global Power Plants](https://www.kaggle.com/datasets/ramjasmaurya/global-powerplants)                  | `backend/data/global_power_plants.csv`   |

<!-- https://www.kaggle.com/code/abdelazizelserty/global-power-plants-renewable-energy-data/input -->

### Step 2 - Create .env file

- create backend\.env

```
SIEMENS_API_KEY
SIEMENS_BASE_URL
EMBED_MODEL
LOCAL_EMBED_MODEL
RERANK_MODEL
LOCAL_RERANK_MODEL
TEXT_GENERATION_MODEL_ID
```

### Step 3 - Install Backend Dependencies
<!-- 
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
``` -->
    cd backend
    python -m venv venv
    .\venv\Scripts\Activate
    pip install -r requirements.txt

### Step 4 - Clean the Dataset

```bash
cd backend
python -m scripts.clean
```

reads `data\global_power_plant.csv` , removes the duplicates and missing values and gives `data\cleaned_dataset.csv`

### Step 5 - Generate Chunks

```bash
cd backend
python -m scripts.chunks
```

Splits the product description into chunks and saves into `data\Combined_data_with_Chunks.csv`

### Step 6 - Create the Embeddings and Insert into ChromaDB

```bash
cd backend
python -m scripts.embed

Reads recomputed chunks from `data\Combined_data_with_Chunks.csv` and generate the embeddings via the siemens API and stores them in `chroma_data\`

### Step 8 - Start the Backend

```bash
cd backend
uvicorn app.main:app --reload --port:8000
```

### Step 9 - Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

### Step 10 - Docker(Alternative to do steps 3 to 9)

```bash
docker-compose up --build
```

- backend : [http://localhost:8000](http://localhost:8000)
- frontend : [http://localhost:5173](http://localhost:5173)

----

## API Endpoints

| Method | Endpoint      | Description                            |
| ------ | ------------- | -------------------------------------- |
| GET    | `/health`     | Health check                           |
| POST   | `/api/query`  | RAG query — returns answer    |

### Chat

| Method | Endpoint                        | Description                                   |
| ------ | ------------------------------- | --------------------------------------------- |
| GET    | `/api/chat`                     | RAG Chat Application                          |

### Energy Dashboards

| Method | Endpoint                                  | Description                                   |
| ------ | -------------------------------           | --------------------------------------------- |
| GET    | `/dashboardpowerplant/energy-capacity`    | Top 20 countries by total capacity (MW)       |
| GET    | `/dashboardpowerplant/energy-trends`      | Capacity added per year (commissioning year)  |
| GET    | `/dashboardpowerplant/country-insights`   | Top 15 countries by total capacity            |
| GET    | `/dashboardpowerplant/energy-sources`     | Plant count by fuel type                      |

----

## Testing

```bash
cd backend
pytest
```
