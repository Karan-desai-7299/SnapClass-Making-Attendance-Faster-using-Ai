import importlib.util
import streamlit as st

st.title("Debug Packages")

spec = importlib.util.find_spec("supabase")

st.write("Supabase spec:")
st.write(spec)

if spec is None:
    st.error("❌ Supabase package NOT found")
else:
    st.success("✅ Supabase package found")