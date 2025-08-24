import streamlit as st

st.set_page_config(page_title="Role Assessment", page_icon="📝")

st.title("📝 Student Association Role Assessment")
st.write("Answer the questions to find your best fit role.")

# Roles dictionary
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

# Questions list
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

# User input
name = st.text_input("Enter your name:")

answers = {}
for idx, (q, mapping, weight) in enumerate(questions, start=1):
    ans = st.radio(f"{idx}. {q}", ["N", "Y"], horizontal=True, key=f"q{idx}")
    answers[q] = ans
    if ans.lower() in mapping:
        for role, score in mapping[ans.lower()].items():
            role_scores[role] += score * weight

if st.button("Submit"):
    best_role = max(role_scores.items(), key=lambda x: x[1])[0]
    st.success(f"🎉 {name}, your best-fit role is: **{best_role}**")
