import streamlit as st

try:
    from supabase import create_client, Client
    st.write("Supabase package imported successfully")
except Exception as e:
    st.exception(e)
    raise

try:
    supabase: Client = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )
    st.write("Supabase client created successfully")
except Exception as e:
    st.exception(e)
    raise