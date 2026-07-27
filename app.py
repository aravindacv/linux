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
    .term-box {
        background-color: #1e1e1e; color: #d4d4d4; border-radius: 8px; 
        padding: 15px; font-family: 'Consolas', 'Courier New', monospace; font-size: 13px;
        height: 75vh; overflow-y: auto; border: 1px solid #333;
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

def render_mcq(questions: List[Dict[str, Any]], key_prefix: str):
    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}. {q['q']}**")
        choice = st.radio(
            f"{key_prefix}_q{i}", q["options"], key=f"radio_{key_prefix}_{i}", index=0, label_visibility="collapsed"
        )
        if st.button(f"Check Answer", key=f"btn_{key_prefix}_{i}"):
            idx = q["options"].index(choice)
            if idx == q["answer"]:
                card("tip", "Correct ✅", q["explain"])
            else:
                card("warn", "Incorrect ❌", q["explain"])

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
# Complete Lesson Database (EVERY TOPIC HAS AN MCQ NOW)
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
        # HOME
        Lesson("intro", "HOME", "Bash Introduction", "Bash (Bourne Again SHell) is a Unix shell and command language interpreter. It is the default login shell for most Linux distributions and macOS.", "echo $BASH_VERSION", 
               [{"q": "What does Bash stand for?", "options": ["Bourne Again SHell", "Basic Shell", "Binary Shell", "Boot Shell"], "answer": 0, "explain": "Bourne Again SHell."}]),
        Lesson("get_started", "HOME", "Get Started", "The prompt `user@hostname:~$` shows user, hostname, and current directory (`~` is home). Command syntax: `command [options] [arguments]`.", "whoami", 
               [{"q": "What does the `~` symbol mean in a terminal path?", "options": ["Root directory", "Current folder", "User's home directory", "Hidden files"], "answer": 2, "explain": "The tilde ~ is a shortcut for the current user's home directory."}]),
        
        # BASIC COMMANDS
        Lesson("ls", "BASIC COMMANDS", "List (ls)", "Lists files. `-l` long format, `-a` hidden files, `-h` human readable sizes.", "ls -lah", 
               [{"q": "Which flag shows hidden files?", "options": ["-l", "-a", "-h", "-r"], "answer": 1, "explain": "The -a flag shows all files, including those starting with a dot."}]),
        Lesson("cd", "BASIC COMMANDS", "Change Dir (cd)", "Changes directory. `cd ..` up one level, `cd ~` go home.", "cd my_folder && pwd && cd ..", 
               [{"q": "What does `cd ..` do?", "options": ["Goes to root", "Moves up one level", "Goes home", "Lists files"], "answer": 1, "explain": "Double dot refers to the parent directory."}]),
        Lesson("pwd", "BASIC COMMANDS", "Print Dir (pwd)", "Prints the full, absolute path of the current working directory.", "pwd", 
               [{"q": "What does PWD stand for?", "options": ["Print Word Doc", "Print Working Directory", "Process Wide Data", "Path Way Down"], "answer": 1, "explain": "It stands for Print Working Directory."}]),
        Lesson("echo", "BASIC COMMANDS", "Echo (echo)", "Prints text to standard output. Used heavily in scripting. `-e` enables backslash escapes.", "echo -e 'Hello\\nWorld'", 
               [{"q": "Which flag allows you to use newlines (\\n) in echo?", "options": ["-n", "-v", "-e", "-f"], "answer": 2, "explain": "The -e flag enables interpretation of backslash escapes."}]),
        Lesson("cat", "BASIC COMMANDS", "Concatenate (cat)", "Reads data from files and outputs contents. Can also combine files.", "cat hello.txt", 
               [{"q": "What is 'cat' short for?", "options": ["Category", "Concatenate", "Catalog", "Capture"], "answer": 1, "explain": "It was originally designed to concatenate files."}]),
        Lesson("cp", "BASIC COMMANDS", "Copy (cp)", "Copies files/directories. `-r` is required to copy a folder recursively.", "cp hello.txt backup.txt && ls", 
               [{"q": "Which flag is required to copy a whole directory?", "options": ["-f", "-a", "-r", "-i"], "answer": 2, "explain": "The -r (recursive) flag is required to copy directories."}]),
        Lesson("mv", "BASIC COMMANDS", "Move (mv)", "Moves files. Also the standard command used to **rename** files.", "mv backup.txt my_folder/ && ls my_folder/", 
               [{"q": "Besides moving, what is 'mv' commonly used for?", "options": ["Deleting", "Renaming", "Copying", "Reading"], "answer": 1, "explain": "Moving a file to the same directory with a new name renames it."}]),
        Lesson("rm", "BASIC COMMANDS", "Remove (rm)", "Deletes files. **Warning:** No recycle bin! `-r` deletes folders.", "cp hello.txt del_me.txt && rm del_me.txt && ls", 
               [{"q": "How do you delete a folder and everything inside it?", "options": ["rm folder/", "rm -r folder/", "rm -f folder/", "rm -a folder/"], "answer": 1, "explain": "The -r (recursive) flag is required to remove directories."}]),
        Lesson("touch", "BASIC COMMANDS", "Timestamp (touch)", "Creates empty files quickly, or updates the timestamp of an existing file to 'now'.", "touch newfile.txt && ls -l newfile.txt", 
               [{"q": "If a file already exists, what does 'touch' do?", "options": ["Deletes it", "Appends to it", "Updates its timestamp", "Overwrites it"], "answer": 2, "explain": "Touch updates the last access and modification times to the current time."}]),
        Lesson("mkdir", "BASIC COMMANDS", "Make Dir (mkdir)", "Creates folders. `-p` creates nested folders in one go (e.g., `a/b/c`).", "mkdir -p project/src && ls -R project", 
               [{"q": "How do you create 'parent/child' if 'parent' doesn't exist?", "options": ["mkdir parent/child", "mkdir -c parent/child", "mkdir -p parent/child", "mkdir -r parent/child"], "answer": 2, "explain": "The -p flag creates parent directories as needed."}]),
        Lesson("man", "BASIC COMMANDS", "Manual (man)", "Opens the built-in manual for commands. *Interactive TTY simulated here.*", "man ls", 
               [{"q": "What do you press to quit the 'man' pages?", "options": ["esc", "ctrl+c", "q", "x"], "answer": 2, "explain": "Pressing 'q' quits the man pager."}]),
        Lesson("alias", "BASIC COMMANDS", "Alias", "Creates custom shortcuts for commands. Temporary unless added to `~/.bashrc`.", "alias c='echo I am an alias!' && c", 
               [{"q": "Where do you save aliases so they persist after reboot?", "options": ["/etc/hosts", "~/.bashrc", "/bin/bash", "~/.alias"], "answer": 1, "explain": "Adding them to ~/.bashrc ensures they load on every new terminal session."}]),
        
        # TEXT PROCESSING
        Lesson("grep", "TEXT PROCESSING", "Search Text (grep)", "Searches for patterns. `-i` case-insensitive, `-n` shows line numbers, `-r` recursive.", "grep 'Alice' data.csv", 
               [{"q": "Which flag makes grep case-insensitive?", "options": ["-n", "-c", "-i", "-r"], "answer": 2, "explain": "The -i flag ignores upper/lower case differences."}]),
        Lesson("awk", "TEXT PROCESSING", "Pattern Scan (awk)", "Programming language for text extraction. Treats lines as records, words as fields (`$1`, `$2`).", "awk -F',' '{print $1, $3}' data.csv", 
               [{"q": "In awk, what does '$1' represent?", "options": ["The whole line", "The first word/column", "The last column", "The filename"], "answer": 1, "explain": "$1 refers to the first field in the record."}]),
        Lesson("sed", "TEXT PROCESSING", "Stream Editor (sed)", "Filters and transforms text (Find & Replace). `s/old/new/g` substitutes globally.", "sed 's/Hello/Hi/g' hello.txt", 
               [{"q": "In 's/old/new/g', what does the 'g' stand for?", "options": ["Global", "Group", "Generate", "Grep"], "answer": 0, "explain": "The 'g' flag means 'global', replacing all instances on a line, not just the first."}]),
        Lesson("cut", "TEXT PROCESSING", "Remove Section (cut)", "Extracts specific columns. `-d','` sets delimiter, `-f1` picks field 1.", "cut -d',' -f2 data.csv", 
               [{"q": "Which flag specifies the delimiter in cut?", "options": ["-d", "-f", "-s", "-c"], "answer": 0, "explain": "The -d flag specifies the delimiter (e.g., -d',')."}]),
        Lesson("sort", "TEXT PROCESSING", "Sort Lines (sort)", "Sorts text. `-n` numerical sort, `-r` reverse order.", "sort data.csv", 
               [{"q": "How do you sort a list of numbers correctly?", "options": ["sort file.txt", "sort -n file.txt", "sort -r file.txt", "sort -c file.txt"], "answer": 1, "explain": "The -n flag sorts numerically instead of alphabetically."}]),
        Lesson("tail", "TEXT PROCESSING", "View End (tail)", "Outputs the last part of files. `-n 5` shows last 5 lines.", "tail -n 2 hello.txt", 
               [{"q": "How do you view the last 10 lines of a file?", "options": ["tail -n 10 file", "tail -l 10 file", "tail -c 10 file", "tail -e 10 file"], "answer": 0, "explain": "tail -n 10 is the correct syntax."}]),
        Lesson("head", "TEXT PROCESSING", "View Start (head)", "Outputs the first part of files. `-n 1` shows first 1 line.", "head -n 1 data.csv", 
               [{"q": "What is the default number of lines 'head' prints?", "options": ["5", "15", "10", "All"], "answer": 2, "explain": "By default, head prints the first 10 lines."}]),
        
        # SYSTEM MONITORING
        Lesson("ps", "SYSTEM MONITORING", "Process Status (ps)", "Reports a snapshot of current processes. `ps aux` shows all processes for all users.", "ps aux | head -n 5", 
               [{"q": "What does 'ps aux' show?", "options": ["Only your processes", "All processes for all users", "Only background tasks", "Network processes"], "answer": 1, "explain": "a=all users, u=user-oriented format, x=includes non-terminal processes."}]),
        Lesson("top", "SYSTEM MONITORING", "List Processes (top)", "Dynamic real-time view of running system. *Interactive TTY simulated.*", "top", 
               [{"q": "How do you quit the 'top' command?", "options": ["ctrl+c", "esc", "q", "Both q and ctrl+c"], "answer": 3, "explain": "Both 'q' and 'ctrl+c' will safely terminate the top interface."}]),
        Lesson("df", "SYSTEM MONITORING", "Disk Space (df)", "Displays disk space available on file systems. `-h` human-readable.", "df -h", 
               [{"q": "What does the '-h' flag do in df?", "options": ["Shows hidden disks", "Human-readable sizes (KB, MB, GB)", "Hides remote drives", "Shows history"], "answer": 1, "explain": "-h converts raw bytes into easily readable formats like Megabytes and Gigabytes."}]),
        Lesson("du", "SYSTEM MONITORING", "Directory Usage (du)", "Estimates file and folder space usage. `-sh *` summarizes current folder.", "du -sh *", 
               [{"q": "What does the 's' flag do in 'du -sh'?", "options": ["Sorts by size", "Displays speed", "Summarizes total for each item", "Shows subdirectories"], "answer": 2, "explain": "-s provides a total for each argument, instead of showing every sub-folder."}]),
        Lesson("free", "SYSTEM MONITORING", "Memory Usage (free)", "Displays total, used, and free physical and swap memory.", "free -h", 
               [{"q": "Which column in 'free' shows actual usable RAM?", "options": ["total", "used", "buff/cache", "available"], "answer": 3, "explain": "available estimates the memory that can be given to applications without swapping."}]),
        Lesson("kill", "SYSTEM MONITORING", "Terminate (kill)", "Sends a signal to terminate a process using its PID. `-9` forces it.", "echo 'Run a sleep command in background (&), find PID with ps, and kill it.'", 
               [{"q": "What does 'kill -9' do?", "options": ["Pauses the process", "Sends a polite stop request", "Forcefully kills it immediately", "Restarts it"], "answer": 2, "explain": "-9 sends SIGKILL, which forcefully and immediately terminates the process."}]),
        Lesson("uptime", "SYSTEM MONITORING", "Uptime", "Tells you how long the system has been running and system load averages.", "uptime", 
               [{"q": "What three numbers does uptime show at the end?", "options": ["CPU temps", "Load averages (1, 5, 15 mins)", "Users logged in", "Process counts"], "answer": 1, "explain": "It shows system load averages over the last 1, 5, and 15 minutes."}]),
        
        # NETWORKING
        Lesson("ping", "NETWORKING", "Ping", "Tests connectivity to another network device using ICMP packets. `-c 3` sends 3 packets.", "ping -c 3 localhost", 
               [{"q": "What protocol does ping use?", "options": ["TCP", "HTTP", "ICMP", "UDP"], "answer": 2, "explain": "Ping uses Internet Control Message Protocol (ICMP) Echo Request messages."}]),
        Lesson("curl", "NETWORKING", "URL Transfer (curl)", "Transfers data to/from a server. Supports HTTP, HTTPS, FTP.", "curl -s http://example.com | head -n 5", 
               [{"q": "What is curl primarily used for in scripting?", "options": ["Editing files", "Transferring data to/from URLs", "Pinging IPs", "Managing disks"], "answer": 1, "explain": "curl is a tool to transfer data from or to a server."}]),
        Lesson("wget", "NETWORKING", "Downloader (wget)", "Non-interactive network downloader. *Disabled in sandbox for security.*", "echo 'wget is disabled in this sandbox.'", 
               [{"q": "What is the main difference between wget and curl?", "options": ["wget is interactive", "wget is designed to download files non-interactively", "curl is slower", "There is no difference"], "answer": 1, "explain": "wget is recursive and great for downloading, while curl is better for API interactions."}]),
        Lesson("ssh", "NETWORKING", "Remote Connect (ssh)", "Secure Shell. Used to log into a remote machine securely. *Interactive TTY simulated.*", "ssh user@server.com", 
               [{"q": "What is the default port for SSH?", "options": ["21", "80", "443", "22"], "answer": 3, "explain": "SSH listens on port 22 by default."}]),
        Lesson("scp", "NETWORKING", "Secure Copy (scp)", "Uses SSH to securely copy files between local and remote hosts. *Simulated.*", "echo 'scp requires a remote host.'", 
               [{"q": "What does scp stand for?", "options": ["Super Copy", "Secure Copy", "System Copy", "Shell Copy"], "answer": 1, "explain": "Secure Copy Protocol."}]),
        Lesson("rsync", "NETWORKING", "File Sync (rsync)", "Fast file-copying tool. Only transfers differences to save bandwidth.", "mkdir backup && rsync -av ./my_folder/ ./backup/ && ls backup", 
               [{"q": "Why is rsync often faster/better than cp for backups?", "options": ["It uses more CPU", "It only transfers the differences (deltas)", "It compresses the hard drive", "It ignores large files"], "answer": 1, "explain": "rsync only copies the parts of files that have changed."}]),
        
        # FILE COMPRESSION
        Lesson("zip", "FILE COMPRESSION", "Compress (zip)", "Compresses files into `.zip`. `-r` is required for folders.", "zip my_archive.zip hello.txt data.csv && ls -lh my_archive.zip", 
               [{"q": "How do you zip an entire directory?", "options": ["zip file.zip folder", "zip -r file.zip folder", "zip -a file.zip folder", "zip -c file.zip folder"], "answer": 1, "explain": "The -r (recursive) flag is required to include subdirectories."}]),
        Lesson("unzip", "FILE COMPRESSION", "Extract (unzip)", "Extracts files from a `.zip`. `-l` lists contents without extracting.", "unzip -l my_archive.zip", 
               [{"q": "How do you just view the contents of a zip without extracting?", "options": ["unzip -v file.zip", "unzip -l file.zip", "unzip -s file.zip", "unzip -c file.zip"], "answer": 1, "explain": "The -l flag lists the contents."}]),
        Lesson("tar", "FILE COMPRESSION", "TAR Archive (tar)", "Standard Linux archiving. `-c` create, `-z` gzip, `-v` verbose, `-f` file, `-x` extract.", "tar -czvf backup.tar.gz hello.txt && ls -lh backup.tar.gz", 
               [{"q": "What does the '-z' flag do in tar?", "options": ["Zip", "Gzip compression", "Unzip", "List"], "answer": 1, "explain": "-z compresses the archive using gzip."}]),
        
        # FILE PERMISSIONS
        Lesson("ownership_concept", "FILE PERMISSIONS", "Ownership Concept", "Every file has a User (owner), Group, and Others. Permissions: **r** (Read=4), **w** (Write=2), **x** (Execute=1).", "ls -l hello.txt", 
               [{"q": "What number represents the 'Execute' permission?", "options": ["1", "2", "3", "4"], "answer": 0, "explain": "Read=4, Write=2, Execute=1."}]),
        Lesson("chmod", "FILE PERMISSIONS", "Modify (chmod)", "Alters permissions using numeric codes. `755` (rwxr-xr-x), `644` (rw-r--r--).", "chmod 777 hello.txt && ls -l hello.txt", 
               [{"q": "What permissions does '644' give?", "options": ["Everyone can edit", "Owner: rw, Group/Others: r", "Owner: rwx, Others: none", "No permissions"], "answer": 1, "explain": "6(rw-) for owner, 4(r--) for group, 4(r--) for others."}]),
        Lesson("chown", "FILE PERMISSIONS", "Ownership (chown)", "Changes the user ownership. Requires root privileges (Will show error in sandbox).", "chown root hello.txt", 
               [{"q": "Why might chown fail for a normal user?", "options": ["File is too big", "You need root/sudo privileges", "File is a directory", "Wrong extension"], "answer": 1, "explain": "Only the root user can change ownership of a file to another user."}]),
        Lesson("chgrp", "FILE PERMISSIONS", "Group (chgrp)", "Changes the group ownership. Also requires elevated privileges.", "chgrp wheel hello.txt", 
               [{"q": "What does chgrp change?", "options": ["The owner", "The group", "The permissions", "The filename"], "answer": 1, "explain": "chgrp changes the group associated with a file."}]),
        
        # SCRIPTING
        Lesson("syntax", "SCRIPTING", "Syntax & Shebang", "First line must be `#!/bin/bash`. Run with `chmod +x script.sh` then `./script.sh`.", "echo '#!/bin/bash\\necho Hello from script' > myscript.sh && chmod +x myscript.sh && ./myscript.sh", 
               [{"q": "What is the first line of a bash script called?", "options": ["Hash line", "Shebang", "Interpreter", "Header"], "answer": 1, "explain": "The shebang (#!) tells the OS which interpreter to use."}]),
        Lesson("variables", "SCRIPTING", "Variables", "Store data. **No spaces around `=`**. Access with `$`.", "MY_OS=\"Linux\" && echo \"I love $MY_OS\"", 
               [{"q": "How do you read a variable in Bash?", "options": ["NAME", "$NAME", "%NAME%", "&NAME"], "answer": 1, "explain": "The dollar sign $ must precede the variable name."}]),
        Lesson("datatypes", "SCRIPTING", "Data Types & Math", "Everything is a string. Use `$((...))` for integer math.", "A=15 && B=5 && echo \"Sum: $((A+B)) Mult: $((A*B))\"", 
               [{"q": "How do you perform math in Bash?", "options": ["$[A+B]", "$(A+B)", "$((A+B))", "math(A+B)"], "answer": 2, "explain": "Double parentheses $((...)) are used for arithmetic expansion."}]),
        Lesson("operators", "SCRIPTING", "Operators (If/Else)", "Conditionals: `-eq` (equal), `-ne` (not equal), `-gt` (greater). *Spaces around `[ ]` are mandatory.*", "A=10 && B=20 && if [ $A -lt $B ]; then echo 'A is less'; fi", 
               [{"q": "What does '-eq' mean in an if statement?", "options": ["Not equal", "Equals", "Greater than", "Less than"], "answer": 1, "explain": "-eq stands for equal (used for numbers)."}]),
        Lesson("loops", "SCRIPTING", "Loops", "Repeat commands. **For loop** iterates over a list of items.", "for i in apple banana cherry; do echo \"Fruit: $i\"; done", 
               [{"q": "What signifies the end of a loop block in Bash?", "options": ["end", "done", "fi", "stop"], "answer": 1, "explain": "Bash uses the keyword 'done' to close for and while loops."}]),
        Lesson("functions", "SCRIPTING", "Functions", "Group commands under a name. `$1` is the first argument passed.", "greet() { echo \"Hello, $1!\"; }\ngreet \"Developer\"", 
               [{"q": "How do you access the first argument passed to a function?", "options": ["$1", "$0", "$first", "$arg1"], "answer": 0, "explain": "$1 is the first positional parameter. ($0 is the script name)"}]),
        Lesson("arrays", "SCRIPTING", "Arrays", "Hold multiple values. Access all with `@` or specific items with index `[0]`.", "FRUITS=(\"Apple\" \"Banana\" \"Cherry\")\necho \"First: ${FRUITS[0]}\"\necho \"All: ${FRUITS[@]}\"", 
               [{"q": "How do you print all elements of an array?", "options": ["${ARRAY}", "${ARRAY[*]}", "${ARRAY[@]}", "Both * and @"], "answer": 3, "explain": "Both ${ARRAY[*]} and ${ARRAY[@]} expand to all elements."}]),
        Lesson("cron", "SCRIPTING", "Schedule (cron)", "Time-based job scheduler. Edit with `crontab -e`.", "crontab -l", 
               [{"q": "What command do you use to edit your cron jobs?", "options": ["cron -e", "crontab -e", "editcron", "schedule -e"], "answer": 1, "explain": "crontab -e opens the crontab file for editing."}]),
    ]

# -------------------------------------------------------
# Main Application Layout
# -------------------------------------------------------
def main():
    init_bash_sandbox()
    lessons = get_all_lessons()
    
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

    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.markdown("### 📚 Syllabus & Lessons")
        selected_label = st.selectbox("Choose a topic", selectbox_options, label_visibility="collapsed")
        
        if selected_label.startswith("    ⚡"):
            current_lesson = options_map[selected_label]
            
            st.markdown(f"## {current_lesson.title}")
            card("note", "Concept", current_lesson.theory)
            
            if st.button(f"▶️ Run Example Command", key=f"run_{current_lesson.id}", use_container_width=True):
                output = run_bash_command(current_lesson.demo_cmd)
                st.session_state.term_history.append({"cmd": current_lesson.demo_cmd, "out": output})
                
            st.code(current_lesson.demo_cmd, language="bash")
            
            # MCQ Section Renders Here Automatically Now
            if current_lesson.quiz:
                st.markdown("---")
                render_mcq(current_lesson.quiz, f"mcq_{current_lesson.id}")
            
            st.markdown("---")
            if st.checkbox(f"✅ Mark '{current_lesson.title}' as Complete", key=f"prog_{current_lesson.id}"):
                st.success("Progress saved!")
        else:
            st.info("👈 Select a specific lesson from the dropdown above to view its theory, MCQs, and run examples.")

    with right_col:
        st.markdown("### 🖥️ Live Linux Terminal")
        st.caption(f"Working Dir: `{st.session_state.sandbox_dir}`")
        
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
        
        if user_cmd := st.chat_input("Enter command:", key="term_input"):
            if user_cmd.strip():
                out = run_bash_command(user_cmd)
                st.session_state.term_history.append({"cmd": user_cmd, "out": out})

if __name__ == "__main__":
    main()