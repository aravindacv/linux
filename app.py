# =========================
# Linux-Virtual — Claymorphism UI (Sidebar Visibility Fixed)
# =========================
import subprocess
import os
import tempfile
from dataclasses import dataclass
from typing import List, Dict, Any
import streamlit as st

st.set_page_config(page_title="Linux-Virtual", page_icon="🪵", layout="wide")

CLAY_CSS = """
<style>
    /* MAIN APP BACKGROUND */
    .stApp { background-color: #e0e5ec !important; }
    
    /* FORCE DARK TEXT EVERYWHERE */
    h1, h2, h3, h4, h5, h6, p, span, li, div { 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        color: #2d3436 !important; 
    }
    h1, h2, h3 { font-weight: 800; text-shadow: 2px 2px 4px rgba(163,177,198,0.6); }

    /* FIX: FORCE SIDEBAR TO BE LIGHT (CLAYMORPHISM) SO TEXT IS VISIBLE */
    [data-testid="stSidebar"] {
        background-color: #e0e5ec !important;
        box-shadow: 4px 0 15px rgba(0,0,0,0.05);
    }
    [data-testid="stSidebar"] * {
        color: #2d3436 !important;
    }
    [data-testid="stSidebar"] label {
        font-weight: 600 !important;
    }
    /* Fix the selectbox dropdown inside the sidebar */
    [data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
        background-color: #d1d9e6 !important;
        color: #2d3436 !important;
        border: 1px solid #b8bec7 !important;
        border-radius: 10px !important;
    }

    /* CLAY CARDS */
    .card { 
        border: none; border-radius: 20px; padding: 22px 25px; background: #e0e5ec; margin: 15px 0; 
        box-shadow: 9px 9px 16px #b8bec7, -9px -9px 16px #ffffff; transition: all 0.2s ease; line-height: 1.7;
    }
    .card .title { font-weight: 800 !important; margin-bottom: 10px; font-size: 1.2rem; color: #000000 !important; }
    .card p, .card div, .card span { color: #333333 !important; }

    .card.note  { border-left: 6px solid #74b9ff; box-shadow: 9px 9px 16px #b8bec7, -9px -9px 16px #ffffff, inset 3px 0 0px #a4d0ff; }
    .card.tip   { border-left: 6px solid #55efc4; box-shadow: 9px 9px 16px #b8bec7, -9px -9px 16px #ffffff, inset 3px 0 0px #81ffdb; }
    .card.warn  { border-left: 6px solid #ffeaa7; box-shadow: 9px 9px 16px #b8bec7, -9px -9px 16px #ffffff, inset 3px 0 0px #fff3b0; }
    
    /* TERMINAL */
    .term-container {
        background: #e0e5ec; border-radius: 25px; padding: 15px;
        box-shadow: 12px 12px 24px #b8bec7, -12px -12px 24px #ffffff; margin-top: 20px;
    }
    .term-container h3 { color: #000000 !important; }
    
    .term-box {
        background-color: #2d3436; color: #dfe6e9; border-radius: 15px; padding: 20px; 
        font-family: 'Fira Code', 'Consolas', monospace; font-size: 14px;
        height: 350px; overflow-y: auto; border: none;
        box-shadow: inset 6px 6px 12px #1e2325, inset -6px -6px 12px #3c4547; 
    }
    .term-cmd { color: #00cec9; margin-bottom: 4px; white-space: pre-wrap; font-weight: bold;}
    .term-out { color: #dfe6e9; white-space: pre-wrap; margin-bottom: 15px; border-bottom: 1px solid #636e72; padding-bottom: 10px;}

    /* BUTTONS */
    .stButton > button {
        background: #e0e5ec !important; color: #2d3436 !important; border: none !important;
        border-radius: 12px !important; box-shadow: 6px 6px 12px #b8bec7, -6px -6px 12px #ffffff !important;
        font-weight: 700 !important; transition: 0.2s !important;
    }
    .stButton > button:active { box-shadow: inset 4px 4px 8px #b8bec7, inset -4px -4px 8px #ffffff !important; }
    
    /* CODE BLOCKS */
    [data-testid="stCode"] {
        background-color: #e0e5ec; border: none; border-radius: 12px;
        box-shadow: inset 4px 4px 8px #b8bec7, inset -4px -4px 8px #ffffff; color: #2d3436 !important; font-weight: 600;
    }
</style>
"""
st.markdown(CLAY_CSS, unsafe_allow_html=True)

# -------------------------------------------------------
# UI Helpers
# -------------------------------------------------------
def card(kind: str, title: str, body: str):
    formatted_body = body.replace('\n', '<br>')
    st.markdown(f'<div class="card {kind}"><div class="title">{title}</div><div>{formatted_body}</div></div>', unsafe_allow_html=True)

def render_mcq(questions: List[Dict[str, Any]], key_prefix: str):
    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}. {q['q']}**")
        choice = st.radio(f"{key_prefix}_q{i}", q["options"], key=f"radio_{key_prefix}_{i}", index=0, label_visibility="collapsed")
        if st.button(f"Check Answer", key=f"btn_{key_prefix}_{i}"):
            idx = q["options"].index(choice)
            if idx == q["answer"]: card("tip", "Correct ✅", q["explain"])
            else: card("warn", "Incorrect ❌", q["explain"])

# -------------------------------------------------------
# Bash Engine
# -------------------------------------------------------
def init_bash_sandbox():
    if 'sandbox_dir' not in st.session_state:
        st.session_state.sandbox_dir = tempfile.mkdtemp(prefix="bash_tutorial_")
        with open(f"{st.session_state.sandbox_dir}/hello.txt", "w") as f: f.write("Hello, Linux Learner!\nLine 2: Test file.")
        with open(f"{st.session_state.sandbox_dir}/data.csv", "w") as f: f.write("Name,Age,City\nAlice,30,New York\nBob,25,London")
        os.makedirs(f"{st.session_state.sandbox_dir}/my_folder", exist_ok=True)
    if 'term_history' not in st.session_state: st.session_state.term_history = []

def run_bash_command(command):
    DANGEROUS = ["rm -rf /", "sudo", "su ", "mkfs", "dd if="]
    INTERACTIVE = ["top", "vim", "vi", "nano", "less", "more", "ssh", "telnet"]
    if any(d in command for d in DANGEROUS): return "🚫 Security Error: Blocked."
    if command.split()[0] in INTERACTIVE: return f"🖥️ [SIMULATED] '{command.split()[0]}' requires a TTY."
    try:
        result = subprocess.run(command, shell=True, executable='/bin/bash', cwd=st.session_state.sandbox_dir, capture_output=True, text=True, timeout=5)
        output = result.stdout + (f"\n[stderr]\n{result.stderr}" if result.stderr else "")
        return output if output else "(Success)"
    except Exception as e: return f"⚠️ Error: {str(e)}"

# -------------------------------------------------------
# DATABASE
# -------------------------------------------------------
@dataclass
class Lesson:
    id: str
    category: str
    title: str
    theory: str
    demo_cmd: str
    quiz: List[Dict[str, Any]]

def get_all_lessons() -> List[Lesson]:
    return [
        Lesson("intro", "HOME", "Bash Introduction", "Bash (Bourne Again SHell) is a Unix shell and command language interpreter. It acts as a bridge between the user and the Linux kernel, taking your text commands and translating them into system operations.", "echo $BASH_VERSION", [{"q": "What does Bash stand for?", "options": ["Bourne Again SHell", "Basic Shell", "Binary Shell", "Boot Shell"], "answer": 0, "explain": "Bourne Again SHell."}]),
        Lesson("filesystem", "HOME", "Linux File System", """Unlike Windows which uses drive letters (C:, D:), Linux has a single root directory represented by a forward slash `/`.\n\n**Key Directories:**\n- `/` (Root): The top-level directory.\n- `/bin`: Essential user command binaries (e.g., `ls`, `cp`, `cat`).\n- `/etc`: System-wide configuration files.\n- `/home`: Personal directories for regular users.\n- `/var`: Variable data files such as logs.\n- `/tmp`: Temporary files; cleared upon reboot.""", "ls /", [{"q": "Where are config files stored?", "options": ["/bin", "/etc", "/var", "/usr"], "answer": 1, "explain": "The /etc directory."}]),
        Lesson("get_started", "HOME", "Get Started", "When you open a terminal, you see a prompt like `user@hostname:~$`. The `~` is a shortcut for your home directory. The `$` indicates you are a standard user. Commands follow the syntax: `command [options] [arguments]`.", "whoami", [{"q": "What does `~` mean?", "options": ["Root", "Current folder", "Home directory", "Hidden files"], "answer": 2, "explain": "Home directory."}]),
        
        Lesson("ls", "BASIC COMMANDS", "List (ls)", "Lists directory contents.\n- `ls -l`: Long format (permissions, size).\n- `ls -a`: Shows hidden files.\n- `ls -h`: Human-readable sizes.", "ls -lah", [{"q": "Which flag shows hidden files?", "options": ["-l", "-a", "-h", "-r"], "answer": 1, "explain": "The -a flag."}]),
        Lesson("cd", "BASIC COMMANDS", "Change Dir (cd)", "Changes directories. `cd ..` moves up, `cd ~` goes home.", "cd my_folder && pwd && cd ..", [{"q": "What does `cd ..` do?", "options": ["Goes to root", "Moves up one level", "Goes home", "Lists files"], "answer": 1, "explain": "Moves up one level."}]),
        Lesson("pwd", "BASIC COMMANDS", "Print Dir (pwd)", "Prints the full, absolute path of the current directory.", "pwd", [{"q": "What does PWD stand for?", "options": ["Print Word Doc", "Print Working Directory", "Process Wide Data", "Path Way Down"], "answer": 1, "explain": "Print Working Directory."}]),
        Lesson("echo", "BASIC COMMANDS", "Echo (echo)", "Prints text to screen. `echo -e` enables backslash escapes like `\\n` for newlines.", "echo -e 'Hello\\nWorld'", [{"q": "Which flag allows newlines?", "options": ["-n", "-v", "-e", "-f"], "answer": 2, "explain": "The -e flag."}]),
        Lesson("cat", "BASIC COMMANDS", "Concatenate (cat)", "Reads and outputs file contents. It can also combine multiple files.", "cat hello.txt", [{"q": "What is 'cat' short for?", "options": ["Category", "Concatenate", "Catalog", "Capture"], "answer": 1, "explain": "Concatenate."}]),
        Lesson("cp", "BASIC COMMANDS", "Copy (cp)", "Copies files. Use `-r` to recursively copy a folder.", "cp hello.txt backup.txt && ls", [{"q": "Which flag copies a directory?", "options": ["-f", "-a", "-r", "-i"], "answer": 2, "explain": "The -r flag."}]),
        Lesson("mv", "BASIC COMMANDS", "Move (mv)", "Moves or renames files. The original disappears from its starting location.", "mv backup.txt my_folder/ && ls my_folder/", [{"q": "What else is 'mv' used for?", "options": ["Deleting", "Renaming", "Copying", "Reading"], "answer": 1, "explain": "Renaming."}]),
        Lesson("rm", "BASIC COMMANDS", "Remove (rm)", "Deletes files. **Warning:** No recycle bin! Use `-r` to delete folders.", "cp hello.txt del_me.txt && rm del_me.txt && ls", [{"q": "How do you delete a folder?", "options": ["rm folder/", "rm -r folder/", "rm -f folder/", "rm -a folder/"], "answer": 1, "explain": "The -r flag."}]),
        Lesson("touch", "BASIC COMMANDS", "Timestamp (touch)", "Creates empty files or updates a file's timestamp to 'now' without altering content.", "touch newfile.txt && ls -l newfile.txt", [{"q": "If a file exists, what does 'touch' do?", "options": ["Deletes it", "Appends to it", "Updates timestamp", "Overwrites it"], "answer": 2, "explain": "Updates timestamp."}]),
        Lesson("mkdir", "BASIC COMMANDS", "Make Dir (mkdir)", "Creates folders. `-p` creates nested folders in one go.", "mkdir -p project/src && ls -R project", [{"q": "How to create nested folders if parent is missing?", "options": ["mkdir parent/child", "mkdir -c parent/child", "mkdir -p parent/child", "mkdir -r parent/child"], "answer": 2, "explain": "The -p flag."}]),
        Lesson("man", "BASIC COMMANDS", "Manual (man)", "Opens built-in documentation. Press **q** to quit.", "man ls", [{"q": "How do you quit 'man'?", "options": ["esc", "ctrl+c", "q", "x"], "answer": 2, "explain": "Pressing 'q'."}]),
        Lesson("alias", "BASIC COMMANDS", "Alias", "Creates custom shortcuts. Save in `~/.bashrc` to make permanent.", "alias c='echo I am an alias!' && c", [{"q": "Where to save aliases permanently?", "options": ["/etc/hosts", "~/.bashrc", "/bin/bash", "~/.alias"], "answer": 1, "explain": "~/.bashrc."}]),
        
        Lesson("grep", "TEXT PROCESSING", "Search Text (grep)", "Searches for patterns. `-i` case-insensitive, `-n` shows line numbers.", "grep 'Alice' data.csv", [{"q": "Which flag makes grep case-insensitive?", "options": ["-n", "-c", "-i", "-r"], "answer": 2, "explain": "The -i flag."}]),
        Lesson("awk", "TEXT PROCESSING", "Pattern Scan (awk)", "Text processing language. `$1` represents the first column.", "awk -F',' '{print $1, $3}' data.csv", [{"q": "What does '$1' represent in awk?", "options": ["Whole line", "First column", "Last column", "Filename"], "answer": 1, "explain": "First field."}]),
        Lesson("sed", "TEXT PROCESSING", "Stream Editor (sed)", "Find and Replace. `s/old/new/g` replaces all occurrences.", "sed 's/Hello/Hi/g' hello.txt", [{"q": "What does 'g' stand for in sed?", "options": ["Global", "Group", "Generate", "Grep"], "answer": 0, "explain": "Global replacement."}]),
        Lesson("cut", "TEXT PROCESSING", "Remove Section (cut)", "Extracts specific columns. `-d` sets delimiter, `-f` picks field.", "cut -d',' -f2 data.csv", [{"q": "Which flag specifies the delimiter?", "options": ["-d", "-f", "-s", "-c"], "answer": 0, "explain": "The -d flag."}]),
        Lesson("sort", "TEXT PROCESSING", "Sort Lines (sort)", "Sorts text. `-n` numerical sort, `-r` reverse order.", "sort data.csv", [{"q": "How to sort numbers correctly?", "options": ["sort file", "sort -n file", "sort -r file", "sort -c file"], "answer": 1, "explain": "The -n flag."}]),
        Lesson("tail", "TEXT PROCESSING", "View End (tail)", "Outputs the last part of files. `tail -n 20` shows last 20 lines.", "tail -n 2 hello.txt", [{"q": "How to view the last 10 lines?", "options": ["tail -n 10 file", "tail -l 10 file", "tail -c 10 file", "tail -e 10 file"], "answer": 0, "explain": "tail -n 10."}]),
        Lesson("head", "TEXT PROCESSING", "View Start (head)", "Outputs the first part of files. Default is 10 lines.", "head -n 1 data.csv", [{"q": "Default number of lines 'head' prints?", "options": ["5", "15", "10", "All"], "answer": 2, "explain": "10 lines."}]),
        
        Lesson("ps", "SYSTEM MONITORING", "Process Status (ps)", "Reports a snapshot of running processes. `ps aux` shows all processes.", "ps aux | head -n 5", [{"q": "What does 'ps aux' show?", "options": ["Only your processes", "All processes", "Only background tasks", "Network processes"], "answer": 1, "explain": "All processes."}]),
        Lesson("top", "SYSTEM MONITORING", "List Processes (top)", "Dynamic real-time view of system. *Simulated here.*", "top", [{"q": "How to quit 'top'?", "options": ["ctrl+c", "esc", "q", "Both q and ctrl+c"], "answer": 3, "explain": "Both 'q' and 'ctrl+c'."}]),
        Lesson("df", "SYSTEM MONITORING", "Disk Space (df)", "Displays disk space. `-h` makes it human-readable.", "df -h", [{"q": "What does '-h' do in df?", "options": ["Shows hidden disks", "Human-readable sizes", "Hides remote drives", "Shows history"], "answer": 1, "explain": "Human-readable."}]),
        Lesson("du", "SYSTEM MONITORING", "Directory Usage (du)", "Estimates folder space usage. `du -sh *` summarizes sizes.", "du -sh *", [{"q": "What does 's' do in 'du -sh'?", "options": ["Sorts by size", "Displays speed", "Summarizes total", "Shows subdirectories"], "answer": 2, "explain": "Summarizes total."}]),
        Lesson("free", "SYSTEM MONITORING", "Memory Usage (free)", "Displays free and used RAM. `-h` makes it human-readable.", "free -h", [{"q": "Which column shows usable RAM?", "options": ["total", "used", "buff/cache", "available"], "answer": 3, "explain": "Available."}]),
        Lesson("kill", "SYSTEM MONITORING", "Terminate (kill)", "Terminates processes using PID. `kill -9` forcefully kills.", "echo 'Run sleep in background, find PID, kill.'", [{"q": "What does 'kill -9' do?", "options": ["Pauses process", "Polite stop request", "Forcefully kills it", "Restarts it"], "answer": 2, "explain": "Forcefully kills."}]),
        Lesson("uptime", "SYSTEM MONITORING", "Uptime", "Shows how long the system has been running and load averages.", "uptime", [{"q": "What numbers does uptime show?", "options": ["CPU temps", "Load averages", "Users logged in", "Process counts"], "answer": 1, "explain": "Load averages."}]),
        
        Lesson("ping", "NETWORKING", "Ping", "Tests network connectivity using ICMP packets.", "ping -c 3 localhost", [{"q": "What protocol does ping use?", "options": ["TCP", "HTTP", "ICMP", "UDP"], "answer": 2, "explain": "ICMP."}]),
        Lesson("curl", "NETWORKING", "URL Transfer (curl)", "Transfers data to/from URLs. Great for APIs.", "curl -s http://example.com | head -n 5", [{"q": "What is curl used for?", "options": ["Editing files", "Transferring data", "Pinging IPs", "Managing disks"], "answer": 1, "explain": "Transferring data."}]),
        Lesson("wget", "NETWORKING", "Downloader (wget)", "Non-interactive downloader. *Disabled in sandbox.*", "echo 'wget is disabled in this sandbox.'", [{"q": "Difference between wget and curl?", "options": ["wget is interactive", "wget downloads non-interactively", "curl is slower", "No difference"], "answer": 1, "explain": "wget downloads."}]),
        Lesson("ssh", "NETWORKING", "Remote Connect (ssh)", "Secure Shell. Securely logs into remote machines. Default port 22.", "ssh user@server.com", [{"q": "Default port for SSH?", "options": ["21", "80", "443", "22"], "answer": 3, "explain": "Port 22."}]),
        Lesson("scp", "NETWORKING", "Secure Copy (scp)", "Securely copies files over SSH. *Simulated.*", "echo 'scp requires a remote host.'", [{"q": "What does scp stand for?", "options": ["Super Copy", "Secure Copy", "System Copy", "Shell Copy"], "answer": 1, "explain": "Secure Copy."}]),
        Lesson("rsync", "NETWORKING", "File Sync (rsync)", "Synchronizes files. Superpower: only transfers differences.", "mkdir backup && rsync -av ./my_folder/ ./backup/ && ls backup", [{"q": "Why is rsync efficient?", "options": ["Uses more CPU", "Transfers only differences", "Compresses drive", "Ignores large files"], "answer": 1, "explain": "Transfers deltas."}]),
        
        Lesson("zip", "FILE COMPRESSION", "Compress (zip)", "Compresses files into `.zip`. `-r` is required for folders.", "zip my_archive.zip hello.txt data.csv && ls -lh my_archive.zip", [{"q": "How to zip a directory?", "options": ["zip file.zip folder", "zip -r file.zip folder", "zip -a file.zip folder", "zip -c file.zip folder"], "answer": 1, "explain": "The -r flag."}]),
        Lesson("unzip", "FILE COMPRESSION", "Extract (unzip)", "Extracts `.zip` files. `-l` lists contents.", "unzip -l my_archive.zip", [{"q": "How to view zip contents without extracting?", "options": ["unzip -v", "unzip -l", "unzip -s", "unzip -c"], "answer": 1, "explain": "The -l flag."}]),
        Lesson("tar", "FILE COMPRESSION", "TAR Archive (tar)", "Standard Linux archiving. `-c` create, `-z` gzip, `-x` extract.", "tar -czvf backup.tar.gz hello.txt && ls -lh backup.tar.gz", [{"q": "What does '-z' do in tar?", "options": ["Zip", "Gzip compression", "Unzip", "List"], "answer": 1, "explain": "Gzip."}]),
        
        Lesson("ownership_concept", "FILE PERMISSIONS", "Ownership Concept", "Permissions: **r** (Read=4), **w** (Write=2), **x** (Execute=1). Applied to User, Group, and Others.", "ls -l hello.txt", [{"q": "Number for 'Execute' permission?", "options": ["1", "2", "3", "4"], "answer": 0, "explain": "Execute=1."}]),
        Lesson("chmod", "FILE PERMISSIONS", "Modify (chmod)", "Alters permissions. `755` (rwxr-xr-x), `644` (rw-r--r--).", "chmod 777 hello.txt && ls -l hello.txt", [{"q": "Permissions for '644'?", "options": ["Everyone can edit", "Owner: rw, Others: r", "Owner: rwx, Others: none", "No permissions"], "answer": 1, "explain": "Owner rw, Others r."}]),
        Lesson("chown", "FILE PERMISSIONS", "Ownership (chown)", "Changes file owner. Requires root. *Shows error in sandbox.*", "chown root hello.txt", [{"q": "Why might chown fail?", "options": ["File too big", "Need root/sudo", "File is directory", "Wrong extension"], "answer": 1, "explain": "Needs root."}]),
        Lesson("chgrp", "FILE PERMISSIONS", "Group (chgrp)", "Changes file group ownership.", "chgrp wheel hello.txt", [{"q": "What does chgrp change?", "options": ["The owner", "The group", "The permissions", "The filename"], "answer": 1, "explain": "The group."}]),
        
        Lesson("syntax", "SCRIPTING", "Syntax & Shebang", "First line: `#!/bin/bash`. Make executable with `chmod +x`.", "echo '#!/bin/bash\\necho Hello' > myscript.sh && chmod +x myscript.sh && ./myscript.sh", [{"q": "First line of a script called?", "options": ["Hash line", "Shebang", "Interpreter", "Header"], "answer": 1, "explain": "Shebang (#!)."}]),
        Lesson("variables", "SCRIPTING", "Variables", "Store data. **NO SPACES** around `=`. Read with `$`.", "MY_OS=\"Linux\" && echo \"I love $MY_OS\"", [{"q": "How to read a variable?", "options": ["NAME", "$NAME", "%NAME%", "&NAME"], "answer": 1, "explain": "Dollar sign $."}]),
        Lesson("datatypes", "SCRIPTING", "Data Types & Math", "No strict types. Use `$((...))` for math.", "A=15 && B=5 && echo \"Sum: $((A+B))\"", [{"q": "How to perform math?", "options": ["$[A+B]", "$(A+B)", "$((A+B))", "math(A+B)"], "answer": 2, "explain": "Double parentheses."}]),
        Lesson("operators", "SCRIPTING", "Operators (If/Else)", "Numeric: `-eq`, `-ne`, `-gt`, `-lt`. Spaces around `[ ]` are mandatory.", "A=10 && B=20 && if [ $A -lt $B ]; then echo 'A is less'; fi", [{"q": "What does '-eq' mean?", "options": ["Not equal", "Equals", "Greater than", "Less than"], "answer": 1, "explain": "Equals."}]),
        Lesson("loops", "SCRIPTING", "Loops", "Repeat commands. Ends with `done`.", "for i in apple banana cherry; do echo \"Fruit: $i\"; done", [{"q": "What ends a loop block?", "options": ["end", "done", "fi", "stop"], "answer": 1, "explain": "Done."}]),
        Lesson("functions", "SCRIPTING", "Functions", "Group commands. First argument is `$1`.", "greet() { echo \"Hello, $1!\"; }\ngreet \"Developer\"", [{"q": "How to access first argument?", "options": ["$1", "$0", "$first", "$arg1"], "answer": 0, "explain": "$1."}]),
        Lesson("arrays", "SCRIPTING", "Arrays", "Hold multiple values. Access all with `@`.", "FRUITS=(\"Apple\" \"Banana\")\necho \"All: ${FRUITS[@]}\"", [{"q": "How to print all elements?", "options": ["${ARRAY}", "${ARRAY[*]}", "${ARRAY[@]}", "Both * and @"], "answer": 3, "explain": "Both * and @."}]),
        Lesson("cron", "SCRIPTING", "Schedule (cron)", "Time-based scheduler. Edit with `crontab -e`.", "crontab -l", [{"q": "Command to edit cron jobs?", "options": ["cron -e", "crontab -e", "editcron", "schedule -e"], "answer": 1, "explain": "crontab -e."}]),
    ]

# -------------------------------------------------------
# Main Application
# -------------------------------------------------------
def main():
    init_bash_sandbox()
    lessons = get_all_lessons()
    
    # ADDED YOUR REQUESTED TITLE HERE
    st.title("Linux-Virtual")
    
    categories = ["HOME", "BASIC COMMANDS", "TEXT PROCESSING", "SYSTEM MONITORING", "NETWORKING", "FILE COMPRESSION", "FILE PERMISSIONS", "SCRIPTING"]
    options_map = {}
    selectbox_options = []
    
    for cat in categories:
        cat_lessons = [l for l in lessons if l.category == cat]
        if cat_lessons:
            selectbox_options.append(f"📂 {cat}")
            for l in cat_lessons:
                label = f"   ⚡ {l.title}"
                selectbox_options.append(label)
                options_map[label] = l

    st.markdown("### 🪵 Syllabus & Lessons")
    selected_label = st.selectbox("Choose a topic to study:", selectbox_options, label_visibility="collapsed")
    
    if selected_label.startswith("   ⚡"):
        current_lesson = options_map[selected_label]
        
        st.markdown(f"## {current_lesson.title}")
        card("note", "Explanation", current_lesson.theory)
        
        if st.button(f"▶️ Run Example", key=f"run_{current_lesson.id}", use_container_width=True):
            output = run_bash_command(current_lesson.demo_cmd)
            st.session_state.term_history.append({"cmd": current_lesson.demo_cmd, "out": output})
            
        st.code(current_lesson.demo_cmd, language="bash")
        
        if current_lesson.quiz:
            st.markdown("---")
            render_mcq(current_lesson.quiz, f"mcq_{current_lesson.id}")
        
        st.markdown("---")
        if st.checkbox(f"✅ Mark '{current_lesson.title}' as Complete", key=f"prog_{current_lesson.id}"):
            st.success("Progress saved!")
    else:
        st.info("👈 Select a specific lesson to view its explanation and quiz.")

    st.markdown("---")
    
    term_container_html = """
    <div class="term-container">
        <h3 style="margin-top:0px; margin-bottom:15px;">🖥️ Practice Terminal</h3>
        <div style="margin-bottom:10px; font-size:0.9rem; color:#636e72;">
            Working Directory: <code style="background:#d1d9e6; padding:2px 6px; border-radius:5px;">%s</code>
        </div>
    """ % st.session_state.sandbox_dir

    term_inner_html = "<div class='term-box'>"
    if not st.session_state.term_history:
        term_inner_html += "<span style='color:#636e72'>Type a command below to begin...</span>"
    else:
        for item in st.session_state.term_history:
            safe_cmd = item['cmd'].replace("<", "&lt;").replace(">", "&gt;")
            safe_out = item['out'].replace("<", "&lt;").replace(">", "&gt;")
            term_inner_html += f"<div class='term-cmd'>student@linux:~$ {safe_cmd}</div>"
            term_inner_html += f"<div class='term-out'>{safe_out}</div>"
    term_inner_html += "</div></div>"

    st.markdown(term_container_html + term_inner_html, unsafe_allow_html=True)
    
    if user_cmd := st.chat_input("Enter command:", key="term_input"):
        if user_cmd.strip():
            out = run_bash_command(user_cmd)
            st.session_state.term_history.append({"cmd": user_cmd, "out": out})

if __name__ == "__main__":
    main()