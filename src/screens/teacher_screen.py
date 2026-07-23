import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects, get_attendance_for_teacher, get_all_students
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog

from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_results import attendance_result_dialog
import numpy as np

from datetime import datetime, timezone, timedelta
IST = timezone(timedelta(hours=5, minutes=30))


def get_current_timestamp_ist():
    return datetime.now(IST).strftime("%Y-%m-%dT%H:%M:%S")


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


def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif "teacher_login_type" in st.session_state and st.session_state.teacher_login_type == 'register':
        teacher_screen_register()
    else:
        teacher_screen_login()


# ── Dashboard ───────────────────────────────────────────────────────────────

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data

    # ── Header & User bar ───────────────────────────────────────────────────
    c1, c2, c3 = st.columns([3, 3, 1.2], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        st.markdown(
            f'<p style="text-align:right;font-size:0.88rem;color:#475569;font-weight:500;margin:0;">'
            f'Signed in as <strong style="color:#0F172A;font-weight:700;">{teacher_data["name"]}</strong></p>',
            unsafe_allow_html=True
        )
    with c3:
        if st.button("Logout", type='secondary', key='teacher_logout_btn', use_container_width=True):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()


    st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)

    # ── Tab Navigation ───────────────────────────────────────────────────────
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "secondary"
        if st.button('📸 Take Attendance', type=type1, use_container_width=True, key='tab_take_attendance'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "secondary"
        if st.button('📚 Manage Subjects', type=type2, use_container_width=True, key='tab_manage_subjects'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "secondary"
        if st.button('📊 Attendance Records', type=type3, use_container_width=True, key='tab_attendance_records'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']

    st.markdown(
        '<p style="font-size:1.35rem;font-weight:800;color:#0F172A;margin:0 0 0.25rem 0;">📸 Take AI Attendance</p>'
        '<p style="font-size:0.88rem;color:#475569;font-weight:500;margin:0 0 1.25rem 0;">Upload classroom photos — AI will scan faces and record attendance automatically.</p>',
        unsafe_allow_html=True
    )

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.info('ℹ️ You haven\'t created any subjects yet. Go to **Manage Subjects** to create one.')
        return

    subject_options = {f"{s['name']} — {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3, 1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('🖼️ Add Photos', type='primary', use_container_width=True, key='add_photos_btn'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.markdown(
            f'<p style="font-size:0.9rem;font-weight:700;color:#334155;margin:0 0 0.5rem 0;">'
            f'📂 {len(st.session_state.attendance_images)} Photo(s) Added</p>',
            unsafe_allow_html=True
        )
        gallery_cols = st.columns(4)
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, use_container_width=True, caption=f'Photo {idx + 1}')
    else:
        st.markdown(
            '<div style="background:#F8FAFC;border:1.5px dashed #CBD5E1;border-radius:14px;'
            'padding:1.75rem;text-align:center;margin:0.5rem 0 1rem 0;">'
            '<p style="color:#475569;font-size:0.88rem;margin:0;font-weight:500;">No photos added yet — click <strong style="color:#4F46E5;">🖼️ Add Photos</strong> above.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('🗑️ Clear All Photos', use_container_width=True, type='tertiary', disabled=not has_photos, key='clear_photos_btn'):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if st.button('⚡ Run Face Analysis', use_container_width=True, type='secondary', disabled=not has_photos, key='run_analysis_btn'):
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx + 1}")

                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course.')
                else:
                    results, attendance_to_log = [], []
                    current_timestamp = get_current_timestamp_ist()

                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present = len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button('🎙️ Voice Attendance', type='primary', use_container_width=True, key='voice_attendance_btn'):
            voice_attendance_dialog(selected_subject_id)


def teacher_tab_manage_subjects():
    col1, col2 = st.columns([2, 1], vertical_alignment='center')
    with col1:
        st.markdown(
            '<p style="font-size:1.35rem;font-weight:800;color:#0F172A;margin:0;">📚 Manage Subjects</p>',
            unsafe_allow_html=True
        )
    with col2:
        teacher_id = st.session_state.teacher_data['teacher_id']
        if st.button('➕ Create Subject', use_container_width=True, type='primary', key='create_subject_btn'):
            create_subject_dialog(teacher_id)

    st.markdown('<div style="height:0.75rem;"></div>', unsafe_allow_html=True)

    teacher_id = st.session_state.teacher_data['teacher_id']
    subjects = get_teacher_subjects(teacher_id)

    if subjects:
        for sub in subjects:
            stats = [
                ("👥", "Students", sub['total_students']),
                ("🕐", "Classes", sub['total_classes']),
            ]

            def share_btn(s_name=sub['name'], s_code=sub['subject_code']):
                if st.button(
                    f"🔗 Share Code: {s_code}",
                    key=f"share_{s_code}",
                    type='tertiary'
                ):
                    share_subject_dialog(s_name, s_code)
                st.markdown('<div style="height:0.25rem;"></div>', unsafe_allow_html=True)

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.markdown(
            '<div style="background:#F8FAFC;border:1.5px dashed #CBD5E1;border-radius:14px;'
            'padding:2rem;text-align:center;margin:0.5rem 0;">'
            '<p style="font-size:1.5rem;margin:0 0 0.5rem 0;">📂</p>'
            '<p style="color:#475569;font-size:0.9rem;margin:0;font-weight:500;">No subjects created yet — click <strong style="color:#4F46E5;">➕ Create Subject</strong> to start.</p>'
            '</div>',
            unsafe_allow_html=True
        )


def teacher_tab_attendance_records():
    st.markdown(
        '<p style="font-size:1.35rem;font-weight:800;color:#0F172A;margin:0 0 1rem 0;">📊 Attendance Records</p>',
        unsafe_allow_html=True
    )

    teacher_id = st.session_state.teacher_data['teacher_id']
    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.markdown(
            '<div style="background:#F8FAFC;border:1.5px dashed #CBD5E1;border-radius:14px;'
            'padding:2rem;text-align:center;">'
            '<p style="font-size:1.5rem;margin:0 0 0.5rem 0;">📋</p>'
            '<p style="color:#475569;font-size:0.9rem;margin:0;font-weight:500;">No attendance records found yet.</p>'
            '</div>',
            unsafe_allow_html=True
        )
        return

    # Map all students for student name lookup
    all_students_db = get_all_students()
    student_name_map = {s['student_id']: s['name'] for s in all_students_db} if all_students_db else {}

    data = []
    session_map = {}

    for r in records:
        ts = r.get('timestamp')
        ts_group = ts.split(".")[0] if ts else "N/A"
        time_str = format_timestamp_ist(ts)
        sub_name = r['subjects']['name']
        sub_code = r['subjects']['subject_code']
        is_present = bool(r.get('is_present', False))
        sid = r.get('student_id')
        s_name = student_name_map.get(sid, f"Student #{sid}")

        data.append({
            "ts_group": ts_group,
            "Time": time_str,
            "Subject": sub_name,
            "Subject Code": sub_code,
            "is_present": is_present
        })

        session_key = f"{time_str} — {sub_name} ({sub_code})"
        if session_key not in session_map:
            session_map[session_key] = []

        session_map[session_key].append({
            "Student ID": sid,
            "Student Name": s_name,
            "Status": "✅ Present" if is_present else "❌ Absent"
        })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        ).reset_index()
    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " / "
        + summary['Total_Count'].astype(str) + ' Students'
    )

    # Sort summary by timestamp ASCENDING first to assign chronological session numbers (1 = 1st attendance taken)
    summary = summary.sort_values(by='ts_group', ascending=True).reset_index(drop=True)
    summary['#'] = range(1, len(summary) + 1)

    # Sort descending for display (latest session at top) with fixed chronological # session number
    display_df = (
        summary.sort_values(by='ts_group', ascending=False)
        [['#', 'Time', 'Subject', 'Subject Code', 'Attendance Stats']]
    ).reset_index(drop=True)


    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)

    # ── Detailed Student Breakdown per Session ──────────────────────────────
    st.markdown(
        '<p style="font-size:1.15rem;font-weight:800;color:#0F172A;margin:0 0 0.4rem 0;">📋 Detailed Student Attendance Breakdown</p>'
        '<p style="font-size:0.85rem;color:#475569;font-weight:500;margin:0 0 0.85rem 0;">Select a session below to view individual student present/absent list.</p>',
        unsafe_allow_html=True
    )

    if session_map:
        selected_session = st.selectbox("Select Class Session", options=list(session_map.keys()))
        session_students = session_map[selected_session]

        df_session = pd.DataFrame(session_students)
        df_session.insert(0, '#', range(1, len(df_session) + 1))

        p_count = sum(1 for s in session_students if s['Status'] == "✅ Present")
        t_count = len(session_students)

        st.markdown(
            f'<div style="display:flex;gap:10px;align-items:center;margin:0.5rem 0 0.75rem 0;">'
            f'<span style="background:#ECFDF5;color:#047857;border:1px solid #A7F3D0;font-size:0.85rem;font-weight:700;padding:4px 12px;border-radius:8px;">✅ {p_count} Present</span>'
            f'<span style="background:#FFF1F2;color:#9F1239;border:1px solid #FECDD3;font-size:0.85rem;font-weight:700;padding:4px 12px;border-radius:8px;">❌ {t_count - p_count} Absent</span>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.dataframe(df_session, use_container_width=True, hide_index=True)





# ── Login / Register Forms ───────────────────────────────────────────────────

def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True

    return False


def teacher_screen_login():
    c1, c2 = st.columns([3, 1], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("← Home", type='secondary', key='teacher_login_back_btn', use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown('<div style="height:1.25rem;"></div>', unsafe_allow_html=True)

    # Wrap the ENTIRE form inside a single clean container card
    _, form_col, _ = st.columns([1, 2, 1])
    with form_col:
        with st.container(border=True):
            st.markdown(
                '<p style="font-size:1.35rem;font-weight:800;color:#0F172A;margin:0 0 0.25rem 0;">Teacher Login</p>'
                '<p style="font-size:0.88rem;color:#475569;font-weight:500;margin:0 0 1.25rem 0;">Sign in to manage subjects &amp; attendance</p>',
                unsafe_allow_html=True
            )

            teacher_username = st.text_input("Username", placeholder='e.g. ananyaroy')
            teacher_pass = st.text_input("Password", type='password', placeholder="Enter password")

            st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)

            btnc1, btnc2 = st.columns(2)
            with btnc1:
                if st.button('🔑 Login', use_container_width=True, type='primary'):
                    if login_teacher(teacher_username, teacher_pass):
                        st.toast("Welcome back! 👋")
                        import time
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

            with btnc2:
                if st.button('Register Instead', type="secondary", use_container_width=True):
                    st.session_state.teacher_login_type = 'register'
                    st.rerun()

    footer_dashboard()


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All fields are required."
    if check_teacher_exists(teacher_username):
        return False, "Username already taken."
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords don't match."

    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Account created! You can now log in."
    except Exception as e:
        return False, "Unexpected error. Please try again."


def teacher_screen_register():
    c1, c2 = st.columns([3, 1], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("← Home", type='secondary', key='teacher_register_back_btn', use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()


    st.markdown('<div style="height:1.25rem;"></div>', unsafe_allow_html=True)

    _, form_col, _ = st.columns([1, 2, 1])
    with form_col:
        with st.container(border=True):
            st.markdown(
                '<p style="font-size:1.35rem;font-weight:800;color:#0F172A;margin:0 0 0.25rem 0;">Create Teacher Account</p>'
                '<p style="font-size:0.88rem;color:#475569;font-weight:500;margin:0 0 1.25rem 0;">Set up your profile to start taking AI attendance</p>',
                unsafe_allow_html=True
            )

            teacher_username = st.text_input("Username", placeholder='e.g. ananyaroy')
            teacher_name = st.text_input("Full Name", placeholder='e.g. Ananya Roy')
            teacher_pass = st.text_input("Password", type='password', placeholder="Choose a password")
            teacher_pass_confirm = st.text_input("Confirm Password", type='password', placeholder="Repeat password")

            st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)

            btnc1, btnc2 = st.columns(2)
            with btnc1:
                if st.button('👤 Create Account', use_container_width=True, type='primary'):
                    success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
                    if success:
                        st.success(message)
                        import time
                        time.sleep(2)
                        st.session_state.teacher_login_type = "login"
                        st.rerun()
                    else:
                        st.error(message)

            with btnc2:
                if st.button('Login Instead', type="secondary", use_container_width=True):
                    st.session_state.teacher_login_type = 'login'
                    st.rerun()

    footer_dashboard()