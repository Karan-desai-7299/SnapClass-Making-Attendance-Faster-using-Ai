import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen

from src.components.dialog_auto_enroll import auto_enroll_dialog


def main():
    st.set_page_config(
        page_title='SnapClass - Making Attendance faster using AI',
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png"
    )
    # Restore view and tab state from URL parameters on page refresh
    view_param = st.query_params.get('view')
    if view_param in ['teacher', 'student'] and st.session_state.get('login_type') is None:
        st.session_state['login_type'] = view_param

    tab_param = st.query_params.get('tab')
    if tab_param in ['take_attendance', 'manage_subjects', 'attendance_records'] and 'current_teacher_tab' not in st.session_state:
        st.session_state['current_teacher_tab'] = tab_param

    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()

        case None:
            home_screen()


    join_code = st.query_params.get('join-code')
    if join_code:
        # If user is not logged in at all, set login_type to student so they land on student auth page
        if not st.session_state.get('is_logged_in') and st.session_state.get('login_type') != 'student':
            st.session_state.login_type = 'student'
            st.rerun()

        # If logged in as student, open quick enrollment modal
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student' and 'student_data' in st.session_state:
            auto_enroll_dialog(join_code)


main()
