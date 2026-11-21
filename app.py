
import streamlit as st
import time

st.set_page_config(
    page_title="Number Hunt Game",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

GAME_TIME = 60

# ---------------- SESSION STATE ----------------
def initialize_game():
    st.session_state.status = "home"
    st.session_state.low = 1
    st.session_state.high = 1000
    st.session_state.guess = 500
    st.session_state.guesses = 0
    st.session_state.start_time = None
    st.session_state.remaining_time = GAME_TIME
    st.session_state.result = ""
    st.session_state.feedback = ""

if "status" not in st.session_state:
    initialize_game()

# ---------------- GAME FUNCTIONS ----------------
def start_game():
    st.session_state.status = "playing"
    st.session_state.low = 1
    st.session_state.high = 1000
    st.session_state.guess = 500
    st.session_state.guesses = 1
    st.session_state.start_time = time.time()
    st.session_state.remaining_time = GAME_TIME
    st.session_state.result = ""
    st.session_state.feedback = ""

def end_game(message):
    st.session_state.status = "finished"
    st.session_state.result = message

def process_feedback(feedback):
    if st.session_state.status != "playing":
        return

    guess = st.session_state.guess
    st.session_state.feedback = feedback

    if feedback == "Too Low":
        st.session_state.low = guess + 1

    elif feedback == "Too High":
        st.session_state.high = guess - 1

    elif feedback == "Correct":
        end_game(f"The computer successfully found your number: {guess}!")
        return

    # Contradiction detection
    if st.session_state.low > st.session_state.high:
        end_game(
            "Contradictory feedback detected! "
            "No possible numbers remain."
        )
        return

    # Binary search midpoint
    st.session_state.guess = (
        st.session_state.low + st.session_state.high
    ) // 2

    st.session_state.guesses += 1

def check_timer():
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, GAME_TIME - int(elapsed))
    st.session_state.remaining_time = remaining

    if remaining <= 0:
        end_game(
            "Time is up! The computer did not confirm your secret number."
        )

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: linear-gradient(145deg, #10172a, #182747);
    color: #f8fafc;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 850px;
    padding-top: 1.5rem;
    padding-bottom: 1rem;
}

h1, h2, h3, p, label {
    color: #f8fafc !important;
}

.brand {
    text-align: center;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #a5b4fc;
    margin-bottom: 8px;
}

.main-title {
    text-align: center;
    font-size: clamp(30px, 6vw, 45px);
    font-weight: 800;
    background: linear-gradient(90deg, #60a5fa, #c4b5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}

.subtitle {
    text-align: center;
    color: #a9b8d0 !important;
    font-size: 14px;
    margin-bottom: 24px;
}

.guess-card {
    background: linear-gradient(135deg, #263e70, #493c83);
    border: 1px solid #6477bd;
    border-radius: 22px;
    padding: 22px 12px;
    text-align: center;
    margin: 15px 0;
    box-shadow: 0 12px 30px #0004;
}

.guess-label {
    color: #dbeafe;
    font-size: 15px;
    font-weight: 600;
}

.guess-number {
    color: white;
    font-size: clamp(65px, 13vw, 100px);
    font-weight: 800;
    line-height: 1.2;
}

.guess-hint {
    color: #dbeafe;
    font-size: 14px;
}

.stat-card {
    background: #202e49;
    border: 1px solid #344663;
    border-radius: 14px;
    padding: 15px 5px;
    text-align: center;
    min-height: 90px;
}

.stat-label {
    color: #a9b8d0;
    font-size: 12px;
    font-weight: 600;
}

.stat-value {
    color: #ffffff;
    font-size: clamp(20px, 4vw, 27px);
    font-weight: 800;
    margin-top: 7px;
}

.section-label {
    text-align: center;
    font-size: 18px;
    font-weight: 700;
    margin: 20px 0 12px;
}

div.stButton > button {
    min-height: 62px;
    border-radius: 14px;
    font-size: 16px;
    font-weight: 800;
    border: 1px solid #63769b;
    background: #263b5e;
    color: white;
    transition: 0.2s;
}

div.stButton > button:hover {
    border-color: #a5b4fc;
    background: #394f79;
    color: white;
    transform: translateY(-2px);
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #4f75e8, #8059dc);
    border: none;
    color: white;
}

.feedback-note {
    background: #263b5e;
    border: 1px solid #6078a3;
    border-radius: 12px;
    padding: 12px;
    text-align: center;
    color: #dbeafe;
    margin: 12px 0;
}

.result-card {
    background: #202e49;
    border: 1px solid #6277a5;
    border-radius: 18px;
    padding: 25px 18px;
    text-align: center;
    margin: 20px 0;
}

.developer {
    text-align: center;
    color: #94a3b8;
    font-size: 12px;
    border-top: 1px solid #344663;
    padding-top: 15px;
    margin-top: 28px;
}

div[data-testid="stProgressBar"] > div {
    background-color: #344663;
}

div[data-testid="stProgressBar"] div[role="progressbar"] {
    background: linear-gradient(90deg, #60a5fa, #a78bfa);
}

@media(max-width: 600px) {
    .block-container {
        padding: 1rem 0.8rem;
    }

    .stat-card {
        min-height: 78px;
    }

    div.stButton > button {
        min-height: 65px;
        font-size: 14px;
    }

    .guess-card {
        padding: 18px 8px;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
def header():
    st.markdown(
        '<div class="brand">🎯 THE THINKING GAME</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="main-title">NUMBER HUNT</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">Can the computer find your secret number?</div>',
        unsafe_allow_html=True
    )

def footer():
    st.markdown("""
    <div class="developer">
        DEVELOPED BY<br>
        <strong style="color:#c4b5fd;">
        Muniffah Siadis &nbsp;|&nbsp; ChatGPT
        </strong>
        <br><br>
        Number Hunt Game • Think. Guess. Discover.
    </div>
    """, unsafe_allow_html=True)

# ---------------- HOME SCREEN ----------------
if st.session_state.status == "home":
    header()

    st.markdown("""
    <div class="guess-card">
        <div class="guess-label">WELCOME TO</div>
        <div style="font-size:55px;">🔢</div>
        <div style="font-size:23px;font-weight:800;color:white;">
            NUMBER HUNT GAME
        </div>
        <p class="guess-hint">
            Think of a number. Let the computer find it!
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🎮 How to Play")

    st.markdown("""
    - Think of a secret whole number from **1 to 1,000**.
    - Keep your number hidden. Do not enter it anywhere.
    - The computer will start guessing from the midpoint.
    - Give feedback after every guess:

    **⬆️ Too Low:** Your number is higher.

    **⬇️ Too High:** Your number is lower.

    **✅ Correct:** The computer found your number!

    - Help the computer find your number within **60 seconds**.
    """)

    st.info("💡 Be honest with your feedback to help the computer win!")

    if st.button("🚀 START GAME", type="primary",
                 use_container_width=True):
        start_game()
        st.rerun()

    footer()

# ---------------- GAME SCREEN ----------------
elif st.session_state.status == "playing":

    @st.fragment(run_every="1s")
    def game_screen():
        if st.session_state.status != "playing":
            return

        check_timer()

        if st.session_state.status != "playing":
            st.rerun()
            return

        header()

        remaining = st.session_state.remaining_time

        st.markdown(
            f"<div class='section-label'>⏱️ {remaining} SECONDS REMAINING</div>",
            unsafe_allow_html=True
        )
        st.progress(remaining / GAME_TIME)

        # Computer guess
        st.markdown(f"""
        <div class="guess-card">
            <div class="guess-label">🤖 COMPUTER'S CURRENT GUESS</div>
            <div class="guess-number">{st.session_state.guess}</div>
            <div class="guess-hint">Is this your secret number?</div>
        </div>
        """, unsafe_allow_html=True)

        # Statistics
        col1, col2, col3 = st.columns(3)

        stats = [
            ("🎯 ATTEMPTS", st.session_state.guesses),
            ("🔽 LOWER", st.session_state.low),
            ("🔼 UPPER", st.session_state.high)
        ]

        for col, (label, value) in zip([col1, col2, col3], stats):
            with col:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value">{value}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(
            '<div class="section-label">📢 YOUR FEEDBACK</div>',
            unsafe_allow_html=True
        )

        st.caption("Choose one response based on the computer's guess.")

        # Large feedback buttons
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("⬆️ TOO LOW", use_container_width=True,
                         key="too_low"):
                process_feedback("Too Low")
                st.rerun()

        with col2:
            if st.button("⬇️ TOO HIGH", use_container_width=True,
                         key="too_high"):
                process_feedback("Too High")
                st.rerun()

        with col3:
            if st.button("✅ CORRECT", type="primary",
                         use_container_width=True, key="correct"):
                process_feedback("Correct")
                st.rerun()

        # Visual feedback
        feedback = st.session_state.feedback

        if feedback:
            messages = {
                "Too Low": "⬆️ Your number is higher. The computer is adjusting its range!",
                "Too High": "⬇️ Your number is lower. The computer is adjusting its range!",
                "Correct": "🎉 The computer found your number!"
            }
            st.markdown(
                f'<div class="feedback-note">{messages[feedback]}</div>',
                unsafe_allow_html=True
            )

        st.caption(
            f"Possible range: {st.session_state.low} – "
            f"{st.session_state.high}"
        )

    game_screen()

# ---------------- RESULT SCREEN ----------------
elif st.session_state.status == "finished":
    header()

    result = st.session_state.result
    success = result.startswith("The computer successfully")

    if success:
        icon = "🏆"
        title = "COMPUTER WINS!"
    elif result.startswith("Time is up"):
        icon = "⏰"
        title = "TIME'S UP!"
    else:
        icon = "⚠️"
        title = "GAME OVER"

    st.markdown(f"""
    <div class="result-card">
        <div style="font-size:65px;">{icon}</div>
        <div style="font-size:27px;font-weight:800;color:white;">
            {title}
        </div>
        <p style="color:#cbd5e1;">{result}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🎯 Total Attempts", st.session_state.guesses)

    with col2:
        st.metric("⏱️ Time Limit", "60 seconds")

    if success:
        st.success("Your secret number was successfully discovered!")
    elif result.startswith("Time is up"):
        st.warning("The computer did not confirm your secret number.")
    else:
        st.error("Your feedback eliminated every possible number.")

    if st.button("🔄 PLAY AGAIN", type="primary",
                 use_container_width=True):
        initialize_game()
        st.rerun()

    footer()
