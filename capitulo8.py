import streamlit as st
import cv2
import numpy as np
from tempfile import NamedTemporaryFile
import time

# ======================================================
# Capítulo 8 — Detección de Movimiento y Color (OpenCV)
# ======================================================
def app():
    st.title("📓 Capítulo 8 — Detección de Movimiento y Color")
    st.info("🎥 En este capítulo aprenderás a **detectar movimiento y color en video** utilizando OpenCV:\n\n"
            "- 🚶‍♂️ **Sustracción de fondo (GMG / MOG2)** para detectar objetos en movimiento.\n"
            "- 🎨 **Detección de color (HSV)** para resaltar zonas específicas.\n"
            "- 📸 **Diferencia de cuadros** para detectar cambios entre imágenes consecutivas.")

    metodo = st.selectbox("🔎 Selecciona el método a ejecutar:",
                          ["Sustracción de Fondo (GMG)",
                           "Sustracción de Fondo (MOG2)",
                           "Detección de Color (Azul)",
                           "Diferencia de Cuadros (Movimiento)"])

    fuente = st.radio("🎥 Fuente del video:", ["Cámara", "Subir archivo"])

    video_file = None
    if fuente == "Subir archivo":
        video_file = st.file_uploader("📂 Sube un video (MP4, AVI, MOV)", type=["mp4", "avi", "mov"])

    iniciar = st.button("🚀 Iniciar Detección")

    if iniciar:
        if fuente == "Cámara":
            cap = cv2.VideoCapture(0)
            ejecutar_metodo(cap, metodo)
        elif video_file:
            temp_file = NamedTemporaryFile(delete=False)
            temp_file.write(video_file.read())
            cap = cv2.VideoCapture(temp_file.name)
            ejecutar_metodo(cap, metodo)
        else:
            st.warning("⚠️ Por favor, selecciona una fuente de video antes de iniciar.")

    st.markdown("---\n✅ **Alumna:** 🦉 Zanabria Yrigoin, Gaby Lizeth")


# ======================================================
# Función principal de ejecución
# ======================================================
def ejecutar_metodo(cap, metodo):
    scaling_factor = 0.5

    stframe1 = st.empty()
    stframe2 = st.empty()

    if metodo == "Sustracción de Fondo (GMG)":
        bgSubtractor = cv2.bgsegm.createBackgroundSubtractorGMG()
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        procesar_video_streamlit(cap, metodo, lambda f: procesar_gmg(f, bgSubtractor, kernel),
                                 stframe1, stframe2, scaling_factor)

    elif metodo == "Sustracción de Fondo (MOG2)":
        bgSubtractor = cv2.createBackgroundSubtractorMOG2()
        history = 100
        procesar_video_streamlit(cap, metodo, lambda f: procesar_mog2(f, bgSubtractor, history),
                                 stframe1, stframe2, scaling_factor)

    elif metodo == "Detección de Color (Azul)":
        lower = np.array([60, 100, 100])
        upper = np.array([180, 255, 255])
        procesar_video_streamlit(cap, metodo, lambda f: procesar_color(f, lower, upper),
                                 stframe1, stframe2, scaling_factor)

    elif metodo == "Diferencia de Cuadros (Movimiento)":
        procesar_diferencia_streamlit(cap, stframe1, stframe2, scaling_factor)

    cap.release()


# ======================================================
# Procesamiento de video dentro de Streamlit
# ======================================================
def procesar_video_streamlit(cap, metodo, procesador, stframe1, stframe2, scaling_factor):
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor)
        original, resultado = procesador(frame)

        stframe1.image(cv2.cvtColor(original, cv2.COLOR_BGR2RGB),
                       caption="🎥 Cámara - " + metodo, channels="RGB", use_container_width=True)
        stframe2.image(cv2.cvtColor(resultado, cv2.COLOR_BGR2RGB),
                       caption="🔍 Resultado - " + metodo, channels="RGB", use_container_width=True)

        time.sleep(0.03)  # Control de velocidad


# ======================================================
# Métodos de procesamiento individuales
# ======================================================
def procesar_gmg(frame, bgSubtractor, kernel):
    mask = bgSubtractor.apply(frame)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    return frame, mask_rgb


def procesar_mog2(frame, bgSubtractor, history):
    mask = bgSubtractor.apply(frame, learningRate=1.0 / history)
    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    combined = cv2.bitwise_and(frame, mask_rgb)
    return frame, combined


def procesar_color(frame, lower, upper):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    res = cv2.medianBlur(res, 5)
    return frame, res


# ======================================================
# Detección de movimiento con diferencia de cuadros
# ======================================================
def procesar_diferencia_streamlit(cap, stframe1, stframe2, scaling_factor):
    prev_frame, cur_frame, next_frame = None, None, None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor)
        prev_frame = cur_frame
        cur_frame = next_frame
        next_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is not None:
            diff1 = cv2.absdiff(next_frame, cur_frame)
            diff2 = cv2.absdiff(cur_frame, prev_frame)
            motion = cv2.bitwise_and(diff1, diff2)
            motion_rgb = cv2.cvtColor(motion, cv2.COLOR_GRAY2BGR)

            stframe1.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                           caption="🎥 Cámara", channels="RGB", use_container_width=True)
            stframe2.image(cv2.cvtColor(motion_rgb, cv2.COLOR_BGR2RGB),
                           caption="📸 Movimiento Detectado", channels="RGB", use_container_width=True)

        time.sleep(0.03)
