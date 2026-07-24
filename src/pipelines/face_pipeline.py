import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec


def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()

    if image_np is None:
        return []

    # Ensure 3-channel RGB uint8 image for dlib
    if len(image_np.shape) == 2:
        image_np = np.stack((image_np,) * 3, axis=-1)
    elif len(image_np.shape) == 3 and image_np.shape[2] == 4:
        image_np = image_np[:, :, :3]
    elif len(image_np.shape) == 3 and image_np.shape[2] == 1:
        image_np = np.repeat(image_np, 3, axis=2)

    image_np = np.ascontiguousarray(image_np, dtype=np.uint8)

    # Detect faces: scale 0 first (fast & accurate for closeup selfies),
    # then scale 1 if no face is found (for smaller faces in classroom photos)
    try:
        faces = detector(image_np, 0)
        if len(faces) == 0:
            faces = detector(image_np, 1)
    except Exception:
        faces = []

    encodings = []
    for face in faces:
        try:
            shape = sp(image_np, face)
            face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)  # 128 embedding
            encodings.append(np.array(face_descriptor))
        except Exception:
            continue

    return encodings


@st.cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))

    if len(X) == 0:
        return None

    clf = SVC(kernel='linear', probability=True, class_weight='balanced')

    try:
        clf.fit(X, y)
    except ValueError:
        pass

    return {'clf': clf, 'X': X, "y": y}


def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)


def predict_attendance(class_image_np):
    try:
        encodings = get_face_embeddings(class_image_np)
    except Exception:
        return {}, [], 0

    detected_student = {}

    model_data = get_trained_model()

    if not model_data or not model_data.get('X') or not model_data.get('y'):
        return detected_student, [], len(encodings)

    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))
    resemblance_threshold = 0.50  # Balanced dlib face recognition threshold

    for encoding in encodings:
        # Calculate Euclidean distances between current face encoding and all registered student embeddings
        distances = [np.linalg.norm(np.array(student_emb) - np.array(encoding)) for student_emb in X_train]
        if distances:
            min_dist_idx = int(np.argmin(distances))
            min_dist = distances[min_dist_idx]

            if min_dist <= resemblance_threshold:
                matched_student_id = y_train[min_dist_idx]
                detected_student[matched_student_id] = True

    return detected_student, all_students, len(encodings)
