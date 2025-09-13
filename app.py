# app.py — Imagen/Text/PDF/PPTX ➜ Sheet Cheat en PDF (LaTeX)
# ===========================================================

import streamlit as st
from openai import OpenAI
from PIL import Image
from io import BytesIO
import base64
import subprocess
import os
import re
import tempfile
import PyPDF2
from pptx import Presentation

st.set_page_config(page_title="Sheet Cheat en PDF", page_icon="📘", layout="centered")

# ------------------ CONFIG ------------------
# Clave de OpenAI: usa secrets o variable de entorno
API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY", "")
if not API_KEY:
    st.warning("⚠️ Configura tu OPENAI_API_KEY en Secrets (Streamlit) o como variable de entorno.")
client = OpenAI(api_key=API_KEY)

st.title("📘 Imagen / Texto / PDF / PPTX ➜ Sheet Cheat en PDF (by Mario Ibarra)")

# ------------------ PROMPT ------------------
PROMPT_CHEATSHEET = (
    "Actúas como un asistente experto en hojas de trucos (cheat sheets). "
    "Devuelve EXCLUSIVAMENTE un DOCUMENTO LaTeX completo y compilable. "
    "FORMATO OBLIGATORIO DE SALIDA: la PRIMERA línea debe ser exactamente 'COOR-BO-ZY'; "
    "a partir de la SEGUNDA línea comienza el documento LaTeX, SIN bloques de ``` ni texto fuera del LaTeX.\n\n"
    "PREÁMBULO (descrito, no pegues este texto): clase 'article' 11pt; español con babel; UTF-8 y T1; Latin Modern; "
    "amsmath, amssymb, mathtools; geometry A4 con ~2–2.5 cm; enumitem; xcolor; tcolorbox sobrio; microtype; hyperref; graphicx. "
    "NO uses 'titlesec' ni \\titleformat/\\titlespacing; evita TikZ y paquetes no listados; nada de \\makeatletter, \\input, \\write18.\n\n"
    "ESTRUCTURA EXACTA (con foco en FÓRMULAS y EXPLICACIONES):\n"
    "1) Portada simple: \\title{Sheet Cheat: <tema>}, \\author{}, \\date{}, \\maketitle.\n"
    "2) \\section{Introducción}: 3–5 líneas: qué es, para qué sirve, contexto breve.\n"
    "3) \\section{Definición}: un tcolorbox con la definición formal y una ecuación en display si aplica.\n"
    "4) \\section{Propiedades}: 5–8 viñetas (itemize), cada una 1–2 líneas; usa notación matemática donde sea útil.\n"
    "5) \\section{Fórmulas clave}: incluye TODAS las fórmulas detectadas + las implícitas importantes que falten. "
    "Usa equation* o align*; agrupa por subbloques comentados si ayuda a la legibilidad.\n"
    "6) \\section{Derivaciones mínimas}: 2–4 derivaciones cortas y limpias (≤6 líneas) para fórmulas usadas.\n"
    "7) \\section{Ejemplos rápidos}: 1–2 ejemplos numéricos (2–5 líneas cada uno).\n"
    "8) \\section{Aplicaciones}: enumerate de 3–6 ítems; cada ítem con \\textbf{Etiqueta:} + explicación breve.\n"
    "9) \\section{Símbolos y notación} (opcional): lista compacta de variables.\n"
    "10) \\section{Resumen de fórmulas esenciales}: tcolorbox final con 4–8 fórmulas en display; bajo cada una, nota breve.\n\n"
    "ESTILO Y CALIDAD:\n"
    "• Español claro y conciso; objetivo 1–2 páginas. "
    "• Al final, pie de página en LaTeX: Desarrollado por [MarioIbago](https://github.com/MarioIbago). "
    "• Matemáticas limpias: \\frac, potencias, sub/superscripts; sin adornos innecesarios. "
    "• NUNCA uses Markdown (**negritas**, _cursivas_, `código`): usa \\textbf{...} y \\emph{...}. "
    "• No imágenes; sin comentarios; balancea entornos; compila con pdflatex.\n\n"
    "ENTRADA: recibe texto o extracto de imagen; destila fórmulas relevantes, explícalas brevemente y cierra con el tcolorbox."
)

# ------------------ UTILS -------------------
_TITLESec_PAT = re.compile(r'\\usepackage\\s*\\{?\\s*titlesec\\s*\\}?', re.I)
_TITLEFORMAT_PAT = re.compile(r'\\title(?:format|spacing)\\*?[^\\n]*', re.I)

def _image_to_base64(uploaded_file):
    buf = BytesIO()
    img = Image.open(uploaded_file).convert("RGB")
    img.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def extract_text_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        parts = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                parts.append(page_text)
        return "\n".join(parts).strip()
    except Exception as e:
        st.error(f"Error leyendo PDF: {e}")
        return ""

def extract_text_from_pptx(uploaded_file):
    try:
        prs = Presentation(uploaded_file)
        parts = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    t = (shape.text or "").strip()
                    if t:
                        parts.append(t)
        return "\n".join(parts).strip()
    except Exception as e:
        st.error(f"Error leyendo PPTX: {e}")
        return ""

def sanitize_latex(content: str) -> str:
    # elimina fences, metadatos y paquetes prohibidos
    lines = []
    for line in content.splitlines():
        s = line.strip()
        if s.startswith("```") or s.startswith("% !TEX"):
            continue
        lines.append(line)
    txt = "\n".join(lines)
    txt = txt.replace("\\r\\n", "\n").replace("\\n", "\n").replace("\r\n", "\n")
    txt = txt.replace("\ufeff", "").strip()
    if txt.startswith("COOR-BO-ZY"):
        txt = txt.split("\n", 1)[-1] if "\n" in txt else ""
    txt = _TITLESec_PAT.sub("", txt)
    txt = _TITLEFORMAT_PAT.sub("", txt)
    return txt.strip()

def ensure_full_document(latex_code: str) -> str:
    if "\\begin{document}" in latex_code:
        return latex_code
    wrapper = (
        "\\documentclass[11pt]{article}\n"
        "\\usepackage[spanish, es-tabla]{babel}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage[T1]{fontenc}\n"
        "\\usepackage{lmodern}\n"
        "\\usepackage{amsmath,amssymb,amsthm,mathtools}\n"
        "\\usepackage[a4paper,margin=2.0cm]{geometry}\n"
        "\\usepackage{enumitem}\n"
        "\\usepackage{xcolor}\n"
        "\\usepackage{tcolorbox}\n"
        "\\usepackage{graphicx}\n"
        "\\usepackage{hyperref}\n"
        "\\usepackage{microtype}\n"
        "\\tcbset{colback=gray!3,colframe=black!50,boxrule=0.5pt,arc=2pt}\n\n"
        "\\begin{document}\n" + latex_code + "\n\\end{document}\n"
    )
    return wrapper

def call_openai(prompt, notes_text=None, image_b64=None):
    if not API_KEY:
        st.error("No hay API key configurada.")
        return ""
    try:
        if image_b64:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=3000,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt + "\n\nTexto de entrada: (extraído de imagen)"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                    ]
                }]
            )
        else:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt + f"\n\nTexto de entrada:\n{notes_text or ''}"}]
            )
        content = (resp.choices[0].message.content or "").strip()
    except Exception as e:
        st.error(f"Error al llamar a OpenAI: {e}")
        return ""

    content = sanitize_latex(content)
    content = ensure_full_document(content)
    return content

def compile_pdf(latex_code: str):
    if not latex_code.strip():
        st.error("No hay código LaTeX para compilar.")
        return None

    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "sheat_cheat.tex")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(latex_code)

        # doble pasada por referencias/índices
        for _ in range(2):
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "sheat_cheat.tex"],
                cwd=tmpdir,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            if result.returncode != 0:
                log_path = os.path.join(tmpdir, "sheat_cheat.log")
                stdout = result.stdout.decode(errors="ignore")
                stderr = result.stderr.decode(errors="ignore")
                logtxt = ""
                if os.path.exists(log_path):
                    with open(log_path, "r", encoding="utf-8", errors="ignore") as logf:
                        logtxt = logf.read()
                st.text_area("❌ Error en LaTeX (log)", logtxt or stdout or stderr, height=360)
                return None

        pdf_path = os.path.join(tmpdir, "sheat_cheat.pdf")
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as fpdf:
                return fpdf.read()
        st.error("❌ No se encontró el PDF tras compilar.")
        return None

# ------------------ INTERFAZ ------------------
mode = st.radio("Entrada:", ["Subir imagen", "Escribir texto", "Subir PDF", "Subir PPTX"], horizontal=True)
notes_text = ""
image_b64 = None

if mode == "Subir imagen":
    up = st.file_uploader("📤 Sube una imagen (JPG/PNG)", type=["jpg","jpeg","png"])
    if up is not None:
        st.image(up, caption="Imagen cargada", width=300)
        image_b64 = _image_to_base64(up)

elif mode == "Escribir texto":
    notes_text = st.text_area("✍️ Escribe o pega tus notas", height=220, placeholder="Tema o contenido...")

elif mode == "Subir PDF":
    up = st.file_uploader("📤 Sube un PDF", type=["pdf"])
    if up is not None:
        notes_text = extract_text_from_pdf(up)
        st.text_area("📄 Texto extraído del PDF", notes_text, height=220)

elif mode == "Subir PPTX":
    up = st.file_uploader("📤 Sube un PPTX", type=["pptx"])
    if up is not None:
        notes_text = extract_text_from_pptx(up)
        st.text_area("📊 Texto extraído del PPTX", notes_text, height=220)

if st.button("⚡ Generar Sheet Cheat"):
    st.info("⏳ Generando LaTeX con GPT...")
    latex_code = call_openai(PROMPT_CHEATSHEET, notes_text=notes_text, image_b64=image_b64)

    if not latex_code:
        st.error("No se obtuvo contenido de LaTeX.")
        st.stop()

    st.subheader("📄 Código LaTeX completo")
    st.code(latex_code, language="latex")

    st.download_button(
        "📥 Descargar .tex",
        data=latex_code.encode("utf-8"),
        file_name="sheat_cheat.tex",
        mime="text/plain"
    )

    st.info("🛠️ Compilando con pdfLaTeX...")
    pdf_bytes = compile_pdf(latex_code)
    if pdf_bytes:
        st.success("✅ PDF generado correctamente.")
        st.download_button(
            "📥 Descargar PDF",
            data=pdf_bytes,
            file_name="sheat_cheat.pdf",
            mime="application/pdf"
        )
    else:
        st.error("❌ Falló la compilación del PDF. Revisa el LaTeX o el log mostrado.")
