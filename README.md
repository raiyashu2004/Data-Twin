# Personal Data Twin 🧠

An AI-powered full-stack application that creates a **digital twin** of your daily behaviour — tracking, analysing, predicting, and optimising your personal productivity and lifestyle.

---

## ✨ Features

| Module | Description |
|---|---|
| 📥 **Data Collection** | Manual entry or CSV upload of daily behavioural data |
| 📊 **Analytics** | Weekly summaries, correlation heatmaps, trend charts |
| 🧠 **ML Models** | Behaviour clustering, productivity prediction, burnout risk, time-series forecasting |
| 🤖 **AI Insights** | Natural-language Q&A powered by OpenAI GPT |
| 🔮 **Simulation** | "What-if" scenario engine to test habit changes |

---

## 🏗️ Project Structure

```
Data-Twin/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   ├── data.py          # Data collection routes
│   │   ├── insights.py      # AI insights routes
│   │   └── simulation.py    # Simulation routes
│   ├── models/
│   │   └── schemas.py       # Pydantic request/response schemas
│   ├── services/
│   │   ├── data_service.py       # In-memory data store (swap with DB)
│   │   ├── analytics_service.py  # Statistical summaries
│   │   └── simulation_service.py # What-if engine
│   ├── ml/
│   │   ├── clustering.py    # K-Means behaviour clustering
│   │   ├── prediction.py    # Random Forest productivity / burnout
│   │   └── forecasting.py   # Linear regression time-series forecast
│   └── ai/
│       └── insight_engine.py  # OpenAI GPT integration
├── frontend/
│   ├── app.py               # Streamlit dashboard entry point
│   └── components/
│       ├── overview.py      # Overview & data entry panel
│       ├── trends.py        # Trend analysis panel
│       ├── simulation.py    # Simulation panel
│       └── ai_insights.py   # AI insights panel
├── data/
│   ├── sample_data.csv      # Example dataset
│   └── db_connection.py     # PostgreSQL/Supabase scaffolding
└── requirements.txt
```

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI backend

```bash
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

### 3. Start the Streamlit frontend

In a separate terminal:

```bash
streamlit run frontend/app.py
```

The dashboard will open at `http://localhost:8501`.

---

## ⚙️ Configuration

| Variable | Description | Required |
|---|---|---|
| `OPENAI_API_KEY` | OpenAI API key for AI insights | Optional |
| `DATABASE_URL` | PostgreSQL connection string | Optional (defaults to in-memory store) |

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://user:password@localhost:5432/datatwin
```

---

## 📊 Sample Data

A sample CSV is provided at `data/sample_data.csv`.  
Upload it via the **Overview → Upload CSV** section of the dashboard.

Required CSV columns:

| Column | Type | Description |
|---|---|---|
| `entry_date` | YYYY-MM-DD | Date of the entry |
| `screen_time_hours` | float | Daily screen time in hours |
| `study_hours` | float | Hours of study/work |
| `sleep_hours` | float | Hours of sleep |
| `exercise_minutes` | float | Minutes of exercise (optional) |
| `expenses` | float | Daily expenses (optional) |
| `notes` | string | Free-text notes (optional) |

---

## 🛠️ Technology Stack

- **Backend**: FastAPI + Uvicorn
- **Frontend**: Streamlit + Plotly
- **ML**: scikit-learn, pandas, NumPy
- **AI**: OpenAI GPT API
- **Database**: PostgreSQL / Supabase (SQLAlchemy ORM)

---

## 🔮 Future Scope

- Wearable device integration (smartwatch data)
- Real-time data streaming
- Reinforcement learning for habit optimisation
- Mobile app version
- Social comparison features