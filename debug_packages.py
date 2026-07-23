import pkgutil
import streamlit as st

packages = sorted([m.name for m in pkgutil.iter_modules()])

st.write("Total packages:", len(packages))
st.write("supabase installed:", "supabase" in packages)

st.write("Packages starting with 's':")
st.write([p for p in packages if p.startswith("s")])