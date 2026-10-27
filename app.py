import streamlit as st

st.set_page_config(page_title="Alps Trek 5-Month Trainer", page_icon="🏔️", layout="wide")

st.title("🏔️ Alps Trek Family Training & Tracker")
st.write("Personalized training schedules, daily exercise guides, and group tracking.")

# ---------------------------------------------------------
# GLOBAL STATE SETUP FOR ALL USERS
# ---------------------------------------------------------
MEMBERS = ["Yoav", "Rotem", "Leeor"]

if "profiles" not in st.session_state:
    st.session_state.profiles = {}

if "completed_workouts" not in st.session_state:
    st.session_state.completed_workouts = {}

# ---------------------------------------------------------
# SIDEBAR NAVIGATION & SHARED DASHBOARD
# ---------------------------------------------------------
st.sidebar.title("Navigation")
current_user = st.sidebar.selectbox("Select Your Profile:", ["Group Dashboard"] + MEMBERS)

# ---------------------------------------------------------
# 1. GROUP DASHBOARD (See Everyone's Progress)
# ---------------------------------------------------------
if current_user == "Group Dashboard":
    st.header("👥 Group Activity & Accountability Dashboard")
    st.write("Check if your family members have completed their workouts for the selected week and day!")
    
    selected_week = st.slider("Select Week to View Progress:", 1, 20, 1)
    selected_day = st.selectbox("Select Day:", ["Day 1 (Cardio)", "Day 2 (Strength)", "Day 3 (Incline)", "Day 4 (Weekend Trek)"])

    st.subheader(f"Status for Week {selected_week} - {selected_day}")
    
    cols = st.columns(3)
    for idx, name in enumerate(MEMBERS):
        with cols[idx]:
            st.markdown(f"### {name}")
            user_has_profile = name in st.session_state.profiles
            
            if not user_has_profile:
                st.info("Assessment not completed yet.")
            else:
                key = f"{name}_W{selected_week}_{selected_day}"
                is_done = st.session_state.completed_workouts.get(key, False)
                
                if is_done:
                    st.success("✅ Workout Completed!")
                else:
                    st.error("❌ Not Done Yet")

    st.divider()
    st.info("💡 Switch to your name in the sidebar to fill out your survey or log your daily workouts.")
    st.stop()

# ---------------------------------------------------------
# 2. INDIVIDUAL PROFILES & INITIAL ASSESSMENT
# ---------------------------------------------------------
st.header(f"Profile: {current_user}")

with st.expander("📋 Initial Fitness Survey", expanded=(current_user not in st.session_state.profiles)):
    st.write("Answer these questions to generate your specific weekly workouts.")
    
    col1, col2 = st.columns(2)
    with col1:
        fitness_level = st.select_slider(
            "Current overall fitness level:",
            options=["Beginner (rarely exercise)", "Intermediate (1-2 times/week)", "Advanced (3+ times/week)"],
            key=f"{current_user}_fitness"
        )
        stair_endurance = st.selectbox(
            "How comfortably can you climb steep stairs/inclines?",
            ["Less than 10 mins", "10–20 mins", "20–45 mins", "45+ mins"],
            key=f"{current_user}_stairs"
        )
    
    with col2:
        joint_concerns = st.multiselect(
            "Any joint sensitivities or past injuries?",
            ["Knee pain on descents", "Ankle issues", "Lower back discomfort", "None"],
            default=["None"],
            key=f"{current_user}_joints"
        )
        pack_target = st.number_input("Target daypack weight for trek (kg):", min_value=3, max_value=15, value=7, key=f"{current_user}_pack")

    if st.button("Save & Generate Training Schedule"):
        st.session_state.profiles[current_user] = {
            "level": fitness_level,
            "stairs": stair_endurance,
            "joints": joint_concerns,
            "pack": pack_target
        }
        st.success(f"Fitness baseline saved for {current_user}!")

if current_user not in st.session_state.profiles:
    st.warning("Please complete and save the survey above to unlock your workouts.")
    st.stop()

profile = st.session_state.profiles[current_user]

# Adjust volume based on fitness level
base_minutes = 30 if "Beginner" in profile["level"] else (40 if "Intermediate" in profile["level"] else 50)

# ---------------------------------------------------------
# 3. DAILY WORKOUT SESSIONS & CHECKLIST
# ---------------------------------------------------------
st.divider()
st.subheader("🗓️ Daily Workout Plans")

week_num = st.slider("Select Week:", 1, 20, 1, key=f"{current_user}_week_select")

# Define progression phase based on week
if week_num <= 4:
    phase = "Phase 1: Foundation & Base Aerobic Conditioning"
    intensity = "Moderate Effort (Zone 2 - Easy Conversational Pace)"
    pack_w = 0
elif week_num <= 8:
    phase = "Phase 2: Elevation & Leg Endurance"
    intensity = "Moderate-High Effort"
    pack_w = round(profile["pack"] * 0.4, 1)
elif week_num <= 12:
    phase = "Phase 3: Alpine Strength & Load Capacity"
    intensity = "High Effort"
    pack_w = round(profile["pack"] * 0.7, 1)
elif week_num <= 16:
    phase = "Phase 4: Full Trekking Simulation"
    intensity = "Peak Effort"
    pack_w = profile["pack"]
else:
    phase = "Phase 5: Peak & Taper (Recovery Focus)"
    intensity = "Reduced Volume / Easy Pace"
    pack_w = round(profile["pack"] * 0.5, 1)

st.caption(f"**Current Phase:** {phase}")

# Days Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Day 1: Endurance Cardio", "Day 2: Strength & Stability", "Day 3: Incline & Stairs", "Day 4: Weekend Training Trek"])

# --- DAY 1 ---
with tab1:
    st.markdown(f"### Day 1: Aerobic Base (Zone 2)")
    st.write(f"**Duration:** {base_minutes + (week_num * 2)} minutes")
    st.write(f"**Target Pace:** {intensity}")
    st.markdown("""
    **Instructions:**
    * Perform brisk walking, light jogging, or cycling.
    * Maintain a pace where you can comfortably talk in full sentences without gasping for breath.
    * Keep posture upright and maintain consistent nasal breathing where possible.
    """)
    
    key1 = f"{current_user}_W{week_num}_Day 1 (Cardio)"
    done1 = st.checkbox("Mark Day 1 as Completed", value=st.session_state.completed_workouts.get(key1, False))
    st.session_state.completed_workouts[key1] = done1

# --- DAY 2 ---
with tab2:
    st.markdown("### Day 2: Leg Strength & Balance Session")
    st.write("**Complete 3 sets of the following routine:**")
    
    st.markdown("""
    1. **Bodyweight Squats (12–15 reps):** 
       * *Instruction:* Stand feet shoulder-width apart. Lower hips back and down like sitting in a chair. Keep chest up and knees tracking over toes.
    2. **Reverse Lunges (10 reps per leg):**
       * *Instruction:* Step back with one leg, bending both knees to 90 degrees. Push through front heel to return. Protects knees better than forward lunges.
    3. **Step-Downs (8 reps per leg):**
       * *Instruction:* Stand on a low step/stair. Slowly lower one foot toward the floor in a controlled 3-second descent, then push back up. *Essential for downhill mountain stability!*
    4. **Glute Bridges (15 reps):**
       * *Instruction:* Lie on back with knees bent and feet flat. Drive hips toward the ceiling, squeezing glutes at the top.
    5. **Plank Hold (45–60 seconds):**
       * *Instruction:* Hold forearms and toes on floor, keeping body in a straight line without letting lower back arch.
    """)
    
    if "Knee pain on descents" in profile["joints"]:
        st.info("💡 **Joint Note:** Take extra care on the 3-second step-down control. Keep movements slow and pain-free.")
        
    key2 = f"{current_user}_W{week_num}_Day 2 (Strength)"
    done2 = st.checkbox("Mark Day 2 as Completed", value=st.session_state.completed_workouts.get(key2, False))
    st.session_state.completed_workouts[key2] = done2

# --- DAY 3 ---
with tab3:
    st.markdown("### Day 3: Incline & Stair Conditioning")
    st.write(f"**Duration:** 30–45 minutes")
    st.write(f"**Current Pack Weight:** {pack_w} kg")
    st.markdown("""
    **Instructions:**
    * Use a stair climber machine, outdoor park stairs, or a high-incline treadmill (8%–12% grade).
    * Focus on pushing through your heels rather than your toes to engage glutes and hamstrings.
    * Wear your trekking shoes to break them in.
    """)
    
    key3 = f"{current_user}_W{week_num}_Day 3 (Incline)"
    done3 = st.checkbox("Mark Day 3 as Completed", value=st.session_state.completed_workouts.get(key3, False))
    st.session_state.completed_workouts[key3] = done3

# --- DAY 4 ---
with tab4:
    st.markdown("### Day 4: Weekend Endurance Trek")
    hike_hours = 1.5 + (week_num * 0.15) if week_num <= 16 else 2.0
    st.write(f"**Target Duration:** {round(hike_hours, 1)} hours")
    st.write(f"**Pack Weight:** {pack_w} kg")
    st.markdown("""
    **Instructions:**
    * Find local trails with rolling terrain or uneven paths.
    * Wear fully loaded backpack with gear/water to hit target weight.
    * Practice using trekking poles on downhill sections to take stress off your knees.
    * Practice taking small hydration/snack breaks every 45–60 minutes.
    """)
    
    key4 = f"{current_user}_W{week_num}_Day 4 (Weekend Trek)"
    done4 = st.checkbox("Mark Day 4 as Completed", value=st.session_state.completed_workouts.get(key4, False))
    st.session_state.completed_workouts[key4] = done4
