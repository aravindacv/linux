import streamlit as st
import subprocess
import os
import tempfile

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Bash Tutorial - Live Linux Terminal-CVA",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. STATE INITIALIZATION
# ==========================================
# Initialize Sandbox Directory
if 'sandbox_dir' not in st.session_state:
    st.session_state.sandbox_dir = tempfile.mkdtemp(prefix="bash_tutorial_")
    with open(f"{st.session_state.sandbox_dir}/hello.txt", "w") as f:
        f.write("Hello, Linux Learner!\nLine 2: This is a test file.\nLine 3: End of file.")
    with open(f"{st.session_state.sandbox_dir}/data.csv", "w") as f:
        f.write("Name,Age,City\nAlice,30,New York\nBob,25,London\nCharlie,35,Paris")
    os.makedirs(f"{st.session_state.sandbox_dir}/my_folder", exist_ok=True)

# Initialize Navigation State
if 'page' not in st.session_state:
    st.session_state.page = "Bash Intro"

# Initialize Terminal History
if 'term_history' not in st.session_state:
    st.session_state.term_history = []

# ==========================================
# 3. SECURITY & EXECUTION ENGINE
# ==========================================
DANGEROUS_COMMANDS = ["rm -rf /", "sudo", "su ", "mkfs", "dd if=", "> /dev/sda", ":(){ :|:& };:", "chmod -R 777 /"]
INTERACTIVE_COMMANDS = ["top", "vim", "vi", "nano", "less", "more", "ssh", "telnet"]

def is_safe(command):
    for dangerous in DANGEROUS_COMMANDS:
        if dangerous in command: return False
    return True

def run_bash_command(command):
    if not is_safe(command):
        return "🚫 Security Error: Dangerous commands are blocked in this sandbox."
    base_cmd = command.split()[0] if command.split() else ""
    if base_cmd in INTERACTIVE_COMMANDS:
        return f"🖥️ [SIMULATED] '{base_cmd}' requires an interactive TTY screen and cannot run in a web browser."
    try:
        result = subprocess.run(command, shell=True, cwd=st.session_state.sandbox_dir, capture_output=True, text=True, timeout=5)
        output = ""
        if result.stdout: output += result.stdout
        if result.stderr:
            if "Operation not permitted" in result.stderr or "Permission denied" in result.stderr:
                output += f"[Permission Denied]\n{result.stderr}\nNote: You are a restricted user on this cloud sandbox."
            else:
                output += f"[stderr]\n{result.stderr}"
        return output if output else "(Command executed successfully)"
    except subprocess.TimeoutExpired: return "⏱️ Error: Command timed out."
    except Exception as e: return f"⚠️ Error: {str(e)}"

# ==========================================
# 4. NAVIGATION CALLBACKS
# ==========================================
def change_page(page_name):
    st.session_state.page = page_name

def run_example_cmd(cmd):
    if cmd:
        output = run_bash_command(cmd)
        st.session_state.term_history.append({"cmd": cmd, "out": output})

# ==========================================
# 5. W3SCHOOLS-STYLE CSS
# ==========================================
st.markdown("""
<style>
    .stApp, .stMarkdown, p, span { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    [data-testid="stSidebar"] { background-color: #282A35; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #f1f1f1; font-size: 14px; }
    [data-testid="stSidebar"] button { 
        color: #f1f1f1; background-color: transparent; border: none; text-align: left; 
        border-radius: 3px; margin-bottom: 2px; padding: 8px 10px; width: 100%; font-size: 14px;
    }
    [data-testid="stSidebar"] button:hover { background-color: #000000; color: #4CAF50; }
    #MainMenu, footer { visibility: hidden; }
    
    .terminal-history {
        background-color: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 5px;
        font-family: 'Consolas', 'Courier New', monospace; font-size: 14px;
        border-left: 4px solid #4CAF50; margin-bottom: 10px; min-height: 100px; max-height: 400px; overflow-y: auto;
    }
    .cmd-line { color: #4CAF50; margin-bottom: 2px; }
    .cmd-out { color: #ffffff; white-space: pre-wrap; margin-bottom: 15px; border-bottom: 1px solid #333; padding-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 6. COMPREHENSIVE TUTORIAL DATABASE
# ==========================================
# Flattened structure for flawless navigation
TUTORIALS = {
    "Bash Intro": {"cat": "HOME", "title": "Bash Introduction", "content": "**What is Bash?**\nBash (Bourne Again SHell) is a Unix shell and command language interpreter. It is the default login shell for most Linux distributions and macOS.\n\n**What is a Shell?**\nA shell is a special program that provides an interface between the user and the operating system. When you type a command, the shell interprets it and tells the OS kernel to execute it.\n\n**Why Learn Bash?**\n- **Automation:** Write scripts to automate repetitive tasks.\n- **Server Administration:** Almost all servers are managed via command line.\n- **DevOps & Cloud:** Essential for Docker, Kubernetes, AWS, and CI/CD pipelines.", "example": "echo 'Welcome to Bash!'"},
    
    "Bash Get Started": {"cat": "HOME", "title": "Getting Started", "content": "To access Bash, you open a **Terminal** application. When you open a terminal, you are placed inside your **home directory**.\n\n**The Prompt**\nYou will see a prompt that looks something like this:\n`user@hostname:~$`\n- `user`: Your username.\n- `hostname`: The name of the computer.\n- `~`: Represents your home directory.\n- `$`: Indicates you are a standard user.\n\n**Command Syntax**\n`command [options] [arguments]`", "example": "whoami"},
    
    "Bash List (ls)": {"cat": "BASIC COMMANDS", "title": "List Files (ls)", "content": "The `ls` command lists the files and directories in your current location.\n\n**Common Options:**\n- `ls -l`: Long listing format (permissions, owner, size).\n- `ls -a`: Shows **all** files, including hidden files (starting with `.`).\n- `ls -h`: Human-readable sizes (e.g., 1K, 234M). Used with `-l`.", "example": "ls -lah"},
    
    "Bash Change Dir (cd)": {"cat": "BASIC COMMANDS", "title": "Change Directory (cd)", "content": "`cd` stands for **C**hange **D**irectory.\n\n**Path Types:**\n- **Absolute Path:** Starts from root `/` (e.g., `cd /var/log`).\n- **Relative Path:** Starts from current location (e.g., `cd my_folder`).\n\n**Shortcuts:**\n- `cd` or `cd ~`: Go to home directory.\n- `cd ..`: Move up one level.\n- `cd -`: Go back to previous directory.", "example": "cd my_folder && pwd && cd .."},
    
    "Bash Print Dir (pwd)": {"cat": "BASIC COMMANDS", "title": "Print Working Directory (pwd)", "content": "`pwd` stands for **P**rint **W**orking **D**irectory. It outputs the full, absolute path of the directory you are currently in.", "example": "pwd"},
    
    "Bash Concatenate (cat)": {"cat": "BASIC COMMANDS", "title": "Concatenate (cat)", "content": "`cat` reads data from files and outputs their contents.\n\n**Uses:**\n- `cat file.txt`: Display the whole file.\n- `cat file1 file2 > combined`: Combine files.\n\n*Note: There is a `hello.txt` file in your sandbox.*", "example": "cat hello.txt"},
    
    "Bash Copy (cp)": {"cat": "BASIC COMMANDS", "title": "Copy (cp)", "content": "`cp` copies files or directories.\n\n**Syntax:**\n- `cp source dest`: Copies a file.\n- `cp -r source_dir dest_dir`: `-r` (recursive) is required to copy a folder.", "example": "cp hello.txt backup.txt && ls"},
    
    "Bash Remove (rm)": {"cat": "BASIC COMMANDS", "title": "Remove (rm)", "content": "`rm` deletes files or directories. **Warning:** Linux does not have a Recycle Bin. When you use `rm`, the file is gone forever.\n\n**Syntax:**\n- `rm file.txt`: Deletes a file.\n- `rm -r folder/`: Deletes a folder and contents.", "example": "cp hello.txt safe_delete.txt && rm safe_delete.txt && ls"},
    
    "Bash Search Text (grep)": {"cat": "TEXT PROCESSING", "title": "Search Text (grep)", "content": "`grep` searches for a specific pattern inside files. It stands for Global Regular Expression Print.\n\n**Options:**\n- `grep 'word' file`: Finds lines containing 'word'.\n- `grep -i 'word' file`: Case-insensitive.\n- `grep -n 'word' file`: Shows line numbers.", "example": "grep 'Alice' data.csv"},
    
    "Bash Stream Editor (sed)": {"cat": "TEXT PROCESSING", "title": "Stream Editor (sed)", "content": "`sed` is used for filtering and transforming text.\n\n**Find and Replace:**\n`sed 's/old/new/g' file`\n- `s`: Substitute command.\n- `g`: Global flag (replaces all occurrences).", "example": "sed 's/Hello/Hi/g' hello.txt"},
    
    "Bash Variables": {"cat": "SCRIPTING", "title": "Bash Variables", "content": "Variables store data.\n**Rules:**\n1. No spaces around the `=` sign.\n2. Access the value using `$`.\n3. Put strings with spaces inside quotes.\n\n```bash\nNAME=\"John\"\necho \"Hello $NAME\"\n```", "example": "MY_OS=\"Linux\" && echo \"I love $MY_OS\""},
    
    "Bash Loops": {"cat": "SCRIPTING", "title": "Bash Loops", "content": "Loops repeat commands.\n\n**For Loop:**\n```bash\nfor i in 1 2 3; do\n  echo \"Number: $i\"\ndone\n```", "example": "for i in apple banana cherry; do echo \"Fruit: $i\"; done"},
}

# Extract categories and order for sidebar
CATEGORIES = ["HOME", "BASIC COMMANDS", "TEXT PROCESSING", "SYSTEM MONITORING", "NETWORKING", "FILE COMPRESSION", "FILE PERMISSIONS", "SCRIPTING"]
PAGE_ORDER = list(TUTORIALS.keys())

# ==========================================
# 7. SIDEBAR NAVIGATION UI
# ==========================================
st.sidebar.markdown("### 📚 Navigation")
st.sidebar.markdown("---")

for cat in CATEGORIES:
    st.sidebar.markdown(f"<div style='color:#aaa; font-weight:bold; margin-top:15px; font-size:13px; text-transform:uppercase; letter-spacing: 1px;'>📂 {cat}</div>", unsafe_allow_html=True)
    
    for page_name, data in TUTORIALS.items():
        if data["cat"] == cat:
            # Use on_click to guarantee state update without full script re-execution bugs
            if st.button(f"⚡ {page_name}", key=f"nav_{page_name}", on_click=change_page, args=(page_name,)):
                pass

# ==========================================
# 8. MAIN CONTENT AREA
# ==========================================
st.markdown("<h1 style='color:#4CAF50;'>💻 Learn Bash in a Live Sandbox</h1>", unsafe_allow_html=True)
st.markdown("---")

# Get current page data
current_data = TUTORIALS.get(st.session_state.page)
st.markdown(f"## {current_data['title']}")
st.markdown(current_data['content'])

# --- Click to Execute Feature ---
st.markdown("---")
col_ex1, col_ex2 = st.columns([1, 5])
with col_ex1:
    st.button("⚡ Run Example", key="run_example_btn", on_click=run_example_cmd, args=(current_data['example'],))
with col_ex2:
    st.code(current_data['example'], language="bash")

# --- Real-Time Terminal Simulator ---
st.markdown("### 🖥️ Live Terminal")
st.caption("Type your command below and press **Enter** to execute.")

# Display Terminal History
if st.session_state.term_history:
    history_html = "<div class='terminal-history'>"
    for item in st.session_state.term_history:
        history_html += f"<div class='cmd-line'>student@linux-sandbox:~$ {item['cmd']}</div>"
        # Escape HTML in output to prevent UI breaking
        safe_out = item['out'].replace("<", "&lt;").replace(">", "&gt;")
        history_html += f"<div class='cmd-out'>{safe_out}</div>"
    history_html += "</div>"
    st.markdown(history_html, unsafe_allow_html=True)
else:
    st.markdown("<div class='terminal-history' style='color: #666;'>Terminal output will appear here...</div>", unsafe_allow_html=True)

# The Input Field (Acts like the terminal prompt)
# Using st.chat_input because it clears itself after pressing Enter, mimicking a real CLI
if user_cmd := st.chat_input("student@linux-sandbox:~$", key="term_input"):
    output = run_bash_command(user_cmd)
    st.session_state.term_history.append({"cmd": user_cmd, "out": output})
    st.rerun() # Rerun to show the new history and clear the input box

# --- Previous / Next Navigation ---
st.markdown("---")
current_idx = PAGE_ORDER.index(st.session_state.page)
col_prev, col_spacer, col_next = st.columns([1, 2, 1])

with col_prev:
    if current_idx > 0:
        prev_page = PAGE_ORDER[current_idx - 1]
        st.button("⬅️ Previous", on_click=change_page, args=(prev_page,), use_container_width=True)

with col_next:
    if current_idx < len(PAGE_ORDER) - 1:
        next_page = PAGE_ORDER[current_idx + 1]
        st.button("Next ➡️", on_click=change_page, args=(next_page,), use_container_width=True)