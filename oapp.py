# app.py
import streamlit as st
import numpy as np
import cv2
from PIL import Image
from detector import load_model, process_image
from pdf_generator import generate_pdf
from risk_map import RISK_MAP
from utils import image_to_array, start_webcam, release_webcam
from time import sleep

st.title("Wheelchair User Risk Assessment")

uploaded_file = st.file_uploader("Upload an Image for Risk Assessment", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    image_np = image_to_array(image)
    model = load_model()
    results = process_image(image_np, model)

    detected_risks = {}
    names = model.names

    for r in results:
        class_ids = r.boxes.cls.int().tolist()
        for class_id in class_ids:
            label = names[class_id]
            if label in RISK_MAP:
                detected_risks[label] = RISK_MAP[label]

    if detected_risks:
        st.write("Detected Risks:")
        for risk, details in detected_risks.items():
            st.write(f"- {risk.capitalize()} (Level: {details[0]})")
            for action in details[1]:
                st.write(f"  - {action}")

        pdf_report = generate_pdf(detected_risks)
        st.download_button("Download PDF Report", pdf_report, "wheelchair_risk_assessment_report.pdf", "application/pdf")
    else:
        st.write("No significant risks detected in the image.")

# Webcam section
if "webcam_active" not in st.session_state:
    st.session_state.webcam_active = False

def toggle_webcam():
    st.session_state.webcam_active = not st.session_state.webcam_active

btn_label = "Stop Webcam" if st.session_state.webcam_active else "Start Webcam"
st.button(btn_label, on_click=toggle_webcam)

if st.session_state.webcam_active:
    stframe = st.empty()
    cap = start_webcam()
    model = load_model()

    while st.session_state.webcam_active:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture image from webcam")
            break

        results = process_image(frame, model)
        annotated_frame = results[0].plot()
        frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame_rgb, channels="RGB", use_column_width=True)

        detected_risks = {}
        names = model.names

        for r in results:
            class_ids = r.boxes.cls.int().tolist()
            for class_id in class_ids:
                label = names[class_id]
                if label in RISK_MAP:
                    detected_risks[label] = RISK_MAP[label]

        if detected_risks:
            pdf_report = generate_pdf(detected_risks)
            st.download_button("Download PDF Report", pdf_report, "wheelchair_risk_assessment_report.pdf", "application/pdf")

        sleep(0.1)

    release_webcam(cap)
    stframe.empty()
