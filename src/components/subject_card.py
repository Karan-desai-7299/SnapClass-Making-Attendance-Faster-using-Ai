import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    # Build the complete HTML string without any blank lines at concatenation seams
    # so Streamlit's markdown parser never breaks mid-block.
    code_badge = (
        f'<span style="background:#EEF2FF;color:#4338CA;border:1.5px solid #C7D2FE;'
        f'font-size:0.8rem;font-weight:700;padding:3px 10px;border-radius:8px;letter-spacing:0.02em;">{code}</span>'
    )
    section_badge = (
        f'<span style="background:#FEF3C7;color:#B45309;border:1.5px solid #FDE68A;'
        f'font-size:0.8rem;font-weight:700;padding:3px 10px;border-radius:8px;">Section {section}</span>'
    )

    html = (
        '<div style="background:#FFFFFF;border:1.5px solid #E2E8F0;'
        'border-top:4px solid transparent;border-image:linear-gradient(90deg, #6366F1, #8B5CF6, #EC4899) 1;'
        'border-radius:18px;padding:1.4rem 1.5rem 1rem 1.5rem;margin-bottom:1rem;'
        'box-shadow:0 8px 20px -4px rgba(15,23,42,0.06);transition:all 0.2s ease;">'
        f'<p style="font-size:1.15rem;font-weight:800;color:#0F172A;margin:0 0 0.6rem 0;line-height:1.3;">{name}</p>'
        f'<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:0.85rem;">'
        f'{code_badge}{section_badge}'
        f'</div>'
    )

    if stats:
        html += '<div style="display:flex;gap:8px;flex-wrap:wrap;">'
        for icon, label, value in stats:
            bg_color = "#ECFDF5" if label == "Attended" or label == "Students" else "#FDF4FF"
            text_color = "#047857" if label == "Attended" or label == "Students" else "#C026D3"
            border_color = "#A7F3D0" if label == "Attended" or label == "Students" else "#F5D0FE"

            html += (
                f'<div style="background:{bg_color};border:1.5px solid {border_color};padding:4px 12px;'
                f'border-radius:10px;font-size:0.84rem;color:{text_color};font-weight:600;">'
                f'{icon} <strong style="color:{text_color};font-weight:800;">{value}</strong> {label}'
                f'</div>'
            )
        html += '</div>'

    html += '</div>'

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
