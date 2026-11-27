import streamlit as st

from ai_report import generate_report_stream
from database import (
    delete_record,
    fetch_records,
    init_db,
    insert_record,
    update_report,
)
from soil_analysis import analyze_soil

st.set_page_config(page_title="Soil Analysis System", layout="wide")
init_db()

STRENGTH_COLORS = {"Strong": "#4f7a3a", "Moderate": "#b8862b", "Weak": "#a5472f"}

CSS = """<style>
#MainMenu, footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}
.block-container {padding-top: 1.2rem; max-width: 1150px;}
h1, h2, h3 {font-family: Georgia, 'Times New Roman', serif; color: #3b2a1c;}
.masthead {background: #4a3322; color: #f4efe4; padding: 22px 28px; border-bottom: 4px solid #8a6a43; margin-bottom: 18px;}
.masthead h1 {color: #f4efe4; margin: 0; font-size: 1.9rem; letter-spacing: 0.3px;}
.masthead p {margin: 4px 0 0 0; color: #d9ccb4; font-size: 0.92rem;}
.sheet {background: #fbf8f0; border: 1px solid #cdbfa5; padding: 18px 20px;}
.sheet-head {display: flex; justify-content: space-between; align-items: center; font-family: Georgia, serif; font-size: 1.05rem; color: #3b2a1c; border-bottom: 1px solid #cdbfa5; padding-bottom: 10px; margin-bottom: 10px;}
.stamp {color: #fff; padding: 3px 12px; font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase;}
.usage {font-size: 1.02rem; margin: 6px 0 16px 0; color: #2e2a24;}
.row {display: flex; justify-content: space-between; font-size: 0.9rem; margin-top: 12px;}
.lbl {color: #6b5a47;}
.val {font-family: Consolas, 'Courier New', monospace; color: #2e2a24;}
.track {height: 7px; background: #e4dac6; margin-top: 4px;}
.fill {height: 7px; background: #7a5b3a;}
.phscale {position: relative; height: 10px; margin-top: 6px; background: linear-gradient(to right, #c0392b, #e67e22, #f1c40f, #7cb342, #2e9d6a, #2b7bb9, #5b4a9e);}
.phmark {position: absolute; top: -4px; width: 3px; height: 18px; background: #1f1a14;}
.phlabels {display: flex; justify-content: space-between; font-size: 0.72rem; color: #8a7a66; margin-top: 4px;}
.placeholder {border: 1px dashed #b9a98c; padding: 40px 20px; text-align: center; color: #8a7a66;}
div.stButton > button, div[data-testid="stFormSubmitButton"] > button {background: #5a3e2b; color: #f4efe4; border: none; border-radius: 2px; padding: 0.5rem 1.4rem;}
div.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {background: #3f2b1d; color: #fff;}
</style>"""
st.markdown(CSS, unsafe_allow_html=True)

st.markdown(
    '<div class="masthead"><h1>Soil Analysis System</h1>'
    "<p>Soil strength classification and land-use suitability from sample readings</p></div>",
    unsafe_allow_html=True,
)


def ph_note(ph):
    if ph < 6.5:
        return "acidic"
    if ph <= 7.5:
        return "near neutral"
    return "alkaline"


def bar_row(label, value_text, pct):
    pct = max(0, min(100, pct))
    return (
        f'<div class="row"><span class="lbl">{label}</span>'
        f'<span class="val">{value_text}</span></div>'
        f'<div class="track"><div class="fill" style="width:{pct}%"></div></div>'
    )


def result_sheet(r):
    color = STRENGTH_COLORS.get(r["strength"], "#7a5b3a")
    ph_pos = max(0, min(100, r["ph"] / 14 * 100))
    return (
        '<div class="sheet">'
        f'<div class="sheet-head"><span>Sample no. {r["id"]}</span>'
        f'<span class="stamp" style="background:{color}">{r["strength"]}</span></div>'
        f'<div class="usage">{r["usage"]}</div>'
        f'<div class="row"><span class="lbl">Soil pH</span>'
        f'<span class="val">{r["ph"]:.1f} ({ph_note(r["ph"])})</span></div>'
        f'<div class="phscale"><div class="phmark" style="left:{ph_pos}%"></div></div>'
        '<div class="phlabels"><span>0 acidic</span><span>7</span><span>14 alkaline</span></div>'
        + bar_row("Moisture content", f'{r["moisture"]:.1f} %', r["moisture"])
        + bar_row("Bulk density", f'{r["density"]:.2f} g/cm³', r["density"] / 2.5 * 100)
        + bar_row("Organic matter", f'{r["organic"]:.1f} %', r["organic"])
        + "</div>"
    )


tab_new, tab_log = st.tabs(["Analysis", "Sample log"])

# ---------------- Analysis ----------------
with tab_new:
    left, right = st.columns([1, 1.25], gap="large")

    with left:
        with st.form("soil_form"):
            st.subheader("Sample readings")
            ph = st.number_input(
                "Soil pH (0 to 14)", min_value=0.0, max_value=14.0, value=6.5, step=0.1
            )
            moisture = st.number_input(
                "Moisture content (%)", min_value=0.0, max_value=100.0, value=30.0, step=0.5
            )
            density = st.number_input(
                "Bulk density (g/cm³)", min_value=0.1, max_value=3.0, value=1.5, step=0.05
            )
            organic = st.number_input(
                "Organic matter (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.5
            )
            want_report = st.checkbox("Write AI report (takes longer)", value=True)
            submitted = st.form_submit_button("Analyze sample")

    if submitted:
        strength, usage = analyze_soil(ph, moisture, density, organic)
        record_id = insert_record(ph, moisture, density, organic, strength, usage)
        st.session_state["last"] = {
            "id": record_id,
            "ph": ph,
            "moisture": moisture,
            "density": density,
            "organic": organic,
            "strength": strength,
            "usage": usage,
            "report": None,
        }

    last = st.session_state.get("last")

    with right:
        if last:
            st.markdown(result_sheet(last), unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="placeholder">Enter the sample readings and press '
                "Analyze sample.<br>The result will appear here.</div>",
                unsafe_allow_html=True,
            )

    if last:
        st.subheader("Written report")
        if submitted and want_report:
            try:
                text = st.write_stream(
                    generate_report_stream(
                        last["ph"], last["moisture"], last["density"],
                        last["organic"], last["strength"], last["usage"],
                    )
                )
                last["report"] = text
                update_report(last["id"], text)
            except Exception:
                st.warning(
                    "Could not reach Ollama, so no report was written. "
                    "Start it with `ollama run llama3:8b` and analyze again. "
                    "The readings and classification are already saved."
                )
        elif last["report"]:
            st.markdown(last["report"])
        else:
            st.caption("No written report for this sample.")

# ---------------- Sample log ----------------
with tab_log:
    st.subheader("Sample log")
    records = fetch_records()

    if records.empty:
        st.info("No samples recorded yet.")
    else:
        table = records.drop(columns=["report"]).rename(
            columns={
                "id": "No.",
                "created_at": "Date (UTC)",
                "ph": "pH",
                "moisture": "Moisture (%)",
                "density": "Density (g/cm³)",
                "organic": "Organic (%)",
                "strength": "Strength",
                "usage": "Usage",
            }
        )
        st.dataframe(table, use_container_width=True, hide_index=True)

        st.download_button(
            "Download log as CSV",
            data=table.to_csv(index=False).encode("utf-8"),
            file_name="soil_samples.csv",
            mime="text/csv",
        )

        st.divider()
        selected = st.selectbox("Open report for sample no.", records["id"].tolist())
        row = records[records["id"] == selected].iloc[0]
        st.markdown(row["report"] if row["report"] else "No report saved for this sample.")

        if st.button("Delete this sample"):
            delete_record(int(selected))
            st.rerun()