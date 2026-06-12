import os
import streamlit as st
import pandas as pd
import os
from soil_analysis import analyze_soil
from ai_report import generate_report

st.title("🌱 Soil Analysis System")

ph = st.number_input("Enter pH value")
moisture = st.number_input("Enter Moisture (%)")
density = st.number_input("Enter Density")
organic = st.number_input("Enter Organic Content (%)")

if st.button("Analyze Soil"):

    strength, usage = analyze_soil(ph, moisture, density, organic)
    report = generate_report(ph, moisture, density, organic, strength, usage)

    st.write("Strength:", strength)
    st.write("Usage:", usage)
    st.write(report)

    # ✅ DEFINE FILE PATH
    file_path = "output/report.csv"

    # ✅ CREATE FOLDER IF NOT EXISTS
    os.makedirs("output", exist_ok=True)

    # ✅ CREATE DATAFRAME
    data = pd.DataFrame({
        "pH": [ph],
        "Moisture": [moisture],
        "Density": [density],
        "Organic": [organic],
        "Strength": [strength],
        "Usage": [usage]
    })

    # ✅ APPEND LOGIC
    if os.path.exists(file_path):
        data.to_csv(file_path, mode='a', header=False, index=False)
    else:
        data.to_csv(file_path, mode='w', header=True, index=False)



# OUTPUT ollama run llama3
# OUTPUT python -m streamlit run app.py
