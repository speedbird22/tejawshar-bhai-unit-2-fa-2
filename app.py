import streamlit as st
import random

# =========================================
# 1. Constants
# =========================================
AGE_GROUPS = {
    "Children (4-8 years)": 1200,
    "Teens (9-13 years)": 1700,
    "Adults (14-64 years)": 2200,
    "Seniors (65+ years)": 1800,
}

HYDRATION_TIPS = [
    "Try drinking a glass of water before meals.",
    "Keep a bottle on your desk as a reminder.",
    "Start your morning with a glass of water.",
    "Set small goals: one cup every hour.",
    "Hydrate after exercise to recover faster."
]

# =========================================
# 2. Session State Initialization
# =========================================
def init_session():
    defaults = {
        "phase": 1,
        "age_group": None,
        "goal": 0,
        "total": 0,
        "log_pref": "quick",
        "show_tips": True,
        "mascot_on": True,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

# =========================================
# 3. Custom Styling
# =========================================
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #E0E0E0;
    }
    h1, h2, h3 {
        color: #00E0FF !important;
        font-family: 'Trebuchet MS', sans-serif;
    }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #FF0080, #7928CA);
        color: white;
        border-radius: 30px;
        font-size: 18px;
        padding: 12px 28px;
        border: none;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
        transition: all 0.3s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #FF4D4D, #FF0080);
        transform: translateY(-3px) scale(1.05);
    }
    .stProgress > div > div {
        background-color: #00E0FF !important;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================
# 4. Phase Functions
# =========================================
def phase_welcome():
    st.title("💧 Welcome to WaterBuddy")
    st.write("Your neon-styled daily hydration companion.")
    if st.button("Let's begin 💧"):
        st.session_state.phase = 2

def phase_age_selection():
    st.header("Step 1: Select your age group")
    for group, ml in AGE_GROUPS.items():
        if st.button(group):
            st.session_state.age_group = group
            st.session_state.goal = ml
            st.session_state.phase = 3

def phase_goal_confirmation():
    st.header("Step 2: Confirm or adjust your daily goal")
    st.write(f"Recommended goal for {st.session_state.age_group}: {AGE_GROUPS[st.session_state.age_group]} ml")
    st.session_state.goal = st.number_input(
        "Your daily water goal (ml):",
        min_value=500,
        max_value=4000,
        value=AGE_GROUPS[st.session_state.age_group],
        step=100
    )
    if st.button("Continue ➡️"):
        st.session_state.phase = 4

def phase_logging_pref():
    st.header("Step 3: Choose your logging preference")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Quick log (+250 ml)"):
            st.session_state.log_pref = "quick"
            st.session_state.phase = 5
    with col2:
        if st.button("Custom entry"):
            st.session_state.log_pref = "custom"
            st.session_state.phase = 5

def phase_optional_settings():
    st.header("Step 4: Personalize your experience")
    st.session_state.show_tips = st.checkbox("Show daily hydration tips", value=True)
    st.session_state.mascot_on = st.checkbox("Enable mascot reactions", value=True)
    if st.button("Finish setup ✅"):
        st.session_state.phase = 6

def phase_dashboard():
    st.title("📊 WaterBuddy Dashboard")
    st.write(f"**Age group:** {st.session_state.age_group}")
    st.write(f"**Daily goal:** {st.session_state.goal} ml")

    # Logging intake
    col1, col2 = st.columns(2)
    with col1:
        if st.button("+250 ml"):
            st.session_state.total += 250
    with col2:
        manual_amount = st.number_input("Log custom amount (ml):", min_value=0, step=50)
        if st.button("Add custom amount"):
            st.session_state.total += manual_amount

    # Reset
    if st.button("🔄 New Day (Reset)"):
        st.session_state.total = 0

    # Progress
    remaining = max(st.session_state.goal - st.session_state.total, 0)
    progress = min(st.session_state.total / st.session_state.goal, 1.0)

    st.progress(progress)
    st.write(f"**Total intake so far:** {st.session_state.total} ml")
    st.write(f"**Remaining to goal:** {remaining} ml")
    st.write(f"**Progress:** {progress*100:.1f}%")

    # Mascot reactions
    if st.session_state.mascot_on:
        if progress == 0:
            st.info("Let's start hydrating! 🚰🙂")
        elif progress < 0.5:
            st.info("Good start! Keep sipping 💦😃")
        elif progress < 0.75:
            st.success("Nice! You're halfway there 😎")
        elif progress < 1.0:
            st.success("Almost at your goal! 🌊🤗")
        else:
            st.balloons()
            st.success("🎉 Congratulations! You hit your hydration goal! 🥳")

    # Tips
    if st.session_state.show_tips:
        st.write("---")
        st.write("💡 Tip of the day:")
        st.write(random.choice(HYDRATION_TIPS))

# =========================================
# 5. Main App Runner
# =========================================
phase_map = {
    1: phase_welcome,
    2: phase_age_selection,
    3: phase_goal_confirmation,
    4: phase_logging_pref,
    5: phase_optional_settings,
    6: phase_dashboard,
}

phase_map[st.session_state.phase]()
