import streamlit as st
import numpy as np
import cv2
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# CACHING: evita reentrenar en cada interacción
@st.cache_data(show_spinner=True)
def load_digits_dataset():
    digits = load_digits()
    X = digits.images  # shape (n_samples, 8, 8)
    y = digits.target
    return X, y

@st.cache_resource(show_spinner=True)
def train_ann(X_flat, y):
    mlp = MLPClassifier(hidden_layer_sizes=(64,), activation='relu', max_iter=500, random_state=42)
    mlp.fit(X_flat, y)
    return mlp

def preprocess_image_for_digits(img_bgr):
    """
    Convierte imagen BGR -> escala de grises, redimensiona a 8x8,
    y escala valores de 0..16 (como el dataset sklearn digits).
    """
    if img_bgr is None:
        return None
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (8, 8), interpolation=cv2.INTER_AREA)
    norm = (16.0 * (resized / 255.0)).astype(np.float32)
    flat = norm.flatten()
    return flat

def app():
    st.header("📑 Capítulo 11 — Machine Learning (ANN) · Demo con Digits")
    st.markdown(
        """
        Este capítulo entrena una red neuronal (MLP) para reconocer dígitos (dataset `digits` de sklearn).
        Ahora puedes subir tu propia imagen y el modelo intentará reconocer el dígito.
        """
    )

    # Cargar dataset
    X_images, y = load_digits_dataset()
    n_samples = len(X_images)

    # Preparar features
    X_flat = X_images.reshape((n_samples, -1))

    # División
    X_train, X_test, y_train, y_test = train_test_split(X_flat, y, test_size=0.25, random_state=42, stratify=y)

    # Entrenar
    with st.spinner("Entrenando la red neuronal (MLP)..."):
        model = train_ann(X_train, y_train)

    # Evaluación rápida
    acc = accuracy_score(y_test, model.predict(X_test))
    st.success(f"Precisión en conjunto de prueba: **{acc * 100:.2f}%**")

    st.markdown("---")
    st.subheader("🔢 Subir una imagen de dígito (PNG/JPG)")

    uploaded = st.file_uploader("Selecciona una imagen", type=["png", "jpg", "jpeg"])
    if uploaded is not None:
        file_bytes = np.frombuffer(uploaded.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Imagen subida", use_container_width=True)

        # Preprocesar y predecir
        flat = preprocess_image_for_digits(img)
        if flat is None:
            st.error("No se pudo procesar la imagen subida.")
        else:
            pred = model.predict([flat])[0]
            st.success(f"✅ Predicción del modelo: **{int(pred)}**")
            # Mostrar la versión 8x8 usada para la predicción
            img8x8 = flat.reshape(8, 8)
            st.image(img8x8 / 16.0, caption="Imagen redimensionada a 8×8 (entrada a la ANN)", width=160)
