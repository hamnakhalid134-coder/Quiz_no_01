import streamlit as st
import streamlit.components.v1 as components
import random
import time

st.set_page_config(
    page_title="Python Revision Quiz",
    page_icon="🐍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- QUESTIONS ----------------

questions = [
    ("Which of these is a Python list?",
     ["[10, 20, 30]", "(10, 20, 30)", '{"a": 10, "b": 20}', "{10, 20, 30}"], 0),

    ("Which of these is a Python tuple?",
     ["(10, 20, 30)", "[10, 20, 30]", '{"x": 10}', "{10, 20, 30}"], 0),

    ("Which of these is a Python dictionary?",
     ['{"name": "Ali", "age": 14}', '["Ali", 14]', '("Ali", 14)', '{"Ali", 14}'], 0),

    ("Which statement about a Python list is true?",
     ["A list can be changed after it is created",
      "A list can never be changed",
      "A list can store only numbers",
      "A list can contain only one item"], 0),

    ("Which collection is useful when values should stay fixed?",
     ["Tuple", "List", "Dictionary", "Loop"], 0),

    ("Which method adds one item to the end of a list?",
     ["append()", "remove()", "sort()", "keys()"], 0),

    ("Which method adds an item at a specific position in a list?",
     ["insert()", "append()", "count()", "values()"], 0),

    ("Which method arranges list items in order?",
     ["sort()", "pop()", "append()", "items()"], 0),

    ("Which method tells how many times a value appears in a list or tuple?",
     ["count()", "append()", "remove()", "clear()"], 0),

    ("Which method removes an item from a list by index?",
     ["pop()", "sort()", "insert()", "copy()"], 0),

    ("What is slicing mainly used for?",
     ["Getting a part of a list or tuple",
      "Deleting a dictionary",
      "Creating a loop",
      "Sorting all values"], 0),

    ("Which method gives all keys from a dictionary?",
     ["keys()", "values()", "append()", "sort()"], 0),

    ("Which method gives all values from a dictionary?",
     ["values()", "keys()", "insert()", "count()"], 0),

    ("Which method gives both dictionary keys and values together?",
     ["items()", "keys()", "values()", "append()"], 0),

    ("What is the main difference between a list and a dictionary?",
     ["Lists use positions; dictionaries use keys",
      "Lists cannot store text",
      "Dictionaries cannot be changed",
      "Lists always need key-value pairs"], 0),

    ("Which is the correct syntax of an if-else statement?",
     ["if condition:\n    statement\nelse:\n    statement",
      "if condition\n    statement\nelse\n    statement",
      "if (condition)\n    statement\nelse",
      "if condition:\n    statement\nelif"], 0),

    ("Which symbol separates a key from its value in a dictionary?",
     [":", ",", "=", ";"], 0),

    ("What does break do inside a loop?",
     ["Stops the loop immediately",
      "Skips only the current iteration",
      "Starts the loop again",
      "Creates a new loop"], 0),

    ("Which method finds the position of a value in a list?",
     ["index()", "count()", "sort()", "append()"], 0),

    ("What does continue do inside a loop?",
     ["Skips the remaining code in the current iteration and moves to the next one",
      "Stops the loop completely",
      "Ends the whole program",
      "Repeats the same iteration forever"], 0)
]

# ---------------- STYLE ----------------

st.markdown("""
<style>
.block-container {
    max-width: 780px;
    padding-top: 0.8rem;
    padding-bottom: 1rem;
}

.quiz-head {
    background: #2563EB;
    border-radius: 14px;
    padding: 16px 12px;
    text-align: center;
    margin-bottom: 14px;
}

.quiz-head h1 {
    color: #FFFFFF !important;
    margin: 0;
    font-size: 2rem;
}

.quiz-head p {
    color: #FFFFFF !important;
    margin: 5px 0 0 0;
}

.result-card {
    background: #FFFFFF;
    color: #111827 !important;
    border: 1px solid #D1D5DB;
    border-radius: 14px;
    padding: 22px;
    margin: 12px 0;
    text-align: center;
}

.result-card h2,
.result-card h3,
.result-card p {
    color: #111827 !important;
}

.score-big {
    font-size: 2.2rem;
    font-weight: 800;
    color: #2563EB !important;
    margin: 8px 0;
}

div.stButton > button {
    min-height: 2.6rem;
    font-weight: 700;
}

div[data-testid="stRadio"] label {
    padding-top: 0.05rem;
    padding-bottom: 0.05rem;
}

@media (max-width: 700px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .quiz-head h1 {
        font-size: 1.6rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------------- HELPERS ----------------

def make_quiz():
    data = []

    for q, opts, ans in questions:
        correct = opts[ans]
        new_opts = opts.copy()
        random.shuffle(new_opts)
        new_ans = new_opts.index(correct)
        data.append((q, new_opts, new_ans))

    random.shuffle(data)
    return data


def reset_all():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


# ---------------- SESSION STATE ----------------

if "page" not in st.session_state:
    st.session_state.page = "start"

if "name" not in st.session_state:
    st.session_state.name = ""

if "quiz" not in st.session_state:
    st.session_state.quiz = []

if "q_no" not in st.session_state:
    st.session_state.q_no = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

if "start_time" not in st.session_state:
    st.session_state.start_time = 0


# ---------------- START PAGE ----------------

if st.session_state.page == "start":

    st.markdown("""
    <div class="quiz-head">
        <h1>Python Revision Quiz</h1>
        <p>20 Questions • 20 Minutes</p>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input("Enter your name to begin:")

    if st.button("START QUIZ", type="primary", use_container_width=True):

        if not name.strip():
            st.warning("Please enter your name.")

        else:
            st.session_state.name = name.strip()
            st.session_state.quiz = make_quiz()
            st.session_state.q_no = 0
            st.session_state.score = 0
            st.session_state.answers = []
            st.session_state.start_time = time.time()
            st.session_state.page = "quiz"
            st.rerun()

    st.stop()


# ---------------- RESULT PAGE ----------------

if st.session_state.page == "result":

    total = len(st.session_state.quiz)
    score = st.session_state.score

    if total == 0:
        total = 20

    percent = round((score / total) * 100)

    if score >= 17:
        remark = "Excellent! You are ready to move ahead."
    elif score >= 14:
        remark = "Good! Just revise a few concepts."
    elif score >= 10:
        remark = "Some concepts need revision."
    else:
        remark = "Let's revise the basics before moving ahead."

    st.markdown("""
    <div class="quiz-head">
        <h1>Quiz Complete</h1>
        <p>Final Result</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="result-card">
            <h3>Player: {st.session_state.name}</h3>
            <div class="score-big">{score} / {total}</div>
            <p><b>Percentage: {percent}%</b></p>
            <p>{remark}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    wrong = [a for a in st.session_state.answers if not a["is_correct"]]

    with st.expander(f"Review Wrong Answers ({len(wrong)})"):

        if len(wrong) == 0:
            st.success("Perfect score! No wrong answers.")

        else:
            for i, item in enumerate(wrong, 1):
                st.markdown(f"**{i}. {item['question']}**")
                st.write("Your Answer:", item["selected"])
                st.write("Correct Answer:", item["correct_answer"])
                st.divider()

    if st.button("RESTART QUIZ", use_container_width=True):
        reset_all()

    st.stop()


# ---------------- QUIZ PAGE ----------------

q_no = st.session_state.q_no
total = len(st.session_state.quiz)

# Safety check
if q_no >= total:
    st.session_state.page = "result"
    st.rerun()

elapsed = int(time.time() - st.session_state.start_time)
remaining = max(0, 20 * 60 - elapsed)

# Timer is visual only and does not rerun the Python quiz.
timer_html = f"""
<div style="
    text-align:right;
    font-family:Arial, sans-serif;
    font-size:16px;
    font-weight:700;
    color:#DC2626;
    padding:0;
    margin:0;
">
    Time Left: <span id="timer"></span>
</div>

<script>
let seconds = {remaining};

function updateTimer() {{
    let m = Math.floor(seconds / 60);
    let s = seconds % 60;

    document.getElementById("timer").innerText =
        String(m).padStart(2, "0") + ":" +
        String(s).padStart(2, "0");

    if (seconds > 0) {{
        seconds--;
    }}
}}

updateTimer();
setInterval(updateTimer, 1000);
</script>
"""

top1, top2 = st.columns([2, 1])

with top1:
    st.write(f"**Player:** {st.session_state.name}")

with top2:
    components.html(timer_html, height=35)

q, opts, ans = st.session_state.quiz[q_no]

st.progress((q_no + 1) / total)
st.caption(f"Question {q_no + 1} of {total}")
st.markdown(f"### {q_no + 1}. {q}")

# One form per question avoids accidental reruns while selecting an option
with st.form(key=f"question_form_{q_no}"):

    choice = st.radio(
        "Choose one answer:",
        opts,
        index=None
    )

    button_text = "SUBMIT QUIZ" if q_no == total - 1 else "NEXT"

    submitted = st.form_submit_button(
        button_text,
        type="primary",
        use_container_width=True
    )

if submitted:

    if choice is None:
        st.warning("Please select one option.")

    else:
        correct_answer = opts[ans]
        is_correct = choice == correct_answer

        st.session_state.answers.append({
            "question": q,
            "selected": choice,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })

        if is_correct:
            st.session_state.score += 1

        # Last question -> result page
        if q_no == total - 1:
            st.session_state.page = "result"

        else:
            st.session_state.q_no += 1

        st.rerun()
