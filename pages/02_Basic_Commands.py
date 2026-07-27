import streamlit as st
from utils import load_css, init_bash_sandbox, render_lesson, render_live_terminal

load_css()
init_bash_sandbox()

st.header("2. Basic Commands")
st.markdown("Master the fundamental commands to navigate and manipulate the Linux file system.")

render_lesson("List Files (ls)", "Lists files and directories.\n- `ls -l`: Long format.\n- `ls -a`: Show hidden files.\n- `ls -h`: Human-readable sizes.", "ls -lah")

render_lesson("Change Directory (cd)", "Moves your current location.\n- `cd ..`: Move up one level.\n- `cd ~`: Go to home directory.", "cd my_folder && pwd && cd ..")

render_lesson("Print Working Directory (pwd)", "Outputs the full, absolute path of the directory you are currently in.", "pwd")

render_lesson("Echo (echo)", "Prints text to the standard output. Used heavily in scripting.\n- `echo -e`: Enables backslash escapes (like `\\n` for newlines).", "echo -e 'Hello\\nWorld'")

render_lesson("Concatenate (cat)", "Reads data from files and outputs their contents. *There is a `hello.txt` file in your sandbox.*", "cat hello.txt")

render_lesson("Copy (cp)", "Copies files or directories.\n- `cp -r dir/ dest/`: Required to copy a folder recursively.", "cp hello.txt backup.txt && ls")

render_lesson("Move (mv)", "Moves files. It is also the command used to **rename** files.", "mv backup.txt my_folder/ && ls my_folder/")

render_lesson("Remove (rm)", "Deletes files. **Warning:** Linux does not have a Recycle Bin.\n- `rm -r folder/`: Deletes a folder.", "cp hello.txt safe_delete.txt && rm safe_delete.txt && ls")

render_lesson("Timestamp (touch)", "Creates empty files quickly, or updates the timestamp of an existing file to 'now'.", "touch newfile.txt && ls -l newfile.txt")

render_lesson("Make Directory (mkdir)", "Creates new folders.\n- `mkdir -p a/b/c`: Creates nested folders in one go.", "mkdir -p project/src && ls -R project")

render_lesson("Manual (man)", "Opens the built-in manual for commands. *Note: This is an interactive TTY command, so the sandbox simulates it.*", "man ls")

render_lesson("Alias", "Creates custom shortcuts for commands.", "alias c='echo I am an alias!' && c")

render_live_terminal()

if st.button("Mark this unit complete ✅"):
    st.session_state.progress_Basic_Commands = True
    st.success("Progress updated!")