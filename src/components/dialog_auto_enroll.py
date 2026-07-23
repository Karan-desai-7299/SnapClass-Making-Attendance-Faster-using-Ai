import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time


@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    if 'student_data' not in st.session_state or not st.session_state.student_data:
        st.warning("⚠️ Please sign in as a student to enroll in this class.")
        if st.button("Got it", use_container_width=True, type="primary"):
            st.query_params.clear()
            st.rerun()
        return

    student_id = st.session_state.student_data.get('student_id')
    if not student_id:
        st.warning("⚠️ Student session invalid. Please sign in again.")
        return

    res = supabase.table('subjects').select('subject_id, name').eq('subject_code', subject_code).execute()
    if not res.data:
        st.error('❌ Subject code not found. Please check the link and try again.')
        if st.button('Close', use_container_width=True):
            st.query_params.clear()
            st.rerun()
        return

    subject = res.data[0]

    check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()
    if check.data:
        st.info(f'ℹ️ You\'re already enrolled in **{subject["name"]}**.')
        if st.button('Got it!', use_container_width=True, type='primary'):
            st.query_params.clear()
            st.rerun()
        return

    st.markdown(
        f'<div style="background:#F5F3FF;border:1.5px solid #DDD6FE;border-radius:14px;padding:1.25rem;margin-bottom:1rem;">'
        f'<p style="font-size:1.05rem;color:#0F172A;margin:0 0 0.4rem 0;">You\'ve been invited to join <strong style="color:#6366F1;">{subject["name"]}</strong>.</p>'
        f'<p style="font-size:0.85rem;color:#475569;margin:0;">Would you like to enroll in this subject now?</p>'
        f'</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button('No thanks', use_container_width=True, type='secondary'):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button('Yes, Enroll Now!', type='primary', use_container_width=True):
            enroll_student_to_subject(student_id, subject['subject_id'])
            st.success('🎉 Successfully enrolled!')
            st.query_params.clear()
            time.sleep(1.5)
            st.rerun()
