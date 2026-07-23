import streamlit as st
from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.markdown(
        '<p style="font-size:0.88rem;color:#334155;font-weight:500;margin:0 0 1rem 0;">'
        'Fill in the details below. Students will use the subject code to enroll.</p>',
        unsafe_allow_html=True
    )

    sub_id = st.text_input("Subject Code", placeholder="e.g. CS101")
    sub_name = st.text_input("Subject Name", placeholder="e.g. Introduction to Computer Science")
    sub_section = st.text_input("Section", placeholder="e.g. A")

    st.markdown('<div style="height:0.4rem;"></div>', unsafe_allow_html=True)

    if st.button("✅ Create Subject", type='primary', use_container_width=True):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id, sub_name, sub_section, teacher_id)
                st.toast("✅ Subject created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("⚠️ Please fill in all fields before creating the subject.")

