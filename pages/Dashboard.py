import streamlit as st
import pandas as pd

from utils.auth import get_history
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# LOGIN CHECK
# ============================================================

if "logged_in" not in st.session_state:

    st.warning("Please login first.")

    st.stop()

username = st.session_state["username"]

history = get_history(username)

# ============================================================
# CALCULATE STATS
# ============================================================

total_scans = len(history)

healthy = 0
diseased = 0

confidence_sum = 0
time_sum = 0

for scan in history:

    plant, disease, confidence, prediction_time, scan_date = scan

    confidence_sum += confidence
    time_sum += prediction_time

    if "healthy" in disease.lower():

        healthy += 1

    else:

        diseased += 1

if total_scans > 0:

    avg_confidence = confidence_sum / total_scans
    avg_time = time_sum / total_scans

else:

    avg_confidence = 0
    avg_time = 0
# ============================================================
# HEADER
# ============================================================

st.markdown(f"""
<div style="
padding:35px;
background:linear-gradient(135deg,#145A32,#2E8B57);
border-radius:25px;
color:white;
box-shadow:0px 12px 30px rgba(0,0,0,.18);
">

<h1>🌿 Welcome Back, {username}!</h1>

<h3>PlantDoctor Pro Dashboard</h3>

</div>
""", unsafe_allow_html=True)
st.write("")

c1,c2,c3,c4 = st.columns(4)

with c1:

    st.metric(
        "📷 Total Scans",
        total_scans
    )

with c2:

    st.metric(
        "🌱 Healthy",
        healthy
    )

with c3:

    st.metric(
        "🦠 Diseased",
        diseased
    )

with c4:

    st.metric(
        "🎯 Avg Confidence",
        f"{avg_confidence*100:.2f}%"
    )

# ============================================================
# DASHBOARD
# ============================================================

st.write("")

left, right = st.columns([1, 1])

# ============================================================
# LEFT SIDE
# ============================================================

with left:

    st.subheader("📈 Disease Distribution")

    if total_scans > 0:

        fig, ax = plt.subplots(figsize=(5,5))

        ax.pie(
            [healthy, diseased],
            labels=["Healthy", "Diseased"],
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={"edgecolor":"white"}
        )

        ax.axis("equal")

        st.pyplot(fig)

    else:

        st.info("No scan data available.")

    st.markdown("---")

    st.subheader("🤖 AI Tip of the Day")

    if diseased > healthy:

        st.warning(
            """
Most of your recent scans are diseased.

✔ Inspect leaves daily.

✔ Remove infected leaves.

✔ Avoid watering the leaves directly.
"""
        )

    else:

        st.success(
            """
Great job!

Most of your plants are healthy.

✔ Continue regular inspection.

✔ Water early in the morning.

✔ Keep monitoring for new symptoms.
"""
        )

# ============================================================
# RIGHT SIDE
# ============================================================

with right:

    st.subheader("🕒 Recent Activity")

    if total_scans == 0:

        st.info("No scans available.")

    else:

        plant, disease, confidence, prediction_time, scan_date = history[0]

        st.success(f"""
🌿 **Plant:** {plant}

🦠 **Disease:** {disease}

🎯 **Confidence:** {confidence*100:.2f}%

⏱ **Prediction Time:** {prediction_time:.2f} sec

📅 **Scan Date:** {scan_date}
""")

    st.markdown("---")

    st.subheader("⚡ Quick Actions")

    col1, col2 = st.columns(2)

    with col1:

        st.button("📷 New Scan", use_container_width=True)

        st.button("📜 History", use_container_width=True)

    with col2:

        st.button("📚 Disease Library", use_container_width=True)

        st.button("🌦 Weather", use_container_width=True)