import streamlit as st
import random

# -------------------------------
# Hydration recommendations by age group (ml)
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

# -------------------------------
# Initialize session state
if "phase" not in st.session_state:
    st.session_state.phase = 1
if "age_group" not in st.session_state:
    st.session_state.age_group = None
if "goal" not in st.session_state:
    st.session_state.goal = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "log_pref" not in st.session_state:
    st.session_state.log_pref = "quick"
if "show_tips" not in st.session_state:
    st.session_state.show_tips = True
if "mascot_on" not in st.session_state:
    st.session_state.mascot_on = True

# -------------------------------
# Custom CSS for new background & buttons
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #FFDEE9, #B5FFFC);
    }
    .stButton>button {
        background-color: #FF6B6B;
        color: white;
        border-radius: 20px;
        font-size: 18px;
        padding: 12px 24px;
        border: none;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF3B3B;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Phase 1: Welcome
if st.session_state.phase == 1:
    st.title("💧 Welcome to WaterBuddy")
    st.write("Your friendly daily hydration companion.")
    if st.button("Let's begin 💧"):
        st.session_state.phase = 2

# -------------------------------
# Phase 2: Age selection
elif st.session_state.phase == 2:
    st.header("Step 1: Select your age group")
    for group, ml in AGE_GROUPS.items():
        if st.button(group):
            st.session_state.age_group = group
            st.session_state.goal = ml
            st.session_state.phase = 3

# -------------------------------
# Phase 3: Goal confirmation
elif st.session_state.phase == 3:
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

# -------------------------------
# Phase 4: Logging preference
elif st.session_state.phase == 4:
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

# -------------------------------
# Phase 5: Optional settings
elif st.session_state.phase == 5:
    st.header("Step 4: Personalize your experience")
    st.session_state.show_tips = st.checkbox("Show daily hydration tips", value=True)
    st.session_state.mascot_on = st.checkbox("Enable mascot reactions", value=True)
    if st.button("Finish setup ✅"):
        st.session_state.phase = 6

# -------------------------------
# Phase 6: Dashboard
elif st.session_state.phase == 6:
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

    # Calculations
    remaining = max(st.session_state.goal - st.session_state.total, 0)
    progress = min(st.session_state.total / st.session_state.goal, 1.0)

    st.progress(progress)
    st.write(f"**Total intake so far:** {st.session_state.total} ml")
    st.write(f"**Remaining to goal:** {remaining} ml")
    st.write(f"**Progress:** {progress*100:.1f}%")

    # Motivational messages with emojis
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
