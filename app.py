# =========================
# Bash Tutorial — Complete Interactive Linux Coach (Single File)
# =========================
import subprocess
import os
import tempfile
from dataclasses import dataclass
from typing import List, Dict, Any
import streamlit as st

# -------------------------------------------------------
# App Meta & W3CSS Accents
# -------------------------------------------------------
st.set_page_config(page_title="Bash Tutorial • Complete Linux Coach", page_icon="💻", layout="wide")

W3CSS = """
<style>
    h1, h2, h3 { font-weight: 700; color: #0f172a; }
    .card { border:1px solid #e5e7eb; border-radius:12px; padding:14px 16px; background:#fff; margin:8px 0; }
    .card .title { font-weight:700; margin-bottom:6px; }
    .card.note  { border-left:6px solid #06b6d4; }
    .card.tip   { border-left:6px solid #22c55e; }
    .card.warn  { border-left:6px solid #f59e0b; }
    .card.exam  { border-left:6px solid #8b5cf6; }
    
    /* Terminal Styling */
    .term-box {
        background-color: #1e1e1e; color: #d4d4d4; border-radius: 8px; 
        padding: 15px; font-family: 'Consolas', 'Courier New', monospace; font-size: 13px;
        height: 70vh; overflow-y: auto; border: 1px solid #333;
    }
    .term-cmd { color: #4CAF50; margin-bottom: 2px; white-space: pre-wrap; }
    .term-out { color: #ffffff; white-space: pre-wrap; margin-bottom: 15px; border-bottom: 1px solid #333; padding-bottom: 10px;}
</style>
"""
st.markdown(W3CSS, unsafe_allow_html=True)

# -------------------------------------------------------
# UI Helpers
# -------------------------------------------------------
def card(kind: str, title: str, body: str):
    st.markdown(f'<div class="card {kind}"><div class="title">{title}</div><div>{body}</div></div>', unsafe_allow_html=True)

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
# Complete Lesson Database (Every topic requested)
# -------------------------------------------------------
@dataclass
class Lesson:
    id: str
    category: str
    title: str
    theory: str
    demo_cmd: str

def get_all_lessons() -> List[Lesson]:
    return [
        # HOME
        Lesson("intro", "HOME", "Bash Introduction", "Bash (Bourne Again SHell) is a Unix shell and command language interpreter. It is the default login shell for most Linux distributions and macOS.", "echo $BASH_VERSION"),
        Lesson("get_started", "HOME", "Get Started", "The prompt `user@hostname:~$` shows user, hostname, and current directory (`~` is home). Command syntax: `command [options] [arguments]`.", "whoami"),
        
        # BASIC COMMANDS
        Lesson("ls", "BASIC COMMANDS", "List (ls)", "Lists files. `-l` long format, `-a` hidden files, `-h` human readable sizes.", "ls -lah"),
        Lesson("cd", "BASIC COMMANDS", "Change Dir (cd)", "Changes directory. `cd ..` up one level, `cd ~` go home.", "cd my_folder && pwd && cd .."),
        Lesson("pwd", "BASIC COMMANDS", "Print Dir (pwd)", "Prints the full, absolute path of the current working directory.", "pwd"),
        Lesson("echo", "BASIC COMMANDS", "Echo (echo)", "Prints text to standard output. Used heavily in scripting. `-e` enables backslash escapes.", "echo -e 'Hello\\nWorld'"),
        Lesson("cat", "BASIC COMMANDS", "Concatenate (cat)", "Reads data from files and outputs contents. Can also combine files.", "cat hello.txt"),
        Lesson("cp", "BASIC COMMANDS", "Copy (cp)", "Copies files/directories. `-r` is required to copy a folder recursively.", "cp hello.txt backup.txt && ls"),
        Lesson("mv", "BASIC COMMANDS", "Move (mv)", "Moves files. Also the standard command used to **rename** files.", "mv backup.txt my_folder/ && ls my_folder/"),
        Lesson("rm", "BASIC COMMANDS", "Remove (rm)", "Deletes files. **Warning:** No recycle bin! `-r` deletes folders.", "cp hello.txt del_me.txt && rm del_me.txt && ls"),
        Lesson("touch", "BASIC COMMANDS", "Timestamp (touch)", "Creates empty files quickly, or updates the timestamp of an existing file to 'now'.", "touch newfile.txt && ls -l newfile.txt"),
        Lesson("mkdir", "BASIC COMMANDS", "Make Dir (mkdir)", "Creates folders. `-p` creates nested folders in one go (e.g., `a/b/c`).", "mkdir -p project/src && ls -R project"),
        Lesson("man", "BASIC COMMANDS", "Manual (man)", "Opens the built-in manual for commands. *Interactive TTY simulated here.*", "man ls"),
        Lesson("alias", "BASIC COMMANDS", "Alias", "Creates custom shortcuts for commands. Temporary unless added to `~/.bashrc`.", "alias c='echo I am an alias!' && c"),
        
        # TEXT PROCESSING
        Lesson("grep", "TEXT PROCESSING", "Search Text (grep)", "Searches for patterns. `-i` case-insensitive, `-n` shows line numbers, `-r` recursive.", "grep 'Alice' data.csv"),
        Lesson("awk", "TEXT PROCESSING", "Pattern Scan (awk)", "Programming language for text extraction. Treats lines as records, words as fields (`$1`, `$2`).", "awk -F',' '{print $1, $3}' data.csv"),
        Lesson("sed", "TEXT PROCESSING", "Stream Editor (sed)", "Filters and transforms text (Find & Replace). `s/old/new/g` substitutes globally.", "sed 's/Hello/Hi/g' hello.txt"),
        Lesson("cut", "TEXT PROCESSING", "Remove Section (cut)", "Extracts specific columns. `-d','` sets delimiter, `-f1` picks field 1.", "cut -d',' -f2 data.csv"),
        Lesson("sort", "TEXT PROCESSING", "Sort Lines (sort)", "Sorts text. `-n` numerical sort, `-r` reverse order.", "sort data.csv"),
        Lesson("tail", "TEXT PROCESSING", "View End (tail)", "Outputs the last part of files. `-n 5` shows last 5 lines.", "tail -n 2 hello.txt"),
        Lesson("head", "TEXT PROCESSING", "View Start (head)", "Outputs the first part of files. `-n 1` shows first 1 line.", "head -n 1 data.csv"),
        
        # SYSTEM MONITORING
        Lesson("ps", "SYSTEM MONITORING", "Process Status (ps)", "Reports a snapshot of current processes. `ps aux` shows all processes for all users.", "ps aux | head -n 5"),
        Lesson("top", "SYSTEM MONITORING", "List Processes (top)", "Dynamic real-time view of running system. *Interactive TTY simulated.*", "top"),
        Lesson("df", "SYSTEM MONITORING", "Disk Space (df)", "Displays disk space available on file systems. `-h` human-readable.", "df -h"),
        Lesson("du", "SYSTEM MONITORING", "Directory Usage (du)", "Estimates file and folder space usage. `-sh *` summarizes current folder.", "du -sh *"),
        Lesson("free", "SYSTEM MONITORING", "Memory Usage (free)", "Displays total, used, and free physical and swap memory.", "free -h"),
        Lesson("kill", "SYSTEM MONITORING", "Terminate (kill)", "Sends a signal to terminate a process using its PID. `-9` forces it.", "echo 'Run a sleep command in background (&), find PID with ps, and kill it.'"),
        Lesson("uptime", "SYSTEM MONITORING", "Uptime", "Tells you how long the system has been running and system load averages.", "uptime"),
        
        # NETWORKING
        Lesson("ping", "NETWORKING", "Ping", "Tests connectivity to another network device using ICMP packets. `-c 3` sends 3 packets.", "ping -c 3 localhost"),
        Lesson("curl", "NETWORKING", "URL Transfer (curl)", "Transfers data to/from a server. Supports HTTP, HTTPS, FTP.", "curl -s http://example.com | head -n 5"),
        Lesson("wget", "NETWORKING", "Downloader (wget)", "Non-interactive network downloader. *Disabled in sandbox for security.*", "echo 'wget is disabled in this sandbox.'"),
        Lesson("ssh", "NETWORKING", "Remote Connect (ssh)", "Secure Shell. Used to log into a remote machine securely. *Interactive TTY simulated.*", "ssh user@server.com"),
        Lesson("scp", "NETWORKING", "Secure Copy (scp)", "Uses SSH to securely copy files between local and remote hosts. *Simulated.*", "echo 'scp requires a remote host.'"),
        Lesson("rsync", "NETWORKING", "File Sync (rsync)", "Fast file-copying tool. Only transfers differences to save bandwidth.", "mkdir backup && rsync -av ./my_folder/ ./backup/ && ls backup"),
        
        # FILE COMPRESSION
        Lesson("zip", "FILE COMPRESSION", "Compress (zip)", "Compresses files into `.zip`. `-r` is required for folders.", "zip my_archive.zip hello.txt data.csv && ls -lh my_archive.zip"),
        Lesson("unzip", "FILE COMPRESSION", "Extract (unzip)", "Extracts files from a `.zip`. `-l` lists contents without extracting.", "unzip -l my_archive.zip"),
        Lesson("tar", "FILE COMPRESSION", "TAR Archive (tar)", "Standard Linux archiving. `-c` create, `-z` gzip, `-v` verbose, `-f` file, `-x` extract.", "tar -czvf backup.tar.gz hello.txt && ls -lh backup.tar.gz"),
        
        # FILE PERMISSIONS
        Lesson("ownership_concept", "FILE PERMISSIONS", "Ownership Concept", "Every file has a User (owner), Group, and Others. Permissions: **r** (Read=4), **w** (Write=2), **x** (Execute=1).", "ls -l hello.txt"),
        Lesson("chmod", "FILE PERMISSIONS", "Modify (chmod)", "Alters permissions using numeric codes. `755` (rwxr-xr-x), `644` (rw-r--r--).", "chmod 777 hello.txt && ls -l hello.txt"),
        Lesson("chown", "FILE PERMISSIONS", "Ownership (chown)", "Changes the user ownership. Requires root privileges (Will show error in sandbox).", "chown root hello.txt"),
        Lesson("chgrp", "FILE PERMISSIONS", "Group (chgrp)", "Changes the group ownership. Also requires elevated privileges.", "chgrp wheel hello.txt"),
        
        # SCRIPTING
        Lesson("syntax", "SCRIPTING", "Syntax & Shebang", "First line must be `#!/bin/bash`. Run with `chmod +x script.sh` then `./script.sh`.", "echo '#!/bin/bash\\necho Hello from script' > myscript.sh && chmod +x myscript.sh && ./myscript.sh"),
        Lesson("variables", "SCRIPTING", "Variables", "Store data. **No spaces around `=`**. Access with `$`.", "MY_OS=\"Linux\" && echo \"I love $MY_OS\""),
        Lesson("datatypes", "SCRIPTING", "Data Types & Math", "Everything is a string. Use `$((...))` for integer math.", "A=15 && B=5 && echo \"Sum: $((A+B)) Mult: $((A*B))\""),
        Lesson("operators", "SCRIPTING", "Operators (If/Else)", "Conditionals: `-eq` (equal), `-ne` (not equal), `-gt` (greater). *Spaces around `[ ]` are mandatory.*", "A=10 && B=20 && if [ $A -lt $B ]; then echo 'A is less'; fi"),
        Lesson("loops", "SCRIPTING", "Loops", "Repeat commands. **For loop** iterates over a list of items.", "for i in apple banana cherry; do echo \"Fruit: $i\"; done"),
        Lesson("functions", "SCRIPTING", "Functions", "Group commands under a name. `$1` is the first argument passed.", "greet() { echo \"Hello, $1!\"; }\ngreet \"Developer\""),
        Lesson("arrays", "SCRIPTING", "Arrays", "Hold multiple values. Access all with `@` or specific items with index `[0]`.", "FRUITS=(\"Apple\" \"Banana\" \"Cherry\")\necho \"First: ${FRUITS[0]}\"\necho \"All: ${FRUITS[@]}\""),
        Lesson("cron", "SCRIPTING", "Schedule (cron)", "Time-based job scheduler. Edit with `crontab -e`.", "crontab -l"),
    ]

# -------------------------------------------------------
# Main Application Layout
# -------------------------------------------------------
def main():
    init_bash_sandbox()
    lessons = get_all_lessons()
    
    # Format options for Selectbox to look like a file tree
    categories = ["HOME", "BASIC COMMANDS", "TEXT PROCESSING", "SYSTEM MONITORING", "NETWORKING", "FILE COMPRESSION", "FILE PERMISSIONS", "SCRIPTING"]
    options_map = {}
    selectbox_options = []
    
    for cat in categories:
        cat_lessons = [l for l in lessons if l.category == cat]
        if cat_lessons:
            selectbox_options.append(f"📁 {cat}")
            for l in cat_lessons:
                label = f"    ⚡ {l.title}"
                selectbox_options.append(label)
                options_map[label] = l

    # --- LAYOUT: Split Screen ---
    left_col, right_col = st.columns([1, 1])

    # ==========================================
    # LEFT COLUMN: LESSONS & CONTENT
    # ==========================================
    with left_col:
        st.markdown("### 📚 Syllabus & Lessons")
        
        selected_label = st.selectbox("Choose a topic", selectbox_options, label_visibility="collapsed")
        
        if selected_label.startswith("    ⚡"):
            current_lesson = options_map[selected_label]
            
            st.markdown(f"## {current_lesson.title}")
            card("note", "Concept", current_lesson.theory)
            
            # One-Click Run
            if st.button(f"▶️ Run Example Command", key=f"run_{current_lesson.id}", use_container_width=True):
                output = run_bash_command(current_lesson.demo_cmd)
                st.session_state.term_history.append({"cmd": current_lesson.demo_cmd, "out": output})
                
            st.code(current_lesson.demo_cmd, language="bash")
            
            # Progress Tracker
            st.markdown("---")
            if st.checkbox(f"✅ Mark '{current_lesson.title}' as Complete", key=f"prog_{current_lesson.id}"):
                st.success("Progress saved!")
        else:
            st.info("👈 Select a specific lesson from the dropdown above to view its theory and run examples.")

       # ==========================================
    # RIGHT COLUMN: PERSISTENT TERMINAL
    # ==========================================
    with right_col:
        st.markdown("### 🖥️ Live Linux Terminal")
        st.caption(f"Working Dir: `{st.session_state.sandbox_dir}`")
        
        # Render Terminal History (Chronological: Oldest at top)
        term_html = "<div class='term-box'>"
        if not st.session_state.term_history:
            term_html += "<span style='color:#666'>Waiting for commands...</span>"
        else:
            for item in st.session_state.term_history:
                safe_cmd = item['cmd'].replace("<", "&lt;").replace(">", "&gt;")
                safe_out = item['out'].replace("<", "&lt;").replace(">", "&gt;")
                term_html += f"<div class='term-cmd'>student@linux:~$ {safe_cmd}</div>"
                term_html += f"<div class='term-out'>{safe_out}</div>"
        term_html += "</div>"
        
        st.markdown(term_html, unsafe_allow_html=True)
        
        # THE FIX: Use st.chat_input instead of st.text_input, and DO NOT use st.rerun()
        if user_cmd := st.chat_input("Enter command:", key="term_input"):
            if user_cmd.strip():
                out = run_bash_command(user_cmd)
                st.session_state.term_history.append({"cmd": user_cmd, "out": out"})
                # st.rerun() is REMOVED here. chat_input natively clears and reruns the app safely!

if __name__ == "__main__":
    main()