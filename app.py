import streamlit as st
import subprocess
import sys

st.set_page_config(page_title="Package Debug")

st.title("Installed Packages")

result = subprocess.run(
    [sys.executable, "-m", "pip", "list"],
    capture_output=True,
    text=True,
)

st.code(result.stdout)

st.write("Python Executable:")
st.code(sys.executable)