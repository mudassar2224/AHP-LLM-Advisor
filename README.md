# 🧠 AHP LLM Advisor Chatbot

A beautiful Streamlit chatbot that uses **Analytic Hierarchy Process (AHP)**  
to recommend the best LLM for any user task — powered by **Groq** fast inference.

---

## 📁 Folder Structure

```
ahp_llm_chatbot/
├── app.py                        ← Main Streamlit app (run this)
├── config.py                     ← API keys & settings
├── requirements.txt
├── .gitignore
├── .streamlit/
│   └── config.toml               ← Theme & server settings
├── assets/
│   └── avatar.png                ← YOUR profile photo (already placed)
├── data/
│   ├── llm_master_dataset.csv    ← 50 LLMs × 52 columns
│   └── keyword_capability_map.csv← 217 keywords → capability weights
├── core/
│   ├── ahp_engine.py             ← AHP pairwise matrix scoring
│   ├── keyword_detector.py       ← Keyword → capability weight mapping
│   ├── rag_engine.py             ← Dataset loader + context formatter
│   └── groq_client.py            ← Groq API (streaming)
└── ui/
    └── styles.py                 ← All CSS for beautiful UI
```

---

## 🚀 Local Setup (Windows / Mac / Linux)

### Step 1 — Clone or unzip the project
```bash
cd ahp_llm_chatbot
```

### Step 2 — Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the app
```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## ☁️ Deploy to Streamlit Cloud

1. Push the whole folder to a **GitHub repo**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo → set `app.py` as entry point
4. Under **Advanced settings → Secrets**, add:
   ```toml
   GROQ_API_KEY = ""
   ```
5. Click **Deploy** 🎉

> ⚠️ **Security tip:** Never commit your API key to GitHub.  
> Always use Streamlit Secrets or environment variables for deployment.

---

## 🔑 Changing the API Key

Edit `config.py`:
```python
GROQ_API_KEY = "your_new_key_here"
```

Or set an environment variable:
```bash
export GROQ_API_KEY="your_new_key_here"   # Mac/Linux
set GROQ_API_KEY=your_new_key_here         # Windows
```

---

## 🧠 How AHP Works (for viva)

| Step | What happens |
|------|-------------|
| 1 | User types a prompt |
| 2 | 217 keywords scanned → capability weights extracted |
| 3 | Domain classified (banking, coding, video, etc.) |
| 4 | AHP pairwise matrix loaded for that domain |
| 5 | Criterion weights computed (Performance / Cost / Safety / Domain Fit) |
| 6 | Every model scored → ranked by AHP score |
| 7 | Top 5 models sent as context to Groq |
| 8 | Groq streams a beautiful natural language response |

---

## 📊 Dataset Overview

| File | Contents |
|------|----------|
| `llm_master_dataset.csv` | 50 LLMs × 52 columns (20 capability scores + cost + safety + arena benchmarks) |
| `keyword_capability_map.csv` | 217 keywords mapping to capability weight vectors |

---

## 🛠️ Tech Stack

- **Streamlit** — Web UI
- **Groq** — Ultra-fast LLM inference (llama-3.3-70b-versatile)
- **AHP** — Analytic Hierarchy Process (Saaty 1980) for multi-criteria decisions
- **Pandas** — Dataset management
- **Pure Python** — No heavy dependencies (no chromadb, no langchain)

---

## 💬 Example Prompts to Try

- *"I want to make a YouTube channel and Pinterest posts"*
- *"Build a banking app with fraud detection"*
- *"Create an e-commerce store for my clothing brand"*
- *"I need a cheap LLM for a student tutoring chatbot"*
- *"Build a medical diagnosis assistant"*
- *"Make a multilingual customer support bot"*
- *"I want to generate code for a REST API"*
