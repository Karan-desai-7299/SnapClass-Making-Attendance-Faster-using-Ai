import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase

import time


@st.dialog("Enroll in a Subject")
def enroll_dialog():
    st.markdown(
        '<p style="font-size:0.88rem;color:#334155;font-weight:500;margin:0 0 1rem 0;">'
        'Ask your teacher for the subject code, then enter it below to enroll.</p>',
        unsafe_allow_html=True
    )

    join_code = st.text_input('Subject Code', placeholder='e.g. CS101')

    st.markdown('<div style="height:0.4rem;"></div>', unsafe_allow_html=True)

    if st.button('Enroll Now', type='primary', use_container_width=True):
        if join_code:
            res = supabase.table('subjects').select('subject_id, name, subject_code').eq('subject_code', join_code).execute()
            if res.data:
                subject = res.data[0]
                student_id = st.session_state.student_data['student_id']

                check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()
                if check.data:
                    st.warning('⚠️ You\'re already enrolled in this subject.')
                else:
                    enroll_student_to_subject(student_id, subject['subject_id'])
                    st.success(f'🎉 Successfully enrolled in {subject["name"]}!')
                    time.sleep(1)
                    st.rerun()
            else:
                st.error('❌ Subject code not found. Please double-check and try again.')
        else:
            st.warning('⚠️ Please enter a subject code.')