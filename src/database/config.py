import streamlit as st

try:
    from supabase import create_client, Client
except Exception as e:
    import traceback
    st.error(f"REAL IMPORT ERROR: {type(e).__name__}: {e}")
    st.code(traceback.format_exc())
    st.stop()

try:
    supabase: Client = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )
except Exception as e:
    import traceback
    st.error(f"CLIENT CREATION ERROR: {type(e).__name__}: {e}")
    st.code(traceback.format_exc())
    st.stop()
