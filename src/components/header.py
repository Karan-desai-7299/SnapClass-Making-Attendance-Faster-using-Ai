import streamlit as st


def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    st.markdown(
        f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:1.75rem 0 1.25rem 0;">'
        f'<img src="{logo_url}" style="height:76px;margin-bottom:0.75rem;" />'
        f'<span style="font-family:\'Plus Jakarta Sans\',sans-serif;font-size:2rem;font-weight:800;color:#0F172A;letter-spacing:-0.03em;">'
        f'Snap<span style="background:linear-gradient(135deg,#6366F1,#EC4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Class</span></span>'
        f'<span style="font-family:\'Plus Jakarta Sans\',sans-serif;font-size:0.9rem;font-weight:600;color:#475569;margin-top:4px;background:#EEF2FF;color:#4F46E5;padding:3px 12px;border-radius:20px;border:1px solid #C7D2FE;">⚡ AI-Powered Attendance · Fast &amp; Accurate</span>'
        f'</div>',
        unsafe_allow_html=True
    )


def header_dashboard():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:10px;">'
        f'<img src="{logo_url}" style="height:44px;" />'
        f'<span style="font-family:\'Plus Jakarta Sans\',sans-serif;font-size:1.4rem;font-weight:800;color:#0F172A;letter-spacing:-0.03em;">'
        f'Snap<span style="background:linear-gradient(135deg,#6366F1,#EC4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Class</span></span>'
        f'</div>',
        unsafe_allow_html=True
    )
