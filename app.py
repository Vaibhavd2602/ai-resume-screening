
import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
from groq import Groq
import PyPDF2
import re
import sqlite3
import hashlib

st.set_page_config(page_title="AI Resume Screening & Job Recommendation", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    .stApp {background: linear-gradient(135deg, #0e1117 0%, #1a1f2e 100%);}
    div[data-testid="stMetric"] {background: linear-gradient(135deg, #1a1f2e, #2d3561); border: 1px solid #667eea; border-radius: 12px; padding: 15px;}
    .stButton>button {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; padding: 10px 25px; font-weight: bold; width: 100%;}
    .title-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 30px;}
    h1, h2, h3 {color: #ffffff;}
    p {color: #a0aec0;}
</style>
""", unsafe_allow_html=True)

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, email TEXT)")
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup_user(username, password, email):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, hash_password(password), email))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result is not None

init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("encoder.pkl", "rb") as f:
    le = pickle.load(f)
df = pd.read_excel("AI_Resume_Screening.csv.xlsx")
client = Groq(api_key=st.secrets["groq"]["api_key"])

def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_skills(text):
    common_skills = ["python", "java", "javascript", "react", "nodejs", "machine learning",
        "deep learning", "sql", "html", "css", "tensorflow", "pytorch", "docker",
        "kubernetes", "aws", "nlp", "computer vision", "tableau", "power bi", "excel",
        "kotlin", "android", "linux", "git", "mongodb", "ethical hacking", "cybersecurity", "networking", "c++"]
    text_lower = text.lower()
    return [skill for skill in common_skills if skill in text_lower]

def calculate_ats_score(experience, ai_score, projects, certifications):
    score = 0
    if experience >= 5:
        score += 30
    elif experience >= 2:
        score += 20
    else:
        score += 10
    score += (ai_score * 0.4)
    if projects >= 5:
        score += 20
    elif projects >= 2:
        score += 10
    else:
        score += 5
    if certifications and certifications.lower() not in ["none", ""]:
        score += 10
    return round(min(score, 100), 2)

def recommend_jobs(skills):
    job_data = {
        "Data Scientist": ["python", "machine learning", "deep learning", "tensorflow"],
        "Web Developer": ["html", "css", "javascript", "react"],
        "Android Developer": ["java", "kotlin", "android"],
        "ML Engineer": ["python", "machine learning", "pytorch", "nlp"],
        "Data Analyst": ["python", "sql", "excel", "tableau", "power bi"],
        "DevOps Engineer": ["docker", "kubernetes", "aws", "linux"],
        "Backend Developer": ["python", "java", "nodejs", "sql"],
        "AI Engineer": ["python", "deep learning", "nlp", "computer vision"],
        "Cybersecurity Analyst": ["ethical hacking", "cybersecurity", "networking", "linux"],
        "Database Administrator": ["sql", "mongodb", "python"]
    }
    skills_lower = skills.lower()
    recommendations = []
    for job, required_skills in job_data.items():
        match = sum(1 for skill in required_skills if skill in skills_lower)
        if match > 0:
            match_percent = round((match / len(required_skills)) * 100)
            recommendations.append((job, match_percent))
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:3]

def chat_with_ai(user_message):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert HR assistant and career coach. Help candidates with resume tips, interview preparation and career guidance. Keep answers short and helpful."},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content

def show_login():
    st.markdown("""
    <div class="title-card">
        <h1 style="color:white;">🤖 AI Resume Screening</h1>
        <p style="color:#e0e0e0;">&amp; Job Recommendation System</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            st.markdown("### Welcome Back!")
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login"):
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid username or password!")
        with tab2:
            st.markdown("### Create Account")
            new_user = st.text_input("Username", key="signup_user")
            new_email = st.text_input("Email", key="signup_email")
            new_pass = st.text_input("Password", type="password", key="signup_pass")
            if st.button("Sign Up"):
                if signup_user(new_user, new_pass, new_email):
                    st.success("Account created! Please login.")
                else:
                    st.error("Username already exists!")

def show_main():
    st.sidebar.markdown(f"""
    <div style="text-align:center; padding:15px;">
        <h3 style="color:#667eea;">🤖 AI Resume</h3>
        <p style="color:#a0aec0;">Welcome, {st.session_state.username}!</p>
    </div>
    """, unsafe_allow_html=True)
    page = st.sidebar.selectbox("Navigation", ["Home", "Resume Screening", "Job Recommendation", "Dashboard", "AI Chatbot"])
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if page == "Home":
        st.markdown("""
        <div class="title-card">
            <h1 style="color:white;">🤖 AI Resume Screening &amp; Job Recommendation</h1>
            <p style="color:#e0e0e0;">A smart AI-powered platform to screen resumes and find the perfect job match</p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Resumes", len(df))
        col2.metric("Hired", len(df[df["Recruiter Decision"] == "Hire"]))
        col3.metric("Rejected", len(df[df["Recruiter Decision"] == "Reject"]))
        col4.metric("Model Accuracy", "100%")
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.info("📄 Resume Screening - Upload your PDF resume and get instant AI screening with ATS score.")
        with c2:
            st.success("💼 Job Recommendation - Get top job matches based on your skills and experience.")
        with c3:
            st.warning("💬 AI Career Coach - Chat with AI for personalized career guidance.")

    elif page == "Resume Screening":
        st.markdown("## 📄 Resume Screening")

        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            college = st.text_input("College/University Name")
            experience = st.slider("Years of Experience", 0, 20, 0)
            projects = st.number_input("Number of Projects", 0, 50, 0)
            uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
        with col2:
            edu_options = ["-- Select Education --", "Bachelor", "Master", "PhD", "Diploma", "12th", "10th", "Other"]
            education = st.selectbox("Education Level", edu_options)
            if education == "Other":
                education = st.text_input("Please specify your education")
            certifications = st.text_input("Certifications (e.g. AWS, Google)")
            job_options = ["-- Select Job Role --"] + list(df["Job Role"].unique()) + ["Data Engineer", "Cloud Engineer", "Full Stack Developer", "Game Developer", "Blockchain Developer", "UI/UX Designer", "Product Manager", "Other"]
            job_role = st.selectbox("Applying For", job_options)
            if job_role == "Other":
                job_role = st.text_input("Please specify the job role")

        skills_input = st.text_input("Your Skills (comma separated)", "")

        if st.button("Screen My Resume"):
            errors = []
            if not name or name.strip() == "":
                errors.append("Full Name is required!")
            if education == "-- Select Education --":
                errors.append("Please select your Education Level!")
            if job_role == "-- Select Job Role --":
                errors.append("Please select the Job Role!")
            if not skills_input or skills_input.strip() == "":
                errors.append("Please enter at least one skill!")

            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
                st.stop()

            if uploaded_file:
                pdf_text = extract_text_from_pdf(uploaded_file)
                extracted_skills = extract_skills(pdf_text)
                st.info(f"Skills extracted from PDF: {', '.join(extracted_skills) if extracted_skills else 'No common skills found'}")

            good_skills = ["python", "machine learning", "deep learning", "tensorflow", "pytorch",
                          "sql", "docker", "kubernetes", "aws", "nlp", "react", "nodejs",
                          "java", "javascript", "cybersecurity", "ethical hacking", "mongodb",
                          "data analysis", "tableau", "power bi", "excel", "c++", "kotlin",
                          "android", "linux", "git", "computer vision", "flask", "django"]

            user_skills = [s.strip().lower() for s in skills_input.split(",")]
            matched = sum(1 for s in user_skills if s in good_skills)
            ai_score = min(100, (matched * 12) + (experience * 4) + (projects * 3))
            ats_score = calculate_ats_score(experience, ai_score, projects, certifications)

            if matched == 0:
                result = "Reject"
                reason = "No relevant technical skills found."
            elif ai_score < 25:
                result = "Reject"
                reason = "Skills and experience are not sufficient for this role."
            elif matched < 3 and experience < 1:
                result = "Reject"
                reason = "No experience or projects found."
            else:
                edu_enc = 0
                try:
                    edu_enc = le.transform([education])[0]
                except:
                    edu_enc = 0
                role_enc = 0
                try:
                    role_enc = le.transform([job_role])[0]
                except:
                    role_enc = 0
                features = [[experience, ai_score, projects, 50000, edu_enc, role_enc]]
                prediction = model.predict(features)[0]
                result = "Hire" if prediction == 0 else "Reject"
                reason = ""

            st.markdown("---")
            st.markdown("### Screening Results")
            r1, r2, r3 = st.columns(3)
            r1.metric("ATS Score", f"{ats_score}/100")
            r2.metric("Screening Decision", result)
            r3.metric("Skills Matched", f"{matched}")

            if result == "Hire":
                st.success(f"🎉 Congratulations {name}! Your profile looks strong. You are likely to be hired!")
            else:
                st.error(f"❌ Sorry {name}! {reason}")
                st.info("💡 Tip: Add more relevant skills, projects and experience to improve your chances.")

            fig = px.bar(x=["Experience", "AI Score", "Projects", "Certifications"],
                        y=[min(experience*6, 30), ai_score*0.4, min(projects*4, 20), 10 if certifications else 0],
                        title="ATS Score Breakdown", color_discrete_sequence=["#667eea"])
            st.plotly_chart(fig, use_container_width=True)

    elif page == "Job Recommendation":
        st.markdown("## 💼 Job Recommendation")
        skills = st.text_input("Enter Your Skills", "Python, Machine Learning, SQL")
        experience = st.slider("Years of Experience", 0, 20, 2)
        if st.button("Get Job Recommendations"):
            recommendations = recommend_jobs(skills)
            if recommendations:
                st.markdown("### Top Job Matches for You")
                for job, match in recommendations:
                    st.progress(match/100)
                    st.markdown(f"**{job}** — {match}% Match")
                    st.markdown("---")
                fig = px.bar(x=[r[0] for r in recommendations], y=[r[1] for r in recommendations],
                            title="Job Match Percentage", color=[r[1] for r in recommendations],
                            color_continuous_scale="purples")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No matching jobs found. Try adding more skills.")

    elif page == "Dashboard":
        st.markdown("## 📊 Dashboard")
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.pie(df, names="Recruiter Decision", title="Hire vs Reject Ratio",
                         color_discrete_sequence=["#667eea", "#764ba2"])
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            skills_list = []
            for s in df["Skills"]:
                for skill in str(s).split(","):
                    skills_list.append(skill.strip())
            skills_df = pd.DataFrame(skills_list, columns=["Skill"])
            top_skills = skills_df["Skill"].value_counts().head(10).reset_index()
            top_skills.columns = ["Skill", "Count"]
            fig2 = px.bar(top_skills, x="Skill", y="Count", title="Top 10 Skills", color="Skill")
            st.plotly_chart(fig2, use_container_width=True)
        fig3 = px.histogram(df, x="Experience (Years)", color="Recruiter Decision",
                           title="Experience Distribution", barmode="group",
                           color_discrete_sequence=["#667eea", "#764ba2"])
        st.plotly_chart(fig3, use_container_width=True)

    elif page == "AI Chatbot":
        st.markdown("## 💬 AI Career Coach")
        st.markdown("Ask anything about resumes, interviews, or career guidance.")
        if "messages" not in st.session_state:
            st.session_state.messages = []
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        user_input = st.chat_input("Ask your career question...")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
            reply = chat_with_ai(user_input)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.write(reply)

if st.session_state.logged_in:
    show_main()
else:
    show_login()
