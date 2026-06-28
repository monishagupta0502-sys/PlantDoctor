import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import os
import time
from datetime import datetime

from disease_info import DISEASE_INFO
from utils.auth import save_scan

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PlantDoctor AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# LOAD CSS
# ============================================================

def load_css():
    from utils.auth import create_database

    create_database()
    if os.path.exists("style.css"):

        with open("style.css") as css:

            st.markdown(
                f"<style>{css.read()}</style>",
                unsafe_allow_html=True
            )

load_css()

# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    model = tf.keras.models.load_model(
    "models/best_plant_disease_model.keras"
)
    return model

model = load_model()

# ============================================================
# LOAD CLASS NAMES
# ============================================================

with open("models/class_names.json", "r") as f:

    class_names = json.load(f)

# ============================================================
# IMAGE PREPROCESSING
# ============================================================

def preprocess_image(image):

    image = image.convert("RGB")

    image = image.resize((224,224))

    image = np.array(image)

    image = image.astype(np.float32)

    image = image / 255.0

    image = np.expand_dims(image,axis=0)

    return image

# ============================================================
# PREDICTION
# ============================================================

def predict(image):

    processed = preprocess_image(image)

    prediction = model.predict(
        processed,
        verbose=0
    )[0]

    predicted_index = np.argmax(prediction)

    confidence = prediction[predicted_index]

    disease = class_names[predicted_index]

    top3 = np.argsort(prediction)[::-1][:3]

    return disease,confidence,prediction,top3

# ============================================================
# SIDEBAR
# ============================================================

def show_sidebar():

    with st.sidebar:

        st.title("🌿 PlantDoctor AI")

        st.markdown(
            "### Deep Learning Powered Plant Disease Detection"
        )

        st.divider()

        st.metric(
            "Model Accuracy",
            "92.14%"
        )

        st.metric(
            "Dataset Classes",
            "38"
        )

        st.metric(
            "Framework",
            "TensorFlow"
        )

        st.metric(
            "Architecture",
            "MobileNetV2"
        )

        st.divider()

        st.success("✅ AI Model Loaded")

        st.info(
            """
Upload a plant leaf image to detect diseases instantly using Artificial Intelligence.
"""
        )

        st.divider()

        st.caption("Version 2.0")

# ============================================================
# HEADER
# ============================================================

def show_header():

    st.markdown("""
<div style="
padding:35px;
background:#F8FFF8;
border:2px solid #A5D6A7;
border-radius:20px;
box-shadow:0px 10px 25px rgba(0,0,0,0.08);
text-align:center;
">

<h1 style="color:#1B5E20;margin-bottom:10px;">
🌿 PlantDoctor AI
</h1>

<h3 style="color:#2E7D32;">
Deep Learning Powered Plant Disease Detection
</h3>

<p style="color:#4CAF50;font-size:18px;">
Upload • Analyze • Diagnose • Treat
</p>

</div>
""", unsafe_allow_html=True)

    st.write("")

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric("🎯 Accuracy", "92.14%")
    metric2.metric("🦠 Diseases", "38")
    metric3.metric("🤖 Framework", "TensorFlow")
    metric4.metric("🧠 Model", "MobileNetV2")

    st.divider()
show_sidebar()
show_header()

# ============================================================
# MAIN LAYOUT
# ============================================================
def show_upload_section():

    st.markdown("""
<div class="section-title">

📤 Upload Leaf Image

</div>
""", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Supported formats: JPG, JPEG, PNG",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Uploaded Leaf",
            use_container_width=True
        )

        st.markdown("---")

        st.info("""
### 📌 Tips for Best Prediction

• Upload one leaf only

• Use a plain background

• Ensure good lighting

• Avoid blurry images

• Keep the leaf centered
""")

    return uploaded_file
left_col, right_col = st.columns([1, 1.25], gap="large")

with left_col:

    st.markdown("""
    <div class="section-title">

     📤 Upload Leaf Image

     </div>
"""
                , unsafe_allow_html=True) 
    uploaded_file = st.file_uploader(
        "Supported formats: JPG, JPEG, PNG",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Uploaded Leaf",
            use_container_width=True
        )

        st.markdown("---")

        st.info("""
### 📌 Tips for Best Prediction

• Upload one leaf only

• Use a plain background

• Ensure good lighting

• Avoid blurry images

• Keep the leaf centered
""")

with right_col:

    st.markdown("""
<div class="section-title">

🤖 AI Diagnosis

</div>
""", unsafe_allow_html=True)
if uploaded_file is None:

    st.warning(
        "Please upload a leaf image to begin prediction."
    )

else:

    with st.spinner("Analyzing image using AI..."):

        start_time = time.time()

        disease, confidence, prediction, top3 = predict(image)

        end_time = time.time()

        prediction_time = end_time - start_time

    # ============================================================
    # PREPARE RESULT
    # ============================================================

    plant = disease.split("___")[0].replace("_", " ")

    disease_name = disease.split("___")[1].replace("_", " ")

    # ============================================================
    # SAVE SCAN TO DATABASE
    # ============================================================

    if st.session_state.get("logged_in", False):

        save_scan(

            st.session_state["username"],

            plant,

            disease_name,

            float(confidence),

            float(prediction_time),

            datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        )
    else:
    # ============================================================
    # SHOW RESULT CARDS
    # ============================================================

     st.markdown("## 🌿 Prediction Result")

     st.markdown("### 🌱 Plant")
     st.success(plant)

     st.markdown("### 🦠 Disease")
     st.error(disease_name)

     st.markdown("### 🎯 Confidence")

     st.progress(float(confidence))

st.write(f"### {confidence*100:.2f}%")

st.divider()
if uploaded_file is not None:

    st.divider()

    st.markdown("## 🏆 Top Predictions")

    medals = ["🥇", "🥈", "🥉"]
    for i, idx in enumerate(top3):

        probability = float(prediction[idx])

        disease_label = (
            class_names[idx]
            .replace("___", " → ")
            .replace("_", " ")
        )

        st.markdown(f"### {medals[i]} {disease_label}")

        st.progress(probability)

        st.caption(f"{probability*100:.2f}% Confidence")

st.divider()
# ============================================================
# DISEASE INFORMATION
# ============================================================

if uploaded_file is not None:

    info = DISEASE_INFO.get(
        disease,
        {
            "description": "Information unavailable.",
            "symptoms": "-",
            "treatment": "-",
            "prevention": "-",
            "severity": "Unknown"
        }
    )

    st.markdown("## 📖 Disease Information")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(f"""
<div class="card">
<h3>📝 Description</h3>
<p>{info["description"]}</p>
</div>
""", unsafe_allow_html=True)

        st.markdown(f"""
<div class="card">
<h3>🔍 Symptoms</h3>
<p>{info["symptoms"]}</p>
</div>
""", unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
<div class="card">
<h3>💊 Treatment</h3>
<p>{info["treatment"]}</p>
</div>
""", unsafe_allow_html=True)

        st.markdown(f"""
<div class="card">
<h3>🛡 Prevention</h3>
<p>{info["prevention"]}</p>
</div>
""", unsafe_allow_html=True)

    # ============================================================
    # PLANT STATUS
    # ============================================================

    st.markdown("---")

    st.markdown("## 🌱 Plant Status")

    if "healthy" in disease.lower():

        st.success("✅ Healthy Plant")

# ============================================================
# DISEASE SEVERITY
# ============================================================

if uploaded_file is not None:

    st.markdown("## ⚠ Disease Severity")

    severity = info.get("severity", "Unknown")

    colors = {
        "Low": "#43A047",
        "Medium": "#FB8C00",
        "High": "#E53935"
    }

    color = colors.get(severity, "#757575")

    st.markdown(
        f"""
<div style="
padding:20px;
border-radius:15px;
background:{color};
color:white;
text-align:center;
font-size:24px;
font-weight:bold;">
{severity} Severity
</div>
""",
        unsafe_allow_html=True
    )

    # ============================================================
    # DOWNLOAD DIAGNOSIS REPORT
    # ============================================================

    report = f"""
=========================================================
                PlantDoctor AI Report
=========================================================

Date:
{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}

---------------------------------------------------------

Plant:
{plant}

Disease:
{disease_name}

Confidence:
{confidence*100:.2f}%

Prediction Time:
{prediction_time:.2f} seconds

---------------------------------------------------------

Description

{info["description"]}

---------------------------------------------------------

Symptoms

{info["symptoms"]}

---------------------------------------------------------

Treatment

{info["treatment"]}

---------------------------------------------------------

Prevention

{info["prevention"]}

---------------------------------------------------------

Severity

{severity}

=========================================================

Generated by PlantDoctor AI

=========================================================
"""

    st.download_button(
        label="📄 Download Diagnosis Report",
        data=report,
        file_name=f"{plant}_{disease_name}_Report.txt",
        mime="text/plain"
    )

    # ============================================================
    # CONFIDENCE ANALYSIS
    # ============================================================

    st.markdown("---")
    st.markdown("## 📊 Confidence Analysis")

    if confidence >= 0.95:

        st.success("✅ Excellent prediction confidence.")

    elif confidence >= 0.80:

        st.success("✅ High confidence prediction.")

    elif confidence >= 0.60:

        st.warning(
            """
⚠ Moderate confidence.

Try uploading a clearer image for improved accuracy.
"""
        )

    else:

        st.error(
            """
❌ Low confidence prediction.

The image may be blurry or outside the training dataset.
"""
        )

    # ============================================================
    # AI RECOMMENDATION
    # ============================================================

    st.markdown("---")
    st.markdown("## 🤖 AI Recommendation")

    if "healthy" in disease.lower():

        st.success(
            """
🌱 The plant appears healthy.

Continue regular watering,
balanced fertilization and periodic monitoring.
"""
        )

    else:

        st.info(
            """
✔ Remove infected leaves.

✔ Apply recommended treatment.

✔ Monitor nearby plants.

✔ Repeat diagnosis after treatment.
"""
        )