# =========================
# Bash Tutorial — Interactive No-Code Linux Coach (Single File Architecture)
# =========================
import subprocess
import os
import tempfile
from dataclasses import dataclass
from typing import List, Dict, Any
from textwrap import dedent
import streamlit as st

# -------------------------------------------------------
# App Meta & W3CSS Accents (From Reference)
# -------------------------------------------------------
st.set_page_config(
    page_title="Bash Tutorial • No-Code Linux Coach",
    page_icon="💻",
    layout="wide",
)

W3CSS = """
<style>
h1, h2, h3 { font-weight: 700; color: #0f172a; }
.badge { display:inline-block; padding:4px 10px; border:1px solid #cbd5e1;
         border-radius:999px; background:#f8fafc; color:#0f172a; margin-right:6px;
         margin-bottom:6px; font-size:0.85rem; }
.card { border:1px solid #e5e7eb; border-radius:12px; padding:14px 16px; background:#fff; margin:8px 0; }
.card .title { font-weight:700; margin-bottom:6px; }
.card.note  { border-left:6px solid #06b6d4; }
.card.tip   { border-left:6px solid #22c55e; }
.card.warn  { border-left:6px solid #f59e0b; }
.card.exam  { border-left:6px solid #8b5cf6; }
.card.try   { border-left:6px solid #0ea5e9; }
.card.terminal { 
    border-left:6px solid #1e1e1e; 
    background-color: #1e1e1e; 
    color: #d4d4d4; 
    font-family: 'Consolas', 'Courier New', monospace; 
    border:1px solid #333;
}
.card.terminal .title { color: #4CAF50; }
</style>
"""
st.markdown(W3CSS, unsafe_allow_html=True)

# -------------------------------------------------------
# Small UI helpers (From Reference)
# -------------------------------------------------------
def chip(text: str):
    st.markdown(
        f"""<span style="display:inline-block;padding:4px 10px;border:1px solid #cbd5e1;border-radius:999px;background:#f8fafc;color:#0f172a;margin-right:6px;margin-bottom:6px;font-size:0.85rem;">{text}</span>""",
        unsafe_allow_html=True
    )

def titled_box(title: str, body: str):
    st.markdown(
        f"""
        <div style="border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;margin:8px 0;background:#ffffff">
            <div style="font-weight:700;margin-bottom:6px">{title}</div>
            <div style="color:#334155">{body}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def badge(text: str):
    st.markdown(f'<span class="badge">{text}</span>', unsafe_allow_html=True)

def card(kind: str, title: str, body: str):
    st.markdown(
        f'<div class="card {kind}"><div class="title">{title}</div><div>{body}</div></div>',
        unsafe_allow_html=True
    )

def terminal_card(title: str, body: str):
    # Escapes HTML to prevent terminal output from breaking the webpage
    safe_body = body.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
    st.markdown(
        f'<div class="card terminal"><div class="title">{title}</div><div style="white-space: pre-wrap; font-size: 14px;">{safe_body}</div></div>',
        unsafe_allow_html=True
    )

# -------------------------------------------------------
# Live Bash Engine & Sandbox
# -------------------------------------------------------
def init_bash_sandbox():
    if 'sandbox_dir' not in st.session_state:
        st.session_state.sandbox_dir = tempfile.mkdtemp(prefix="bash_tutorial_")
        with open(f"{st.session_state.sandbox_dir}/hello.txt", "w") as f:
            f.write("Hello, Linux Learner!\nLine 2: This is a test file.")
        with open(f"{st.session_state.sandbox_dir}/data.csv", "w") as f:
            f.write("Name,Age,City\nAlice,30,New York\nBob,25,London")
        os.makedirs(f"{st.session_state.sandbox_dir}/my_folder", exist_ok=True)
    if 'term_history' not in st.session_state:
        st.session_state.term_history = []

def run_bash_command(command):
    DANGEROUS = ["rm -rf /", "sudo", "su ", "mkfs", "dd if="]
    INTERACTIVE = ["top", "vim", "vi", "nano", "less", "more", "ssh", "telnet"]
    if any(d in command for d in DANGEROUS): return "🚫 Security Error: Dangerous command blocked."
    if command.split()[0] in INTERACTIVE: return f"🖥️ [SIMULATED] '{command.split()[0]}' requires an interactive TTY screen."
    try:
        result = subprocess.run(command, shell=True, executable='/bin/bash', cwd=st.session_state.sandbox_dir, capture_output=True, text=True, timeout=5)
        output = result.stdout + (f"\n[stderr]\n{result.stderr}" if result.stderr else "")
        return output if output else "(Command executed successfully)"
    except Exception as e: return f"⚠️ Error: {str(e)}"

# -------------------------------------------------------
# Lesson Data Structure
# -------------------------------------------------------
@dataclass
class Lesson:
    id: str
    title: str
    theory: str
    demo_cmd: str
    quiz: List[Dict[str, Any]]

def get_lessons() -> List[Lesson]:
    return [
        Lesson("intro", "Bash Introduction", 
               "Bash (Bourne Again SHell) is a Unix shell and command language interpreter. It is the default login shell for most Linux distributions. A shell provides an interface between the user and the operating system kernel.", 
               "echo $BASH_VERSION", 
               [{"q": "What does Bash stand for?", "options": ["Bourne Again SHell", "Basic Shell", "Binary Shell", "Boot Shell"], "answer": 0, "explain": "Bourne Again SHell."}]),
        
        Lesson("basic_ls", "Command: ls (List)", 
               "Lists files and directories. Use `ls -lah` for a long listing with human-readable sizes and hidden files.", 
               "ls -lah", 
               [{"q": "Which flag shows hidden files?", "options": ["-l", "-a", "-h", "-r"], "answer": 1, "explain": "-a shows all files, including those starting with a dot."}]),
        
        Lesson("basic_cd", "Command: cd (Change Dir)", 
               "Changes your current working directory. `cd ..` moves up one level. `cd ~` goes to your home directory.", 
               "cd my_folder && pwd && cd ..", 
               [{"q": "What does `cd ..` do?", "options": ["Goes to root", "Moves up one level", "Goes home", "Lists files"], "answer": 1, "explain": "Double dot refers to the parent directory."}]),

        Lesson("basic_cat", "Command: cat (Read)", 
               "Reads data from files and outputs their contents. There is a `hello.txt` file in your sandbox.", 
               "cat hello.txt", 
               [{"q": "What is cat short for?", "options": ["category", "concatenate", "catalog", "capture"], "answer": 1, "explain": "It was originally designed to concatenate files."}]),

        Lesson("basic_grep", "Command: grep (Search)", 
               "Searches for a specific pattern inside files. Use `grep 'Alice' data.csv` to find Alice in the CSV.", 
               "grep 'Alice' data.csv", 
               [{"q": "Which flag makes grep case-insensitive?", "options": ["-n", "-c", "-i", "-r"], "answer": 2, "explain": "-i ignores case."}]),

        Lesson("scripting_vars", "Scripting: Variables", 
               "Variables store data. **No spaces around `=`**. Access the value using a dollar sign `$`.", 
               "MY_OS=\"Linux\" && echo \"I love $MY_OS\"", 
               [{"q": "How do you read a variable?", "options": ["NAME", "$NAME", "%NAME%", "&NAME"], "answer": 1, "explain": "The dollar sign prefixes the variable name."}]),
               
        Lesson("scripting_loops", "Scripting: Loops", 
               "Loops repeat commands. A basic for loop iterates over a list of items.", 
               "for i in apple banana cherry; do echo \"Fruit: $i\"; done", 
               [{"q": "What signifies the end of a loop block?", "options": ["end", "done", "fi", "stop"], "answer": 1, "explain": "Bash uses 'done' to close for/while loops."}]),
    ]

# -------------------------------------------------------
# Quiz Helper (From Reference)
# -------------------------------------------------------
def quiz_block(questions: List[Dict[str, Any]], key_prefix: str):
    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}. {q['q']}**")
        choice = st.radio(
            f"{key_prefix}_q{i}", q["options"], key=f"{key_prefix}_q{i}", index=0, label_visibility="collapsed"
        )
        if st.button(f"Check Q{i+1}", key=f"{key_prefix}_btn{i}"):
            idx = q["options"].index(choice)
            if idx == q["answer"]:
                card("tip", "Correct ✅", q["explain"])
            else:
                card("warn", "Not quite ❌", q["explain"])

# -------------------------------------------------------
# Main App Logic
# -------------------------------------------------------
def main():
    init_bash_sandbox()
    lessons = get_lessons()

    # --- Sidebar Navigation (Replaces Multi-Page) ---
    with st.sidebar:
        st.markdown("### 📚 Navigation")
        page_names = ["🏠 Home"] + [f"⚡ {l.title}" for l in lessons]
        # Using st.radio for bulletproof single-file navigation
        selected_page = st.radio("Go to", page_names, label_visibility="collapsed")
        
        st.markdown("---")
        st.markdown("### 📊 Progress")
        for l in lessons:
            st.checkbox(l.title, key=f"progress_{l.id}")

    # --- Page Routing ---
    if selected_page == "🏠 Home":
        st.title("Bash Tutorial — Interactive Tutor")
        st.markdown("Basic Commands • Text Processing • Scripting • System Monitoring\n\nUse the sidebar to navigate units. Your terminal session persists!")
        
        titled_box("How this works", 
                   "Each unit is its own section with a no-code runnable example.\n"
                   "Click **Run Example** to see it execute in the Live Terminal.\n"
                   "You can type your own custom commands in the terminal at the bottom.")
        
        chip("W3Schools Style")
        chip("Live Sandbox")
        chip("No-Code Demos")

    else:
        # Find the matching lesson
        current_lesson = next((l for l in lessons if f"⚡ {l.title}" == selected_page), None)
        
        if current_lesson:
            st.header(current_lesson.title)
            
            # 1. Theory
            card("note", "Concept", current_lesson.theory)
            
            # 2. One-Click No-Code Demo
            st.markdown("#### 🚀 No-Code Live Demo")
            if st.button(f"▶️ Run Example Command", key=f"run_{current_lesson.id}"):
                output = run_bash_command(current_lesson.demo_cmd)
                st.session_state.term_history.append({"cmd": current_lesson.demo_cmd, "out": output})
            
            st.code(current_lesson.demo_cmd, language="bash")

            # 3. Quiz Block
            st.markdown("---")
            quiz_block(current_lesson.quiz, f"quiz_{current_lesson.id}")

    # --- Global Persistent Terminal (At the bottom of every page) ---
    st.markdown("---")
    st.subheader("🖥️ Free-Play Linux Terminal")
    st.caption("Type any Linux command and press Enter.")

    # Render History using the W3CSS terminal card
    for item in reversed(st.session_state.term_history):
        terminal_card(f"student@linux:~$ {item['cmd']}", item['out'])

    # Chat input for commands
    if user_cmd := st.chat_input("student@linux-sandbox:~$"):
        if user_cmd.strip():
            out = run_bash_command(user_cmd)
            st.session_state.term_history.append({"cmd": user_cmd, "out": out})
            st.rerun()

if __name__ == "__main__":
    main()