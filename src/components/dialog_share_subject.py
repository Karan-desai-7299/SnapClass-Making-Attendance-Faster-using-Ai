import streamlit as st
import segno
import io


@st.dialog("Share Class Invitation")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "https://snapclass-main.streamlit.app"
    join_url = f"{app_domain}/?join-code={subject_code}"

    st.markdown(
        f'<div style="background:#EEF2FF;border:1.5px solid #C7D2FE;border-radius:14px;padding:1rem;margin-bottom:1rem;">'
        f'<p style="font-size:1.1rem;font-weight:800;color:#3730A3;margin:0 0 0.2rem 0;">{subject_name}</p>'
        f'<p style="font-size:0.85rem;color:#4F46E5;font-weight:600;margin:0;">Share the link or QR code below so students can enroll instantly.</p>'
        f'</div>',
        unsafe_allow_html=True
    )

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind='png', scale=10, border=1)

    col1, col2 = st.columns([1.1, 0.9], gap="medium")

    with col1:
        st.markdown(
            '<p style="font-size:0.88rem;font-weight:700;color:#0F172A;margin:0 0 0.3rem 0;">🔗 Invite Link</p>',
            unsafe_allow_html=True
        )
        st.code(join_url, language="text")

        st.markdown(
            '<p style="font-size:0.88rem;font-weight:700;color:#0F172A;margin:0.6rem 0 0.3rem 0;">🏷 Subject Code</p>',
            unsafe_allow_html=True
        )
        st.code(subject_code, language="text")

        st.markdown(
            '<div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:10px;padding:0.6rem 0.8rem;margin-top:0.5rem;">'
            '<p style="font-size:0.82rem;font-weight:600;color:#166534;margin:0;">💡 Share via WhatsApp, Email, or Class Groups.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<p style="font-size:0.88rem;font-weight:700;color:#0F172A;margin:0 0 0.3rem 0;text-align:center;">📱 Scan to Join</p>',
            unsafe_allow_html=True
        )
        st.image(out.getvalue(), use_container_width=True, caption='Scan with phone camera')
