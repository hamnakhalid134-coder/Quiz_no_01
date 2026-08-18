import streamlit as st
import random
import time

st.set_page_config(page_title="Python Revision Quiz", page_icon="🐍", layout="centered")

questions = [
    ("Which of these is a Python list?", ["[10, 20, 30]", "(10, 20, 30)", '{"a": 10, "b": 20}', "{10, 20, 30}"], 0),
    ("Which of these is a Python tuple?", ["(10, 20, 30)", "[10, 20, 30]", '{"x": 10}', "{10, 20, 30}"], 0),
    ("Which of these is a Python dictionary?", ['{"name": "Ali", "age": 14}', '["Ali", 14]', '("Ali", 14)', '{"Ali", 14}'], 0),
    ("Which statement about a Python list is true?", ["A list can be changed after it is created", "A list can never be changed", "A list can store only numbers", "A list can contain only one item"], 0),
    ("Which collection is useful when values should stay fixed?", ["Tuple", "List", "Dictionary", "Loop"], 0),
    ("Which method adds one item to the end of a list?", ["append()", "remove()", "sort()", "keys()"], 0),
    ("Which method adds an item at a specific position in a list?", ["insert()", "append()", "count()", "values()"], 0),
    ("Which method arranges list items in order?", ["sort()", "pop()", "append()", "items()"], 0),
    ("Which method tells how many times a value appears in a list or tuple?", ["count()", "append()", "remove()", "clear()"], 0),
    ("Which method removes an item from a list by index?", ["pop()", "sort()", "insert()", "copy()"], 0),
    ("What is slicing mainly used for?", ["Getting a part of a list or tuple", "Deleting a dictionary", "Creating a loop", "Sorting all values"], 0),
    ("Which method gives all keys from a dictionary?", ["keys()", "values()", "append()", "sort()"], 0),
    ("Which method gives all values from a dictionary?", ["values()", "keys()", "insert()", "count()"], 0),
    ("Which method gives both dictionary keys and values together?", ["items()", "keys()", "values()", "append()"], 0),
    ("What is the main difference between a list and a dictionary?", ["Lists use positions; dictionaries use keys", "Lists cannot store text", "Dictionaries cannot be changed", "Lists always need key-value pairs"], 0),
    ("Which is the correct syntax of an if-else statement?", ["if condition:\n    statement\nelse:\n    statement", "if condition\n    statement\nelse\n    statement", "if (condition)\n    statement\nelse", "if condition:\n    statement\nelif"], 0),
    ("Which symbol separates a key from its value in a dictionary?", [":", ",", "=", ";"], 0),
    ("Which method removes all items from a list or dictionary?", ["clear()", "remove()", "pop()", "delete()"], 0),
    ("Which method finds the position of a value in a list?", ["index()", "count()", "sort()", "append()"], 0),
    ("Which method adds all items of another list to an existing list?", ["extend()", "append()", "insert()", "sort()"], 0),
]

st.markdown("""
<style>
.block-container {max-width: 850px; padding-top: 2rem;}
.title-box {text-align:center; padding:22px; border-radius:16px; background:#f4f7fb; margin-bottom:20px;}
.timer {text-align:right; font-size:18px; font-weight:700; color:#b91c1c;}
div.stButton > button {width:100%;}
</style>
""", unsafe_allow_html=True)


def prepare_questions():
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
    st.session_state.clear()
    st.rerun()


def init_state():
    defaults = {
        "started": False,
        "finished": False,
        "name": "",
        "q_no": 0,
        "score": 0,
        "answers": [],
        "quiz_questions": [],
        "start_time": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()

if not st.session_state.started:
    st.markdown('<div class="title-box"><h1>Python Revision Quiz</h1><p>20 Questions • 20 Minutes</p></div>', unsafe_allow_html=True)
    name = st.text_input("Enter your name to begin:")
    if st.button("START QUIZ", type="primary"):
        if not name.strip():
            st.warning("Please enter your name.")
        else:
            st.session_state.name = name.strip()
            st.session_state.quiz_questions = prepare_questions()
            st.session_state.q_no = 0
            st.session_state.score = 0
            st.session_state.answers = []
            st.session_state.start_time = time.time()
            st.session_state.started = True
            st.session_state.finished = False
            st.rerun()
    st.stop()


@st.fragment(run_every=1)
def show_timer():
    if st.session_state.finished:
        return
    elapsed = int(time.time() - st.session_state.start_time)
    left = max(0, 20 * 60 - elapsed)
    mins, secs = divmod(left, 60)
    st.markdown(f'<div class="timer">Time Left: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
    if left <= 0:
        st.session_state.finished = True
        st.rerun()


if st.session_state.finished:
    total = len(st.session_state.quiz_questions)
    score = st.session_state.score
    percent = score / total * 100 if total else 0

    if score >= 17:
        remark = "Excellent! You are ready to move ahead."
    elif score >= 14:
        remark = "Good! Just revise a few concepts."
    elif score >= 10:
        remark = "Some concepts need revision."
    else:
        remark = "Let's revise the basics before moving ahead."

    st.markdown('<div class="title-box"><h1>Quiz Complete</h1></div>', unsafe_allow_html=True)
    st.subheader(f"Player: {st.session_state.name}")
    st.metric("Score", f"{score} / {total}")
    st.write(f"**Percentage:** {percent:.0f}%")
    st.info(remark)

    wrong = [x for x in st.session_state.answers if not x["correct"]]
    with st.expander(f"Review Wrong Answers ({len(wrong)})"):
        if not wrong:
            st.success("Perfect score! No wrong answers.")
        else:
            for i, item in enumerate(wrong, 1):
                st.markdown(f"**{i}. {item['question']}**")
                st.write("Your answer:", item["selected"])
                st.write("Correct answer:", item["correct_answer"])
                st.divider()

    if st.button("RESTART QUIZ"):
        reset_quiz()
    st.stop()

left_col, right_col = st.columns([2, 1])
with left_col:
    st.write(f"**Player:** {st.session_state.name}")
with right_col:
    show_timer()

q_no = st.session_state.q_no
total = len(st.session_state.quiz_questions)
if q_no >= total:
    st.session_state.finished = True
    st.rerun()

q, opts, ans = st.session_state.quiz_questions[q_no]
st.progress((q_no + 1) / total)
st.caption(f"Question {q_no + 1} of {total}")
st.subheader(f"{q_no + 1}. {q}")

choice = st.radio("Choose one answer:", opts, index=None, key=f"answer_{q_no}")
button_text = "SUBMIT QUIZ" if q_no == total - 1 else "NEXT"

if st.button(button_text, type="primary"):
    if choice is None:
        st.warning("Please select one option.")
    else:
        is_correct = choice == opts[ans]
        st.session_state.answers.append({
            "question": q,
            "selected": choice,
            "correct_answer": opts[ans],
            "correct": is_correct,
        })
        if is_correct:
            st.session_state.score += 1
        st.session_state.q_no += 1
        if st.session_state.q_no >= total:
            st.session_state.finished = True
        st.rerun()
