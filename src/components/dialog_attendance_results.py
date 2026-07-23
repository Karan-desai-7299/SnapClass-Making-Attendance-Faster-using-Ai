import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time


from src.database.db import create_attendance


def show_attendance_result(df, logs):
    st.markdown(
        '<p style="font-size:0.88rem;color:#334155;font-weight:500;margin:0 0 0.75rem 0;">'
        'Review the results below. Confirm to save attendance records, or discard to cancel.</p>',
        unsafe_allow_html=True
    )
    if '#' not in df.columns:
        df = df.copy()
        df.insert(0, '#', range(1, len(df) + 1))
    st.dataframe(df, hide_index=True, use_container_width=True)


    st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button('🗑 Discard', use_container_width=True, type='secondary'):
            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []
            st.rerun()

    with col2:
        if st.button('✅ Confirm & Save', use_container_width=True, type='primary'):
            try:
                create_attendance(logs)
                st.toast("✅ Attendance saved successfully!")
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception as e:
                st.error('⚠️ Sync failed — please try again.')


@st.dialog("Attendance Report")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)

