import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home


def home_screen():
    style_base_layout()
    style_background_home()

    header_home()

    st.markdown('<div style="height:0.75rem;"></div>', unsafe_allow_html=True)

    # ── Portal Selection Cards ──────────────────────────────────────────────
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        with st.container(border=True):
            st.markdown(
                '<div style="text-align:center;padding:0.5rem 0;">'
                '<div style="font-size:2.75rem;margin-bottom:0.5rem;">🎓</div>'
                '<p style="font-size:1.3rem;font-weight:800;color:#0F172A;margin:0 0 0.35rem 0;">Student Portal</p>'
                '<p style="font-size:0.88rem;color:#475569;font-weight:500;margin:0 0 1rem 0;">Login with your face — fast and instant sign in.</p>'
                '</div>',
                unsafe_allow_html=True
            )
            st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=95)
            st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
            if st.button(
                'Enter as Student ➔',
                type='primary',
                use_container_width=True,
                key='btn_student'
            ):
                st.session_state['login_type'] = 'student'
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown(
                '<div style="text-align:center;padding:0.5rem 0;">'
                '<div style="font-size:2.75rem;margin-bottom:0.5rem;">📋</div>'
                '<p style="font-size:1.3rem;font-weight:800;color:#0F172A;margin:0 0 0.35rem 0;">Teacher Portal</p>'
                '<p style="font-size:0.88rem;color:#475569;font-weight:500;margin:0 0 1rem 0;">Manage subjects &amp; run AI face/voice attendance.</p>'
                '</div>',
                unsafe_allow_html=True
            )
            st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=115)
            st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
            if st.button(
                'Enter as Teacher ➔',
                type='primary',
                use_container_width=True,
                key='btn_teacher'
            ):
                st.session_state['login_type'] = 'teacher'
                st.rerun()

    footer_home()