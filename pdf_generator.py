from fpdf import FPDF
from risk_map import RISK_MAP
from io import BytesIO

def generate_pdf(detected_risks):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Wheelchair User Risk Assessment Report", ln=True, align="C")
    pdf.ln(10)

    for risk, details in detected_risks.items():
        risk_level, actions = RISK_MAP.get(risk, ("Unknown", []))
        pdf.cell(200, 10, txt=f"Risk: {risk.capitalize()} - Level: {risk_level}", ln=True)
        for action in actions:
            pdf.cell(200, 10, txt=f"  - {action}", ln=True)
        pdf.ln(5)

    # Instead of writing to buffer, get PDF as string bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')

    buffer = BytesIO(pdf_bytes)
    buffer.seek(0)
    return buffer

