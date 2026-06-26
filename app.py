import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import os
import time
from datetime import datetime

from disease_info import DISEASE_INFO

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
        "best_plant_disease_model.keras"
    )

    return model

model = load_model()

# ============================================================
# LOAD CLASS NAMES
# ============================================================

with open("class_names.json","r") as f:

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

st.markdown("""
# 🌿 PlantDoctor AI

### Smart Plant Disease Detection using Deep Learning
""")

st.write(
"""
PlantDoctor AI helps farmers and researchers identify plant diseases using an AI model trained on the PlantVillage dataset.

Upload a clear image of a plant leaf and receive:

✅ Disease Prediction

✅ Confidence Score

✅ Treatment

✅ Prevention

✅ Severity Level
"""
)

st.divider()
# ============================================================
# MAIN LAYOUT
# ============================================================

left_col, right_col = st.columns([1, 1.25], gap="large")

with left_col:

    st.markdown("## 📤 Upload Leaf Image")

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

    st.markdown("## 🤖 AI Diagnosis")

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

        plant = disease.split("___")[0].replace("_", " ")

        disease_name = disease.split("___")[1].replace("_", " ")

        st.success("Prediction Completed Successfully")

        st.metric(
            "Prediction Time",
            f"{prediction_time:.2f} sec"
        )

        st.markdown("### 🌱 Plant")

        st.success(plant)

        st.markdown("### 🦠 Disease")

        st.error(disease_name)

        st.markdown("### 🎯 Confidence")

        st.progress(float(confidence))

        st.write(
            f"### {confidence*100:.2f}%"
        )

        st.divider()

        st.markdown("## 🏆 Top 3 Predictions")

        medals = [
            "🥇",
            "🥈",
            "🥉"
        ]

        for i, idx in enumerate(top3):

            probability = float(prediction[idx])

            class_name = class_names[idx]

            class_name = class_name.replace(
                "___",
                " → "
            )

            class_name = class_name.replace(
                "_",
                " "
            )

            st.write(
                f"{medals[i]} **{class_name}**"
            )

            st.progress(probability)

            st.caption(
                f"{probability*100:.2f}%"
            )

        st.divider()

        info = DISEASE_INFO.get(
            disease,
            {
                "description":"Information unavailable.",
                "symptoms":"-",
                "treatment":"-",
                "prevention":"-",
                "severity":"Unknown"
            }
        )
        # ============================================================
# DISEASE INFORMATION
# ============================================================

        st.markdown("## 📖 Disease Information")

        st.markdown("### 📝 Description")

        st.write(info["description"])

        st.markdown("---")

        st.markdown("### 🔍 Symptoms")

        st.info(info["symptoms"])

        st.markdown("---")

        st.markdown("### 💊 Recommended Treatment")

        st.success(info["treatment"])

        st.markdown("---")

        st.markdown("### 🛡 Prevention")

        st.warning(info["prevention"])

        st.markdown("---")

        st.markdown("### ⚠ Disease Severity")

        severity = info.get("severity", "Unknown")

        if severity.lower() == "low":

            st.success("🟢 Low Severity")

        elif severity.lower() == "medium":

            st.warning("🟠 Medium Severity")

        elif severity.lower() == "high":

            st.error("🔴 High Severity")

        else:

            st.info("⚪ Unknown")

# ============================================================
# PLANT STATUS
# ============================================================

        st.markdown("---")

        st.markdown("## 🌱 Plant Health Status")

        if "healthy" in disease.lower():

            st.success(
                """
### ✅ Healthy Plant

Your plant appears to be healthy.

Continue following good agricultural practices.
"""
            )

        else:

            st.error(
                """
### 🦠 Disease Detected

The uploaded plant appears to be infected.

Please follow the recommended treatment and prevention methods shown above.
"""
            )

# ============================================================
# MODEL INFORMATION
# ============================================================

        st.markdown("---")

        st.markdown("## 🤖 AI Model Details")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Framework",
                "TensorFlow"
            )

            st.metric(
                "Architecture",
                "MobileNetV2"
            )

        with col2:

            st.metric(
                "Classes",
                "38"
            )

            st.metric(
                "Validation Accuracy",
                "92.14%"
            )

        st.markdown("---")
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

            st.success(
                "✅ Excellent prediction confidence."
            )

        elif confidence >= 0.80:

            st.success(
                "✅ High confidence prediction."
            )

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

# ============================================================
# DISCLAIMER
# ============================================================

st.markdown("---")

st.info(
"""
### ⚠ Disclaimer

This prediction is generated using a Deep Learning model
trained on the PlantVillage Dataset.

Results are intended for educational and research purposes.

For severe crop infections,
consult a professional agricultural expert.
"""
)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
"""
<center>

### 🌿 PlantDoctor AI

Deep Learning Powered Plant Disease Detection

TensorFlow • MobileNetV2 • Streamlit

Version 2.0

Made with ❤️ by Monisha

</center>
""",
unsafe_allow_html=True
)