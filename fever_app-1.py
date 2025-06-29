import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="Fever Diagnosis Assistant", layout="centered")

st.title("🩺 Comprehensive Fever Diagnosis")
st.subheader("Enter patient's symptoms, severity and duration:")

def symptom_input(name):
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        present = st.checkbox(name)
    with col2:
        severity = st.selectbox(f"{name} Severity", ["Mild", "Moderate", "Severe"], key=f"sev_{name}") if present else None
    with col3:
        duration = st.number_input(f"{name} Days", min_value=0, max_value=30, step=1, key=f"dur_{name}") if present else None
    return {"present": present, "severity": severity, "duration": duration}

symptom_data = {
    "Fever": symptom_input("Fever"),
    "Body pain": symptom_input("Body pain"),
    "Rash": symptom_input("Rash"),
    "Chills": symptom_input("Chills"),
    "Sweating": symptom_input("Sweating"),
    "Abdominal pain": symptom_input("Abdominal pain"),
    "Diarrhea": symptom_input("Diarrhea"),
    "Cough": symptom_input("Cough"),
    "Breathlessness": symptom_input("Breathlessness"),
    "Burning micturition": symptom_input("Burning micturition")
}

diagnosis = set()
investigations = set()

def has(symptom):
    return symptom_data[symptom]["present"]

if has("Body pain") and has("Rash"):
    if symptom_data["Fever"]["severity"] in ["Moderate", "Severe"]:
        diagnosis.update(["Dengue", "Chikungunya"])
        investigations.update(["CBC", "Dengue NS1", "Dengue IgM"])

if has("Chills") and has("Sweating"):
    if symptom_data["Fever"]["duration"] and symptom_data["Fever"]["duration"] >= 2:
        diagnosis.add("Malaria")
        investigations.update(["CBC", "Peripheral smear", "Rapid Malaria Test"])

if has("Abdominal pain") and has("Diarrhea"):
    diagnosis.update(["Typhoid", "Gastroenteritis"])
    investigations.update(["CBC", "Widal test", "Stool culture"])

if has("Cough") and has("Breathlessness"):
    diagnosis.update(["COVID-19", "Pneumonia", "Tuberculosis"])
    investigations.update(["CBC", "Chest X-ray", "RT-PCR", "Sputum AFB"])

if has("Burning micturition"):
    if symptom_data["Burning micturition"]["severity"] == "Severe":
        diagnosis.add("Urinary Tract Infection")
        investigations.update(["Urine routine", "Urine culture"])

red_flags = []
if has("Breathlessness") and symptom_data["Breathlessness"]["severity"] == "Severe":
    red_flags.append("Severe breathlessness")
if has("Burning micturition") and symptom_data["Burning micturition"]["severity"] == "Severe":
    red_flags.append("Suspected UTI with severe symptoms")
if has("Fever") and symptom_data["Fever"]["duration"] and symptom_data["Fever"]["duration"] >= 7:
    red_flags.append("Fever >7 days – prolonged febrile illness")

if red_flags:
    st.markdown("### 🚨 Red Flags")
    for flag in red_flags:
        st.error(f"⚠️ {flag}")
else:
    st.success("No critical red flags identified based on input.")

if any([s["present"] for s in symptom_data.values()]):
    st.markdown("### 🧾 Possible Differential Diagnosis:")
    for d in diagnosis:
        st.write(f"• {d}")

    st.markdown("### 🧪 Suggested Investigations:")
    for inv in investigations:
        st.write(f"• {inv}")
else:
    st.info("Please select symptoms to get diagnosis suggestions.")

if st.button("Generate Summary Report"):
    st.markdown("### 🧾 Patient Summary Report")
    with st.expander("View full report"):
        st.write("**Date:**", datetime.date.today())
        st.write("**Symptoms:**")
        for k, v in symptom_data.items():
            if v["present"]:
                st.write(f"- {k}: {v['severity']}, for {v['duration']} days")

        st.write("**Possible Diagnoses:**")
        for d in diagnosis:
            st.write(f"- {d}")

        st.write("**Recommended Investigations:**")
        for i in investigations:
            st.write(f"- {i}")

        if red_flags:
            st.write("**Red Flags:**")
            for r in red_flags:
                st.write(f"- ⚠️ {r}")
        else:
            st.write("**Red Flags:** None")

if st.button("Download Report as PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Fever Diagnostic Summary", ln=True, align="C")
    pdf.cell(200, 10, txt=str(datetime.date.today()), ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Symptoms:", ln=True)
    for k, v in symptom_data.items():
        if v["present"]:
            pdf.cell(200, 10, txt=f"- {k}: {v['severity']}, {v['duration']} days", ln=True)

    pdf.cell(200, 10, txt="Diagnoses:", ln=True)
    for d in diagnosis:
        pdf.cell(200, 10, txt=f"- {d}", ln=True)

    pdf.cell(200, 10, txt="Investigations:", ln=True)
    for inv in investigations:
        pdf.cell(200, 10, txt=f"- {inv}", ln=True)

    if red_flags:
        pdf.cell(200, 10, txt="Red Flags:", ln=True)
        for r in red_flags:
            pdf.cell(200, 10, txt=f"- ⚠️ {r}", ln=True)

    pdf.output("fever_summary_report.pdf")
    st.success("PDF saved as 'fever_summary_report.pdf' in your folder.")

