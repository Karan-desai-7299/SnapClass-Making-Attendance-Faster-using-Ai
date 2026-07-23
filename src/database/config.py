import streamlit as st

try:
    from supabase import create_client, Client
    st.write("✅ Supabase imported successfully")
except Exception as e:
    st.error(f"Supabase import failed: {type(e).__name__}: {e}")
    raise

supabase: Client = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)