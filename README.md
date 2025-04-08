# Generative-AI-powered-recommender-system 

A Generative AI-powered system that recommends the **most relevant SHL assessments** based on job descriptions or job roles. This project combines NLP, semantic search, web scraping, and a beautiful Streamlit UI to create a smart HR tool! 💼✨

---

## 📁 Project Structure 
📦 SHL-Assessment-Recommender/ ├── json_data/ # 📂 Contains scraped SHL assessments in JSON format ├── embeder.py # 🧠 Embeds assessment data & computes cosine similarity ├── evaluate.py # 📈 Evaluation logic using Recall@5 and MAP@5 ├── test_eval.py # 🧪 Unit tests for evaluation ├── scraper.py # 🌐 Web scraper to extract assessment info from SHL ├── streamlit_app.py # 🌟 Streamlit UI for user interaction ├── final_report.pdf # 📝 Final project report (formatted and visual) ├── SHL_Assessment_recommendation_Evaluarion.pdf # 📊 Evaluation insights PDF └── README.md # 📘 Project documentation (this file!) 


---

## 🚀 Features

- 🔎 **Semantic Search**: Uses Sentence Transformers (MiniLM) + cosine similarity
- 🧠 **Smart Matching**: Recommends best-fit assessments for job roles/JDs
- 📊 **Evaluation Metrics**: Recall@5 and MAP@5 for measuring accuracy
- 🌐 **Live Streamlit App**: Clean UI to input and view results
- 🧹 **Web Scraping**: Automatically pulls SHL assessments from the website
- 📄 **PDF Report**: Final report included with detailed walkthrough

---

## ⚙️ How It Works

1. **Data Scraping**  
   `scraper.py` extracts SHL assessment catalog → stores it as JSON (`json_data/`)

2. **Embedding Generation**  
   `embeder.py` creates sentence embeddings and matches them with cosine similarity

3. **User Input Matching**  
   `streamlit_app.py` allows users to enter job role or JD → recommends top 5 assessments

4. **Evaluation**  
   `evaluate.py` + `test_eval.py` validate performance with metrics

5. **Reporting**  
   `final_report.pdf` and `SHL_Assessment_recommendation_Evaluarion.pdf` provide complete insight

---

## 🧪 Sample Results

- Query: `"Manage cash register"`  
  → Top Match: `"Cashier Solution"` ✅

- Evaluation:  
  - **Recall@5**: `1.0`  
  - **MAP@5**: `1.0`  
  ✅ 100% relevant top recommendations!

---

## 📦 Installation

```bash
git clone https://github.com/your-username/shl-assessment-recommender.git
cd shl-assessment-recommender
pip install -r requirements.txt
