import streamlit as st
import cv2
import numpy as np

# ======================================================
# 📘 Capítulo 9 — Clasificación de Imágenes (SIFT + Comparación)
# ======================================================

def app():
    st.title("📘 Capítulo 9 — Clasificación de Imágenes con SIFT y Comparación Directa")
    st.info("🎯 En este capítulo aprenderás a **comparar imágenes automáticamente** usando **SIFT** (Scale-Invariant Feature Transform).\n\n"
            "- 📷 Extracción de características clave\n"
            "- 🧩 Comparación entre descriptores de dos imágenes\n"
            "- 🔍 Emparejamiento visual basado en similitud\n")

    # =========================
    # Subir dos imágenes
    # =========================
    st.subheader("🖼️ Cargar imágenes a comparar")
    img1_file = st.file_uploader("Selecciona la primera imagen", type=["jpg", "jpeg", "png"])
    img2_file = st.file_uploader("Selecciona la segunda imagen", type=["jpg", "jpeg", "png"])

    if img1_file and img2_file:
        # Leer imágenes
        file_bytes1 = np.asarray(bytearray(img1_file.read()), dtype=np.uint8)
        file_bytes2 = np.asarray(bytearray(img2_file.read()), dtype=np.uint8)
        img1 = cv2.imdecode(file_bytes1, cv2.IMREAD_COLOR)
        img2 = cv2.imdecode(file_bytes2, cv2.IMREAD_COLOR)

        # Mostrar imágenes originales
        st.image([cv2.cvtColor(img1, cv2.COLOR_BGR2RGB),
                  cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)],
                 caption=["Imagen 1", "Imagen 2"],
                 use_container_width=True)

        # Botón de comparación
        if st.button("🚀 Comparar imágenes"):
            resultado, matched_img = comparar_sift(img1, img2)
            st.success(f"🔎 Coincidencias encontradas: **{resultado}**")

            st.image(cv2.cvtColor(matched_img, cv2.COLOR_BGR2RGB),
                     caption="🔗 Coincidencias encontradas (SIFT)",
                     use_container_width=True)


# ======================================================
# 🔍 Funciones de apoyo
# ======================================================

def comparar_sift(img1, img2):
    """Compara dos imágenes usando SIFT y muestra los emparejamientos."""
    sift = cv2.SIFT_create()

    # Convertir a escala de grises
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Detectar keypoints y descriptores
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)

    if des1 is None or des2 is None:
        return "No se detectaron suficientes características.", img1

    # Crear el comparador (BFMatcher)
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(des1, des2)

    # Ordenar los mejores matches
    matches = sorted(matches, key=lambda x: x.distance)
    num_matches = len(matches)

    # Dibujar coincidencias (máximo 50)
    matched_img = cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None,
                                  flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    return num_matches, matched_img