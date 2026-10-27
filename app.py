import streamlit as st

st.set_page_config(page_title="Alps Trek Training Tracker", page_icon="🏔️", layout="wide")

st.title("🏔️ Alps Trek 5-Month Family Training Tracker")
st.write("Track individual fitness assessments, tailored progression plans, and weekly training goals.")

# ---------------------------------------------------------
# 1. USER SELECTION
# ---------------------------------------------------------
user = st.sidebar.selectbox("Select Family Member:", ["Select...", "You", "Mom", "Sister"])

if user == "Select...":
    st.info("👈 Please select a family member from the sidebar to begin.")
    st.stop()

st.header(f"Profile: {user}")

# Initialize session state storage
if "profiles" not in st.session_state:
    st.session_state.profiles = {}

# ---------------------------------------------------------
# 2. ASSESSMENT SURVEY
# ---------------------------------------------------------
with st.expander("📋 Initial Fitness Assessment Survey", expanded=(user not in st.session_state.profiles)):
    st.write("Complete this quick survey to generate your personalized 5-month plan.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cardio_days = st.slider("Days per week of current cardio (walking, running, cycling):", 0, 7, 2, key=f"{user}_cardio")
        stair_capacity = st.selectbox("How long can you comfortably climb stairs or steep inclines?", 
                                      ["< 10 minutes", "10–20 minutes", "20–45 minutes", "45+ minutes"], key=f"{user}_stairs")
        pack_exp = st.selectbox("Have you carried a weighted daypack (10+ lbs / 4.5+ kg) on hikes?", 
                                ["Never", "Rarely", "Occasionally", "Regularly"], key=f"{user}_pack")
    
    with col2:
        joint_issues = st.multiselect("Any current physical constraints or joint sensitivities?",
                                      ["Knee pain (especially descents)", "Ankle instability", "Lower back tightness", "None"], 
                                      default=["None"], key=f"{user}_joints")
        
        target_pack = st.number_input("Target daypack weight for Alps trip (lbs):", min_value=5, max_value=35, value=15, key=f"{user}_target_pack")

    if st.button("Save Survey & Build Training Plan"):
        # Calculate baseline fitness score (1 to 3)
        score = 0
        score += 1 if cardio_days <= 2 else (2 if cardio_days <= 4 else 3)
        score += 1 if stair_capacity in ["< 10 minutes", "10–20 minutes"] else 2
        
        st.session_state.profiles[user] = {
            "score": score,
            "target_pack": target_pack,
            "joints": joint_issues
        }
        st.success(f"Assessment saved for {user}!")

# ---------------------------------------------------------
# 3. TRAINING PLAN & PROGRESS CHECKLIST
# ---------------------------------------------------------
if user in st.session_state.profiles:
    profile = st.session_state.profiles[user]
    st.divider()
    
    st.subheader("🗓️ Your 5-Month Progression Overview")
    
    # Customize recommendations based on joint issues
    if "Knee pain (especially descents)" in profile["joints"]:
        st.warning("⚠️ **Joint Focus:** Focus on eccentric leg strength (controlled step-downs) and use trekking poles during all training hikes.")
    
    # 5-Month Breakdown
    months = {
        "Month 1 (Weeks 1–4): Aerobic Base": {
            "cardio": "3x weekly Zone 2 cardio (30–40 mins brisk walking, cycling, or flat hiking).",
            "strength": "2x weekly bodyweight exercises (squats, glute bridges, step-ups).",
            "pack": "No weight or light daypack (5 lbs max)."
        },
        "Month 2 (Weeks 5–8): Elevation Focus": {
            "cardio": "3x weekly cardio including 1 stair/incline session (30 mins).",
            "strength": "2x weekly lunges, step-ups, plank holds.",
            "pack": f"Weekend hike: {round(profile['target_pack'] * 0.4)} lbs pack weight."
        },
        "Month 3 (Weeks 9–12): Strength & Endurance": {
            "cardio": "3–4x weekly cardio (45 mins), alternating flat and incline terrain.",
            "strength": "2x weekly weighted step-ups, calf raises, core stability.",
            "pack": f"Weekend hike: {round(profile['target_pack'] * 0.7)} lbs pack weight."
        },
        "Month 4 (Weeks 13–16): Alpine Trek Simulation": {
            "cardio": "Long weekend hike (3–5 hours) with steep ascents/descents.",
            "strength": "2x weekly maintenance strength & knee stability drills.",
            "pack": f"Weekend hike: Full target weight ({profile['target_pack']} lbs)."
        },
        "Month 5 (Weeks 17–20): Peak & Taper": {
            "cardio": "Weeks 17–18: Peak weekend volume. Weeks 19–20: Reduce volume by 50% to rest.",
            "strength": "1–2x weekly light mobility and bodyweight exercises.",
            "pack": f"Light practice hikes with full gear ({profile['target_pack']} lbs)."
        }
    }

    selected_month = st.selectbox("Select Month to View Goals:", list(months.keys()))
    m_data = months[selected_month]

    st.markdown(f"**Cardio Target:** {m_data['cardio']}")
    st.markdown(f"**Strength Target:** {m_data['strength']}")
    st.markdown(f"**Target Pack Weight:** {m_data['pack']}")

    st.subheader("✅ Weekly Log")
    col_w1, col_w2 = st.columns(2)
    
    with col_w1:
        st.checkbox("Completed Session 1: Mid-week Cardio", key=f"{user}_{selected_month}_c1")
        st.checkbox("Completed Session 2: Strength & Balance", key=f"{user}_{selected_month}_s1")
    with col_w2:
        st.checkbox("Completed Session 3: Incline/Stair Climb", key=f"{user}_{selected_month}_c2")
        st.checkbox("Completed Session 4: Weekend Training Hike", key=f"{user}_{selected_month}_h1")

    st.text_area("Notes / How did your body feel?", placeholder="e.g., Felt good on the climbs, slight fatigue in calves...", key=f"{user}_{selected_month}_notes")
