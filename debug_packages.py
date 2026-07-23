import pkgutil
import streamlit as st

packages = sorted([m.name for m in pkgutil.iter_modules()])

st.write("Is supabase installed?", "supabase" in packages)

if "supabase" not in packages:
    st.write("Installed packages starting with 's':")
    st.write([p for p in packages if p.startswith("s")])