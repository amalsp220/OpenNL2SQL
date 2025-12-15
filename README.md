# 🚀 OpenNL2SQL

<div align="center">

**AI-Powered Natural Language to SQL Analytics System**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io)

[Features](#-features) • [Architecture](#-architecture) • [Setup](#-quick-start) • [Security](#-security) • [Deployment](#-deployment)

</div>

---

## 📋 Overview

OpenNL2SQL transforms natural language questions into executable SQL queries using open-source LLMs via Groq API. Built with production-grade security, auto-recovery mechanisms, and a clean, professional UI.

**Perfect for:**
- Business analysts without SQL knowledge
- Data teams building internal analytics tools
- Developers learning NL2SQL systems
- Portfolio projects showcasing AI engineering skills

## ✨ Features

### 🧠 **AI-Powered Query Generation**
- Groq API with Mixtral-8x7B for accurate SQL generation
- Context-aware conversations with memory
- Supports complex queries with JOINs, aggregations, and filters

### 🛡️ **Enterprise-Grade Security**
- **SQL Injection Prevention**: Blocks dangerous keywords (DROP, DELETE, UPDATE, etc.)
- **Query Validation**: Only SELECT queries allowed
- **Row Limits**: Automatic LIMIT enforcement (max 1000 rows)
- **Timeout Protection**: Query execution timeouts
- **No Exposed Secrets**: Environment-based configuration

### 🔄 **Auto-Recovery System**
- Detects SQL execution errors
- Sends error feedback to LLM
- Regenerates corrected SQL automatically
- Retries once with improved query

### 🎨 **Professional UI**
- Clean, dashboard-style Streamlit interface
- Real-time loading indicators
- Expandable sections for SQL, explanations, and results
- Styled tables and error handling
- Mobile-responsive design

### 📊 **Analytics & Insights**
- Plain English explanations of SQL queries
- Natural language summaries of results
- Session-based conversation history

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Question                             │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │  Streamlit UI   │
              └────────┬────────┘
                       │ HTTP POST /query
                       ▼
         ┌─────────────────────────┐
         │   FastAPI Backend       │
         │  (main.py)              │
         └──────────┬──────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
  ┌─────────┐ ┌─────────┐ ┌─────────┐
  │ Schema  │ │ Memory  │ │  SQL    │
  │ Service │ │ Service │ │Validator│
  └─────────┘ └─────────┘ └─────────┘
        │           │           │
        └───────────┼───────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │   NL2SQL Service     │
         │   (Groq/Mixtral)     │
         └──────────┬───────────┘
                    │
                    ▼
              ┌──────────┐
              │Validation│
              └────┬─────┘
                   │
        ┌──────────┼──────────┐
        │  Valid   │  Invalid │
        ▼          ▼          │
   ┌─────────┐  Error ───────┘
   │Execute  │  Detection
   │  SQL    │      │
   └────┬────┘      │
        │           ▼
        │    ┌──────────────┐
        │    │Auto-Recovery │
        │    │ (Fix & Retry)│
        │    └──────┬───────┘
        │           │
        └───────────┼───────────┐
                    │           │
                    ▼           ▼
            ┌───────────┐ ┌──────────┐
            │Explanation│ │  Store   │
            │  Service  │ │  Memory  │
            └─────┬─────┘ └──────────┘
                  │
                  ▼
           Return Results
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Groq API Key ([Get it here](https://console.groq.com))
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/amalsp220/OpenNL2SQL.git
cd OpenNL2SQL
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
cd backend
pip install -r requirements.txt
cd ../frontend
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

5. **Run the backend**
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

6. **Run the frontend** (in a new terminal)
```bash
cd frontend
streamlit run streamlit_app.py
```

7. **Open your browser**
```
http://localhost:8501
```

## 📁 Project Structure

```
OpenNL2SQL/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application
│   │   ├── services/
│   │   │   ├── nl2sql_service.py   # LLM integration
│   │   │   ├── sql_validator.py    # Security layer
│   │   │   ├── query_executor.py   # SQL execution
│   │   │   ├── schema_service.py   # DB schema extraction
│   │   │   ├── explanation_service.py
│   │   │   └── memory_service.py   # Conversation context
│   │   ├── db/
│   │   │   └── database.py         # DB connection
│   │   └── security/
│   └── requirements.txt
├── frontend/
│   ├── streamlit_app.py            # Streamlit UI
│   └── requirements.txt
├── data/
│   └── sample.db                   # Sample SQLite DB
├── .env.example
├── docker-compose.yml
├── README.md
└── LICENSE
```

## 🔐 Security

### Built-in Protection

| Feature | Description |
|---------|-------------|
| **Keyword Blocking** | Blocks DROP, DELETE, UPDATE, INSERT, ALTER, etc. |
| **Query Type Restriction** | Only SELECT queries permitted |
| **Row Limiting** | Automatic LIMIT clause (max 1000 rows) |
| **Injection Prevention** | Sanitizes inputs, blocks SQL comments |
| **Timeout Protection** | Query execution timeouts |
| **Environment Secrets** | API keys in .env, never committed |

### Security Best Practices

```python
# ✅ Good - Using environment variables
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

# ❌ Bad - Hardcoding secrets
GROQ_API_KEY="gsk_xxxxx"  # Never do this!
```

## 🧪 Usage Examples

### Example Queries

**Simple Aggregation:**
```
"How many customers do we have?"
→ SELECT COUNT(*) FROM customers;
```

**Complex Join:**
```
"Show me the top 5 products by revenue this year"
→ SELECT p.name, SUM(oi.price * oi.quantity) as revenue
   FROM products p
   JOIN order_items oi ON p.id = oi.product_id
   JOIN orders o ON oi.order_id = o.id
   WHERE YEAR(o.created_at) = YEAR(CURRENT_DATE)
   GROUP BY p.id, p.name
   ORDER BY revenue DESC
   LIMIT 5;
```

**Follow-up Questions:**
```
User: "Show me all orders"
User: "Now filter only the ones from last month"
→ Context-aware: Uses conversation history
```

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access at http://localhost:8501
```

## ☁️ Deployment

### Streamlit Community Cloud (Frontend)

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy `frontend/streamlit_app.py`
4. Add `GROQ_API_KEY` in Secrets
5. Set `BACKEND_URL` to your backend API

### Render (Backend)

1. Create new Web Service on [Render](https://render.com)
2. Connect your GitHub repo
3. Set:
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variable: `GROQ_API_KEY`

### Railway (Alternative)

Similar setup to Render, use Railway's automatic deployment.

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI, Python 3.10+ |
| **Frontend** | Streamlit |
| **AI/LLM** | Groq API (Mixtral-8x7B) |
| **Database** | SQLite (demo), PostgreSQL (production-ready) |
| **ORM** | SQLAlchemy |
| **Validation** | Pydantic |
| **Deployment** | Docker, Render, Streamlit Cloud |

## 📊 API Endpoints

### `POST /query`
Process natural language query

**Request:**
```json
{
  "question": "How many users signed up last month?",
  "session_id": "optional-session-id",
  "db_path": "optional-custom-db-path"
}
```

**Response:**
```json
{
  "success": true,
  "sql": "SELECT COUNT(*) FROM users WHERE...",
  "results": [{"count": 150}],
  "sql_explanation": "This query counts users...",
  "results_explanation": "150 users signed up...",
  "session_id": "abc123"
}
```

### `GET /schema`
Get database schema

### `GET /sessions/{session_id}`
Retrieve conversation history

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 👤 Author

**Amal SP**
- GitHub: [@amalsp220](https://github.com/amalsp220)
- Portfolio: Building AI-powered applications

## 🙏 Acknowledgments

- [Groq](https://groq.com) for fast LLM inference
- [FastAPI](https://fastapi.tiangolo.com) for the excellent web framework
- [Streamlit](https://streamlit.io) for rapid UI development
- Open-source community
- 
## 🚀 Live Deployment

**Frontend (Streamlit):** [https://opennl2sql-tccpqxu3vocvgpn8zphunh.streamlit.app/](https://opennl2sql-tccpqxu3vocvgpn8zphunh.streamlit.app/)

The application is deployed on Streamlit Cloud and is ready to use! The frontend provides a clean, professional interface for:
- Converting natural language questions to SQL queries
- Viewing query history
- Configuring backend settings

### Deployment Architecture

```
┌─────────────────────────────────────────┐
│  Streamlit Cloud (Frontend)             │
│  https://opennl2sql-...streamlit.app/   │
│  - User Interface                       │
│  - Query Input                          │
│  - Results Display                      │
└────────────────┬────────────────────────┘
                 │
                 │ HTTP API Calls
                 ▼
┌─────────────────────────────────────────┐
│  Backend API (Optional)                 │
│  Deploy to: Render / Railway / Local   │
│  - FastAPI Server                       │
│  - Groq AI Integration                  │
│  - SQLite Database                      │
└─────────────────────────────────────────┘
```

### Deploy Your Own Instance

#### Option 1: Frontend Only (Streamlit Cloud)

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Deploy from your forked repo:
   - Repository: `your-username/OpenNL2SQL`
   - Branch: `main`
   - Main file path: `frontend/streamlit_app.py`
4. Add secrets in Streamlit Cloud dashboard:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```

#### Option 2: Full Stack Deployment

**Backend (Render/Railway):**

1. Create account on [Render](https://render.com/) or [Railway](https://railway.app/)
2. Create new Web Service
3. Connect your GitHub repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable:
   - `GROQ_API_KEY`: Your Groq API key
6. Deploy!

**Frontend (Streamlit Cloud):**

1. Follow Option 1 steps above
2. In Settings tab of deployed app, update Backend API URL to your deployed backend URL



## 🔮 Future Enhancements

- [ ] Support for PostgreSQL, MySQL, MongoDB
- [ ] Multi-table relationship auto-detection
- [ ] Query result visualization (charts/graphs)
- [ ] Export results to CSV/Excel
- [ ] User authentication & authorization
- [ ] Query history and favorites
- [ ] Custom AI model fine-tuning
- [ ] Real-time collaboration

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with ❤️ for the AI community

</div>
