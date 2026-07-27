import streamlit as st
from utils import app_header, init_bash_sandbox, progress_sidebar, load_css

st.set_page_config(page_title="Bash Tutorial — Live Tutor", layout="wide", page_icon="💻")
st.set_option('client.showErrorDetails', True) 

load_css()
init_bash_sandbox()

app_header("Bash Tutorial — Interactive Tutor",
           "Basic Commands • Text Processing • Scripting • System Monitoring\n\n"
           "Use the sidebar **Pages** to navigate units. Your terminal session persists across pages!")

st.markdown("""
### How this works
- Each unit is its **own page** with real Linux command execution.
- Click the **▶️ Run** button next to any example to see it execute in the Live Terminal below.
- You can also type your own custom commands directly into the Live Terminal.
- All commands run in a safe, isolated cloud sandbox.
""")
progress_sidebar()
st.markdown("---")
st.markdown("**Start with `1️⃣ Bash Intro` from the left sidebar → Pages. Enjoy learning!**")




