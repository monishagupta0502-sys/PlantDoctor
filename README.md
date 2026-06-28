![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.19-orange?logo=tensorflow)
![Streamlit](https://img.shields.io/badge/Streamlit-Live-red?logo=streamlit)
![License](https://img.shields.io/badge/License-Educational-green)
[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-PlantDoctor-success)](https://plantdoctor-kazldlecm3frjpqwtacncx.streamlit.app/)
# 🌿 PlantDoctor AI

An AI-powered web application for plant disease detection using Deep Learning, built with TensorFlow and Streamlit.

## 🚀 Live Demo

🔗 https://plantdoctor-kazldlecm3frjpqwtacncx.streamlit.app/

---

## 📌 Overview

PlantDoctor AI helps farmers, gardeners, and agriculture enthusiasts detect plant diseases by simply uploading a leaf image.

The application uses a trained Deep Learning model to classify plant diseases and provides:

- 🌱 Plant identification
- 🦠 Disease detection
- 🎯 Confidence score
- 📖 Disease description
- 💊 Treatment recommendations
- 🛡 Prevention tips
- ⚠ Disease severity
- 🌦 Weather-based farming advice
- 🤖 AI-powered assistant
- 📄 Professional PDF diagnosis report

---

## ✨ Features

- 🔍 AI-based Plant Disease Detection
- 🌿 Supports Multiple Plant Diseases
- 🏆 Top 3 Prediction Results
- 📊 Confidence Analysis
- 📖 Disease Information
- 💊 Treatment Suggestions
- 🛡 Prevention Tips
- ⚠ Severity Indicator
- 🌦 Live Weather Intelligence
- 🤖 AI Chat Assistant
- 📜 Prediction History
- 👤 User Login & Registration
- 📄 Downloadable PDF Reports
- 📱 Modern Responsive Interface

---

## 🛠 Tech Stack

### Frontend
- Streamlit
- HTML
- CSS

### Backend
- Python

### AI / Machine Learning
- TensorFlow
- MobileNetV2
- NumPy

### Database
- SQLite

### APIs
- Open-Meteo Weather API

### Libraries
- Pillow
- Pandas
- Matplotlib
- ReportLab

### Version Control
- Git
- GitHub

---

## 📂 Project Structure

```text
PlantDoctor/
│
├── app.py
├── requirements.txt
├── runtime.txt
├── style.css
├── disease_info.py
│
├── models/
│   ├── best_plant_disease_model.keras
│   └── class_names.json
│
├── pages/
│   ├── Dashboard.py
│   ├── AI_Assistant.py
│   ├── History.py
│
├── utils/
│   ├── auth.py
│   ├── chatbot.py
│   ├── weather.py
│   └── pdf_report.py
│
└── database/
```

---

## 🧠 Model Information

- Model: MobileNetV2
- Framework: TensorFlow
- Image Size: 224 × 224
- Output Classes: 38 Plant Disease Classes

---

## ⚙ Installation

Clone the repository:

```bash
git clone https://github.com/monishagupta0502-sys/PlantDoctor.git
```

Go into the project folder:

```bash
cd PlantDoctor
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## 📸 Screenshots

Add screenshots of:

- Home Page
  <img width="2928" height="1658" alt="image" src="https://github.com/user-attachments/assets/c2f32578-077f-407e-a198-f241d5de5b37" />

- Prediction Result
  <img width="2940" height="1678" alt="image" src="https://github.com/user-attachments/assets/04e82eaa-ec9b-46e3-9fd4-ba92c098e44f" />

- Dashboard
  <img width="2940" height="1670" alt="image" src="https://github.com/user-attachments/assets/6c403582-afda-45c3-a783-05e4080076b1" />

  <img width="2940" height="1678" alt="image" src="https://github.com/user-attachments/assets/c8e9b604-5a43-4c64-a394-9f329dd99b0a" />

- AI Assistant
  <img width="2934" height="1664" alt="image" src="https://github.com/user-attachments/assets/04957aa0-b8a9-44dd-8023-635cb2a0e1a7" />
  
  <img width="2940" height="1686" alt="image" src="https://github.com/user-attachments/assets/40e65d10-59d7-493a-b5d2-6dec235c4e14" />

- Weather Section
  <img width="2940" height="1662" alt="image" src="https://github.com/user-attachments/assets/12f7e8b3-0e69-4836-82dd-f99a05f1eef2" />

- PDF Report
  <img width="1060" height="1466" alt="image" src="https://github.com/user-attachments/assets/9d367658-8e7c-4ff5-9f69-7a12b9edec91" />


---

## 👩‍💻 Developer

**Monisha Gupta**

B.Tech Computer Science Engineering 
Second-Year Undergraduate Student

---

## 📜 License

This project was developed for educational and internship purposes.

---

## ⭐ Acknowledgements

- TensorFlow
- Streamlit
- Open-Meteo API
- PlantVillage Dataset
- Kaggle

