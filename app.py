# =========================
# Linux-Virtual-Tutor — Claymorphism UI + Full Data (Text Visibility Fixed)
# =========================
import subprocess
import os
import tempfile
from dataclasses import dataclass
from typing import List, Dict, Any
import streamlit as st

# -------------------------------------------------------
# CLAYMORPHISM CSS (Fixed Text Visibility)
# -------------------------------------------------------
st.set_page_config(page_title="Linux-Virtual-Tutor • Clay UI", page_icon="🪵", layout="wide")

CLAY_CSS = """
<style>
    /* Global Background */
    .stApp { background-color: #e0e5ec !important; }

    /* FORCE DARK TEXT EVERYWHERE TO PREVENT INVISIBLE TEXT BUG */
    h1, h2, h3, h4, h5, h6, p, span, li, div, label, a,
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span,
    .stText, .stCaption, .stCaption p {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #2d3436 !important;
    }
    h1, h2, h3 { font-weight: 800; text-shadow: 2px 2px 4px rgba(163,177,198,0.6); }

    /* Clay Card Base */
    .card {
        border: none; border-radius: 20px; padding: 22px 25px; background: #e0e5ec; margin: 15px 0;
        box-shadow: 9px 9px 16px #b8bec7, -9px -9px 16px #ffffff; transition: all 0.2s ease; line-height: 1.7;
    }

    /* SPECIFIC FIX FOR INVISIBLE TITLE & TEXT INSIDE CARDS */
    .card .title {
        font-weight: 800 !important; margin-bottom: 10px; font-size: 1.2rem;
        color: #000000 !important; /* Force Black for titles */
    }
    .card p, .card div, .card span {
        color: #333333 !important; /* Force Dark Grey for body text */
    }

    /* Clay Card Variants */
    .card.note  { border-left: 6px solid #74b9ff; box-shadow: 9px 9px 16px #b8bec7, -9px -9px 16px #ffffff, inset 3px 0 0px #a4d0ff; }
    .card.tip   { border-left: 6px solid #55efc4; box-shadow: 9px 9px 16px #b8bec7, -9px -9px 16px #ffffff, inset 3px 0 0px #81ffdb; }
    .card.warn  { border-left: 6px solid #ffeaa7; box-shadow: 9px 9px 16px #b8bec7, -9px -9px 16px #ffffff, inset 3px 0 0px #fff3b0; }

    /* Terminal Container */
    .term-container {
        background: #e0e5ec; border-radius: 25px; padding: 15px;
        box-shadow: 12px 12px 24px #b8bec7, -12px -12px 24px #ffffff; margin-top: 20px;
    }
    .term-container h3 { color: #000000 !important; } /* Terminal Title Fix */
    .term-container div { color: #2d3436 !important; }

    /* Terminal Inner Screen (deliberately light text on dark screen) */
    .term-box {
        background-color: #2d3436; color: #dfe6e9 !important; border-radius: 15px; padding: 20px;
        font-family: 'Fira Code', 'Consolas', monospace; font-size: 14px;
        height: 350px; overflow-y: auto; border: none;
        box-shadow: inset 6px 6px 12px #1e2325, inset -6px -6px 12px #3c4547;
    }
    .term-box span, .term-box div { color: inherit !important; }
    .term-cmd { color: #00cec9 !important; margin-bottom: 4px; white-space: pre-wrap; font-weight: bold;}
    .term-out { color: #dfe6e9 !important; white-space: pre-wrap; margin-bottom: 15px; border-bottom: 1px solid #636e72; padding-bottom: 10px;}

    /* Buttons Override */
    .stButton > button, .stButton > button p, .stButton > button div, .stButton > button span {
        background: #e0e5ec !important; color: #2d3436 !important; border: none !important;
        border-radius: 12px !important; box-shadow: 6px 6px 12px #b8bec7, -6px -6px 12px #ffffff !important;
        font-weight: 700 !important; transition: 0.2s !important;
    }
    .stButton > button:active { box-shadow: inset 4px 4px 8px #b8bec7, inset -4px -4px 8px #ffffff !important; }

    /* Code Blocks */
    [data-testid="stCode"], [data-testid="stCode"] * {
        background-color: #e0e5ec; border: none; border-radius: 12px;
        color: #2d3436 !important; font-weight: 600;
    }
    [data-testid="stCode"] { box-shadow: inset 4px 4px 8px #b8bec7, inset -4px -4px 8px #ffffff; }

    /* Selectbox, Radio & Checkbox Labels */
    [data-testid="stSelectbox"] label, [data-testid="stCheckbox"] label,
    [data-testid="stRadio"] label, [data-testid="stRadio"] div,
    [data-testid="stRadio"] p, [data-testid="stMarkdownContainer"] p {
        color: #2d3436 !important;
        font-weight: 600 !important;
    }

    /* Closed Selectbox control (the visible box before you click it) */
    [data-baseweb="select"] > div {
        background-color: #e0e5ec !important;
        border-color: #b8bec7 !important;
        box-shadow: inset 3px 3px 6px #b8bec7, inset -3px -3px 6px #ffffff !important;
    }
    [data-baseweb="select"] * {
        color: #2d3436 !important;
        fill: #2d3436 !important;
    }

    /* Open dropdown menu / options list (rendered in a portal, easy to miss) */
    div[data-baseweb="popover"] { z-index: 9999 !important; }
    div[data-baseweb="popover"] ul, div[data-baseweb="popover"] li,
    div[data-baseweb="menu"] ul, div[data-baseweb="menu"] li {
        background-color: #ffffff !important;
        color: #2d3436 !important;
    }
    div[data-baseweb="popover"] li:hover, div[data-baseweb="menu"] li:hover {
        background-color: #e0e5ec !important;
        color: #000000 !important;
    }

    /* Alerts: st.info / st.success / st.warning / st.error */
    div[data-testid="stAlert"], div[data-testid="stAlert"] * {
        color: #2d3436 !important;
    }

    /* Chat input box (Practice Terminal input) */
    [data-testid="stChatInput"] textarea, [data-testid="stChatInput"] * {
        color: #2d3436 !important;
    }
    [data-testid="stChatInput"] {
        background-color: #e0e5ec !important;
        box-shadow: inset 3px 3px 6px #b8bec7, inset -3px -3px 6px #ffffff !important;
        border-radius: 12px !important;
    }
</style>
"""
st.markdown(CLAY_CSS, unsafe_allow_html=True)

# -------------------------------------------------------
# UI Helpers
# -------------------------------------------------------
def card(kind: str, title: str, body: str):
    # Ensure body text maintains line breaks
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
# COMPLETE DATABASE (Using Triple Quotes)
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
        Lesson("intro", "HOME", "Bash Introduction",
               """Bash (Bourne Again SHell) is a Unix shell and command language interpreter. It is the default login shell for most Linux distributions and macOS. A shell is simply a macro processor that executes commands from a terminal or a file. It acts as a bridge between the user and the Linux kernel, taking your text commands and translating them into system operations.""",
               "echo $BASH_VERSION",
               [{"q": "What does Bash stand for?", "options": ["Bourne Again SHell", "Basic Shell", "Binary Shell", "Boot Shell"], "answer": 0, "explain": "Bourne Again SHell, a pun on the earlier Bourne shell (sh)."}]),

        Lesson("filesystem", "HOME", "Linux File System",
               """Unlike Windows which uses drive letters (C:, D:), Linux has a single root directory represented by a forward slash `/`. Everything on the system resides under this root. Understanding this hierarchy is crucial.\n\n**Key Directories:**\n- `/` (Root): The top-level directory.\n- `/bin`: Essential user command binaries (e.g., `ls`, `cp`, `cat`) needed in single-user mode.\n- `/etc`: System-wide configuration files for the system and installed software.\n- `/sbin`: System binaries, typically used by the root user for system administration (e.g., `reboot`, `fdisk`).\n- `/home`: Personal directories for regular users (e.g., `/home/student`).\n- `/var`: Variable data files such as logs (`/var/log`), databases, and email spools.\n- `/usr`: Read-only user application data, utilities, and documentation (e.g., `/usr/bin`, `/usr/lib`).\n- `/tmp`: Temporary files created by programs; usually cleared upon reboot.""",
               "ls /",
               [{"q": "Where are system-wide configuration files stored?", "options": ["/bin", "/etc", "/var", "/usr"], "answer": 1, "explain": "The /etc directory contains host-specific system-wide configuration files."}]),

        Lesson("get_started", "HOME", "Get Started",
               """When you open a terminal, you are placed inside your home directory. You will see a prompt like `user@hostname:~$`. The `~` is a shortcut for your home directory. The `$` indicates you are a standard user (if you were root, it would be `#`). All commands follow the syntax: `command [options] [arguments]`.""",
               "whoami",
               [{"q": "What does the `~` symbol mean in a terminal path?", "options": ["Root directory", "Current folder", "User's home directory", "Hidden files"], "answer": 2, "explain": "The tilde ~ is a shortcut for the current user's home directory."}]),

        # BASIC COMMANDS
        Lesson("ls", "BASIC COMMANDS", "List (ls)",
               """The `ls` command is one of the most frequently used commands in Linux. It stands for 'list' and is used to display the contents of a directory. By default, it lists the files and directories in your current location.\n\n**Common Options:**\n- `ls -l`: Displays files in a long listing format, showing permissions, owner, size, and modification date.\n- `ls -a`: Shows all files, including hidden files (those starting with a dot `.` like `.bashrc`).\n- `ls -h`: Used with `-l`, it prints file sizes in a human-readable format (e.g., 1K, 234M, 2G) instead of raw bytes.\n- `ls -R`: Recursively lists all subdirectories found.""",
               "ls -lah",
               [{"q": "Which flag shows hidden files?", "options": ["-l", "-a", "-h", "-r"], "answer": 1, "explain": "The -a flag shows all files, including those starting with a dot."}]),

        Lesson("cd", "BASIC COMMANDS", "Change Dir (cd)",
               """The `cd` command stands for 'Change Directory'. It is used to navigate between different folders in the file system. Without any arguments, `cd` will always return you to your home directory.\n\n**Path Types:**\n- **Absolute Path:** Starts from the root `/` (e.g., `cd /var/log`).\n- **Relative Path:** Starts from your current location (e.g., `cd my_folder`).\n\n**Shortcuts:**\n- `cd ..`: Moves up one level to the parent directory.\n- `cd ~` or `cd`: Goes straight to your home directory.\n- `cd -`: Toggles you back to the previous directory you were in.""",
               "cd my_folder && pwd && cd ..",
               [{"q": "What does `cd ..` do?", "options": ["Goes to root", "Moves up one level", "Goes home", "Lists files"], "answer": 1, "explain": "Double dot refers to the parent directory."}]),

        Lesson("pwd", "BASIC COMMANDS", "Print Dir (pwd)",
               """The `pwd` command stands for 'Print Working Directory'. It outputs the full, absolute path of the directory you are currently in. This is incredibly useful when you are deep inside a nested folder structure and have lost track of your exact location.""",
               "pwd",
               [{"q": "What does PWD stand for?", "options": ["Print Word Doc", "Print Working Directory", "Process Wide Data", "Path Way Down"], "answer": 1, "explain": "It stands for Print Working Directory."}]),

        Lesson("echo", "BASIC COMMANDS", "Echo (echo)",
               """The `echo` command is used to print text or variables to the standard output (your screen). While simple, it is one of the most heavily used commands in Bash scripting for displaying status messages, debugging, and writing text into files.\n\n**Common Options:**\n- `echo -n`: Does not output the trailing newline (useful for prompts).\n- `echo -e`: Enables interpretation of backslash escapes, allowing you to format text (e.g., `\\n` for newlines, `\\t` for tabs).""",
               "echo -e 'Hello\\nWorld'",
               [{"q": "Which flag allows you to use newlines (\\n) in echo?", "options": ["-n", "-v", "-e", "-f"], "answer": 2, "explain": "The -e flag enables interpretation of backslash escapes."}]),

        Lesson("cat", "BASIC COMMANDS", "Concatenate (cat)",
               """The `cat` command (short for concatenate) reads data from files and outputs their contents to the terminal. It is the quickest way to view small files.\n\n**Uses:**\n- `cat file.txt`: Displays the entire content of a file.\n- `cat file1.txt file2.txt > combined.txt`: Concatenates multiple files and saves them into a new one using the `>` redirect operator.\n- `cat > new.txt`: Creates a new file and allows you to type into it directly (press `Ctrl+D` to save and exit).""",
               "cat hello.txt",
               [{"q": "What is 'cat' short for?", "options": ["Category", "Concatenate", "Catalog", "Capture"], "answer": 1, "explain": "It was originally designed to concatenate files."}]),

        Lesson("cp", "BASIC COMMANDS", "Copy (cp)",
               """The `cp` command is used to copy files or directories from one location to another. It requires at least two arguments: the source and the destination.\n\n**Common Options:**\n- `cp source.txt dest.txt`: Copies a file.\n- `cp -r source_folder/ dest_folder/`: The `-r` (recursive) flag is strictly required when copying an entire directory and everything inside it. Without it, the command will fail.""",
               "cp hello.txt backup.txt && ls",
               [{"q": "Which flag is required to copy a whole directory?", "options": ["-f", "-a", "-r", "-i"], "answer": 2, "explain": "The -r (recursive) flag is required to copy directories."}]),

        Lesson("mv", "BASIC COMMANDS", "Move (mv)",
               """The `mv` command serves two distinct purposes in Linux: moving files from one place to another, and renaming files. It does not create a copy; the original file disappears from its starting location.\n\n**Syntax:**\n- `mv old_name.txt new_name.txt`: Renames a file in the current directory.\n- `mv file.txt /my_folder/`: Moves the file into the specified folder.""",
               "mv backup.txt my_folder/ && ls my_folder/",
               [{"q": "Besides moving, what is 'mv' commonly used for?", "options": ["Deleting", "Renaming", "Copying", "Reading"], "answer": 1, "explain": "Moving a file to the same directory with a new name renames it."}]),

        Lesson("rm", "BASIC COMMANDS", "Remove (rm)",
               """The `rm` command is used to delete files or directories. **Warning:** Linux does not have a 'Recycle Bin' by default. When you use `rm`, the file is permanently deleted.\n\n**Common Options:**\n- `rm file.txt`: Deletes a file.\n- `rm -r folder/`: Deletes a folder and all of its contents recursively.\n- `rm -i file.txt`: Interactive mode; asks you to confirm before deleting each file (safer).""",
               "cp hello.txt del_me.txt && rm del_me.txt && ls",
               [{"q": "How do you delete a folder and everything inside it?", "options": ["rm folder/", "rm -r folder/", "rm -f folder/", "rm -a folder/"], "answer": 1, "explain": "The -r (recursive) flag is required to remove directories."}]),

        Lesson("touch", "BASIC COMMANDS", "Timestamp (touch)",
               """The `touch` command has two primary uses. First, it is the fastest way to create empty files (e.g., creating placeholder files for a project). Second, if a file already exists, `touch` updates its 'last accessed' and 'last modified' timestamps to the current time without altering the file's content.""",
               "touch newfile.txt && ls -l newfile.txt",
               [{"q": "If a file already exists, what does 'touch' do?", "options": ["Deletes it", "Appends to it", "Updates its timestamp", "Overwrites it"], "answer": 2, "explain": "Touch updates the last access and modification times."}]),

        Lesson("mkdir", "BASIC COMMANDS", "Make Dir (mkdir)",
               """The `mkdir` command stands for 'Make Directory' and is used to create new folders.\n\n**Common Options:**\n- `mkdir folder_name`: Creates a single folder.\n- `mkdir -p parent/child/grandchild`: The `-p` (parents) flag is incredibly useful. It creates the entire nested path, including any missing parent directories, in one single command. Without `-p`, it would throw an error if `parent` didn't already exist.""",
               "mkdir -p project/src && ls -R project",
               [{"q": "How do you create 'parent/child' if 'parent' doesn't exist?", "options": ["mkdir parent/child", "mkdir -c parent/child", "mkdir -p parent/child", "mkdir -r parent/child"], "answer": 2, "explain": "The -p flag creates parent directories as needed."}]),

        Lesson("man", "BASIC COMMANDS", "Manual (man)",
               """The `man` command opens the built-in Linux manual pages. Almost every command, configuration file, or system call has a 'man page' that serves as its ultimate documentation. It is the most important command for learning Linux.\n\n**How to use it:**\n- Type `man ls` to open the manual for `ls`.\n- Use **Arrow Keys** to scroll up and down.\n- Press **q** to quit and return to the terminal.""",
               "man ls",
               [{"q": "What do you press to quit the 'man' pages?", "options": ["esc", "ctrl+c", "q", "x"], "answer": 2, "explain": "Pressing 'q' quits the man pager."}]),

        Lesson("alias", "BASIC COMMANDS", "Alias",
               """The `alias` command allows you to create custom keyboard shortcuts or alternate names for commands. It is heavily used to save typing long, complex commands.\n\n**Example:** `alias ll='ls -la'`. Now, typing just `ll` will execute `ls -la`.\n\n*Note: Aliases created in the terminal are temporary and will be lost when you close the session. To make them permanent, you must add them to your `~/.bashrc` file.*""",
               "alias c='echo I am an alias!' && c",
               [{"q": "Where do you save aliases so they persist after reboot?", "options": ["/etc/hosts", "~/.bashrc", "/bin/bash", "~/.alias"], "answer": 1, "explain": "Adding them to ~/.bashrc ensures they load on every new terminal session."}]),

        # TEXT PROCESSING
        Lesson("grep", "TEXT PROCESSING", "Search Text (grep)",
               """The `grep` command stands for 'Global Regular Expression Print'. It is an incredibly powerful tool used to search for specific text patterns or words inside files. It prints the lines that match your search term.\n\n**Common Options:**\n- `grep 'word' file.txt`: Finds lines containing 'word'.\n- `grep -i 'word' file.txt`: Case-insensitive search (matches Word, WORD, word).\n- `grep -n 'word' file.txt`: Shows the line number where the match was found.\n- `grep -r 'word' /folder/`: Recursively searches all files inside a directory.""",
               "grep 'Alice' data.csv",
               [{"q": "Which flag makes grep case-insensitive?", "options": ["-n", "-c", "-i", "-r"], "answer": 2, "explain": "The -i flag ignores upper/lower case differences."}]),

        Lesson("awk", "TEXT PROCESSING", "Pattern Scan (awk)",
               """`awk` is not just a command, but a full programming language designed specifically for text processing and data extraction. It reads a file line by line, treats each line as a record, and splits words (separated by spaces or custom delimiters) into fields.\n\n**Basic Syntax:** `awk -F',' '{print $1}' file.csv`\n- `-F','`: Sets the field separator to a comma.\n- `$1`: Represents the first column. `$0` represents the entire line.""",
               "awk -F',' '{print $1, $3}' data.csv",
               [{"q": "In awk, what does '$1' represent?", "options": ["The whole line", "The first word/column", "The last column", "The filename"], "answer": 1, "explain": "$1 refers to the first field in the record."}]),

        Lesson("sed", "TEXT PROCESSING", "Stream Editor (sed)",
               """`sed` stands for 'Stream Editor'. It is primarily used for filtering and transforming text, most commonly for 'Find and Replace' operations directly in the terminal without opening a text editor.\n\n**Find and Replace Syntax:** `sed 's/old_word/new_word/g' file.txt`\n- `s`: Stands for substitute.\n- `g`: Stands for global. It replaces all occurrences on a line. Without `g`, it only replaces the first occurrence.""",
               "sed 's/Hello/Hi/g' hello.txt",
               [{"q": "In 's/old/new/g', what does the 'g' stand for?", "options": ["Global", "Group", "Generate", "Grep"], "answer": 0, "explain": "The 'g' flag means 'global', replacing all instances on a line."}]),

        Lesson("cut", "TEXT PROCESSING", "Remove Section (cut)",
               """The `cut` command is used to extract specific columns or characters from each line of a file or input. It is simpler than `awk` and perfect for quick column extraction.\n\n**Common Options:**\n- `cut -d',' -f1 file.csv`: Uses a comma `-d','` as the delimiter and extracts field 1 `-f1`.\n- `cut -c1-5 file.txt`: Extracts characters 1 through 5 from every line.""",
               "cut -d',' -f2 data.csv",
               [{"q": "Which flag specifies the delimiter in cut?", "options": ["-d", "-f", "-s", "-c"], "answer": 0, "explain": "The -d flag specifies the delimiter (e.g., -d',')."}]),

        Lesson("sort", "TEXT PROCESSING", "Sort Lines (sort)",
               """The `sort` command, as the name implies, sorts the lines of a text file alphabetically or numerically and outputs the result.\n\n**Common Options:**\n- `sort file.txt`: Sorts alphabetically.\n- `sort -n file.txt`: Sorts numerically (crucial for numbers like 2, 10, 1, otherwise 10 comes before 2).\n- `sort -r file.txt`: Reverses the sorting order (descending).""",
               "sort data.csv",
               [{"q": "How do you sort a list of numbers correctly?", "options": ["sort file.txt", "sort -n file.txt", "sort -r file.txt", "sort -c file.txt"], "answer": 1, "explain": "The -n flag sorts numerically instead of alphabetically."}]),

        Lesson("tail", "TEXT PROCESSING", "View End (tail)",
               """The `tail` command outputs the last part of files. It is an essential tool for system administrators to read the bottom of constantly updating log files (e.g., checking the latest errors).\n\n**Common Options:**\n- `tail -n 20 file.txt`: Shows exactly the last 20 lines.\n- `tail -f /var/log/syslog`: Follows the file in real-time, printing new lines as they are added (cannot be used in this sandbox).""",
               "tail -n 2 hello.txt",
               [{"q": "How do you view the last 10 lines of a file?", "options": ["tail -n 10 file", "tail -l 10 file", "tail -c 10 file", "tail -e 10 file"], "answer": 0, "explain": "tail -n 10 is the correct syntax."}]),

        Lesson("head", "TEXT PROCESSING", "View Start (head)",
               """The `head` command is the exact opposite of `tail`. It outputs the first part of files, which is useful for previewing the structure or headers of a large file without loading the whole thing into memory.\n\n**Common Options:**\n- `head -n 5 file.txt`: Shows exactly the first 5 lines.""",
               "head -n 1 data.csv",
               [{"q": "What is the default number of lines 'head' prints?", "options": ["5", "15", "10", "All"], "answer": 2, "explain": "By default, head prints the first 10 lines."}]),

        # SYSTEM MONITORING
        Lesson("ps", "SYSTEM MONITORING", "Process Status (ps)",
               """The `ps` command stands for 'Process Status'. It reports a snapshot of the currently running processes on your system, including their Process IDs (PIDs), CPU usage, and memory usage.\n\n**Common Options:**\n- `ps`: Shows only processes running in your current terminal.\n- `ps aux`: Shows **all** processes for **all** users in a detailed format. `a`=all users, `u`=user-oriented, `x`=non-terminal processes.""",
               "ps aux | head -n 5",
               [{"q": "What does 'ps aux' show?", "options": ["Only your processes", "All processes for all users", "Only background tasks", "Network processes"], "answer": 1, "explain": "a=all users, u=user format, x=non-terminal processes."}]),

        Lesson("top", "SYSTEM MONITORING", "List Processes (top)",
               """Unlike `ps` which shows a static snapshot, `top` provides a dynamic, real-time view of the running system. It constantly updates to show which processes are consuming the most CPU and Memory. *Note: This is an interactive TTY application, simulated here.*""",
               "top",
               [{"q": "How do you quit the 'top' command?", "options": ["ctrl+c", "esc", "q", "Both q and ctrl+c"], "answer": 3, "explain": "Both 'q' and 'ctrl+c' will safely terminate the top interface."}]),

        Lesson("df", "SYSTEM MONITORING", "Disk Space (df)",
               """The `df` command stands for 'Disk Free'. It displays the amount of disk space available on your computer's file systems, showing total size, used space, and available space.\n\n**Common Options:**\n- `df -h`: The `-h` (human-readable) flag is almost always used with `df` to print sizes in KB, MB, or GB instead of raw, hard-to-read bytes.""",
               "df -h",
               [{"q": "What does the '-h' flag do in df?", "options": ["Shows hidden disks", "Human-readable sizes", "Hides remote drives", "Shows history"], "answer": 1, "explain": "-h converts raw bytes into easily readable formats like Megabytes."}]),

        Lesson("du", "SYSTEM MONITORING", "Directory Usage (du)",
               """While `df` shows entire drives, the `du` command ('Disk Usage') estimates the file and directory space usage for specific folders. It helps you find out which folders are eating up your storage.\n\n**Common Options:**\n- `du -sh *`: `-s` summarizes the total size of each item in the current folder, and `-h` makes it human-readable. This is the most common way to check folder sizes.""",
               "du -sh *",
               [{"q": "What does the 's' flag do in 'du -sh'?", "options": ["Sorts by size", "Displays speed", "Summarizes total for each item", "Shows subdirectories"], "answer": 2, "explain": "-s provides a total for each argument, instead of showing sub-folders."}]),

        Lesson("free", "SYSTEM MONITORING", "Memory Usage (free)",
               """The `free` command displays the total amount of free and used physical and swap memory in the system. It is the quickest way to check if your server is running out of RAM.\n\n**Common Options:**\n- `free -h`: Prints the output in a human-readable format (Gigabytes/Megabytes).""",
               "free -h",
               [{"q": "Which column in 'free' shows actual usable RAM?", "options": ["total", "used", "buff/cache", "available"], "answer": 3, "explain": "available estimates memory that can be given to apps without swapping."}]),

        Lesson("kill", "SYSTEM MONITORING", "Terminate (kill)",
               """The `kill` command is used to manually terminate unresponsive or unwanted processes. To use it, you must know the Process ID (PID) of the program, which you can find using `ps` or `top`.\n\n**Common Options:**\n- `kill 1234`: Politely asks process 1234 to stop (SIGTERM).\n- `kill -9 1234`: Forcefully and immediately kills process 1234 (SIGKILL). Use this if the polite request fails.""",
               "echo 'Run a sleep command in background (&), find PID with ps, and kill it.'",
               [{"q": "What does 'kill -9' do?", "options": ["Pauses the process", "Sends a polite stop request", "Forcefully kills it immediately", "Restarts it"], "answer": 2, "explain": "-9 sends SIGKILL, which forcefully terminates the process."}]),

        Lesson("uptime", "SYSTEM MONITORING", "Uptime",
               """The `uptime` command tells you how long the Linux system has been running since its last boot. It also provides the current time, the number of logged-in users, and the system load averages over the last 1, 5, and 15 minutes.""",
               "uptime",
               [{"q": "What three numbers does uptime show at the end?", "options": ["CPU temps", "Load averages (1, 5, 15 mins)", "Users logged in", "Process counts"], "answer": 1, "explain": "It shows system load averages over 1, 5, and 15 minutes."}]),

        # NETWORKING
        Lesson("ping", "NETWORKING", "Ping",
               """The `ping` command is a foundational network troubleshooting tool. It tests the connectivity between your machine and another network device (like a website or server) by sending small data packets (ICMP Echo Requests) and waiting for a reply.\n\n**Common Options:**\n- `ping -c 4 google.com`: Sends exactly 4 packets and then stops. Without `-c`, it runs forever until you press Ctrl+C.""",
               "ping -c 3 localhost",
               [{"q": "What protocol does ping use?", "options": ["TCP", "HTTP", "ICMP", "UDP"], "answer": 2, "explain": "Ping uses Internet Control Message Protocol (ICMP)."}]),

        Lesson("curl", "NETWORKING", "URL Transfer (curl)",
               """`curl` is a command-line tool used to transfer data to or from a server. It supports almost every internet protocol (HTTP, HTTPS, FTP). It is heavily used in scripting to download files, test APIs, or fetch webpage source code.""",
               "curl -s http://example.com | head -n 5",
               [{"q": "What is curl primarily used for in scripting?", "options": ["Editing files", "Transferring data to/from URLs", "Pinging IPs", "Managing disks"], "answer": 1, "explain": "curl is a tool to transfer data from or to a server."}]),

        Lesson("wget", "NETWORKING", "Downloader (wget)",
               """`wget` is a non-interactive network downloader. Unlike `curl`, which requires user interaction or complex flags to download files, `wget` is designed to simply download files robustly. It can resume broken downloads and recursively download entire websites. *Disabled in sandbox for security.*""",
               "echo 'wget is disabled in this sandbox.'",
               [{"q": "What is the main difference between wget and curl?", "options": ["wget is interactive", "wget is designed to download files non-interactively", "curl is slower", "There is no difference"], "answer": 1, "explain": "wget is recursive and great for downloading, curl for APIs."}]),

        Lesson("ssh", "NETWORKING", "Remote Connect (ssh)",
               """`ssh` stands for 'Secure Shell'. It is a cryptographic network protocol used to securely log into a remote machine over an unsecured network. It encrypts all traffic, preventing password sniffing. *Interactive TTY simulated here.*""",
               "ssh user@server.com",
               [{"q": "What is the default port for SSH?", "options": ["21", "80", "443", "22"], "answer": 3, "explain": "SSH listens on port 22 by default."}]),

        Lesson("scp", "NETWORKING", "Secure Copy (scp)",
               """`scp` stands for 'Secure Copy'. It uses the same SSH protocol to securely copy files between your local machine and a remote server. It is the safest way to transfer files over the internet. *Simulated here.*""",
               "echo 'scp requires a remote host.'",
               [{"q": "What does scp stand for?", "options": ["Super Copy", "Secure Copy", "System Copy", "Shell Copy"], "answer": 1, "explain": "Secure Copy Protocol."}]),

        Lesson("rsync", "NETWORKING", "File Sync (rsync)",
               """`rsync` is a fast, versatile file-copying tool specialized in synchronizing files and directories between two locations. Its superpower is that it only transfers the *differences* (deltas) between the source and destination, making it incredibly efficient for backups.""",
               "mkdir backup && rsync -av ./my_folder/ ./backup/ && ls backup",
               [{"q": "Why is rsync often faster/better than cp for backups?", "options": ["It uses more CPU", "It only transfers the differences (deltas)", "It compresses the hard drive", "It ignores large files"], "answer": 1, "explain": "rsync only copies the parts of files that have changed."}]),

        # FILE COMPRESSION
        Lesson("zip", "FILE COMPRESSION", "Compress (zip)",
               """The `zip` command compresses files into a `.zip` archive. The `.zip` format is highly compatible and is the standard for sharing files with Windows users.\n\n**Common Options:**\n- `zip archive.zip file1 file2`: Compresses files into an archive.\n- `zip -r archive.zip folder/`: The `-r` (recursive) flag is strictly required to include subdirectories.""",
               "zip my_archive.zip hello.txt data.csv && ls -lh my_archive.zip",
               [{"q": "How do you zip an entire directory?", "options": ["zip file.zip folder", "zip -r file.zip folder", "zip -a file.zip folder", "zip -c file.zip folder"], "answer": 1, "explain": "The -r (recursive) flag is required to include subdirectories."}]),

        Lesson("unzip", "FILE COMPRESSION", "Extract (unzip)",
               """The `unzip` command lists, tests, or extracts files from a `.zip` archive.\n\n**Common Options:**\n- `unzip archive.zip`: Extracts everything to the current directory.\n- `unzip -l archive.zip`: Lists the contents of the archive without actually extracting them (useful for peeking inside).""",
               "unzip -l my_archive.zip",
               [{"q": "How do you just view the contents of a zip without extracting?", "options": ["unzip -v file.zip", "unzip -l file.zip", "unzip -s file.zip", "unzip -c file.zip"], "answer": 1, "explain": "The -l flag lists the contents."}]),

        Lesson("tar", "FILE COMPRESSION", "TAR Archive (tar)",
               """`tar` stands for 'Tape Archive'. It is the standard Linux archiving utility. On its own, `tar` just bundles files together without compressing them. It is almost always combined with a compression algorithm like gzip (`.tar.gz` or `.tgz`).\n\n**Common Flags:**\n- `-c`: Create a new archive.\n- `-x`: Extract an archive.\n- `-z`: Compress/decompress using gzip.\n- `-v`: Verbose (show files being processed).\n- `-f`: Specify the filename of the archive.""",
               "tar -czvf backup.tar.gz hello.txt && ls -lh backup.tar.gz",
               [{"q": "What does the '-z' flag do in tar?", "options": ["Zip", "Gzip compression", "Unzip", "List"], "answer": 1, "explain": "-z compresses the archive using gzip."}]),

        # FILE PERMISSIONS
        Lesson("ownership_concept", "FILE PERMISSIONS", "Ownership Concept",
               """Linux security is built on file permissions. Every file and directory is owned by a **User** and a **Group**, and has specific permissions for three categories: User (owner), Group, and Others (everyone else).\n\nPermissions are split into three types, represented by letters or numbers:\n- **r (Read = 4):** Permission to view the file's contents.\n- **w (Write = 2):** Permission to modify or delete the file.\n- **x (Execute = 1):** Permission to run the file as a program (or enter a directory).""",
               "ls -l hello.txt",
               [{"q": "What number represents the 'Execute' permission?", "options": ["1", "2", "3", "4"], "answer": 0, "explain": "Read=4, Write=2, Execute=1."}]),

        Lesson("chmod", "FILE PERMISSIONS", "Modify (chmod)",
               """`chmod` stands for 'Change Mode'. It alters the permissions of a file or directory. You can use either letters (symbolic) or numbers (numeric/octal). Numeric is more common.\n\n**Numeric Syntax:** `chmod XYZ file`\n- X (Owner), Y (Group), Z (Others).\n- Example: `chmod 755 script.sh` gives the Owner rwx(7), and Group/Others r-x(5). This is the standard permission for executable scripts.\n- Example: `chmod 644 file.txt` gives Owner rw-(6), and Group/Others r--(4). Standard for documents.""",
               "chmod 777 hello.txt && ls -l hello.txt",
               [{"q": "What permissions does '644' give?", "options": ["Everyone can edit", "Owner: rw, Group/Others: r", "Owner: rwx, Others: none", "No permissions"], "answer": 1, "explain": "6(rw-) for owner, 4(r--) for group, 4(r--) for others."}]),

        Lesson("chown", "FILE PERMISSIONS", "Ownership (chown)",
               """`chown` stands for 'Change Owner'. It changes the user who owns the file. Because changing ownership is a high-level security action, this command typically requires root/sudo privileges. *Will show a permission error in this sandbox.*""",
               "chown root hello.txt",
               [{"q": "Why might chown fail for a normal user?", "options": ["File is too big", "You need root/sudo privileges", "File is a directory", "Wrong extension"], "answer": 1, "explain": "Only root can change ownership of a file to another user."}]),

        Lesson("chgrp", "FILE PERMISSIONS", "Group (chgrp)",
               """`chgrp` stands for 'Change Group'. It changes the group ownership of a file. Like `chown`, changing a file to a group you do not belong to requires root/sudo privileges.""",
               "chgrp wheel hello.txt",
               [{"q": "What does chgrp change?", "options": ["The owner", "The group", "The permissions", "The filename"], "answer": 1, "explain": "chgrp changes the group associated with a file."}]),

        # SCRIPTING
        Lesson("syntax", "SCRIPTING", "Syntax & Shebang",
               """A Bash script is simply a plain text file containing a sequence of commands. To tell the Linux operating system to execute this file using the Bash interpreter, the very first line of the file must be a 'shebang'.\n\n**Shebang:** `#!/bin/bash`\n\n**How to run a script:**\n1. Write the commands in a file (e.g., `script.sh`).\n2. Make it executable: `chmod +x script.sh`.\n3. Run it: `./script.sh`.""",
               "echo '#!/bin/bash\\necho Hello from script' > myscript.sh && chmod +x myscript.sh && ./myscript.sh",
               [{"q": "What is the first line of a bash script called?", "options": ["Hash line", "Shebang", "Interpreter", "Header"], "answer": 1, "explain": "The shebang (#!) tells the OS which interpreter to use."}]),

        Lesson("variables", "SCRIPTING", "Variables",
               """Variables are used to store data temporarily in memory so it can be used later.\n\n**Crucial Rules:**\n1. **NO SPACES** around the equals sign (`NAME="John"` is correct, `NAME = "John"` is an error).\n2. To read the value, you must prefix it with a dollar sign (`$NAME`).\n3. By default, all variables are treated as strings.""",
               "MY_OS=\"Linux\" && echo \"I love $MY_OS\"",
               [{"q": "How do you read a variable in Bash?", "options": ["NAME", "$NAME", "%NAME%", "&NAME"], "answer": 1, "explain": "The dollar sign $ must precede the variable name."}]),

        Lesson("datatypes", "SCRIPTING", "Data Types & Math",
               """Unlike Python or Java, Bash does not have strict data types; everything is essentially a string. However, Bash can perform arithmetic on integers.\n\nTo do math, you must wrap the expression in double parentheses: `$((...))`.\nExample: `SUM=$((5+5))`.""",
               "A=15 && B=5 && echo \"Sum: $((A+B)) Mult: $((A*B))\"",
               [{"q": "How do you perform math in Bash?", "options": ["$[A+B]", "$(A+B)", "$((A+B))", "math(A+B)"], "answer": 2, "explain": "Double parentheses $((...)) are used for arithmetic expansion."}]),

        Lesson("operators", "SCRIPTING", "Operators (If/Else)",
               """Conditionals allow your script to make decisions. Bash uses specific operators for numbers and strings.\n\n**Numeric Operators:** `-eq` (equal), `-ne` (not equal), `-gt` (greater than), `-lt` (less than).\n*Note: You CANNOT use `=` or `<` for numbers in Bash if statements!*\n\n**Syntax:** `if [ $A -lt $B ]; then ... fi`\n*Warning: There MUST be spaces around the brackets `[ ]`!*""",
               "A=10 && B=20 && if [ $A -lt $B ]; then echo 'A is less'; fi",
               [{"q": "What does '-eq' mean in an if statement?", "options": ["Not equal", "Equals", "Greater than", "Less than"], "answer": 1, "explain": "-eq stands for equal (used for numbers)."}]),

        Lesson("loops", "SCRIPTING", "Loops",
               """Loops are used to repeat a block of commands multiple times.\n\n**For Loop Syntax:**\n`for variable in list; do`\n  `commands`\n`done`\n\nThis iterates over a predefined list of items (like words, files, or numbers) and runs the commands for each one.""",
               "for i in apple banana cherry; do echo \"Fruit: $i\"; done",
               [{"q": "What signifies the end of a loop block in Bash?", "options": ["end", "done", "fi", "stop"], "answer": 1, "explain": "Bash uses the keyword 'done' to close for and while loops."}]),

        Lesson("functions", "SCRIPTING", "Functions",
               """Functions allow you to group a set of commands together under a single name. This promotes code reuse and organization.\n\n**Syntax:**\n`my_function() {`\n  `echo \"Hello $1\"`\n`}`\n- `$1` represents the first argument passed to the function when it is called.""",
               "greet() { echo \"Hello, $1!\"; }\ngreet \"Developer\"",
               [{"q": "How do you access the first argument passed to a function?", "options": ["$1", "$0", "$first", "$arg1"], "answer": 0, "explain": "$1 is the first positional parameter. ($0 is the script name)"}]),

        Lesson("arrays", "SCRIPTING", "Arrays",
               """An array is a variable that can hold multiple values. Bash supports one-dimensional arrays.\n\n**Syntax:**\n- `ARRAY=("Val1" "Val2" "Val3")`: Defines an array.\n- `${ARRAY[0]}`: Accesses the first element (index starts at 0).\n- `${ARRAY[@]}`: Accesses ALL elements in the array.""",
               "FRUITS=(\"Apple\" \"Banana\" \"Cherry\")\necho \"First: ${FRUITS[0]}\"\necho \"All: ${FRUITS[@]}\"",
               [{"q": "How do you print all elements of an array?", "options": ["${ARRAY}", "${ARRAY[*]}", "${ARRAY[@]}", "Both * and @"], "answer": 3, "explain": "Both ${ARRAY[*]} and ${ARRAY[@]} expand to all elements."}]),

        Lesson("cron", "SCRIPTING", "Schedule (cron)",
               """`cron` is a time-based job scheduler in Unix-like operating systems. It allows you to automate tasks to run at specific times, dates, or intervals (e.g., backing up a database every night at 2 AM).\n\nYou configure cron jobs by editing your crontab file using `crontab -e`.""",
               "crontab -l",
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
            selectbox_options.append(f"📂 {cat}")
            for l in cat_lessons:
                label = f"   ⚡ {l.title}"
                selectbox_options.append(label)
                options_map[label] = l

    # TOP SECTION
    st.markdown("### 🪵 Linux-Virtual-Tutor Syllabus")
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

    # BOTTOM SECTION: CLAY TERMINAL
    st.markdown("---")

    term_container_html = """
    <div class="term-container">
        <h3 style="margin-top:0px; margin-bottom:15px;">🖥️ Practice Terminal</h3>
        <div style="margin-bottom:10px; font-size:0.9rem; color:#636e72;">
            Working Directory: <code style="background:#d1d9e6; padding:2px 6px; border-radius:5px; color:#2d3436;">%s</code>
        </div>
    """ % st.session_state.sandbox_dir

    term_inner_html = "<div class='term-box'>"
    if not st.session_state.term_history:
        term_inner_html += "<span style='color:#b2bec3'>Type a command below to begin...</span>"
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