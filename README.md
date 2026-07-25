# SnapClass — Making Attendance Faster using AI

**Live demo:** [snapclass-main-karansinh787repo.streamlit.app](https://snapclass-main-karansinh787repo.streamlit.app/)
**Landing page repo:** [github.com/Karan-desai-7299/landing-page-for-SnapClass-Attendance-using-Ai](https://github.com/Karan-desai-7299/landing-page-for-SnapClass-Attendance-using-Ai)
**Landing page live:** [snapclass-aipowered-attendancesystem-karand16.vercel.app](https://snapclass-aipowered-attendancesystem-karand16.vercel.app/)

SnapClass is an AI-powered classroom attendance system built with Streamlit. It replaces manual roll-calls with **face recognition** and **voice recognition**, backed by a Supabase database for real-time storage and sync.

---

## ✨ Features

- **FaceID login & registration** — students register and log in using their face, captured via the browser camera, no passwords needed on the student side.
- **AI photo-based attendance** — teachers snap or upload classroom photos, and the app detects and matches every enrolled student's face in one pass.
- **Voice ID attendance** — students say "I am present" one after another; the app matches each voice against stored voice embeddings.
- **QR / link-based enrollment** — every subject gets a unique code and shareable QR, so students can join a class in seconds.
- **Review before saving** — every AI attendance run (photo or voice) shows a results table first; a teacher confirms or discards it before anything is written to the database.
- **Teacher dashboard** — create and manage subjects, run attendance, and view historical attendance records with present/absent breakdowns.
- **Student dashboard** — track enrolled subjects and personal attendance history.
- **Persisted session state** — the current view (teacher/student) and active dashboard tab are restored from the URL, so a page refresh doesn't kick you back to the home screen.

## 🧠 Tech Stack

| Layer | Technology |
|---|---|
| Frontend / App framework | [Streamlit](https://streamlit.io/) |
| Face recognition | `dlib` (via `dlib-bin`), `face_recognition_models`, `scikit-learn` (SVM classifier) |
| Voice recognition | [Resemblyzer](https://github.com/resemble-ai/Resemblyzer), `librosa` |
| Database & Auth | [Supabase](https://supabase.com/) (PostgreSQL) |
| QR generation | `segno` |
| Password hashing | `bcrypt` |
| Image handling | `Pillow` |

## 📁 Project Structure

```
├── app.py                        # Entry point & routing (home / teacher / student)
├── requirements.txt
├── .streamlit/config.toml        # Native Streamlit theme (Indigo primary)
├── .devcontainer/                # GitHub Codespaces / Dev Container config
└── src/
    ├── ui/
    │   └── base_layout.py        # Centralized design system (CSS, colors, typography)
    ├── components/
    │   ├── header.py, footer.py
    │   ├── subject_card.py
    │   └── dialog_*.py           # Create subject, enroll, share, add photos, voice/photo attendance results
    ├── screens/
    │   ├── home_screen.py
    │   ├── teacher_screen.py
    │   └── student_screen.py
    ├── pipelines/
    │   ├── face_pipeline.py      # Face embedding extraction + classifier
    │   └── voice_pipeline.py     # Voice embedding extraction
    └── database/
        ├── config.py             # Supabase client init
        └── db.py                 # All Supabase queries
```

## 🔒 Data & Privacy Notes

- Registration converts a photo/voice sample into a numerical **embedding** — the raw image/audio is not persisted after the embedding is generated.
- Attendance results are always shown for review before being saved; nothing is written to the database automatically.

## 🚀 Running Locally

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Python **3.11** is required — several dependencies (`dlib-bin`, `numpy`, `scikit-learn`) are version-pinned against 3.11 wheels. The included `.python-version` file pins this for tools that respect it (e.g. Streamlit Cloud).

2. Create `.streamlit/secrets.toml` (this file is git-ignored) with your Supabase credentials:
   ```toml
   SUPABASE_URL = "your-supabase-project-url"
   SUPABASE_KEY = "your-supabase-anon-or-service-key"
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## ☁️ Deployment Notes (Streamlit Community Cloud)

- Set the **Python version to 3.11** in the app's Advanced Settings — newer versions may not have prebuilt wheels for some of the pinned scientific-computing dependencies, which forces slow/unstable source builds.
- Add `SUPABASE_URL` and `SUPABASE_KEY` under **App settings → Secrets** (these are not committed to the repo).
- `requirements.txt` includes `--extra-index-url https://download.pytorch.org/whl/cpu` so `resemblyzer`'s `torch` dependency installs the small CPU-only build instead of the multi-gigabyte CUDA/GPU build, which isn't needed on this platform.

## 👨‍💻 Author

**Karansinh Desai** — Computer Science Engineering Student, AI & Full Stack Developer
[LinkedIn](https://www.linkedin.com/in/karansinh-desai-a249a0289/)
