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

    # Create scale pyramid so all face sizes (large front-row & small back-row) are captured!
    scales = [(image_np, 1.0)]

    if max(h, w) > 800:
        s1 = 800.0 / float(max(h, w))
        w1, h1 = int(w * s1), int(h * s1)
        img_800 = np.array(Image.fromarray(image_np).resize((w1, h1)))
        scales.append((img_800, s1))

    faces_found = []

    for img_scaled, scale_factor in scales:
        try:
            rects = list(detector(img_scaled, 0))
            if len(rects) == 0 or max(h, w) <= 1000:
                rects += list(detector(img_scaled, 1))

            for rect in rects:
                if scale_factor != 1.0:
                    orig_l = int(rect.left() / scale_factor)
                    orig_t = int(rect.top() / scale_factor)
                    orig_r = int(rect.right() / scale_factor)
                    orig_b = int(rect.bottom() / scale_factor)
                    faces_found.append(dlib.rectangle(orig_l, orig_t, orig_r, orig_b))
                else:
                    faces_found.append(rect)
        except Exception:
            continue

    # IoU Deduplication
    unique_faces = []
    for face in faces_found:
        is_dup = False
        for u in unique_faces:
            xA = max(face.left(), u.left())
            yA = max(face.top(), u.top())
            xB = min(face.right(), u.right())
            yB = min(face.bottom(), u.bottom())

            interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
            boxAArea = (face.right() - face.left() + 1) * (face.bottom() - face.top() + 1)
            boxBArea = (u.right() - u.left() + 1) * (u.bottom() - u.top() + 1)

            iou = interArea / float(boxAArea + boxBArea - interArea)
            if iou > 0.3:
                is_dup = True
                break
        if not is_dup:
            unique_faces.append(face)

    encodings = []
    for face in unique_faces:
        try:
            shape = sp(image_np, face)
            face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)  # 128 embedding
            encodings.append(np.array(face_descriptor))
        except Exception:
            continue

    return encodings


def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding, dtype=np.float64))
            y.append(int(student.get('student_id')))

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
    return True


def predict_attendance(class_image_np):
    try:
        encodings = get_face_embeddings(class_image_np)
    except Exception:
        return {}, [], 0

    detected_student = {}

    student_db = get_all_students()
    if not student_db:
        return detected_student, [], len(encodings)

    X_train = []
    y_train = []

    for student in student_db:
        emb = student.get('face_embedding')
        if emb:
            X_train.append(np.array(emb, dtype=np.float64))
            y_train.append(int(student.get('student_id')))

    if len(X_train) == 0:
        return detected_student, [], len(encodings)

    all_students = sorted(list(set(y_train)))
    resemblance_threshold = 0.55  # Official dlib 128D face verification threshold

    for encoding in encodings:
        distances = [np.linalg.norm(np.array(student_emb) - np.array(encoding)) for student_emb in X_train]
        if distances:
            min_dist_idx = int(np.argmin(distances))
            min_dist = distances[min_dist_idx]

            if min_dist <= resemblance_threshold:
                matched_student_id = int(y_train[min_dist_idx])
                detected_student[matched_student_id] = True

    return detected_student, all_students, len(encodings)
