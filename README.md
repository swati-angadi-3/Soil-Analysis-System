#  Soil Analysis System

An intelligent soil analysis system that classifies soil strength based on pH, moisture, density, and organic content. The application recommends suitable construction or agricultural uses and generates AI-powered soil reports using LLaMA3 (via Ollama).

The project also includes an interactive Power BI dashboard for visualizing and exploring soil analysis data.

##  Features

### 1. Soil Analysis Application
- Soil strength classification (Strong / Moderate / Weak).
- Construction suitability recommendations.
- Agricultural suitability recommendations.
- AI-generated soil analysis reports.
- SQLite database for storing analysis inputs and outputs.
- Saved records view and CSV export.

### 2. Power BI Dashboard
- Interactive soil analysis dashboard.
- Data visualization and analysis.
- Visual representation of soil properties.
- Insights into soil strength classification.
- Analysis of pH, moisture, density, and organic content.

## 📊 Power BI Dashboard

The Power BI dashboard provides visual insights into soil properties and their classifications, helping users understand soil conditions through interactive visualizations.

**Dashboard Preview:**

Add your dashboard screenshot here.

`![Soil Analysis Dashboard](Dashboard.png)`

**Dashboard File:** `Soil-Analysis.pbix`

## 🛠️ Technologies Used

- Python
- Streamlit
- Microsoft Power BI
- Pandas
- Requests
- SQLite
- Ollama (LLaMA3)
- Data Visualization

## ⚙️ How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the AI model

```bash
ollama run llama3:8b
```

### 3. Start the Streamlit application

```bash
python -m streamlit run app.py
```

## 🗄️ Database

Analysis data is stored locally using SQLite.

- Database: `data/soil.db`
- Table: `soil_records`

The database stores soil analysis inputs and generated outputs.

##  Project Structure

```text
Soil-Analysis-System/
│
├── app.py
├── requirements.txt
├── data/
│   └── soil.db
│
├── Power-BI/
│   ├── Soil-Analysis.pbix
│   └── Dashboard.png
│
└── README.md
```

##  Project Objective

To combine AI-powered soil analysis with interactive data visualization, making soil assessment and decision-making more accessible and informative.

---

**Project:** Soil Analysis System  
**Tools:** Python | Streamlit | Power BI | SQLite | LLaMA3
