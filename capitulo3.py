import streamlit as st
import cv2
import numpy as np
import av
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# ============================
# Función de cartoonización
# ============================
def cartoonize_image(img, ksize=5, sketch_mode=False):
    """
    Convierte una imagen a estilo cartoon o sketch.
    """
    num_repetitions, sigma_color, sigma_space, ds_factor = 10, 5, 7, 4

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.medianBlur(img_gray, 7)

    edges = cv2.Laplacian(img_gray, cv2.CV_8U, ksize=ksize)
    _, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)

    if sketch_mode:
        return cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    img_small = cv2.resize(img, None, fx=1.0/ds_factor, fy=1.0/ds_factor, interpolation=cv2.INTER_AREA)
    for _ in range(num_repetitions):
        img_small = cv2.bilateralFilter(img_small, ksize, sigma_color, sigma_space)

    img_output = cv2.resize(img_small, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_LINEAR)
    dst = cv2.bitwise_and(img_output, img_output, mask=mask)
    return dst

# ============================
# Clase para stream en vivo
# ============================
class Cartoonizer(VideoTransformerBase):
    def __init__(self):
        self.ksize = 5
        self.sketch_mode = False

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        cartoon = cartoonize_image(img, ksize=self.ksize, sketch_mode=self.sketch_mode)
        return cartoon

# ============================
# App principal
# ============================
def app():
    st.title("📙 Capítulo 3 — Cartoonizing (Webcam/Photo)")
    st.info("📷 Puedes subir una imagen, tomar una foto o activar el stream en vivo para aplicar el efecto cartoon.")

    fuente = st.radio(
        "Selecciona la fuente de la imagen:",
        ["📂 Subir imagen", "📸 Tomar foto", "📹 Video en vivo (Stream)"],
        horizontal=True
    )

    frame = None

    # ------------------------------
    # Subida de imagen
    # ------------------------------
    if fuente == "📂 Subir imagen":
        uploaded_file = st.file_uploader("Sube tu imagen", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # ------------------------------
    # Foto estática con cámara
    # ------------------------------
    elif fuente == "📸 Tomar foto":
        camera_file = st.camera_input("Toma una foto con la cámara web")
        if camera_file is not None:
            file_bytes = np.asarray(bytearray(camera_file.read()), dtype=np.uint8)
            frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # ------------------------------
    # Video en vivo con streamlit-webrtc
    # ------------------------------
    elif fuente == "📹 Video en vivo (Stream)":
        st.markdown("🎥 Streaming en vivo desde la cámara (usa WebRTC en el navegador).")
        webrtc_streamer(
            key="cartoonizer",
            video_transformer_factory=Cartoonizer,
            media_stream_constraints={"video": True, "audio": False},
        )

    # ------------------------------
    # Procesamiento de imagen estática
    # ------------------------------
    if frame is not None and fuente != "📹 Video en vivo (Stream)":
        st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), caption="Imagen original", use_container_width=True)
        st.divider()
        st.subheader("🎨 Ajustes del efecto Cartoon")

        with st.expander("ℹ️ ¿Qué hace cada control?"):
            st.markdown("""
            - **Modo de cartoonización** → Con colores o solo sketch en blanco y negro.  
            - **Tamaño de kernel (Laplaciano)** → Controla el grosor de las líneas detectadas.
            """)

        modo = st.radio("Selecciona modo de cartoonización:", ["Con color", "Solo sketch"])
        ksize = st.slider("Tamaño de kernel", 1, 9, 5, step=2)

        sketch_mode = True if modo == "Solo sketch" else False
        output = cartoonize_image(frame, ksize=ksize, sketch_mode=sketch_mode)

        st.image(cv2.cvtColor(output, cv2.COLOR_BGR2RGB), caption=f"Resultado: {modo}", use_container_width=True)

        st.markdown("---\n✅ **Alumna:** 🦉Zanabria Yrigoin, Gaby Lizeth")