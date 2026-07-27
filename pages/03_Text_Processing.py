import streamlit as st
from utils import load_css, init_bash_sandbox, render_lesson, render_live_terminal

load_css()
init_bash_sandbox()

st.header("3. Text Processing")
st.markdown("Linux has incredibly powerful built-in tools for searching, parsing, and editing text.")

render_lesson("Search Text (grep)", "Searches for patterns in files.\n- `grep -i`: Case-insensitive.\n- `grep -n`: Shows line numbers.", "grep 'Alice' data.csv")

render_lesson("Pattern Scan (awk)", "A programming language for text extraction. It treats lines as records and words as fields.\n`-F','` sets the delimiter to a comma.", "awk -F',' '{print $1, $3}' data.csv")

render_lesson("Stream Editor (sed)", "Used for filtering and transforming text (Find and Replace).\n`s/old/new/g` substitutes all occurrences.", "sed 's/Hello/Hi/g' hello.txt")

render_lesson("Remove Sections (cut)", "Extracts specific columns from delimited text.", "cut -d',' -f2 data.csv")

render_lesson("Sort Lines (sort)", "Sorts lines of text files alphabetically or numerically.\n- `sort -n`: Numerical sort.", "sort data.csv")

render_lesson("View End (tail)", "Outputs the last part of files. Essential for reading logs.", "tail -n 2 hello.txt")

render_lesson("View Start (head)", "Outputs the first part of files.", "head -n 1 data.csv")

render_live_terminal()

if st.button("Mark this unit complete ✅"):
    st.session_state.progress_Text_Processing = True
    st.success("Progress updated!")