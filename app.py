import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import os
import time
from utils.pdf_report import generate_pdf
from utils.weather import (
    CITY_COORDINATES,
    get_weather,
    weather_advice
)
from datetime import datetime

from disease_info import DISEASE_INFO
from utils.auth import create_database, save_scan

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
# CREATE DATABASE
# ============================================================

create_database()

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

    return tf.keras.models.load_model(
        "models/best_plant_disease_model.keras"
    )



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

    image = np.array(image).astype(np.float32)

    image /= 255.0

    image = np.expand_dims(image, axis=0)

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

    index = np.argmax(prediction)

    confidence = float(prediction[index])

    disease = class_names[index]

    top3 = np.argsort(prediction)[::-1][:3]

    return disease, confidence, prediction, top3
# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🌿 PlantDoctor AI")

    st.markdown("### Deep Learning Powered Plant Disease Detection")

    st.divider()

    st.metric("🎯 Model Accuracy", "92.14%")
    st.metric("🦠 Disease Classes", "38")
    st.metric("🤖 Framework", "TensorFlow")
    st.metric("🧠 Model", "MobileNetV2")

    st.divider()

    st.success("✅ AI Model Loaded")

    st.info(
        """
Upload a clear plant leaf image.

The AI will detect diseases and provide treatment recommendations.
"""
    )

    st.divider()

    st.caption("Version 2.0")


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div style="
padding:35px;
background:#F8FFF8;
border:2px solid #A5D6A7;
border-radius:20px;
box-shadow:0px 10px 25px rgba(0,0,0,0.08);
text-align:center;
">

<h1 style="color:#1B5E20;">
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

m1, m2, m3, m4 = st.columns(4)

m1.metric("🎯 Accuracy", "92.14%")
m2.metric("🦠 Diseases", "38")
m3.metric("🤖 Framework", "TensorFlow")
m4.metric("🧠 Model", "MobileNetV2")

st.divider()


# ============================================================
# MAIN LAYOUT
# ============================================================

left, right = st.columns([1, 1.25], gap="large")


# ============================================================
# LEFT COLUMN
# ============================================================

with left:

    st.markdown("## 📤 Upload Leaf Image")

    uploaded_file = st.file_uploader(
        "Choose a leaf image",
        type=["jpg", "jpeg", "png"]
    )

    image = None

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Uploaded Leaf",
            use_container_width=True
        )

        st.info(
            """
### 📌 Tips

• Upload one leaf

• Use good lighting

• Avoid blurry images

• Plain background gives best results
"""
        )


# ============================================================
# RIGHT COLUMN
# ============================================================

with right:

    st.markdown("## 🤖 AI Diagnosis")
# ============================================================
# AI PREDICTION
# ============================================================

with right:

    if uploaded_file is None:

        st.warning("📤 Upload a leaf image to begin prediction.")

    else:

        with st.spinner("🔍 Analyzing leaf image..."):

            start_time = time.time()

            disease, confidence, prediction, top3 = predict(image)

            prediction_time = time.time() - start_time

        plant = disease.split("___")[0].replace("_", " ")

        disease_name = disease.split("___")[1].replace("_", " ")

        # ============================================================
        # SAVE LAST PREDICTION FOR AI ASSISTANT
        # ============================================================

        st.session_state["last_disease"] = disease
        st.session_state["last_plant"] = plant
        st.session_state["last_disease_name"] = disease_name
        st.session_state["last_confidence"] = confidence

        # ============================================================
        # SAVE SCAN
        # ============================================================

        if st.session_state.get("logged_in", False):

            save_scan(

                st.session_state["username"],

                plant,

                disease_name,

                confidence,

                prediction_time,

                datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            )

        # ============================================================
        # RESULT
        # ============================================================

        st.success("✅ Prediction Complete")

        st.markdown("### 🌱 Plant")
        st.success(plant)

        st.markdown("### 🦠 Disease")
        st.error(disease_name)

        st.markdown("### 🎯 Confidence")

        st.progress(confidence)

        st.write(f"**{confidence*100:.2f}%**")

        st.caption(f"Prediction completed in {prediction_time:.2f} seconds")   
 # ============================================================
# TOP 3 PREDICTIONS
# ============================================================

        st.divider()

        st.markdown("## 🏆 Top Predictions")

        medals = ["🥇", "🥈", "🥉"]

        for i, idx in enumerate(top3):

            probability = float(prediction[idx])

            label = (
                class_names[idx]
                .replace("___", " → ")
                .replace("_", " ")
            )

            st.markdown(f"### {medals[i]} {label}")

            st.progress(probability)

            st.caption(f"{probability*100:.2f}% Confidence") 
        # ============================================================
        # DISEASE INFORMATION
        # ============================================================

        info = DISEASE_INFO.get(
            disease,
            {
                "description": "Information unavailable.",
                "symptoms": "Not available.",
                "treatment": "Not available.",
                "prevention": "Not available.",
                "severity": "Unknown"
            }
        )

        st.divider()

        st.markdown("## 📖 Disease Information")

        c1, c2 = st.columns(2)

        with c1:

            st.markdown("### 📝 Description")
            st.info(info["description"])

            st.markdown("### 🔍 Symptoms")
            st.info(info["symptoms"])

        with c2:

            st.markdown("### 💊 Treatment")
            st.success(info["treatment"])

            st.markdown("### 🛡 Prevention")
            st.success(info["prevention"])
        # ============================================================
        # PLANT STATUS
        # ============================================================

        st.divider()

        st.markdown("## 🌱 Plant Status")

        if "healthy" in disease.lower():

            st.success("✅ Healthy Plant")

        else:

            st.error("🦠 Disease Detected")

        severity = info.get("severity", "Unknown")

        color_map = {
            "Low": "🟢",
            "Medium": "🟡",
            "High": "🔴"
        }

        st.markdown(
            f"### Severity: {color_map.get(severity,'⚪')} **{severity}**"
        )

        # ============================================================
        # CONFIDENCE ANALYSIS
        # ============================================================

        st.divider()

        st.markdown("## 📊 Confidence Analysis")

        if confidence >= 0.95:

            st.success("Excellent prediction confidence.")

        elif confidence >= 0.80:

            st.success("High confidence prediction.")

        elif confidence >= 0.60:

            st.warning(
                "Moderate confidence. Try uploading a clearer image."
            )

        else:

            st.error(
                "Low confidence prediction. Please try another image."
            )

        # ============================================================
        # AI RECOMMENDATION
        # ============================================================

        st.divider()

        st.markdown("## 🤖 AI Recommendation")

        if "healthy" in disease.lower():

            st.success(
                """
🌱 The plant appears healthy.

• Continue regular watering.

• Maintain balanced fertilization.

• Monitor leaves regularly.
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
        # WEATHER INTELLIGENCE
        # ============================================================

        weather = st.session_state.get("weather", None)

        st.divider()

        st.markdown("## 🌦 Weather Intelligence")

        city = st.selectbox(
            "📍 Select Your City",
            list(CITY_COORDINATES.keys())
        )

        if st.button("Get Weather"):

            latitude, longitude = CITY_COORDINATES[city]

            st.session_state["weather"] = get_weather(latitude, longitude)

            weather = st.session_state["weather"]

            if weather:

                c1, c2, c3 = st.columns(3)

                with c1:

                    st.metric(
                        "🌡 Temperature",
                        f"{weather['temperature']} °C"
                    )

                with c2:

                    st.metric(
                        "💧 Humidity",
                        f"{weather['humidity']} %"
                    )

                with c3:

                    st.metric(
                        "🍃 Wind",
                        f"{weather['wind']} km/h"
                    )

                st.markdown("### 🌱 Smart Farming Advice")

                advice = weather_advice(
                    weather["humidity"],
                    disease_name
                )

                for tip in advice:

                    st.success(tip)

            else:

                st.error("Unable to fetch weather data.")  
# ============================================================
# PROFESSIONAL PDF REPORT
# ============================================================

        pdf_file = generate_pdf(
            filename="PlantDoctor_Report.pdf",
            username=st.session_state.get("username", "Guest"),
            plant=plant,
            disease=disease_name,
            confidence=confidence,
            prediction_time=prediction_time,
            info=info,
            severity=severity,
            weather=weather
        )

        with open(pdf_file, "rb") as pdf:

            st.download_button(
                label="📄 Download Professional PDF Report",
                data=pdf,
                file_name=f"{plant}_{disease_name}_Report.pdf",
                mime="application/pdf"
            )                        

# ============================================================
# DISCLAIMER
# ============================================================

st.divider()

st.info(
"""
### ⚠ Disclaimer

This prediction is generated using a Deep Learning model trained on the PlantVillage dataset.

Always consult an agricultural expert before taking critical crop management decisions.
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