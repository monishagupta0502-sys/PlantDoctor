import streamlit as st
import pandas as pd

from utils.auth import get_history

st.set_page_config(
    page_title="History",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Scan History")

if "logged_in" not in st.session_state:

    st.warning("Please login first.")

    st.stop()

history = get_history(
    st.session_state["username"]
)

if len(history) == 0:

    st.info("No scans available.")

else:

    df = pd.DataFrame(

        history,

        columns=[
            "Plant",
            "Disease",
            "Confidence",
            "Prediction Time (s)",
            "Scan Date"
        ]
    )

    df["Confidence"] = (
        df["Confidence"] * 100
    ).round(2)

    st.dataframe(
        df,
        use_container_width=True
    )