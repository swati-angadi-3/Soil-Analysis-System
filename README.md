# Soil Analysis System

A Streamlit application that classifies soil strength from pH, moisture,
density and organic content, recommends construction or agricultural use,
and generates a written report using LLaMA3 (via Ollama). Every analysis
(inputs and outputs) is stored in a local SQLite database.

## Features
- Soil strength classification (Strong / Moderate / Weak)
- Construction and agriculture suitability
- AI-written soil report
- SQLite storage with a saved-records view and CSV export

## Technologies
Python, Streamlit, Pandas, Requests, SQLite, Ollama (LLaMA3)

## Run
    pip install -r requirements.txt
    ollama run llama3:8b
    python -m streamlit run app.py

Data is saved in `data/soil.db`, table `soil_records`.