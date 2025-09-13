# app.py — Imagen/Text/PDF/PPTX ➜ Sheet Cheat en PDF (LaTeX)
# ===========================================================

import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import subprocess
import os
import re
import tempfile
import PyPDF2
from pptx import Presentation
import unicodedata

# =================== PÁGINA ===================
st.set_page_config(
    page_title="Sheet Cheat Maker — by Mario Ibarra",
    page_icon="📘",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("📘 Imagen / Texto / PDF / PPTX ➜ Sheet Cheat en PDF (by Mario Ibarra)")
st.markdown("---")
st.markdown("**Imagen / Texto / PDF / PPTX ➜ Sheat Cheat en PDF (by Mario Ibarra)** - Desarrollado por [MarioIbago](https://github.com/MarioIbago) | Usando GPT-4 Vision API")

# ============ OPENAI SDK SHIM (v1 / legacy) ============
SDK_MODE = None
client = None
try:
    from openai import OpenAI  # SDK nuevo (>=1.0)
    SDK_MODE = "v1"
except ModuleNotFoundError:
    SDK_MODE = "legacy"
except Exception:
    SDK_MODE = "legacy"

API_KEY = st.secrets.get("OPENAI_API_KEY", "")
if not API_KEY:
    st.warning("⚠️ Falta OPENAI_API_KEY en .streamlit/secrets.toml o en Secrets de Streamlit Cloud.")

if SDK_MODE == "v1":
    try:
        from openai import OpenAI
        client = OpenAI(api_key=API_KEY)
    except Exception as e:
        st.error(f"No se pudo inicializar SDK v1 de OpenAI: {e}")
        SDK_MODE = "legacy"

if SDK_MODE == "legacy":
    try:
        import openai  # SDK antiguo (<1.0)
        openai.api_key = API_KEY
    except Exception as e:
        st.error(f"No se pudo importar SDK legacy de OpenAI: {e}")
        openai = None

# ================ PROMPT =================
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
    "6) \\section{Derivaciones mínimas}: 2–4 derivaciones cortas y limpias que muestren el origen de las fórmulas más usadas; "
    "cada derivación ≤ 6 líneas y sin pasos redundantes.\n"
    "7) \\section{Ejemplos rápidos}: 1–2 ejemplos numéricos (2–5 líneas cada uno) resolviendo con las fórmulas anteriores.\n"
    "8) \\section{Aplicaciones}: enumerate de 3–6 ítems; cada ítem inicia con \\textbf{Etiqueta:} seguido de explicación breve.\n"
    "9) \\section{Símbolos y notación} (opcional): lista compacta de variables/constantes con su significado.\n"
    "10) \\section{Resumen de fórmulas esenciales}: un tcolorbox final con 4–8 fórmulas “de oro”, cada una en display; "
    "si procede, añade una línea debajo de cada fórmula con una nota muy breve (p. ej. dominio, suposición, o uso típico).\n\n"

    "ESTILO Y CALIDAD:\n"
    "• Español claro y conciso; objetivo 1–2 páginas. "
    "• Matemáticas limpias: usa \\frac, potencias, sub/superscripts adecuados; evita adornos innecesarios. "
    "• NUNCA uses Markdown (**negritas**, _cursivas_, `código`): usa \\textbf{...} y \\emph{...} en su lugar. "
    "• No imágenes ni rutas; no comentarios LaTeX; balancea todos los entornos; debe compilar con pdflatex.\n\n"

    "ENTRADA: recibirás texto o extracto de imagen; debes destilar todas las fórmulas relevantes, explicarlas brevemente, "
    "y cerrar con un tcolorbox de fórmulas esenciales bien formateadas.\n\n"
    "MUY IMPORTANTE: usa exactamente este <tema> en \\title: 'Sheet Cheat: {tema_exacto}'. "
).replace("{tema_exacto}", "{topic_placeholder}")

# =============== UTILS ==================
def _image_to_base64(uploaded_file):
    buf = BytesIO()
    img = Image.open(uploaded_file).convert("RGB")
    img.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def extract_text_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
        return "\n".join(text).strip()
    except Exception as e:
        st.error(f"Error leyendo PDF: {e}")
        return ""

def extract_text_from_pptx(uploaded_file):
    try:
        prs = Presentation(uploaded_file)
        text = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    t = (shape.text or "").strip()
                    if t:
                        text.append(t)
        return "\n".join(text).strip()
    except Exception as e:
        st.error(f"Error leyendo PPTX: {e}")
        return ""

_TITLESec_PAT = re.compile(r'\\usepackage\\s*\\{?\\s*titlesec\\s*\\}?', re.I)
_TITLEFORMAT_PAT = re.compile(r'\\title(?:format|spacing)\\*?[^\\]*', re.I)

def sanitize_latex(content: str) -> str:
    lines = []
    for line in content.splitlines():
        s = line.strip()
        if s.startswith("```"):
            continue
        if s.startswith("% !TEX"):
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
    pre = (
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
        "\\tcbset{colback=gray!3,colframe=black!50,boxrule=0.5pt,arc=2pt}\n"
    )
    if "\\begin{document}" in latex_code:
        return latex_code
    return pre + "\n\\begin{document}\n" + latex_code + "\n\\end{document}\n"

def enforce_title(latex_code: str, topic: str) -> str:
    desired = f"\\title{{Sheet Cheat: {topic}}}"
    if re.search(r'\\title\{', latex_code):
        latex_code = re.sub(r'\\title\{.*?\}', desired, latex_code, count=1, flags=re.S)
    else:
        if "\\begin{document}" in latex_code:
            latex_code = latex_code.replace(
                "\\begin{document}",
                "\\begin{document}\n" + desired + "\n\\author{}\n\\date{}\n\\maketitle\n",
                1
            )
        else:
            latex_code = desired + "\n\\author{}\n\\date{}\n\\maketitle\n" + latex_code
    if "\\maketitle" not in latex_code:
        latex_code = latex_code.replace(desired, desired + "\n\\author{}\n\\date{}\n\\maketitle", 1)
    return latex_code

def inject_footer(latex_code: str) -> str:
    footer = (
        "\n\\vspace{1em}\n"
        "\\begin{center}\\scriptsize "
        "Desarrollado por Mario Ibarra — \\url{https://github.com/MarioIbago}"
        "\\end{center}\n"
    )
    if "\\end{document}" in latex_code:
        return latex_code.replace("\\end{document}", footer + "\\end{document}")
    return latex_code + footer

def _slugify(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^a-zA-Z0-9_-]+', '_', text).strip('_')
    return (text or "Tema").lower()

# ============== OPENAI CALL =================
def call_openai(prompt, notes_text=None, image_b64=None, topic="Tema"):
    if not API_KEY:
        st.error("No hay API key configurada.")
        return ""
    prompt_final = prompt.replace("{topic_placeholder}", topic.strip() or "Tema")
    try:
        if SDK_MODE == "v1" and client is not None:
            if image_b64:
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    max_tokens=3000,
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_final + "\n\nTexto de entrada: (extraído de imagen)"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                        ]
                    }]
                )
            else:
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    max_tokens=3000,
                    messages=[{"role": "user", "content": prompt_final + f"\n\nTexto de entrada:\n{notes_text or ''}"}]
                )
            content = (resp.choices[0].message.content or "").strip()
        else:
            if 'openai' not in globals() or openai is None:
                st.error("No se pudo inicializar OpenAI (SDK legacy).")
                return ""
            if image_b64:
                resp = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    max_tokens=3000,
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_final + "\n\nTexto de entrada: (extraído de imagen)"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                        ]
                    }]
                )
            else:
                resp = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    max_tokens=3000,
                    messages=[{"role": "user", "content": prompt_final + f"\n\nTexto de entrada:\n{notes_text or ''}"}]
                )
            content = (resp["choices"][0]["message"]["content"] or "").strip()
    except Exception as e:
        st.error(f"Error al llamar a OpenAI: {e}")
        return ""

    content = sanitize_latex(content)
    content = ensure_full_document(content)
    content = enforce_title(content, topic.strip() or "Tema")
    content = inject_footer(content)
    return content

def compile_pdf_bytes(latex_code: str):
    if not latex_code.strip():
        st.error("No hay código LaTeX para compilar.")
        return None
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tex_path = os.path.join(tmpdir, "cheat_sheat.tex")
            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(latex_code)
            for _ in range(2):
                result = subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "cheat_sheat.tex"],
                    cwd=tmpdir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                if result.returncode != 0:
                    logtxt = ""
                    log_path = os.path.join(tmpdir, "cheat_sheat.log")
                    if os.path.exists(log_path):
                        with open(log_path, "r", encoding="utf-8", errors="ignore") as logf:
                            logtxt = logf.read()
                    else:
                        logtxt = result.stdout.decode(errors="ignore") + "\n" + result.stderr.decode(errors="ignore")
                    st.text_area("❌ Error en LaTeX (log)", logtxt, height=360)
                    return None
            pdf_path = os.path.join(tmpdir, "cheat_sheat.pdf")
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as fpdf:
                    return fpdf.read()
            st.error("❌ No se encontró el PDF tras compilar.")
            return None
    except FileNotFoundError:
        st.info("ℹ️ No se encontró `pdflatex` en el sistema. Descarga el .tex o instala TeX Live para compilar.")
        return None

# ============== UI ==================
topic = st.text_input("🧾 Tema del cheat sheet", value="Tema")
compile_pdf_toggle = st.checkbox("Compilar PDF con pdflatex (requiere TeX Live instalado)", value=False)

mode = st.radio("Entrada:", ["Subir imagen", "Escribir texto", "Subir PDF", "Subir PPTX"], horizontal=True)
notes_text = ""
image_b64 = None

if mode == "Subir imagen":
    up = st.file_uploader("📤 Sube una imagen (JPG/PNG)", type=["jpg","jpeg","png"])
    if up is not None:
        st.image(up, caption="Imagen cargada", width=300)
        image_b64 = _image_to_base64(up)
elif mode == "Escribir texto":
    notes_text = st.text_area("✍️ Escribe o pega tus notas", height=220)
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

if st.button("⚡ Generar Sheet Cheat", type="primary", use_container_width=True):
    if not API_KEY:
        st.stop()
    st.info("⏳ Generando LaTeX con GPT...")
    if image_b64:
        latex_code = call_openai(PROMPT_CHEATSHEET, image_b64=image_b64, topic=topic)
    else:
        latex_code = call_openai(PROMPT_CHEATSHEET, notes_text=notes_text, topic=topic)

    if not latex_code:
        st.error("No se obtuvo contenido de LaTeX.")
        st.stop()

    st.subheader("📄 Código LaTeX completo")
    st.code(latex_code, language="latex")

    slug = _slugify(topic)
    st.download_button(
        "📥 Descargar .tex",
        data=latex_code.encode("utf-8"),
        file_name=f"cheat_sheat_{slug}.tex",
        mime="text/plain",
        use_container_width=True
    )

    if compile_pdf_toggle:
        st.info("🛠️ Compilando con pdfLaTeX...")
        pdf_bytes = compile_pdf_bytes(latex_code)
        if pdf_bytes:
            st.success("✅ PDF generado correctamente.")
            st.download_button(
                "📥 Descargar PDF",
                data=pdf_bytes,
                file_name=f"cheat_sheat_{slug}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.warning("No se generó el PDF. Puedes descargar el .tex y compilar localmente con TeX Live.")

            st.warning("No se generó el PDF. Puedes descargar el .tex y compilar localmente con TeX Live.")
