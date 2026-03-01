
import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
from groq import Groq
import PyPDF2
import re

st.set_page_config(
    page_title="AI Resume Screening & Job Recommendation",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
    .main {background-color: #0e1117;}
    .stApp {background: linear-gradient(135deg, #0e1117 0%, #1a1f2e 100%);}

    .title-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1f2e, #2d3561);
        border: 1px solid #667eea;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }

    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 25px;
        font-weight: bold;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }

    h1, h2, h3 {color: #ffffff;}
    p {color: #a0aec0;}
</style>
""", unsafe_allow_html=True)

client = Groq(api_key="your_api_key_here")

with open(r"C:\\AI Project\\model.pkl", "rb") as f:
    model = pickle.load(f)

with open(r"C:\\AI Project\\encoder.pkl", "rb") as f:
    le = pickle.load(f)

df = pd.read_excel(r"C:\\AI Project\\AI_Resume_Screening.csv.xlsx")

st.sidebar.markdown("""
<div style="text-align:center; padding: 20px 0;">
    <h2 style="color: #667eea;">🤖 AI Resume</h2>
    <p style="color: #a0aec0; font-size: 12px;">Screening & Job Recommendation</p>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.selectbox("Navigation", 
    ["🏠 Home", "📄 Resume Screening", "💼 Job Recommendation", "📊 Dashboard", "💬 AI Chatbot"])

if page == "🏠 Home":
    st.markdown("""
    <div class="title-card">
        <h1 style="color: white; font-size: 2.5em;">🤖 AI Resume Screening</h1>
        <h3 style="color: #e0e0e0;">& Job Recommendation System</h3>
        <p style="color: #d0d0d0;">A smart AI-powered platform to screen resumes and find the perfect job match</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("###  System Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(" Total Resumes", len(df))
    col2.metric("✅ Hired", len(df[df["Recruiter Decision"] == "Hire"]))
    col3.metric("❌ Rejected", len(df[df["Recruiter Decision"] == "Reject"]))
    col4.metric("🎯 Model Accuracy", "100%")

    st.markdown("---")
    st.markdown("###  Key Features")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info(" **Resume Screening**\n\nUpload your PDF resume and get instant AI-powered screening with ATS score.")
    with c2:
        st.success("💼 **Job Recommendation**\n\nGet top job matches based on your skills and experience level.")
    with c3:
        st.warning(" **AI Career Coach**\n\nChat with our AI assistant for personalized career guidance and interview tips.")
