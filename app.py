import streamlit as st
import subprocess
import os
import tempfile

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Bash Tutorial - Learn Linux Terminal",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize safe sandbox environment for the user
if 'sandbox_dir' not in st.session_state:
    st.session_state.sandbox_dir = tempfile.mkdtemp(prefix="bash_tutorial_")
    # Setup initial dummy files for the student to interact with
    with open(f"{st.session_state.sandbox_dir}/hello.txt", "w") as f:
        f.write("Hello, Linux Learner!\nLine 2: This is a test file.\nLine 3: End of file.")
    with open(f"{st.session_state.sandbox_dir}/data.csv", "w") as f:
        f.write("Name,Age,City\nAlice,30,New York\nBob,25,London\nCharlie,35,Paris")
    os.makedirs(f"{st.session_state.sandbox_dir}/my_folder", exist_ok=True)

# ==========================================
# 2. SECURITY & EXECUTION ENGINE
# ==========================================
DANGEROUS_COMMANDS = ["rm -rf /", "sudo", "su ", "mkfs", "dd if=", "> /dev/sda", ":(){ :|:& };:", "chmod -R 777 /"]
INTERACTIVE_COMMANDS = ["top", "vim", "vi", "nano", "less", "more", "ssh", "telnet"]

def is_safe(command):
    for dangerous in DANGEROUS_COMMANDS:
        if dangerous in command:
            return False, f"🚫 Security Error: Dangerous commands like '{dangerous}' are blocked in this sandbox."
    return True, ""

def is_interactive(command):
    base_cmd = command.split()[0] if command.split() else ""
    if base_cmd in INTERACTIVE_COMMANDS:
        return True
    return False

def run_bash_command(command):
    safe, msg = is_safe(command)
    if not safe:
        return msg

    if is_interactive(command):
        return f"🖥️ [SIMULATED OUTPUT]\nThe command '{command.split()[0]}' requires an interactive TTY terminal.\nIn a real Linux machine, this would open a full-screen interface.\nWeb browsers cannot render TTY screens directly."

    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=st.session_state.sandbox_dir,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            # Educational handling for permission errors on Streamlit Cloud
            if "Operation not permitted" in result.stderr or "Permission denied" in result.stderr:
                output += f"[Permission Denied]\n{result.stderr}\nNote: On Streamlit Cloud, you are a restricted user. Commands like 'chown' require root privileges."
            else:
                output += f"[stderr]\n{result.stderr}"
                
        return output if output else "(Command executed successfully with no output)"
    except subprocess.TimeoutExpired:
        return "⏱️ Error: Command timed out after 5 seconds."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ==========================================
# 3. W3SCHOOLS-STYLE CSS
# ==========================================
st.markdown("""
<style>
    .stApp, .stMarkdown, p, span { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    [data-testid="stSidebar"] { background-color: #282A35; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #f1f1f1; font-size: 14px; }
    [data-testid="stSidebar"] button { 
        color: #f1f1f1; background-color: transparent; border: none; text-align: left; 
        border-radius: 3px; margin-bottom: 2px; padding: 8px 10px; width: 100%;
    }
    [data-testid="stSidebar"] button:hover { background-color: #000000; color: #4CAF50; }
    #MainMenu, footer { visibility: hidden; }
    
    .terminal-box {
        background-color: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 5px;
        font-family: 'Consolas', 'Courier New', monospace; font-size: 14px;
        border-left: 4px solid #4CAF50; margin-bottom: 20px; white-space: pre-wrap;
    }
    .try-it-box {
        background-color: #f1f1f1; padding: 20px; border: 1px solid #cccccc; border-radius: 5px; margin-top: 20px;
    }
    .code-snippet {
        background-color: #fff; padding: 10px; border: 1px solid #ddd; border-radius: 4px;
        font-family: 'Consolas', monospace; color: #d63384;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. COMPREHENSIVE TUTORIAL DATABASE
# ==========================================
TUTORIALS = {
    "HOME": {
        "Bash Intro": {
            "title": "Bash Introduction",
            "content": """
            **What is Bash?**
            Bash (Bourne Again SHell) is a Unix shell and command language interpreter. It is the default login shell for most Linux distributions and macOS.
            
            **What is a Shell?**
            A shell is a special program that provides an interface between the user and the operating system. When you type a command, the shell interprets it and tells the OS kernel to execute it.
            
            **Why Learn Bash?**
            - **Automation:** Write scripts to automate repetitive tasks (e.g., backups).
            - **Server Administration:** Almost all servers are managed via command line.
            - **DevOps & Cloud:** Essential for Docker, Kubernetes, AWS, and CI/CD pipelines.
            - **Data Processing:** Quickly parse, search, and manipulate text files.
            """,
            "example_cmd": "echo 'Welcome to Bash!'"
        },
        "Bash Get Started": {
            "title": "Getting Started",
            "content": """
            To access Bash, you open a **Terminal** application. 
            When you open a terminal, you are placed inside your **home directory**.
            
            **The Prompt**
            You will see a prompt that looks something like this:
            `user@hostname:~$`
            - `user`: Your username.
            - `hostname`: The name of the computer.
            - `~`: Represents your home directory.
            - `$`: Indicates you are a standard user (if you were root, it would be `#`).
            
            **Command Syntax**
            `command [options] [arguments]`
            - **Command**: The program you want to run (e.g., `ls`).
            - **Options**: Flags that modify the command, usually starting with `-` (e.g., `-l`).
            - **Arguments**: The target the command acts upon (e.g., a filename).
            """,
            "example_cmd": "whoami"
        }
    },
    "BASIC COMMANDS": {
        "Bash List (ls)": {
            "title": "List Files (ls)",
            "content": """
            The `ls` command lists the files and directories in your current location.
            
            **Common Options:**
            - `ls -l`: Long listing format. Shows permissions, owner, size, and modification date.
            - `ls -a`: Shows **all** files, including hidden files (those starting with a dot `.`).
            - `ls -h`: Human-readable sizes (e.g., 1K, 234M, 2G). Used with `-l`.
            - `ls -R`: Recursive list (lists all subdirectories and their files).
            """,
            "example_cmd": "ls -lah"
        },
        "Bash Change Dir (cd)": {
            "title": "Change Directory (cd)",
            "content": """
            `cd` stands for **C**hange **D**irectory. It moves your current working directory.
            
            **Path Types:**
            - **Absolute Path:** Starts from the root `/`. Example: `cd /var/log`
            - **Relative Path:** Starts from your current location. Example: `cd my_folder`
            
            **Shortcuts:**
            - `cd` or `cd ~`: Go to your home directory.
            - `cd ..`: Move up one directory level.
            - `cd -`: Go back to the previous directory you were in.
            """,
            "example_cmd": "cd my_folder && pwd && cd .."
        },
        "Bash Print Dir (pwd)": {
            "title": "Print Working Directory (pwd)",
            "content": """
            `pwd` stands for **P**rint **W**orking **D**irectory. 
            It outputs the full, absolute path of the directory you are currently in. 
            It is highly useful when you get lost in the file system.
            """,
            "example_cmd": "pwd"
        },
        "Bash Echo (echo)": {
            "title": "Echo (echo)",
            "content": """
            `echo` prints text to the standard output (your screen). 
            It is heavily used in scripting to display status messages or output variable values.
            
            **Options:**
            - `echo -n`: Do not output the trailing newline.
            - `echo -e`: Enable interpretation of backslash escapes (e.g., `echo -e "Line 1\\nLine 2"`).
            """,
            "example_cmd": "echo -e 'Hello\\nWorld'"
        },
        "Bash Concatenate (cat)": {
            "title": "Concatenate (cat)",
            "content": """
            `cat` reads data from files and outputs their contents. It stands for con**cat**enate.
            
            **Uses:**
            - `cat file.txt`: Display the whole file.
            - `cat file1.txt file2.txt > combined.txt`: Combine two files into a new one.
            - `cat > new.txt`: Create a new file and type into it (press Ctrl+D to save).
            
            *Note: There is a `hello.txt` file in your sandbox. Try reading it.*
            """,
            "example_cmd": "cat hello.txt"
        },
        "Bash Copy (cp)": {
            "title": "Copy (cp)",
            "content": """
            `cp` copies files or directories.
            
            **Syntax:**
            - `cp source destination`: Copies a file.
            - `cp -r source_dir destination_dir`: The `-r` (recursive) flag is required to copy a directory and everything inside it.
            - `cp -i source dest`: Prompts you before overwriting an existing file.
            """,
            "example_cmd": "cp hello.txt hello_backup.txt && ls"
        },
        "Bash Move (mv)": {
            "title": "Move (mv)",
            "content": """
            `mv` moves files from one place to another. It is also the command used to **rename** files.
            
            **Syntax:**
            - `mv old_name.txt new_name.txt`: Renames a file.
            - `mv file.txt /my_folder/`: Moves the file into the folder.
            - `mv -i`: Prompts before overwriting.
            """,
            "example_cmd": "mv hello_backup.txt my_folder/ && ls my_folder/"
        },
        "Bash Remove (rm)": {
            "title": "Remove (rm)",
            "content": """
            `rm` deletes files or directories. **Warning:** Linux does not have a "Recycle Bin" by default. When you use `rm`, the file is gone.
            
            **Syntax:**
            - `rm file.txt`: Deletes a file.
            - `rm -r folder_name/`: Deletes a folder and its contents recursively.
            - `rm -i file.txt`: Interactive mode (asks "are you sure?").
            - `rm -f file.txt`: Force delete (ignores non-existent files and prompts).
            """,
            "example_cmd": "cp hello.txt safe_delete.txt && rm safe_delete.txt && ls"
        },
        "Bash Timestamp (touch)": {
            "title": "Timestamp (touch)",
            "content": """
            `touch` is primarily used to create empty files quickly, but its actual purpose is to update the access and modification timestamps of a file to the current time.
            
            **Syntax:**
            - `touch newfile.txt`: Creates `newfile.txt` if it doesn't exist.
            - `touch existingfile.txt`: Updates the timestamp of the existing file to "now".
            """,
            "example_cmd": "touch empty_file.txt && ls -l empty_file.txt"
        },
        "Bash Make Dir (mkdir)": {
            "title": "Make Directory (mkdir)",
            "content": """
            `mkdir` creates new directories (folders).
            
            **Syntax:**
            - `mkdir folder1`: Creates a single folder.
            - `mkdir -p parent/child/grandchild`: The `-p` flag creates parent directories if they don't exist. Without `-p`, this command would fail because `parent` doesn't exist yet.
            """,
            "example_cmd": "mkdir -p project/src && ls -R project"
        },
        "Bash Manual (man)": {
            "title": "Manual (man)",
            "content": """
            `man` opens the built-in manual pages for almost any command. It is the most important command for learning Linux.
            
            **How to use it:**
            - Type `man ls` to see the manual for `ls`.
            - Use **Arrow keys** to scroll up and down.
            - Press **q** to quit.
            
            *Note: Because `man` is an interactive command (like vim), this sandbox will simulate its output.*
            """,
            "example_cmd": "man ls"
        },
        "Bash Alias": {
            "title": "Alias",
            "content": """
            `alias` creates custom shortcuts or alternate names for commands.
            
            **Syntax:**
            - `alias ll='ls -la'`: Now typing `ll` will execute `ls -la`.
            - `alias c='clear'`: Typing `c` clears the screen.
            
            *Note: Aliases created in the terminal are temporary and lost when the session ends. To make them permanent, you add them to your `~/.bashrc` file.*
            """,
            "example_cmd": "alias c='echo I just created an alias!' && c"
        }
    },
    "TEXT PROCESSING": {
        "Bash Search Text (grep)": {
            "title": "Search Text (grep)",
            "content": """
            `grep` searches for a specific pattern or word inside files. It stands for **G**lobal **R**egular **E**xpression **P**rint.
            
            **Common Options:**
            - `grep "word" file.txt`: Finds lines containing "word".
            - `grep -i "word" file.txt`: Case-insensitive search.
            - `grep -n "word" file.txt`: Shows line numbers.
            - `grep -r "word" /folder/`: Recursively searches all files in a folder.
            
            *Try searching for "Alice" in the `data.csv` file.*
            """,
            "example_cmd": "grep 'Alice' data.csv"
        },
        "Bash Pattern Scan (awk)": {
            "title": "Pattern Scanning (awk)",
            "content": """
            `awk` is a powerful programming language designed for text processing and data extraction. It treats each line as a record and words (separated by spaces) as fields.
            
            **Basic Syntax:** `awk '{action}' file`
            - `$0`: The entire line.
            - `$1`: The first field (word).
            - `$2`: The second field, etc.
            
            *Extract just the names (first column) from the CSV.*
            """,
            "example_cmd": "awk -F',' '{print $1}' data.csv"
        },
        "Bash Stream Editor (sed)": {
            "title": "Stream Editor (sed)",
            "content": """
            `sed` is used for filtering and transforming text. It reads text line by line, modifies it according to rules, and outputs the result.
            
            **Most common use (Find and Replace):**
            `sed 's/old_word/new_word/g' file.txt`
            - `s`: Substitute command.
            - `g`: Global flag (replace all occurrences on a line, not just the first one).
            
            *Try changing "Hello" to "Hi" in the output.*
            """,
            "example_cmd": "sed 's/Hello/Hi/g' hello.txt"
        },
        "Bash Remove Section (cut)": {
            "title": "Remove Sections (cut)",
            "content": """
            `cut` extracts specific columns or characters from each line of a file.
            
            **Options:**
            - `cut -d',' -f1 file`: Uses a comma `-d','` as a delimiter and extracts field 1 `-f1`.
            - `cut -c1-5 file`: Extracts characters 1 through 5 from every line.
            
            *Extract just the Cities (column 3) from the CSV.*
            """,
            "example_cmd": "cut -d',' -f3 data.csv"
        },
        "Bash Sort Lines (sort)": {
            "title": "Sort Lines (sort)",
            "content": """
            `sort` sorts the lines of a text file alphabetically or numerically.
            
            **Options:**
            - `sort file.txt`: Alphabetical sort.
            - `sort -n file.txt`: Numerical sort (treats numbers as values, not text).
            - `sort -r file.txt`: Reverse order.
            - `sort -u file.txt`: Removes duplicates (unique).
            """,
            "example_cmd": "sort data.csv"
        },
        "Bash View End (tail)": {
            "title": "View End (tail)",
            "content": """
            `tail` outputs the last part of files. By default, it shows the last 10 lines. It is essential for reading log files in real-time.
            
            **Options:**
            - `tail -n 5 file.txt`: Shows the last 5 lines.
            - `tail -f /var/log/syslog`: Follows the file (prints new lines as they are added). *Cannot be used in this sandbox.*
            """,
            "example_cmd": "tail -n 2 hello.txt"
        },
        "Bash View Start (head)": {
            "title": "View Start (head)",
            "content": """
            `head` outputs the first part of files. By default, it shows the first 10 lines.
            
            **Options:**
            - `head -n 2 file.txt`: Shows the first 2 lines.
            """,
            "example_cmd": "head -n 1 data.csv"
        }
    },
    "SYSTEM MONITORING": {
        "Bash Process Status (ps)": {
            "title": "Process Status (ps)",
            "content": """
            `ps` reports a snapshot of the current running processes.
            
            **Options:**
            - `ps`: Shows only processes running in your current terminal.
            - `ps aux`: Shows **all** processes for **all** users in a detailed format.
                - `a`: All users.
                - `u`: User-oriented format.
                - `x`: Processes not attached to a terminal.
            """,
            "example_cmd": "ps aux | head -n 5"
        },
        "Bash List Processes (top)": {
            "title": "List Processes (top)",
            "content": """
            `top` provides a dynamic, real-time view of the running system. It shows CPU usage, memory usage, and a list of tasks sorted by resource consumption.
            
            *Note: `top` is an interactive TTY application. In this web sandbox, we simulate its behavior.*
            """,
            "example_cmd": "top"
        },
        "Bash Disk Space (df)": {
            "title": "Disk Space (df)",
            "content": """
            `df` (Disk Free) displays the amount of disk space available on your file systems.
            
            **Option:**
            - `df -h`: Human-readable format (prints sizes in KB, MB, GB instead of raw bytes).
            """,
            "example_cmd": "df -h"
        },
        "Bash Directory Usage (du)": {
            "title": "Directory Usage (du)",
            "content": """
            `du` (Disk Usage) estimates file and directory space usage. Unlike `df` which shows entire drives, `du` shows specific folders.
            
            **Options:**
            - `du`: Shows size of all subdirectories.
            - `du -sh *`: **s**ummarize total size of each item in current folder in **h**uman-readable format.
            """,
            "example_cmd": "du -sh *"
        },
        "Bash Memory Usage (free)": {
            "title": "Memory Usage (free)",
            "content": """
            `free` displays the total amount of free and used physical and swap memory in the system.
            
            **Option:**
            - `free -h`: Human-readable output.
            """,
            "example_cmd": "free -h"
        },
        "Bash Terminate (kill)": {
            "title": "Terminate Process (kill)",
            "content": """
            `kill` sends a signal to a process to terminate it. You must know the Process ID (PID), which you can find using `ps`.
            
            **Syntax:**
            - `kill 1234`: Politely asks process 1234 to stop (SIGTERM).
            - `kill -9 1234`: Forcefully kills process 1234 immediately (SIGKILL). Use this if the process is stuck.
            """,
            "example_cmd": "echo 'To test kill: run a sleep command in background, find PID with ps, and kill it.'"
        },
        "Bash Uptime": {
            "title": "Uptime",
            "content": """
            `uptime` tells you how long the system has been running, how many users are currently logged on, and the system load averages.
            """,
            "example_cmd": "uptime"
        }
    },
    "NETWORKING": {
        "Bash Ping": {
            "title": "Ping",
            "content": """
            `ping` tests the connectivity between your machine and another network device. It sends ICMP echo requests and waits for replies.
            
            **Option:**
            - `ping -c 4 google.com`: Sends exactly 4 packets and stops. (Without `-c`, it runs forever).
            """,
            "example_cmd": "ping -c 3 localhost"
        },
        "Bash URL Transfer (curl)": {
            "title": "URL Transfer (curl)",
            "content": """
            `curl` transfers data to or from a server. It supports almost every internet protocol (HTTP, HTTPS, FTP).
            
            **Uses:**
            - `curl url`: Downloads the HTML source code of a webpage and prints it to your terminal.
            - `curl -O url`: Downloads the file and saves it with its original name.
            """,
            "example_cmd": "curl -s http://example.com | head -n 5"
        },
        "Bash Downloader (wget)": {
            "title": "Downloader (wget)",
            "content": """
            `wget` is a non-interactive network downloader. Unlike `curl`, `wget` is designed to download files recursively and can resume broken downloads.
            
            **Syntax:**
            - `wget url`: Downloads the file directly into your current directory.
            """,
            "example_cmd": "echo 'wget is disabled in this sandbox to prevent unauthorized downloads.'"
        },
        "Bash Remote Connect (ssh)": {
            "title": "Remote Connect (ssh)",
            "content": """
            `ssh` (Secure Shell) is used to log into a remote machine and execute commands. It provides a secure, encrypted connection.
            
            **Syntax:**
            - `ssh user@hostname`: Connects to a remote server.
            """,
            "example_cmd": "ssh user@server.com"
        },
        "Bash Secure Copy (scp)": {
            "title": "Secure Copy (scp)",
            "content": """
            `scp` uses SSH to securely copy files between your local machine and a remote server.
            
            **Syntax:**
            - `scp file.txt user@remote:/path/`: Uploads a file.
            - `scp user@remote:/path/file.txt .`: Downloads a file.
            """,
            "example_cmd": "echo 'scp requires a remote host and is simulated here.'"
        },
        "Bash File Sync (rsync)": {
            "title": "File Sync (rsync)",
            "content": """
            `rsync` is a fast, versatile file-copying tool. It is famous for syncing files because it only transfers the differences (deltas) between the source and destination, saving bandwidth.
            
            **Syntax:**
            - `rsync -avz source/ destination/`: `-a` (archive), `-v` (verbose), `-z` (compress during transfer).
            """,
            "example_cmd": "mkdir backup && rsync -av ./my_folder/ ./backup/ && ls backup"
        }
    },
    "FILE COMPRESSION": {
        "Bash Compress (zip)": {
            "title": "Compress (zip)",
            "content": """
            `zip` compresses files into a `.zip` archive, which is highly compatible with Windows and macOS.
            
            **Syntax:**
            - `zip archive.zip file1 file2`: Creates an archive.
            - `zip -r archive.zip folder/`: The `-r` flag is required to zip a directory recursively.
            """,
            "example_cmd": "zip my_archive.zip hello.txt data.csv && ls -lh my_archive.zip"
        },
        "Bash Extract (unzip)": {
            "title": "Extract (unzip)",
            "content": """
            `unzip` lists, tests, or extracts files from a `.zip` archive.
            
            **Syntax:**
            - `unzip archive.zip`: Extracts to the current directory.
            - `unzip -l archive.zip`: Lists the contents without extracting.
            """,
            "example_cmd": "unzip -l my_archive.zip"
        },
        "Bash TAR Archive": {
            "title": "TAR Archive (tar)",
            "content": """
            `tar` (Tape Archive) is the standard Linux archiving tool. It bundles files together. It is often combined with compression algorithms like gzip (`.tar.gz` or `.tgz`).
            
            **Syntax:**
            - `tar -cvf archive.tar file1 folder/`: **c**reate archive, **v**erbose, **f**ile.
            - `tar -czvf archive.tar.gz file1 folder/`: Same, but adds **z** (gzip compression).
            - `tar -xzvf archive.tar.gz`: E**x**tract **z**ipped archive.
            """,
            "example_cmd": "tar -czvf backup.tar.gz hello.txt && ls -lh backup.tar.gz"
        }
    },
    "FILE PERMISSIONS": {
        "Bash Ownership": {
            "title": "Understanding Ownership",
            "content": """
            In Linux, every file and directory is owned by a **User** and a **Group**. Permissions are divided into three levels:
            
            1. **User (u):** The owner of the file.
            2. **Group (g):** Users who are in the group assigned to the file.
            3. **Others (o):** Everyone else.
            
            There are three types of permissions:
            - **r (Read):** 4 - Can view the file's contents.
            - **w (Write):** 2 - Can modify or delete the file.
            - **x (Execute):** 1 - Can run the file as a program (or enter a directory).
            """,
            "example_cmd": "ls -l hello.txt"
        },
        "Bash Modify (chmod)": {
            "title": "Modify Permissions (chmod)",
            "content": """
            `chmod` (Change Mode) alters the permissions of a file or directory.
            
            **Numeric Method:**
            Add the values (r=4, w=2, x=1) for each level.
            - `chmod 755 file.sh`: User gets 7 (rwx), Group gets 5 (r-x), Others get 5 (r-x). This is standard for scripts.
            - `chmod 644 file.txt`: User gets 6 (rw-), Group gets 4 (r--), Others get 4 (r--). Standard for documents.
            
            *Try changing the permissions of your file.*
            """,
            "example_cmd": "chmod 777 hello.txt && ls -l hello.txt"
        },
        "Bash Ownership (chown)": {
            "title": "Change Owner (chown)",
            "content": """
            `chown` (Change Owner) changes the user and/or group ownership of a file.
            
            **Syntax:**
            - `chown user:group file`
            - `chown root file.txt`: Changes owner to root.
            
            *Note: You must be root (use `sudo`) to change ownership. This sandbox will demonstrate the permission error.*
            """,
            "example_cmd": "chown root hello.txt"
        },
        "Bash Group (chgrp)": {
            "title": "Change Group (chgrp)",
            "content": """
            `chgrp` changes the group ownership of a file. It functions similarly to `chown` but only affects the group.
            
            **Syntax:**
            - `chgrp newgroup file.txt`
            """,
            "example_cmd": "chgrp wheel hello.txt"
        }
    },
    "SCRIPTING": {
        "Bash Syntax": {
            "title": "Scripting Syntax",
            "content": """
            A Bash script is a plain text file containing a sequence of commands. To tell Linux to execute it using Bash, the first line must be a **shebang**:
            
            ```bash
            #!/bin/bash
            # This is a comment
            echo "This is a script"
            ```
            
            To run a script:
            1. Write the code.
            2. Make it executable: `chmod +x script.sh`
            3. Run it: `./script.sh`
            """,
            "example_cmd": "echo '#!/bin/bash\\necho Hello from script' > myscript.sh && chmod +x myscript.sh && ./myscript.sh"
        },
        "Bash Variables": {
            "title": "Variables",
            "content": """
            Variables store data. 
            **Rules:**
            1. No spaces around the `=` sign.
            2. Access the value using a dollar sign `$`.
            3. By default, all variables are treated as strings.
            4. Put strings with spaces inside quotes.
            
            ```bash
            NAME="John Doe"
            echo "Hello $NAME"
            ```
            """,
            "example_cmd": "MY_OS=\"Linux\" && echo \"I love $MY_OS\""
        },
        "Bash Data Types": {
            "title": "Data Types",
            "content": """
            Unlike Python or Java, Bash does not have strict data types. Everything is essentially a string. However, Bash can perform arithmetic on integers.
            
            To do math, you must use the `$((...))` syntax or the `expr` command.
            
            ```bash
            NUM1=5
            NUM2=10
            SUM=$((NUM1 + NUM2))
            echo $SUM
            ```
            """,
            "example_cmd": "A=15 && B=5 && echo \"Sum: $((A+B)) Multiplication: $((A*B))\""
        },
        "Bash Operators": {
            "title": "Operators",
            "content": """
            Bash uses different operators for files, strings, and numbers.
            
            **Numeric:**
            - `-eq` (equal), `-ne` (not equal), `-gt` (greater than), `-lt` (less than)
            
            **String:**
            - `==` (equal), `!=` (not equal), `-z` (is empty)
            
            **Files:**
            - `-f file` (exists and is a file)
            - `-d dir` (exists and is a directory)
            """,
            "example_cmd": "A=10 && B=20 && if [ $A -lt $B ]; then echo 'A is less than B'; fi"
        },
        "Bash If...Else": {
            "title": "If...Else Statements",
            "content": """
            Conditionals allow your script to make decisions.
            
            **Syntax:**
            ```bash
            if [ condition ]; then
                # commands
            elif [ condition ]; then
                # commands
            else
                # commands
            fi
            ```
            *Note the spaces around the brackets `[ ]`! They are mandatory.*
            """,
            "example_cmd": "AGE=20\nif [ $AGE -ge 18 ]; then\n  echo 'You are an adult.'\nelse\n  echo 'You are a minor.'\nfi"
        },
        "Bash Loops": {
            "title": "Loops",
            "content": """
            Loops repeat commands.
            
            **For Loop:**
            ```bash
            for i in 1 2 3 4 5; do
              echo "Number: $i"
            done
            ```
            
            **While Loop:**
            ```bash
            COUNT=0
            while [ $COUNT -lt 3 ]; do
              echo "Count: $COUNT"
              COUNT=$((COUNT+1))
            done
            ```
            """,
            "example_cmd": "for i in apple banana cherry; do echo \"Fruit: $i\"; done"
        },
        "Bash Functions": {
            "title": "Functions",
            "content": """
            Functions group commands together under a single name. They help reuse code.
            
            **Syntax:**
            ```bash
            my_function() {
              echo "Hello, $1" # $1 is the first argument passed
            }
            my_function "World"
            ```
            """,
            "example_cmd": "greet() {\n  echo \"Hello, $1!\"\n}\ngreet \"Developer\"\ngreet \"Linux User\""
        },
        "Bash Arrays": {
            "title": "Arrays",
            "content": """
            Arrays hold multiple values. Bash only supports one-dimensional arrays.
            
            **Syntax:**
            ```bash
            MY_ARRAY=("Apple" "Banana" "Cherry")
            echo ${MY_ARRAY[0]} # Prints first item
            echo ${MY_ARRAY[@]} # Prints all items
            ```
            """,
            "example_cmd": "FRUITS=(\"Apple\" \"Banana\" \"Cherry\")\necho \"First: ${FRUITS[0]}\"\necho \"All: ${FRUITS[@]}\""
        },
        "Bash Schedule (cron)": {
            "title": "Scheduling (cron)",
            "content": """
            `cron` is a time-based job scheduler in Unix-like OS. It runs scripts in the background at specific times.
            
            You edit your schedule using `crontab -e`. The format is:
            `* * * * * command`
            (Minute Hour DayOfMonth Month DayOfWeek Command)
            
            *Note: Modifying system crontabs requires root privileges and is blocked in this sandbox.*
            """,
            "example_cmd": "crontab -l"
        }
    },
    "EXERCISES AND QUIZ": {
        "Bash Exercises": {
            "title": "Practical Exercises",
            "content": """
            Complete these tasks using the terminal below. Try to do them without looking at the answers.
            
            **Exercise 1:** Print your current working directory.
            **Exercise 2:** Create a new directory called `exercise_lab` and move into it.
            **Exercise 3:** Create an empty file named `notes.txt`.
            **Exercise 4:** Write the text "Bash is powerful" into `notes.txt` (Hint: use `echo` with `>`).
            **Exercise 5:** Read the contents of `notes.txt` to verify.
            **Exercise 6:** Go back up one directory level.
            
            *Hint for Exercise 4:* `echo 'text' > file`
            """,
            "example_cmd": "pwd && mkdir exercise_lab && cd exercise_lab && touch notes.txt && echo 'Bash is powerful' > notes.txt && cat notes.txt && cd .."
        },
        "Bash Quiz": "QUIZ_MODE" # Special flag to trigger Streamlit widgets
    }
}

# ==========================================
# 5. QUIZ LOGIC (Interactive Widgets)
# ==========================================
def render_quiz():
    st.markdown("## Test Your Bash Knowledge")
    st.write("Answer the following questions to see if you are ready for the real command line.")
    
    score = 0
    total_questions = 3
    
    q1 = st.radio("1. Which command prints the current working directory?", 
                  ("dir", "pwd", "cd", "path"), key="q1")
    if q1 == "pwd": score += 1

    q2 = st.radio("2. What flag do you use with `rm` to delete a directory and its contents?", 
                  ("-d", "-f", "-r", "-a"), key="q2")
    if q2 == "-r": score += 1

    q3 = st.radio("3. In a bash script, how do you read a variable named `NAME`?", 
                  ("NAME", "$NAME", "%NAME%", "&NAME"), key="q3")
    if q3 == "$NAME": score += 1

    if st.button("Check Score", type="primary"):
        st.success(f"You got {score} out of {total_questions} correct!")
        if score == total_questions:
            st.balloons()
            st.markdown("🎉 Excellent! You are ready to claim your Bash Certificate!")
        elif score >= 2:
            st.info("Good job! Review the sections you missed to perfect your knowledge.")
        else:
            st.warning("Keep studying! Go through the basic commands section again.")

# ==========================================
# 6. UI LAYOUT & NAVIGATION
# ==========================================
st.sidebar.markdown("### 📚 Navigation")
st.sidebar.markdown("---")

nav_options = ["🏠 HOME"]
nav_keys = ["HOME"]

for category, lessons in TUTORIALS.items():
    nav_options.append(f"📂 {category}")
    nav_keys.append(None)
    for lesson_name in lessons.keys():
        nav_options.append(f"   ⚡ {lesson_name}")
        nav_keys.append(lesson_name)

selected_key = "Bash Intro" 
with st.sidebar:
    for i, option in enumerate(nav_options):
        key = nav_keys[i]
        if key is None:
            st.markdown(f"<div style='color:#aaa; font-weight:bold; margin-top:15px; font-size:13px; text-transform:uppercase; letter-spacing: 1px;'>{option}</div>", unsafe_allow_html=True)
        else:
            if st.button(option, key=f"nav_{i}", use_container_width=True):
                selected_key = key
                st.rerun()

# Main Content Area
st.markdown("<h1 style='color:#4CAF50;'>💻 Learn Bash in a Live Sandbox</h1>", unsafe_allow_html=True)
st.markdown("---")

# Handle Quiz separately
if selected_key == "QUIZ_MODE":
    render_quiz()
    st.stop()

# Find selected lesson data
lesson_data = None
for category, lessons in TUTORIALS.items():
    if selected_key in lessons:
        lesson_data = lessons[selected_key]
        break

if lesson_data:
    st.markdown(f"## {lesson_data['title']}")
    st.markdown(lesson_data['content'])
    
    # Interactive Sandbox Area
    st.markdown("<div class='try-it-box'>", unsafe_allow_html=True)
    st.markdown("#### 🚀 Live Linux Sandbox")
    st.caption(f"Working Directory: `{st.session_state.sandbox_dir}`")
    
    default_cmd = lesson_data.get('example_cmd', "echo 'Hello'")
    
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_area("Enter your Bash commands here:", value=default_cmd, height=80, label_visibility="collapsed")
    with col2:
        st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
        run_btn = st.button("▶️ Execute", type="primary", use_container_width=True)
    
    if run_btn or user_input:
        commands = user_input.split('\n')
        full_output = ""
        for cmd in commands:
            if cmd.strip():
                output = run_bash_command(cmd)
                # Escape HTML to prevent injection in the terminal output
                safe_output = output.replace("<", "&lt;").replace(">", "&gt;")
                full_output += f"<span style='color:#4CAF50;'>student@linux-sandbox:~$</span> {cmd}\n{safe_output}\n\n"
        
        st.markdown("<b>Terminal Output:</b>", unsafe_allow_html=True)
        st.markdown(f"<div class='terminal-box'>{full_output}</div>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

# Bottom Navigation
st.markdown("---")
clickable_keys = [k for k in nav_keys if k is not None]
current_idx = clickable_keys.index(selected_key) if selected_key in clickable_keys else 0

col_prev, col_spacer, col_next = st.columns([1, 2, 1])

with col_prev:
    if current_idx > 0:
        if st.button("⬅️ Previous"):
            selected_key = clickable_keys[current_idx - 1]
            st.rerun()

with col_next:
    if current_idx < len(clickable_keys) - 1:
        if st.button("Next ➡️"):
            selected_key = clickable_keys[current_idx + 1]
            st.rerun()