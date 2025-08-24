import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Role Assessment", page_icon="📝")

st.title("📝 Student Association Role Assessment")
st.write("Answer the questions to find your best fit role.")

# ========================
# Google Sheets Setup
# ========================
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["google_service_account"], scope
)
client = gspread.authorize(creds)
sheet = client.open("Role_Assessment_Results").sheet1

# ========================
# Roles dictionary
# ========================
role_scores = {
    "Secretary": 0,
    "Joint Secretary": 0,
    "Treasurer": 0,
    "Creative & Media Team": 0,
    "Technical Team": 0,
    "Host / Anchor": 0,
    "Senior Coordinator": 0,
    "Vice President": 0
}

# ========================
# Questions list
# ========================
questions = [
    ("Do you enjoy writing meeting notes and official emails?", {"y": {"Secretary": 3}}, 3),
    ("Are you detail-oriented and good with documentation?", {"y": {"Joint Secretary": 3, "Secretary": 1}}, 3),
    ("Do you like organizing schedules and reminders?", {"y": {"Secretary": 2, "Joint Secretary": 1}}, 2),
    ("Do you enjoy managing money and tracking expenses?", {"y": {"Treasurer": 4}}, 4),
    ("Are you comfortable creating budgets and financial plans?", {"y": {"Treasurer": 3}}, 3),
    ("Do you consider yourself trustworthy with funds?", {"y": {"Treasurer": 2}}, 3),
    ("Do you like designing posters or digital content?", {"y": {"Creative & Media Team": 3}}, 3),
    ("Are you active on social media and enjoy content creation?", {"y": {"Creative & Media Team": 2}}, 2),
    ("Do you enjoy photography/videography?", {"y": {"Creative & Media Team": 2}}, 2),
    ("Do you enjoy coding, websites, or tech setup?", {"y": {"Technical Team": 3}}, 3),
    ("Do you like solving technical problems quickly?", {"y": {"Technical Team": 2}}, 3),
    ("Do you have experience with AV equipment or event tech?", {"y": {"Technical Team": 2}}, 2),
    ("Do you enjoy speaking in front of an audience?", {"y": {"Host / Anchor": 4}}, 4),
    ("Are you confident in engaging a crowd?", {"y": {"Host / Anchor": 3}}, 3),
    ("Do you have good stage presence?", {"y": {"Host / Anchor": 2}}, 2),
    ("Do you like coordinating and managing people?", {"y": {"Vice President": 3, "Senior Coordinator": 2}}, 4),
    ("Can you handle logistics and planning for events?", {"y": {"Senior Coordinator": 3, "Vice President": 1}}, 3),
    ("Do you enjoy making decisions under pressure?", {"y": {"Vice President": 3}}, 3),
    ("Do you see yourself as a leader who inspires others?", {"y": {"Vice President": 3}}, 3)
]

# ========================
# User Input
# ========================
name = st.text_input("Enter your name:")

answers = {}
for idx, (q, mapping, weight) in enumerate(questions, start=1):
    ans = st.radio(f"{idx}. {q}", ["N", "Y"], horizontal=True, key=f"q{idx}")
    answers[q] = ans
    if ans.lower() in mapping:
        for role, score in mapping[ans.lower()].items():
            role_scores[role] += score * weight

# ========================
# Submit button
# ========================
if st.button("Submit") and name.strip() != "":
    # Pick top 2 roles
    sorted_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)
    top_roles = [r for r, s in sorted_roles[:2] if s > 0]

    if len(top_roles) == 1:
        st.success(f"🎉 {name}, your best-fit role is: **{top_roles[0]}**")
    else:
        st.success(f"🎉 {name}, your best-fit roles could be: **{top_roles[0]}** or **{top_roles[1]}**")

    # Save result + answers to Google Sheets
    try:
        row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, ", ".join(top_roles)]
        for q in questions:
            row.append(answers[q[0]])  # Add Y/N answers

        sheet.append_row(row)
        st.info("✅ Your response was saved to Google Sheets!")
    except Exception as e:
        st.error(f"⚠️ Could not save to Google Sheets: {e}")

# ========================
# Admin Dashboard
# ========================
st.sidebar.subheader("🔐 Admin Login")
password = st.sidebar.text_input("Enter admin password", type="password")

if password == st.secrets["admin_password"]:  # Add admin_password in Streamlit Secrets
    st.sidebar.success("✅ Logged in as Admin")

    try:
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        st.subheader("📊 Role Distribution")
        if not df.empty and "Best Role" in df.columns:
            role_counts = df["Best Role"].value_counts()
            st.bar_chart(role_counts)

        st.subheader("📋 All Responses")
        st.dataframe(df)

        st.download_button("📥 Download CSV", df.to_csv(index=False), "results.csv", "text/csv")

    except Exception as e:
        st.error(f"⚠️ Could not fetch admin data: {e}")
