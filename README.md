# 🔬 ResearchMind — Multi-Agent AI Research System

A multi-agent AI pipeline that automates end-to-end research report generation from a single topic query. Four specialized agents — **Search**, **Scrape**, **Write**, and **Critique** — collaborate to gather live information, extract deep content, draft a structured report, and score its quality.

Built with **LangChain**, **Mistral AI**, **Tavily Search**, and **Streamlit**.

---

## ✨ Features

- **Search Agent** — Queries the web via the Tavily Search API to gather recent, reliable sources on any topic.
- **Scrape Agent** — Extracts and cleans full-page content from the most relevant source using BeautifulSoup.
- **Writer Chain** — Synthesizes search and scraped data into a structured research report (Introduction, Key Findings, Conclusion, Sources).
- **Critic Chain** — Independently reviews the generated report, scoring it out of 10 with strengths and areas to improve.
- **Streamlit UI** — Interactive interface with live pipeline-stage tracking, expandable raw outputs, and a downloadable Markdown report.

---

## 🏗️ Architecture

```
Topic Input
    │
    ▼
┌─────────────┐     ┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│ Search Agent │ ──▶ │ Scrape Agent │ ──▶ │ Writer Chain │ ──▶ │ Critic Chain │
│  (Tavily)    │     │(BeautifulSoup)│    │  (Mistral)   │     │  (Mistral)   │
└─────────────┘     └─────────────┘     └──────────────┘     └──────────────┘
                                                │                     │
                                                ▼                     ▼
                                          Final Report          Quality Score
```

---

## 📁 Project Structure

```
.
├── app.py           # Streamlit UI
├── pipeline.py       # Core orchestration logic (CLI runnable)
├── agents.py          # Agent + chain definitions (search, scrape, writer, critic)
├── tools.py           # Custom LangChain tools (web_search, scrape_url)
├── requirements.txt   # Python dependencies
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Create a virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root:
```env
MISTRAL_API_KEY=your_mistral_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

---

## 🚀 Usage

### Run via CLI
```bash
python pipeline.py
```
You'll be prompted to enter a research topic, and the pipeline will print each stage's output to the console.

### Run via Streamlit UI
```bash
streamlit run app.py
```
Enter a topic, click **Run Research Pipeline**, and watch each agent complete its stage in real time. Download the final report as Markdown once ready.

---

## 🧠 Tech Stack

| Layer | Technology |
|---|---|
| LLM | Mistral AI (`mistral-medium-3-5`) |
| Agent Framework | LangChain (`create_agent`) |
| Web Search | Tavily Search API |
| Web Scraping | Requests + BeautifulSoup |
| UI | Streamlit |
| Env Management | python-dotenv |

---

## 📌 Notes

- The scraper relies on static HTML parsing; JavaScript-heavy pages may return limited content.
- API keys for Mistral and Tavily are required — both offer free tiers suitable for development and testing.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
