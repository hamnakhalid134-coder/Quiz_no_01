import streamlit as st
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
    (
        "Which of these is a Python list?",
        ["[10, 20, 30]", "(10, 20, 30)", '{"a": 10, "b": 20}', "{10, 20, 30}"],
        0
    ),
    (
        "Which of these is a Python tuple?",
        ["(10, 20, 30)", "[10, 20, 30]", '{"x": 10}', "{10, 20, 30}"],
        0
    ),
    (
        "Which of these is a Python dictionary?",
        ['{"name": "Ali", "age": 14}', '["Ali", 14]', '("Ali", 14)', '{"Ali", 14}'],
        0
    ),
    (
        "Which statement about a Python list is true?",
        [
            "A list can be changed after it is created",
            "A list can never be changed",
            "A list can store only numbers",
            "A list can contain only one item"
        ],
        0
    ),
    (
        "Which collection is useful when values should stay fixed?",
        ["Tuple", "List", "Dictionary", "Loop"],
        0
    ),
    (
        "Which method adds one item to the end of a list?",
        ["append()", "remove()", "sort()", "keys()"],
        0
    ),
    (
        "Which method adds an item at a specific position in a list?",
        ["insert()", "append()", "count()", "values()"],
        0
    ),
    (
        "Which method arranges list items in order?",
        ["sort()", "pop()", "append()", "items()"],
        0
    ),
    (
        "Which method tells how many times a value appears in a list or tuple?",
        ["count()", "append()", "remove()", "clear()"],
        0
    ),
    (
        "Which method removes an item from a list by index?",
        ["pop()", "sort()", "insert()", "copy()"],
        0
    ),
    (
        "What is slicing mainly used for?",
        [
            "Getting a part of a list or tuple",
            "Deleting a dictionary",
            "Creating a loop",
            "Sorting all values"
        ],
        0
    ),
    (
        "Which method gives all keys from a dictionary?",
        ["keys()", "values()", "append()", "sort()"],
        0
    ),
    (
        "Which method gives all values from a dictionary?",
        ["values()", "keys()", "insert()", "count()"],
        0
    ),
    (
        "Which method gives both dictionary keys and values together?",
        ["items()", "keys()", "values()", "append()"],
        0
    ),
    (
        "What is the main difference between a list and a dictionary?",
        [
            "Lists use positions; dictionaries use keys",
            "Lists cannot store text",
            "Dictionaries cannot be changed",
            "Lists always need key-value pairs"
        ],
        0
    ),
    (
        "Which is the correct syntax of an if-else statement?",
        [
            "if condition:\n    statement\nelse:\n    statement",
            "if condition\n    statement\nelse\n    statement",
            "if (condition)\n    statement\nelse",
            "if condition:\n    statement\nelif"
        ],
        0
    ),
    (
        "Which symbol separates a key from its value in a dictionary?",
        [":", ",", "=", ";"],
        0
    ),
    (
        "What does break do inside a loop?",
        [
            "Stops the loop immediately",
            "Skips only the current iteration",
            "Starts the loop again",
            "Creates a new loop"
        ],
        0
    ),
    (
        "Which method finds the position of a value in a list?",
        ["index()", "count()", "sort()", "append()"],
        0
    ),
    (
        "What does continue do inside a loop?",
        [
            "Skips the remaining code in the current iteration and moves to the next one",
            "Stops the loop completely",
            "Ends the whole program",
            "Repeats the same iteration forever"
        ],
        0
    )
]

# ---------------- STYLE ----------------

st.markdown(
    """
    <style>
    .block-container {
        max-width: 780px;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    .quiz-head {
        background: #2563EB;
        border-radius: 14px;
        padding: 18px 12px;
        text-align: center;
        margin-bottom: 14px;
    }

    .quiz-head h1 {
        color: white !important;
        margin: 0;
        font-size: 2rem;
        line-height: 1.15;
    }

    .quiz-head p {
        color: white !important;
        margin: 6px 0 0 0;
        font-size: 1rem;
    }

    .timer {
        text-align: right;
        font-weight: 700;
        font-size: 1rem;
        color: #dc2626;
    }

    div[data-testid="stRadio"] {
        margin-top: -0.5rem;
    }

    div[data-testid="stRadio"] label {
        padding-top: 0.1rem;
        padding-bottom: 0.1rem;
    }

    div.stButton > button {
        min-height: 2.6rem;
        font-weight: 700;
    }

    .stProgress {
        margin-top: -0.2rem;
        margin-bottom: -0.4rem;
    }

    @media (max-width: 700px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 0.6rem;
        }

        .quiz-head h1 {
            font-size: 1.6rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- FUNCTIONS ----------------

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


def reset_quiz():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def submit_answer():
    q_no = st.session_state.q_no
    q, opts, ans = st.session_state.quiz[q_no]
    choice = st.session_state.get(f"choice_{q_no}")

    if choice is None:
        st.session_state.warning = True
        return

    st.session_state.warning = False
    correct = opts[ans]
    is_correct = choice == correct

    st.session_state.answers.append(
        {
            "question": q,
            "selected": choice,
            "correct_answer": correct,
            "is_correct": is_correct
        }
    )

    if is_correct:
        st.session_state.score += 1

    # Last question -> go directly to result screen
    if q_no == len(st.session_state.quiz) - 1:
        st.session_state.finished = True
    else:
        st.session_state.q_no += 1

    st.rerun()


# ---------------- SESSION STATE ----------------

if "started" not in st.session_state:
    st.session_state.started = False

if "finished" not in st.session_state:
    st.session_state.finished = False

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
    st.session_state.start_time = None

if "warning" not in st.session_state:
    st.session_state.warning = False


# ---------------- START SCREEN ----------------

if not st.session_state.started:
    st.markdown(
        """
        <div class="quiz-head">
            <h1>Python Revision Quiz</h1>
            <p>20 Questions • 20 Minutes</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    student_name = st.text_input("Enter your name to begin:")

    if st.button("START QUIZ", type="primary", use_container_width=True):
        if not student_name.strip():
            st.warning("Please enter your name.")
        else:
            st.session_state.name = student_name.strip()
            st.session_state.quiz = make_quiz()
            st.session_state.q_no = 0
            st.session_state.score = 0
            st.session_state.answers = []
            st.session_state.start_time = time.time()
            st.session_state.started = True
            st.session_state.finished = False
            st.session_state.warning = False
            st.rerun()

    st.stop()


# ---------------- RESULT SCREEN ----------------

if st.session_state.finished:
    total = len(st.session_state.quiz)
    score = st.session_state.score
    percent = (score / total) * 100 if total else 0

    if score >= 17:
        remark = "Excellent! You are ready to move ahead."
    elif score >= 14:
        remark = "Good! Just revise a few concepts."
    elif score >= 10:
        remark = "Some concepts need revision."
    else:
        remark = "Let's revise the basics before moving ahead."

    st.markdown(
        """
        <div class="quiz-head">
            <h1>Quiz Complete</h1>
            <p>Your final result</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader(f"Player: {st.session_state.name}")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Score", f"{score} / {total}")
    with c2:
        st.metric("Percentage", f"{percent:.0f}%")

    st.info(remark)

    wrong = [x for x in st.session_state.answers if not x["is_correct"]]

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
        reset_quiz()

    st.stop()


# ---------------- LIVE TIMER ----------------

@st.fragment(run_every="1s")
def timer():
    if st.session_state.finished or st.session_state.start_time is None:
        return

    elapsed = int(time.time() - st.session_state.start_time)
    left = max(0, (20 * 60) - elapsed)
    mins, secs = divmod(left, 60)

    st.markdown(
        f'<div class="timer">Time Left: {mins:02d}:{secs:02d}</div>',
        unsafe_allow_html=True
    )

    if left == 0:
        st.session_state.finished = True
        st.rerun()


# ---------------- QUIZ SCREEN ----------------

top1, top2 = st.columns([2, 1])

with top1:
    st.write(f"**Player:** {st.session_state.name}")

with top2:
    timer()

q_no = st.session_state.q_no
total = len(st.session_state.quiz)

q, opts, ans = st.session_state.quiz[q_no]

st.progress((q_no + 1) / total)
st.caption(f"Question {q_no + 1} of {total}")

st.markdown(f"### {q_no + 1}. {q}")

st.radio(
    "Choose one answer:",
    opts,
    index=None,
    key=f"choice_{q_no}"
)

if st.session_state.warning:
    st.warning("Please select one option.")

button_text = "SUBMIT QUIZ" if q_no == total - 1 else "NEXT"

if st.button(button_text, type="primary", use_container_width=True):
    submit_answer()
