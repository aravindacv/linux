import streamlit as st
from utils import load_css, init_bash_sandbox, render_lesson, render_live_terminal

load_css()
init_bash_sandbox()

st.header("1. Introduction to Bash")
render_lesson(
    "What is Bash?",
    "Bash (Bourne Again SHell) is a Unix shell and command language interpreter. It is the default login shell for most Linux distributions and macOS. A shell provides an interface between the user and the operating system kernel.",
    "echo $BASH_VERSION"
)

render_lesson(
    "Getting Started & The Prompt",
    "When you open a terminal, you see a prompt like `user@hostname:~$`. \n- `~` represents your home directory.\n- `$` indicates you are a standard user (if you were root, it would be `#`).\n\nCommands follow this syntax: `command [options] [arguments]`",
    "whoami"
)

render_live_terminal()

if st.button("Mark this unit complete ✅"):
    st.session_state.progress_Bash_Intro = True
    st.success("Progress updated!")