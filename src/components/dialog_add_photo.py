import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
from PIL import Image
import time


@st.dialog("Add Classroom Photos")
def add_photos_dialog():
    st.markdown(
        '<p style="font-size:0.9rem;color:#1E293B;font-weight:600;margin:0 0 1rem 0;">'
        'Add photos of your classroom — AI will scan every face and match attendance.</p>',
        unsafe_allow_html=True
    )

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    t1, t2 = st.columns(2)

    with t1:
        type_camera = "primary" if st.session_state.photo_tab == 'camera' else 'secondary'
        if st.button('📷 Camera', type=type_camera, use_container_width=True):
            st.session_state.photo_tab = 'camera'

    with t2:
        type_upload = "primary" if st.session_state.photo_tab == 'upload' else 'secondary'
        if st.button('📁 Upload Photos', type=type_upload, use_container_width=True):
            st.session_state.photo_tab = 'upload'

    st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)

    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input('Take a snapshot of the class', key='dialog_cam')
        if cam_photo:
            img = Image.open(cam_photo).convert('RGB')
            st.session_state.attendance_images.append(img)
            st.toast('📸 Photo captured!')
            st.rerun()

    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader(
            'Choose image files',
            type=['jpg', 'png', 'jpeg'],
            accept_multiple_files=True,
            key='dialog_upload'
        )
        if uploaded_files:
            if 'uploaded_file_names' not in st.session_state:
                st.session_state.uploaded_file_names = set()

            added_count = 0
            for f in uploaded_files:
                file_key = f"{f.name}_{f.size}"
                if file_key not in st.session_state.uploaded_file_names:
                    st.session_state.uploaded_file_names.add(file_key)
                    # Load RGB image into memory synchronously so file handle closure doesn't corrupt image data
                    img = Image.open(f).convert('RGB').copy()
                    st.session_state.attendance_images.append(img)
                    added_count += 1

            if added_count > 0:
                st.toast(f'✅ {added_count} photo(s) added!')

    st.divider()

    count = len(st.session_state.get('attendance_images', []))
    label = f'Done — {count} photo(s) added' if count else 'Done'
    if st.button(label, type='primary', use_container_width=True):
        st.rerun()
