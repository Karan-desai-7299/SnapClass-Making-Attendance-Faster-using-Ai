import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
import time

import pandas as pd
from datetime import datetime, timezone, timedelta
IST = timezone(timedelta(hours=5, minutes=30))


def format_timestamp_ist(ts_str):
    if not ts_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(ts_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc).astimezone(IST)
        else:
            dt = dt.astimezone(IST)
        return dt.strftime("%Y-%m-%d %I:%M %p")
    except Exception:
        return ts_str

from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card



def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    c1, c2, c3 = st.columns([3, 3, 1.2], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        st.markdown(
            f'<p style="text-align:right;font-size:0.88rem;color:#475569;font-weight:500;margin:0;">'
            f'Welcome, <strong style="color:#0F172A;font-weight:700;">{student_data["name"]}</strong> 👋</p>',
            unsafe_allow_html=True
        )
    with c3:
        if st.button("Logout", type='secondary', key='student_logout_btn', use_container_width=True):
            st.session_state['is_logged_in'] = False
            if 'student_data' in st.session_state:
                del st.session_state.student_data
            st.session_state['login_type'] = None
            st.query_params.clear()
            st.rerun()

    st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)


    hc1, hc2 = st.columns([2, 1], vertical_alignment='center')
    with hc1:
        st.markdown(
            '<p style="font-size:1.3rem;font-weight:800;color:#0F172A;margin:0;">📚 Your Enrolled Subjects</p>',
            unsafe_allow_html=True
        )
    with hc2:
        if st.button('➕ Enroll in Subject', type='primary', use_container_width=True):
            enroll_dialog()

    st.divider()

    with st.spinner('Loading your enrolled subjects...'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}
    for log in logs:
        sid = log['subject_id']
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]['total'] += 1
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    if not subjects:
        st.markdown(
            '<div style="background:#F8FAFC;border:1.5px dashed #CBD5E1;border-radius:14px;'
            'padding:2.5rem;text-align:center;">'
            '<p style="font-size:1.5rem;margin:0 0 0.5rem 0;">📂</p>'
            '<p style="color:#475569;font-size:0.9rem;margin:0;font-weight:500;">You\'re not enrolled in any subjects yet.<br>Click <strong style="color:#4F46E5;">➕ Enroll in Subject</strong> above to get started.</p>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        cols = st.columns(2)
        for i, sub_node in enumerate(subjects):
            sub = sub_node['subjects']
            sid = sub['subject_id']

            stats = stats_map.get(sid, {"total": 0, "attended": 0})

            def unenroll_button(curr_sid=sid, curr_sub_name=sub['name']):
                if st.button(
                    "🗑️ Unenroll from this course",
                    type='tertiary',
                    use_container_width=True,
                    key=f"unenroll_{curr_sid}"
                ):
                    unenroll_student_to_subject(student_id, curr_sid)
                    st.toast(f'Unenrolled from {curr_sub_name} successfully!')
                    st.rerun()


            with cols[i % 2]:
                subject_card(
                    name=sub['name'],
                    code=sub['subject_code'],
                    section=sub['section'],
                    stats=[
                        ('📅', 'Total', stats['total']),
                        ('✅', 'Attended', stats['attended']),
                    ],
                    footer_callback=unenroll_button
                )

    # ── Detailed Attendance Log History for Student ──────────────────────────
    st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:1.25rem;font-weight:800;color:#0F172A;margin:0 0 0.25rem 0;">📅 Your Attendance History</p>'
        '<p style="font-size:0.85rem;color:#475569;font-weight:500;margin:0 0 0.85rem 0;">View date-wise attendance status for all your classes.</p>',
        unsafe_allow_html=True
    )

    if logs:
        history_data = []
        for log in logs:
            ts = log.get('timestamp')
            time_str = format_timestamp_ist(ts)
            sub_info = log.get('subjects', {})
            is_p = bool(log.get('is_present', False))

            history_data.append({
                "Date & Time": time_str,
                "Subject": sub_info.get('name', 'N/A'),
                "Subject Code": sub_info.get('subject_code', 'N/A'),
                "Status": "✅ Present" if is_p else "❌ Absent"
            })

        df_student_history = pd.DataFrame(history_data)
        df_student_history.insert(0, '#', range(1, len(df_student_history) + 1))
        st.dataframe(df_student_history, use_container_width=True, hide_index=True)

    else:
        st.markdown(
            '<div style="background:#F8FAFC;border:1.5px dashed #CBD5E1;border-radius:12px;'
            'padding:1.25rem;text-align:center;">'
            '<p style="color:#64748B;font-size:0.88rem;margin:0;font-weight:500;">No class attendance records recorded yet.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    footer_dashboard()



def student_screen():

    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    # ── Student Login (Camera View) ──────────────────────────────────────────
    c1, c2 = st.columns([3, 1], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("← Home", type='secondary', key='student_login_back_btn', use_container_width=True):
            st.session_state['login_type'] = None
            st.query_params.clear()
            st.rerun()


    st.markdown('<div style="height:1.25rem;"></div>', unsafe_allow_html=True)

    st.markdown(
        '<p style="font-size:1.35rem;font-weight:800;color:#0F172A;text-align:center;margin:0 0 0.25rem 0;">Student Login — Face ID</p>'
        '<p style="font-size:0.88rem;color:#475569;font-weight:500;text-align:center;margin:0 0 1.25rem 0;">Position your face clearly in the camera to sign in instantly.</p>',
        unsafe_allow_html=True
    )

    if 'show_student_registration' not in st.session_state:
        st.session_state.show_student_registration = False

    # Centered Camera Frame Container
    photo_source = st.camera_input("Position your face in the center")

    if photo_source:
        photo_bytes = photo_source.getvalue()
        photo_hash = hash(photo_bytes)

        if st.session_state.get('last_scanned_photo_hash') != photo_hash:
            st.session_state.last_scanned_photo_hash = photo_hash
            img = np.array(Image.open(photo_source).convert('RGB'))

            with st.spinner('AI is scanning your face...'):
                detected, all_ids, num_faces = predict_attendance(img)

                st.session_state.scan_detected = detected
                st.session_state.scan_num_faces = num_faces

                if num_faces == 0:
                    st.session_state.show_student_registration = False
                elif num_faces > 1:
                    st.session_state.show_student_registration = False
                else:
                    if detected:
                        student_id = list(detected.keys())[0]
                        all_students = get_all_students()
                        student = next((s for s in all_students if s['student_id'] == student_id), None)

                        if student:
                            st.session_state.is_logged_in = True
                            st.session_state.user_role = 'student'
                            st.session_state.student_data = student
                            st.session_state.show_student_registration = False
                            st.toast(f'Welcome back, {student["name"]}! 🎉')
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.session_state.show_student_registration = True
                        st.session_state.captured_registration_photo = img

        num_faces = st.session_state.get('scan_num_faces', 0)
        detected = st.session_state.get('scan_detected', {})

        if num_faces == 0:
            st.warning('⚠️ No face detected — make sure your face is visible and well-lit.')
        elif num_faces > 1:
            st.warning('⚠️ Multiple faces detected — please ensure only one person is in frame.')
        elif not detected:
            st.info('ℹ️ Face not recognized. Are you a new student? Register below!')
    else:
        st.session_state.last_scanned_photo_hash = None
        st.session_state.show_student_registration = False

    if st.session_state.get('show_student_registration'):
        st.markdown('<div style="height:0.75rem;"></div>', unsafe_allow_html=True)
        _, reg_col, _ = st.columns([1, 2, 1])
        with reg_col:
            with st.container(border=True):
                st.markdown(
                    '<p style="font-size:1.2rem;font-weight:800;color:#0F172A;margin:0 0 0.25rem 0;">👤 Register New Profile</p>'
                    '<p style="font-size:0.85rem;color:#475569;font-weight:500;margin:0 0 1rem 0;">Create your student account using your facial scan photo above.</p>',
                    unsafe_allow_html=True
                )

                new_name = st.text_input("Your Full Name", placeholder='e.g. Hamza Rizvi')

                st.markdown(
                    '<p style="font-size:0.85rem;font-weight:700;color:#1E293B;margin:0.75rem 0 0.2rem 0;">🎙️ Voice Enrollment (Optional)</p>'
                    '<p style="font-size:0.8rem;color:#475569;font-weight:500;margin:0 0 0.5rem 0;">Record a short phrase like "I am present" for voice attendance.</p>',
                    unsafe_allow_html=True
                )

                audio_data = None
                try:
                    audio_data = st.audio_input('Record your voice phrase')
                except Exception:
                    st.error('Audio input failed — voice enrollment skipped.')

                st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)

                if st.button('✨ Create Account', type='primary', use_container_width=True):
                    if new_name:
                        with st.spinner('Creating your profile...'):
                            reg_img = st.session_state.get('captured_registration_photo')
                            if reg_img is None and photo_source:
                                reg_img = np.array(Image.open(photo_source))

                            if reg_img is not None:
                                encodings = get_face_embeddings(reg_img)
                                if encodings:
                                    face_emb = encodings[0].tolist()

                                    voice_emb = None
                                    if audio_data:
                                        voice_emb = get_voice_embedding(audio_data.read())

                                    response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)

                                    if response_data:
                                        train_classifier()
                                        st.session_state.is_logged_in = True
                                        st.session_state.user_role = 'student'
                                        st.session_state.student_data = response_data[0]
                                        st.session_state.show_student_registration = False
                                        st.toast(f'Profile created! Hi {new_name}! 🎉')
                                        time.sleep(1)
                                        st.rerun()
                                else:
                                    st.error('Could not capture facial features — please retake your photo.')
                            else:
                                st.error('No photo found — please take a photo first.')
                    else:
                        st.warning('Please enter your name to continue.')

    footer_dashboard()