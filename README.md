# AI Resume Screening & Job Recommendation System

## What is this project?

I built this project to solve a real problem that most companies face during hiring — manually going through hundreds of resumes takes a lot of time and is often inconsistent. This system automates that entire process using machine learning and AI.

You can upload your resume, get an ATS score, see which jobs match your profile, and even chat with an AI career coach — all in one place.

---

## Features

- Login and Signup system so each user has their own account
- Upload your PDF resume and get it screened automatically
- ATS score calculated based on your experience, projects, skills and certifications
- Job recommendations based on what skills you have
- Dashboard with charts showing hiring trends and skill distribution
- AI chatbot to help with career advice and interview tips

---

## Tech Stack

- **Python** — everything is built in Python
- **Streamlit** — for the web interface
- **Scikit-learn (Random Forest)** — the ML model that predicts hiring decisions
- **Groq API with LLaMA 3.3** — powers the AI chatbot
- **PyPDF2** — reads and extracts text from uploaded PDF resumes
- **Plotly** — for the interactive graphs and charts
- **SQLite** — stores user login data
- **Pandas** — for data handling and processing

---

## Project Structure
```
AI-Resume-Screening/
│
├── app.py                            # main application file
├── model.pkl                         # trained random forest model
├── encoder.pkl                       # label encoder for categories
├── AI_Resume_Screening.csv.xlsx      # dataset used for training
├── users.db                          # stores user accounts
└── README.md                         # this file
```

---

## How to Run

**Step 1 — Clone the repo**
```bash
git clone https://github.com/yourusername/ai-resume-screening.git
cd ai-resume-screening
```

**Step 2 — Install the required libraries**
```bash
pip install streamlit scikit-learn PyPDF2 groq plotly pandas openpyxl
```

**Step 3 — Add your Groq API key**

Go to [console.groq.com](https://console.groq.com), create a free account and generate an API key.
Open `app.py` and replace `YOUR_API_KEY_HERE` with your actual key.

**Step 4 — Run the app**
```bash
streamlit run app.py
```

---

## Dataset Details

The dataset has 1000 resume records with the following columns — Resume ID, Name, Skills, Experience in Years, Education, Certifications, Job Role, Recruiter Decision, Salary Expectation, Projects Count, and AI Score.

The Random Forest model trained on this dataset gives 100% accuracy on the test set.

---

## How It Works

**Resume Screening**
Upload your PDF resume or manually enter your details. The system extracts your skills, calculates an ATS score, and predicts whether your profile would likely get a hire or reject decision.

**Job Recommendation**
Enter your skills and the system matches them against common job roles. You get the top 3 job matches along with a match percentage for each.

**AI Chatbot**
Ask anything related to your career — resume tips, how to prepare for interviews, what skills to learn next. The chatbot is powered by LLaMA 3.3 through Groq and gives practical advice.

---

## What I Learned

This project taught me how to connect machine learning models with a proper frontend, how to handle PDF parsing, how to use LLM APIs in a real application, and how to manage user sessions and authentication without any heavy frameworks.

---

## Possible Improvements

- Better resume parsing using NLP instead of keyword matching
- Adding more job categories
- Letting recruiters log in separately and view candidate reports
- Sending email notifications after screening
- Deploying it online so anyone can use it

---

## Author

**Vaibhav Dubey**
BTech CS AI — Kanpur

GitHub: [Vaibhavd2602](https://github.com/Vaibhavd2602)
