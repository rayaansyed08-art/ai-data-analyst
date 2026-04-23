# ai-data-analyst

AI Data Analyst using LLMs and RAG. This system helps users analyze data using simple questions.

---

## Overview

In this project, users can upload a dataset (CSV file) and ask questions in natural language.

The system understands the data and gives answers, insights, and charts.

---

## Features

* Upload CSV file
* Ask questions in simple English
* Get answers from data
* Generate charts automatically
* Memory for conversation
* Safe responses using guardrails

---

## AI Working (RAG)

This system uses Retrieval-Augmented Generation (RAG) to improve accuracy.

* User queries are matched with dataset
* Relevant data is retrieved using FAISS
* LLM generates answers based on context
* Guardrails ensure safe output

This makes the system more reliable than normal LLM responses.

---

## Tech Used

* Python
* Streamlit
* LangChain
* FAISS
* Pandas
* Matplotlib

---

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run app:

```bash
streamlit run app.py
```

---

## Project Files

* app.py → main app
* agent.py → AI logic
* rag.py → retrieval system
* guardrails.py → safety checks
* report.pdf → project report
* grandma.md → simple explanation

---

## Author

Syed Rayaan

---

## Course

Generative AI and Large Language Models
