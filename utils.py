import streamlit as st
import subprocess
import os
import tempfile

# ==========================================
# 1. STYLING & INITIALIZATION
# ==========================================
def load_css():
    st.markdown("""<style>
        .stApp, .stMarkdown, p, span { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        [data-testid="stSidebar"] { background-color: #282A35; }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #f1f1f1; }
        #MainMenu, footer { visibility: hidden; }
        
        .terminal-history {
            background-color: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 5px;
            font-family: 'Consolas', monospace; font-size: 14px;
            border-left: 4px solid #4CAF50; margin-bottom: 10px; min-height: 100px; max-height: 400px; overflow-y: auto;
        }
        .cmd-line { color: #4CAF50; margin-bottom: 2px; }
        .cmd-out { color: #ffffff; white-space: pre-wrap; margin-bottom: 15px; border-bottom: 1px solid #333; padding-bottom: 10px;}
    </style>""", unsafe_allow_html=True)

def init_bash_sandbox():
    if 'sandbox_dir' not in st.session_state:
        st.session_state.sandbox_dir = tempfile.mkdtemp(prefix="bash_tutorial_")
        with open(f"{st.session_state.sandbox_dir}/hello.txt", "w") as f:
            f.write("Hello, Linux Learner!\nLine 2: This is a test file.\nLine 3: End of file.")
        with open(f"{st.session_state.sandbox_dir}/data.csv", "w") as f:
            f.write("Name,Age,City\nAlice,30,New York\nBob,25,London\nCharlie,35,Paris")
        os.makedirs(f"{st.session_state.sandbox_dir}/my_folder", exist_ok=True)
        
    if 'term_history' not in st.session_state:
        st.session_state.term_history = []

# ==========================================
# 2. BASH EXECUTION ENGINE (FIXED FOR CLOUD)
# ==========================================
def run_bash_command(command):
    DANGEROUS = ["rm -rf /", "sudo", "su ", "mkfs", "dd if=", "> /dev/sda", ":(){ :|:& };:"]
    INTERACTIVE = ["top", "vim", "vi", "nano", "less", "more", "ssh", "telnet"]
    
    if any(d in command for d in DANGEROUS): return "🚫 Security Error: Dangerous command blocked."
    if command.split()[0] in INTERACTIVE: return f"🖥️ [SIMULATED] '{command.split()[0]}' requires an interactive TTY screen."
    
    try:
        # CRITICAL FIX: Added executable='/bin/bash' so commands like 'alias' don't crash the cloud server
        result = subprocess.run(
            command, 
            shell=True, 
            executable='/bin/bash', 
            cwd=st.session_state.sandbox_dir, 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        output = result.stdout + (f"\n[stderr]\n{result.stderr}" if result.stderr else "")
        return output if output else "(Command executed successfully)"
    except Exception as e: return f"⚠️ Error: {str(e)}"

# ==========================================
# 3. REUSABLE UI COMPONENTS
# ==========================================
def app_header(title, subtitle):
    st.markdown(f"<h1 style='color:#4CAF50;'>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:16px; color:#888;'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown("---")

def progress_sidebar():
    st.sidebar.markdown("### 📊 Progress Tracker")
    pages = ["Bash Intro", "Basic Commands", "Text Processing", "System Monitoring", 
             "Networking", "Compression", "Permissions", "Scripting", "Quiz"]
    for p in pages:
        st.sidebar.checkbox(p, key=f"progress_{p}")

def render_lesson(title, content, example_cmd):
    """Renders a specific lesson block with a 'Try it' button."""
    st.markdown(f"### {title}")
    st.markdown(content)
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button(f"▶️ Run", key=f"btn_{title.replace(' ', '_')}"):
            out = run_bash_command(example_cmd)
            st.session_state.term_history.append({"cmd": example_cmd, "out": out})
            # CRITICAL FIX: Removed st.rerun() here. It causes Streamlit to crash inside loops.
    with col2:
        st.code(example_cmd, language="bash")
    st.markdown("---")

def render_live_terminal():
    """Renders the persistent Linux terminal at the bottom of the page."""
    st.subheader("🖥️ Live Linux Terminal")
    st.caption("Type your own commands below. Press Enter to execute.")

    if st.session_state.term_history:
        history_html = "<div class='terminal-history'>"
        for item in st.session_state.term_history:
            safe_out = item['out'].replace("<", "&lt;").replace(">", "&gt;")
            history_html += f"<div class='cmd-line'>student@linux-sandbox:~$ {item['cmd']}</div><div class='cmd-out'>{safe_out}</div>"
        history_html += "</div>"
        st.markdown(history_html, unsafe_allow_html=True)
    else:
        st.markdown("<div class='terminal-history' style='color:#666;'>Terminal output will appear here...</div>", unsafe_allow_html=True)

    if user_cmd := st.chat_input("student@linux-sandbox:~$"):
        out = run_bash_command(user_cmd)
        st.session_state.term_history.append({"cmd": user_cmd, "out": out})
        # Removed st.rerun() here as well to prevent cloud exceptions. Streamlit handles chat input clearing natively now.