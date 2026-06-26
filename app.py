import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import json
from disease_info import DISEASE_INFO

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Plant Disease Detection",
    page_icon="🌿",
    layout="centered"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.big-title{
    text-align:center;
    color:#2E8B57;
    font-size:42px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    font-size:18px;
    color:gray;
}

.result-box{
    background-color:#F0FFF4;
    padding:20px;
    border-radius:12px;
    border:2px solid #2E8B57;
}

.footer{
    text-align:center;
    color:gray;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("🌿 Plant Disease AI")

st.sidebar.success("Model Accuracy: 92.14%")

st.sidebar.markdown("---")

st.sidebar.write("### 🧠 Model")
st.sidebar.write("MobileNetV2")

st.sidebar.write("### 📊 Dataset")
st.sidebar.write("PlantVillage")

st.sidebar.write("### 🌱 Classes")
st.sidebar.write("38 Plant Diseases")

st.sidebar.markdown("---")

st.sidebar.write("Developed by")
st.sidebar.write("**Monisha** ❤️")

# -----------------------------------
# TITLE
# -----------------------------------

st.markdown(
    "<div class='big-title'>🌿 Plant Disease Detection</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Upload a leaf image and let AI identify the disease.</div>",
    unsafe_allow_html=True
)

# -----------------------------------
# ABOUT
# -----------------------------------

with st.expander("ℹ️ About this Project"):

    st.write("""
This application uses **Deep Learning** to identify diseases in plant leaves.

### Features

✅ Detects **38 plant diseases**

✅ MobileNetV2 CNN

✅ Top-5 Predictions

✅ Confidence Score

✅ Disease Description

✅ Symptoms

✅ Treatment

✅ Prevention

Dataset: **PlantVillage**
""")

# -----------------------------------
# LOAD MODEL
# -----------------------------------

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(
        "best_plant_disease_model.keras"
    )

model = load_model()

# -----------------------------------
# LOAD CLASS NAMES
# -----------------------------------

with open("class_names.json","r") as f:
    class_names = json.load(f)

# -----------------------------------
# IMAGE PREPROCESSING
# -----------------------------------

def preprocess_image(image):

    image = image.convert("RGB")

    image = image.resize((224,224))

    image = np.array(image)

    image = image.astype(np.float32)

    image = image / 255.0

    image = np.expand_dims(image,axis=0)

    return image

# -----------------------------------
# FILE UPLOADER
# -----------------------------------

uploaded_file = st.file_uploader(
    "📷 Upload a Leaf Image",
    type=["jpg","jpeg","png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Leaf",
        use_container_width=True
    )

    input_image = preprocess_image(image)

    with st.spinner("🔍 Analyzing image..."):

        prediction = model.predict(input_image)

        prediction = prediction[0]

        predicted_index = np.argmax(prediction)

        confidence = prediction[predicted_index]

        disease = class_names[predicted_index]

        info = DISEASE_INFO.get(
            disease,
            {
                "description":"No information available.",
                "symptoms":"-",
                "treatment":"-",
                "prevention":"-"
            }
        )

    # Prediction results will be added in Part 2
        # -----------------------------------
    # PREDICTION RESULT
    # -----------------------------------

    st.markdown("---")

    clean_name = disease.replace("___", " → ").replace("_", " ")

    st.success(f"🌿 **Prediction:** {clean_name}")

    st.metric(
        label="🎯 Confidence",
        value=f"{confidence*100:.2f}%"
    )

    st.progress(float(confidence))

    # -----------------------------------
    # TOP 5 PREDICTIONS
    # -----------------------------------

    st.markdown("---")
    st.subheader("📊 Top 5 Predictions")

    top5 = np.argsort(prediction)[::-1][:5]

    for idx in top5:

        probability = prediction[idx]

        disease_name = class_names[idx].replace(
            "___",
            " → "
        ).replace(
            "_",
            " "
        )

        col1, col2 = st.columns([4,1])

        with col1:

            st.write(disease_name)

            st.progress(float(probability))

        with col2:

            st.write(f"{probability*100:.2f}%")

    # -----------------------------------
    # DISEASE INFORMATION
    # -----------------------------------

    st.markdown("---")

    st.subheader("📖 Disease Description")

    st.write(info["description"])

    st.subheader("🔍 Symptoms")

    st.info(info["symptoms"])

    st.subheader("💊 Treatment")

    st.success(info["treatment"])

    st.subheader("🛡 Prevention")

    st.warning(info["prevention"])

    # -----------------------------------
    # DOWNLOAD REPORT
    # -----------------------------------

    report = f"""
Plant Disease Detection Report

Prediction:
{clean_name}

Confidence:
{confidence*100:.2f}%

Description:
{info['description']}

Symptoms:
{info['symptoms']}

Treatment:
{info['treatment']}

Prevention:
{info['prevention']}
"""

    st.download_button(
        label="📄 Download Report",
        data=report,
        file_name="plant_disease_report.txt",
        mime="text/plain"
    )
        # -----------------------------------
    # PREDICTION STATUS
    # -----------------------------------

    st.markdown("---")

    if confidence >= 0.95:
        st.success("✅ Very High Confidence Prediction")
    elif confidence >= 0.80:
        st.info("👍 High Confidence Prediction")
    elif confidence >= 0.60:
        st.warning(
            "⚠️ Moderate Confidence. Consider uploading a clearer image for better accuracy."
        )
    else:
        st.error(
            "❌ Low Confidence. The uploaded image may not belong to the trained dataset or may be unclear."
        )

    # -----------------------------------
    # HEALTH STATUS
    # -----------------------------------

    st.markdown("---")

    if "healthy" in disease.lower():
        st.success("🌱 Plant Status: Healthy")
    else:
        st.error("🦠 Plant Status: Diseased")

    # -----------------------------------
    # DISCLAIMER
    # -----------------------------------

    st.markdown("---")

    st.info(
        """
        **Disclaimer**

        This prediction is generated using a Deep Learning model trained on the
        PlantVillage dataset. It is intended for educational purposes and should
        not replace professional agricultural advice.
        """
    )

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.markdown(
    """
<div class='footer'>
Made with ❤️ using TensorFlow, MobileNetV2 & Streamlit<br>
Developed by <b>Monisha</b>
</div>
""",
    unsafe_allow_html=True
)