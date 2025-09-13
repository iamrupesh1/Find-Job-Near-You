import streamlit as st
import requests

st.set_page_config(page_title="Nearby IT Jobs", page_icon="💼", layout="wide")

# ========================= CSS Styling including dark mode fix =========================
st.markdown("""
<style>
/* Force light background for whole app */
body, .stApp {
    background-color: #f0f2f6 !important;
    color: #111 !important;
    font-family: Arial, sans-serif;
}

/* Header */
.header {
    font-size: 45px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
    color: #111 !important;
}

/* Subheader with rocket animation */
.subheader {
    font-size: 22px;
    color: #555 !important;
    text-align: center;
    margin-bottom: 20px;
}
.rocket {
    display: inline-block;
    animation: rocketFly 2s ease-in-out infinite;
}
@keyframes rocketFly {
    0% { transform: translateY(0) rotate(0deg); }
    25% { transform: translateY(-6px) rotate(-10deg); }
    50% { transform: translateY(0) rotate(0deg); }
    75% { transform: translateY(-6px) rotate(10deg); }
    100% { transform: translateY(0) rotate(0deg); }
}

/* Instruction closer to city input box */
.instruction {
    font-size: 14px;
    color: #111 !important;
    margin-bottom: -8px;  /* closer to city input */
    text-align: left;
}

/* Input box */
.stTextInput>div>div>input {
    font-size: 16px;
    padding: 12px 15px;
    border-radius: 10px;
    border: 2px solid #111;
    width: 100%;
    box-sizing: border-box;
    color: #111 !important;
    background-color: #fff !important;
}
.stTextInput>div>div>input::placeholder {
    color: #555 !important;
    font-weight: 500;
}

/* Style select box input like city input */
.stSelectbox > div > div > select {
    font-size: 16px;
    padding: 12px 15px;
    border-radius: 10px;
    border: 2px solid #111;
    width: 100%;
    box-sizing: border-box;
    color: #111 !important;
    background-color: #fff !important;
    font-family: Arial, sans-serif;
}

/* Select box label fully visible and consistent */
.stSelectbox > label {
    color: #111 !important;
    font-weight: 500;
    font-size: 16px;
    margin-bottom: 5px;
}

/* Company Card */
.company-card {
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* Buttons */
.apply-btn {
    background-color: #4CAF50;
    color: white !important;
    border: none;
    padding: 5px 10px;
    border-radius: 6px;
    text-decoration: none;
    font-weight: bold;
    margin-right: 5px;
    font-size: 14px;
}
.apply-btn:hover { background-color: #45a049; }
.profile-btn {
    background-color: #007BFF;
    color: white !important;
    border: none;
    padding: 5px 10px;
    border-radius: 6px;
    text-decoration: none;
    font-weight: bold;
    margin-right: 5px;
    font-size: 14px;
}
.profile-btn:hover { background-color: #0056b3; }

/* Responsive */
@media (max-width:600px){
    .header { font-size: 28px; }
    .subheader { font-size: 18px; }
    .instruction {
        font-size: 13px;
        margin-bottom: -6px;
    }
    .stTextInput>div>div>input { font-size: 14px; }
    .stSelectbox > div > div > select {
        font-size: 14px;
        padding: 10px 12px;
    }
    .stSelectbox > label {
        font-size: 14px;
    }
}
</style>
""", unsafe_allow_html=True)

# ========================= Header & Subheader =========================
st.markdown('<div class="header">🌍 Nearby IT/Software Companies Hiring Jobs/Internships</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Find jobs & internships near you <span class="rocket">🚀</span></div>', unsafe_allow_html=True)

# ========================= Instruction above input box =========================
st.markdown('<p class="instruction">Enter your city e.g., Bangalore, Delhi...</p>', unsafe_allow_html=True)

# ========================= City input and Job type =========================
city_input = st.text_input("", placeholder="🏙️ Enter here…")
job_type = st.selectbox("Select job type:", ["All", "Internship", "Full-time"], index=0, format_func=lambda x: f"{x}")

# ========================= API Keys =========================
app_id = "3ce16951"
app_key = "e915c9b51f3fab1a160272b0a66bd143"

# ========================= Fetch jobs =========================
def fetch_jobs(city, job_type_filter, max_pages=5):
    all_jobs = []
    for page in range(1, max_pages + 1):
        url = f"https://api.adzuna.com/v1/api/jobs/in/search/{page}"
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "what": "software",
            "where": city,
            "results_per_page": 50
        }
        try:
            res = requests.get(url, params=params, timeout=5)
            data = res.json()
            jobs = data.get("results", [])
            if not jobs:
                break
            all_jobs.extend(jobs)
        except:
            st.error("Error fetching jobs! Try again later.")
            break

    companies = {}
    for job in all_jobs:
        company = job.get("company", {}).get("display_name", "").strip()
        if not company or company.lower() in ["unknown", "unnamed company"]:
            continue
        title = job.get("title", "")
        location = job.get("location", {}).get("display_name", "")
        apply = job.get("redirect_url", "")
        if job_type_filter == "Internship" and "intern" not in title.lower():
            continue
        if job_type_filter == "Full-time" and "intern" in title.lower():
            continue
        if company not in companies:
            companies[company] = {"location": location, "jobs": []}
        companies[company]["jobs"].append({"title": title, "apply": apply})

    clean_jobs = []
    for company, details in companies.items():
        clean_jobs.append({
            "company": company,
            "location": details["location"],
            "jobs": details["jobs"]
        })
    return clean_jobs

# ========================= Main Execution =========================
if city_input:
    with st.spinner(f"Fetching jobs in {city_input}... ⏳"):
        jobs_list = fetch_jobs(city_input, job_type)

    if not jobs_list and job_type == "Internship":
        st.warning(f"No internships found in {city_input}. Showing all available jobs instead.")
        jobs_list = fetch_jobs(city_input, "All")

    if not jobs_list:
        st.warning("No real jobs found for this city.")
    else:
        st.success(f"✅ Found {len(jobs_list)} companies in {city_input}")
        for job in jobs_list:
            job_items = "".join([f'<li>{j["title"]} — <a href="{j["apply"]}" target="_blank" class="apply-btn">Apply here</a></li>' for j in job['jobs']])
            company_profile_url = f"https://www.google.com/search?q={job['company']} official site"
            st.markdown(f"""
            <div class="company-card">
            <h2>🏢 {job['company']}</h2>
            <p>📍 {job['location']}</p>
            <p>💼 Job Opening(s):</p>
            <ul>
                {job_items}
            </ul>
            <a href="{company_profile_url}" target="_blank" class="profile-btn">🌐 Visit Company Website</a>
            </div>
            """, unsafe_allow_html=True)