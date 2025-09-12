import streamlit as st
import requests

st.set_page_config(page_title="Nearby IT Jobs", page_icon="💼", layout="wide")

# CSS for styling including dark mode fix
st.markdown("""
<style>
.header { font-size:45px; font-weight:bold; color:black; text-align:center; margin-bottom:10px; }
.subheader { font-size:22px; color:gray; text-align:center; margin-bottom:30px; }
.company-card { border-radius:12px; padding:20px; margin-bottom:20px; box-shadow:0 4px 15px rgba(0,0,0,0.1); background-color:#ffffff; color:#000000; }
.apply-btn { background-color:#4CAF50; color:white; border:none; padding:5px 10px; border-radius:6px; text-decoration:none; font-weight:bold; margin-right:5px; font-size:14px; }
.apply-btn:hover { background-color:#45a049; }
.profile-btn { background-color:#007BFF; color:white; border:none; padding:5px 10px; border-radius:6px; text-decoration:none; font-weight:bold; margin-right:5px; font-size:14px; }
.profile-btn:hover { background-color:#0056b3; }
body { background: #f0f2f6; color:#000000; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">🌍 Nearby IT/Software Companies Hiring Jobs/Internships</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Find jobs & internships near you 🚀</div>', unsafe_allow_html=True)

city_input = st.text_input("Enter your city (e.g., Bangalore, Delhi, Hyderabad):")
job_type = st.selectbox("Select job type:", ["All", "Internship", "Full-time"])

app_id = "3ce16951"
app_key = "e915c9b51f3fab1a160272b0a66bd143"

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
            
            # Direct Google search for company
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
