import streamlit as st
import cv2
import numpy as np
from tempfile import NamedTemporaryFile

# ======================================================
# Capítulo 7 — Segmentación de Imágenes (GrabCut / Contornos / Watershed)
# ======================================================
def app():
    st.title("📗 Capítulo 7 — Segmentación de Imágenes")
    st.info("🖼️ En este capítulo aprenderás a **segmentar imágenes** utilizando "
            "distintos algoritmos clásicos de OpenCV:\n\n"
            "- ✂️ **GrabCut** para separar objetos interactivos.\n"
            "- 🔹 **Contornos** para delinear figuras.\n"
            "- 🌊 **Watershed** para dividir regiones complejas.")

    uploaded_file = st.file_uploader("📂 Sube una imagen", type=["jpg", "jpeg", "png"])
    metodo = st.selectbox("🔎 Selecciona el método de segmentación:",
                          ["GrabCut", "Contornos", "Watershed"])

    if uploaded_file is not None:
        temp_file = NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())
        temp_file.close()

        img = cv2.imread(temp_file.name)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        st.image(img_rgb, caption="📸 Imagen original", use_container_width=True)

        if metodo == "GrabCut":
            st.subheader("✂️ Selecciona el rectángulo de interés con sliders interactivos")
            x = st.slider("↔️ Posición horizontal (X)", 0, img.shape[1]-1, 10,
                        help="Mueve la esquina izquierda del rectángulo en el eje X")
            y = st.slider("↕️ Posición vertical (Y)", 0, img.shape[0]-1, 10,
                        help="Mueve la esquina superior del rectángulo en el eje Y")
            w = st.slider("📏 Ancho", 10, img.shape[1]-x, img.shape[1]//2,
                        help="Ajusta el ancho del rectángulo")
            h = st.slider("📐 Alto", 10, img.shape[0]-y, img.shape[0]//2,
                        help="Ajusta el alto del rectángulo")
            rect = (x, y, w, h)

            # Mostrar la previsualización del rectángulo
            img_preview = img_rgb.copy()
            cv2.rectangle(img_preview, (x, y), (x + w, y + h), (255, 0, 0), 2)
            st.image(img_preview, caption="📏 Rectángulo seleccionado", use_container_width=True)

        if st.button("🚀 Ejecutar Segmentación"):
            if metodo == "GrabCut":
                result = aplicar_grabcut(img, rect)
                st.image(result, caption="✂️ Resultado con GrabCut", use_container_width=True)

            elif metodo == "Contornos":
                result = aplicar_contornos(img)
                st.image(result, caption="🔹 Resultado con Contornos", use_container_width=True)

            elif metodo == "Watershed":
                result = aplicar_watershed(img)
                st.image(result, caption="🌊 Resultado con Watershed", use_container_width=True)

            st.success("✅ Segmentación completada")

    st.markdown("---\n✅ **Alumna:** 🦉 Zanabria Yrigoin, Gaby Lizeth")


# ===============================
# Funciones auxiliares
# ===============================
def aplicar_grabcut(img, rect):
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    output = img * mask2[:, :, np.newaxis]
    return cv2.cvtColor(output, cv2.COLOR_BGR2RGB)


def aplicar_contornos(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    contour_img = img.copy()
    cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)
    return cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB)


def aplicar_watershed(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=4)

    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    img_copy = img.copy()
    markers = cv2.watershed(img_copy, markers)
    img_copy[markers == -1] = [255, 0, 0]  # Bordes en rojo
    return cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
