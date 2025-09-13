# Sheet Cheat Maker — by Mario Ibarra 📘

[![Streamlit](https://img.shields.io/badge/Streamlit-1.37+-FF4B4B.svg)](#)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Genera **cheat sheets (hojas de trucos) en PDF usando LaTeX** a partir de:
- 🖼️ **Imagen (JPG/PNG)**
- 📝 **Texto libre**
- 📄 **PDF**
- 🖥️ **PPTX (PowerPoint)**

La app aprovecha la API de OpenAI para destilar **definiciones, propiedades, fórmulas clave, derivaciones mínimas, ejemplos rápidos** y un **resumen final** – todo con **matemáticas limpias** y formato LaTeX listo para compilar.

> **Crédito:** Pie de página automático en el PDF:  
> `Desarrollado por Mario Ibarra — https://github.com/MarioIbago`

---

## ✨ Características

- **Entrada flexible:** imagen / texto / PDF / PPTX.
- **LaTeX impecable:** limpia `titlesec`, fuerza `\title{Sheet Cheat: <tema>}` y añade `\maketitle`.
- **Resumen de fórmulas esenciales** en `tcolorbox`.
- **Descarga del `.tex`** siempre disponible.
- **Compilación PDF opcional** (requiere `pdflatex`/TeX Live local).
- **Tema claro** (white) por defecto.
- **API key segura** vía `st.secrets`.

---

## 📁 Estructura del proyecto

