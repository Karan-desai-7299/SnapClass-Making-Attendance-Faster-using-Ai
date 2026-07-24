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

    if image_np is None or image_np.size == 0:
        return []

    # Ensure 3-channel RGB uint8 image for dlib
    if len(image_np.shape) == 2:
        image_np = np.stack((image_np,) * 3, axis=-1)
    elif len(image_np.shape) == 3 and image_np.shape[2] == 4:
        image_np = image_np[:, :, :3]
    elif len(image_np.shape) == 3 and image_np.shape[2] == 1:
        image_np = np.repeat(image_np, 3, axis=2)

    image_np = np.ascontiguousarray(image_np, dtype=np.uint8)
    h, w = image_np.shape[:2]

    # Build scale pyramid for dlib detection:
    # 1. Downscaled version (max dimension 640px) - optimal for high-res webcam selfies!
    # 2. Downscaled version (max dimension 1024px)
    # 3. Original size
    scales = []

    if max(h, w) > 640:
        s1 = 640.0 / float(max(h, w))
        w1, h1 = int(w * s1), int(h * s1)
        img_640 = np.array(Image.fromarray(image_np).resize((w1, h1), Image.Resampling.LANCZOS))
        scales.append((img_640, s1))

    if max(h, w) > 1024:
        s2 = 1024.0 / float(max(h, w))
        w2, h2 = int(w * s2), int(h * s2)
        img_1024 = np.array(Image.fromarray(image_np).resize((w2, h2), Image.Resampling.LANCZOS))
        scales.append((img_1024, s2))

    scales.append((image_np, 1.0))

    faces_found = []

    for img_scaled, scale_factor in scales:
        try:
            rects = detector(img_scaled, 0)
            if len(rects) == 0:
                rects = detector(img_scaled, 1)

            if len(rects) > 0:
                for rect in rects:
                    if scale_factor != 1.0:
                        orig_l = int(rect.left() / scale_factor)
                        orig_t = int(rect.top() / scale_factor)
                        orig_r = int(rect.right() / scale_factor)
                        orig_b = int(rect.bottom() / scale_factor)
                        faces_found.append(dlib.rectangle(orig_l, orig_t, orig_r, orig_b))
                    else:
                        faces_found.append(rect)
                break  # Found faces at this optimal scale!
        except Exception:
            continue

    encodings = []
    for face in faces_found:
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
