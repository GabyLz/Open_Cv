import streamlit as st
import cv2
import numpy as np
from tempfile import NamedTemporaryFile

# ======================================================
# Capítulo 6 — Seam Carving (Eliminación de Objetos)
# ======================================================
def app():
    st.title("📒 Capítulo 6 — Seam Carving (Eliminación de Objetos)")
    st.info("✂️ En este capítulo aprenderás a **eliminar objetos de una imagen** usando "
            "el algoritmo de **Seam Carving**, que redimensiona de forma inteligente "
            "preservando las regiones más importantes.")

    # ===============================
    # Subir imagen
    # ===============================
    uploaded_file = st.file_uploader("📂 Sube una imagen", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Guardar en archivo temporal
        temp_file = NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())
        temp_file.close()

        img_input = cv2.imread(temp_file.name)

        # 🔹 Limitar tamaño máximo para evitar demoras
        max_width = 400
        if img_input.shape[1] > max_width:
            scale = max_width / img_input.shape[1]
            img_input = cv2.resize(
                img_input,
                None,
                fx=scale,
                fy=scale,
                interpolation=cv2.INTER_AREA
            )

        img_rgb = cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB)

        # Mostrar original
        st.image(img_rgb, caption="📸 Imagen original (redimensionada si era muy grande)", use_container_width=True)

        # ===============================
        # Parámetros
        # ===============================
        num_seams = st.slider("👉 Número de seams a eliminar", 10, 200, 50)

        # ===============================
        # Procesar
        # ===============================
        if st.button("🚀 Ejecutar Seam Carving"):
            img = np.copy(img_input)
            energy = compute_energy_matrix(img)
            img_overlay_seam = np.copy(img_input)

            # Proceso iterativo
            for i in range(num_seams):
                seam = find_vertical_seam(img, energy)
                img_overlay_seam = overlay_vertical_seam(img_overlay_seam, seam)
                img = remove_vertical_seam(img, seam)
                energy = compute_energy_matrix(img)

            # Mostrar resultados
            st.image(cv2.cvtColor(img_overlay_seam, cv2.COLOR_BGR2RGB),
                     caption=f"✨ Imagen con {num_seams} seams resaltados", use_container_width=True)

            st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB),
                     caption=f"🎯 Resultado final tras {num_seams} seams eliminados",
                     use_container_width=True)

            st.success("✅ Procesamiento completado")

    st.markdown("---\n✅ **Alumna:** 🦉 Zanabria Yrigoin, Gaby Lizeth")


# ===============================
# Funciones auxiliares
# ===============================
def overlay_vertical_seam(img, seam):
    img_seam_overlay = np.copy(img)
    for row in range(len(seam)):
        col = int(seam[row])
        img_seam_overlay[row, col] = (0, 255, 0)  # Verde para los seams
    return img_seam_overlay

def compute_energy_matrix(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    abs_sobel_x = cv2.convertScaleAbs(sobel_x)
    abs_sobel_y = cv2.convertScaleAbs(sobel_y)
    return cv2.addWeighted(abs_sobel_x, 0.5, abs_sobel_y, 0.5, 0)

def find_vertical_seam(img, energy):
    rows, cols = img.shape[:2]
    seam = np.zeros(rows)

    dist_to = np.zeros((rows, cols)) + float('inf')
    dist_to[0, :] = np.zeros(cols)
    edge_to = np.zeros((rows, cols))

    for row in range(rows - 1):
        for col in range(cols):
            if col != 0 and dist_to[row+1, col-1] > dist_to[row, col] + energy[row+1, col-1]:
                dist_to[row+1, col-1] = dist_to[row, col] + energy[row+1, col-1]
                edge_to[row+1, col-1] = 1

            if dist_to[row+1, col] > dist_to[row, col] + energy[row+1, col]:
                dist_to[row+1, col] = dist_to[row, col] + energy[row+1, col]
                edge_to[row+1, col] = 0

            if col != cols-1 and dist_to[row+1, col+1] > dist_to[row, col] + energy[row+1, col+1]:
                dist_to[row+1, col+1] = dist_to[row, col] + energy[row+1, col+1]
                edge_to[row+1, col+1] = -1

    seam[rows-1] = np.argmin(dist_to[rows-1, :])
    for i in (x for x in reversed(range(rows)) if x > 0):
        seam[i-1] = seam[i] + edge_to[i, int(seam[i])]
    return seam

def remove_vertical_seam(img, seam):
    rows, cols = img.shape[:2]
    for row in range(rows):
        for col in range(int(seam[row]), cols - 1):
            img[row, col] = img[row, col + 1]
    img = img[:, 0:cols - 1]
    return img
