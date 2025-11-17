import streamlit as st
import random

# =========================================
# Constants
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
# Session State Initialization
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
# Custom Styling (Square Cards + Dark Theme)
# =========================================
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1f1c2c, #928dab);
        color: #E0E0E0;
    }
    h1, h2, h3 {
        color: #FFD700 !important;
        font-family: 'Trebuchet MS', sans-serif;
    }
    .card {
        background: #2c2c54;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
        margin: 10px;
        text-align: center;
    }
    div.stButton > button:first-child {
        background: #00ADB5;
        color: white;
        border-radius: 8px;
        font-size: 16px;
        padding: 10px 20px;
        border: none;
        transition: all 0.3s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        background: #007B7F;
        transform: scale(1.05);
    }
    .stProgress > div > div {
        background-color: #FFD700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================
# Phases
# =========================================
def phase_welcome():
    st.title("💧 Welcome to WaterBuddy")
    st.write("Your redesigned hydration companion.")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    begin = st.button("Let's begin 💧")
    st.markdown('</div>', unsafe_allow_html=True)

    if begin:
        st.session_state.phase = 2

def phase_age_selection():
    st.header("Step 1: Select your age group")
    cols = st.columns(2)
    for i, (group, ml) in enumerate(AGE_GROUPS.items()):
        with cols[i % 2]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            if st.button(group):
                st.session_state.age_group = group
                st.session_state.goal = ml
                st.session_state.phase = 3
            st.markdown('</div>', unsafe_allow_html=True)

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
    st.markdown('<div class="card">', unsafe_allow_html=True)
    cont = st.button("Continue ➡️")
    st.markdown('</div>', unsafe_allow_html=True)
    if cont:
        st.session_state.phase = 4

def phase_logging_pref():
    st.header("Step 3: Choose your logging preference")
    cols = st.columns(2)
    with cols[0]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        quick = st.button("Quick log (+250 ml)")
        st.markdown('</div>', unsafe_allow_html=True)
        if quick:
            st.session_state.log_pref = "quick"
            st.session_state.phase = 5
    with cols[1]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        custom = st.button("Custom entry")
        st.markdown('</div>', unsafe_allow_html=True)
        if custom:
            st.session_state.log_pref = "custom"
            st.session_state.phase = 5

def phase_optional_settings():
    st.header("Step 4: Personalize your experience")
    st.session_state.show_tips = st.checkbox("Show daily hydration tips", value=True)
    st.session_state.mascot_on = st.checkbox("Enable mascot reactions", value=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    finish = st.button("Finish setup ✅")
    st.markdown('</div>', unsafe_allow_html=True)
    if finish:
        st.session_state.phase = 6

def phase_dashboard():
    st.title("📊 WaterBuddy Dashboard")
    st.write(f"**Age group:** {st.session_state.age_group}")
    st.write(f"**Daily goal:** {st.session_state.goal} ml")

    cols = st.columns(2)
    with cols[0]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        add_quick = st.button("+250 ml")
        st.markdown('</div>', unsafe_allow_html=True)
        if add_quick:
            st.session_state.total += 250
    with cols[1]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        manual_amount = st.number_input("Log custom amount (ml):", min_value=0, step=50)
        add_custom = st.button("Add custom amount")
        st.markdown('</div>', unsafe_allow_html=True)
        if add_custom:
            st.session_state.total += manual_amount

    st.markdown('<div class="card">', unsafe_allow_html=True)
    reset = st.button("🔄 New Day (Reset)")
    st.markdown('</div>', unsafe_allow_html=True)
    if reset:
        st.session_state.total = 0

    remaining = max(st.session_state.goal - st.session_state.total, 0)
    progress = min(st.session_state.total / st.session_state.goal, 1.0)

    st.progress(progress)
    st.write(f"**Total intake so far:** {st.session_state.total} ml")
    st.write(f"**Remaining to goal:** {remaining} ml")
    st.write(f"**Progress:** {progress*100:.1f}%")

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

    if st.session_state.show_tips:
        st.write("---")
        st.write("💡 Tip of the day:")
        st.write(random.choice(HYDRATION_TIPS))

# =========================================
# Main Runner
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
