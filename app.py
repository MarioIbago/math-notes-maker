# app.py — SIGMA AI · Integrales y Area bajo la Curva (IB Math AA SL)
# Ejecuta local: streamlit run app.py

from __future__ import annotations
import os, re, json, uuid, random, urllib.request, urllib.parse
from datetime import datetime
from typing import List, Dict, Optional
import streamlit as st

# =========================
# Configuracion base
# =========================
st.set_page_config(
    page_title="SIGMA AI — Math AA SL (Integrales y Area bajo la Curva)",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# Estilos mejorados con animaciones
# =========================
STYLES = """
<style>
:root {
    --ink: #1b1930;
    --muted: #6b6f82;
    --brand: #6c5ce7;
    --brand2: #a78bfa;
    --ok: #10b981;
    --warn: #f59e0b;
    --err: #ef4444;
    --panel: #ffffff;
    --bg: #f7f7fb;
}

.stApp {
    background: linear-gradient(180deg, #eef1ff 0%, #fafbff 20%, #ffffff 100%);
}

.brain-animated {
    animation: pulse 2s infinite;
    display: inline-block;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

.header {
    background: linear-gradient(135deg, var(--brand), var(--brand2));
    color: #fff;
    padding: 32px 28px 24px;
    border-radius: 24px;
    box-shadow: 0 20px 60px rgba(108, 92, 231, .3);
    position: relative;
    overflow: hidden;
}

.header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: rotate 20s linear infinite;
}

@keyframes rotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.header h1 {
    margin: 0;
    letter-spacing: .3px;
    font-size: 36px;
    position: relative;
    z-index: 2;
    font-weight: 700;
}

.header p {
    margin: .5rem 0 0;
    opacity: .93;
    position: relative;
    z-index: 2;
    font-size: 16px;
}

.card {
    background: var(--panel);
    border-radius: 20px;
    padding: 24px;
    border: 1px solid rgba(108, 92, 231, .15);
    box-shadow: 0 15px 40px rgba(20, 20, 60, .08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 20px 50px rgba(20, 20, 60, .12);
}

.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    border: 1px solid rgba(108, 92, 231, .25);
    background: linear-gradient(135deg, #fafaff, #f0f0ff);
    color: #3b2f8a;
    font-size: 13px;
    margin-right: 10px;
    margin-bottom: 6px;
    font-weight: 500;
    transition: all 0.2s ease;
}

.badge:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(108, 92, 231, .2);
}

.mode-status {
    padding: 14px 16px;
    border-radius: 16px;
    margin: 12px 0 16px;
    font-weight: 600;
    border: 2px solid;
    color: #fff;
    text-align: center;
}

.free {
    background: linear-gradient(135deg, #16a34a, #22c55e);
    border-color: #bbf7d0;
}

.lock {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    border-color: #fecaca;
}

.pwd {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    border-color: #fde68a;
}

.small {
    font-size: 13px;
    color: #4b5563;
    text-align: center;
    margin-top: 20px;
}

hr {
    border: none;
    height: 1px;
    background: rgba(108, 92, 231, .25);
    margin: 16px 0 20px;
}

.locked-list {
    font-size: 13px;
    color: #4b5563;
    margin-top: 10px;
}

.locked-list li {
    margin: 4px 0;
}

/* Formato matematico mejorado */
.prob-list {
    margin: 10px 0 10px 24px;
}

.prob-list > li {
    margin: 12px 0;
    line-height: 1.6;
}

.inciso-list {
    list-style-type: lower-alpha;
    margin: 8px 0 8px 30px;
    padding-left: 20px;
}

.inciso-list li {
    margin: 12px 0;
    line-height: 1.6;
}

.inciso-list li::marker {
    content: "(" counter(list-item, lower-alpha) ") ";
    font-weight: 600;
}

/* Soluciones con formato mejorado */
.step-list {
    list-style: none;
    padding-left: 0;
    margin: 12px 0;
}

.step-list .step {
    position: relative;
    margin: 16px 0;
    padding: 16px 14px 16px 40px;
    border-left: 4px solid #e3f2fd;
    background: linear-gradient(135deg, #f8fbff, #ffffff);
    border-radius: 12px;
    line-height: 1.7;
    box-shadow: 0 2px 8px rgba(13, 71, 161, .08);
}

.step-list .step::before {
    content: "▶";
    position: absolute;
    left: 12px;
    top: 16px;
    font-weight: 700;
    color: #0d47a1;
    font-size: 14px;
}

/* Mejoras para ecuaciones */
.MathJax {
    margin: 12px 0 !important;
}

.MathJax_Display {
    background: rgba(108, 92, 231, .03) !important;
    padding: 8px 0 !important;
    border-radius: 8px !important;
    margin: 16px 0 !important;
}

/* Footer mejorado */
.footer-brain {
    animation: spin 3s linear infinite;
    display: inline-block;
    margin-right: 8px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Stats panel */
.stats-panel {
    background: linear-gradient(135deg, #f0f9ff, #ffffff);
    border: 1px solid #bae6fd;
    border-radius: 12px;
    padding: 12px;
    margin: 10px 0;
}

.stats-item {
    display: flex;
    justify-content: space-between;
    margin: 6px 0;
    font-size: 13px;
}

.stats-label {
    color: #374151;
    font-weight: 500;
}

.stats-value {
    color: #1e40af;
    font-weight: 600;
}

/* Boton mejorado */
.stButton > button {
    background: linear-gradient(135deg, var(--brand), var(--brand2)) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(108, 92, 231, .3) !important;
}

/* Status tracking */
.tracking-status {
    position: fixed;
    top: 10px;
    right: 10px;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 500;
    z-index: 1000;
    opacity: 0.8;
    transition: opacity 0.3s ease;
}

.tracking-success {
    background: #10b981;
    color: white;
}

.tracking-error {
    background: #ef4444;
    color: white;
}

.tracking-loading {
    background: #f59e0b;
    color: white;
}
</style>
"""

st.markdown(STYLES, unsafe_allow_html=True)

# =========================
# Sesion / paths / tracking
# =========================
SESS_DATE = datetime.now().strftime("%Y-%m-%d")
SESSION_ID = f"S{datetime.now().strftime('%H%M%S')}-{uuid.uuid4().hex[:6]}"
DEFAULT_LOCAL_ROOT = "./exam_output"

def _slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9aeiouñü]+", "_", (s or "").strip().lower())
    return re.sub(r"_+", "_", s).strip("_") or "sin_nombre"

def _new_run_code() -> str:
    return datetime.now().strftime("%H%M%S") + "-" + uuid.uuid4().hex[:4]

def _save_text(path: str, text: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def _track_usage(student: str, n_problems: int, seed: int, topics: List[str], model: str, success: bool):
    """Envia datos de uso al Google Sheet usando webhook"""
    # Obtener webhook URL desde secrets/env
    webhook_url = safe_secret("GOOGLE_WEBHOOK_URL", "")
    
    if not webhook_url:
        print("⚠️ GOOGLE_WEBHOOK_URL no configurada - tracking deshabilitado")
        return
    
    try:
        # Mostrar status de envío
        status_placeholder = st.empty()
        status_placeholder.markdown(
            '<div class="tracking-status tracking-loading">📊 Enviando datos...</div>',
            unsafe_allow_html=True
        )
        
        # Datos a enviar
        data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'session_id': SESSION_ID,
            'student_name': student,
            'n_problems': str(n_problems),
            'seed': str(seed),
            'topics_used': "; ".join(topics[:3]) if topics else "Sin temas",
            'model_used': model,
            'success': "YES" if success else "NO",
            'app_version': 'SIGMA-AI-v2.1'
        }
        
        # Codificar datos
        post_data = urllib.parse.urlencode(data).encode('utf-8')
        
        # Crear request
        req = urllib.request.Request(
            webhook_url,
            data=post_data,
            method='POST',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'SIGMA-AI-StreamlitApp/2.1',
                'Accept': 'text/plain'
            }
        )
        
        # Enviar datos con timeout
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                response_text = response.read().decode('utf-8')
                
                if 'SUCCESS' in response_text:
                    print(f"✅ Tracking enviado exitosamente: {response_text}")
                    status_placeholder.markdown(
                        '<div class="tracking-status tracking-success">✅ Datos enviados</div>',
                        unsafe_allow_html=True
                    )
                    # Limpiar status después de 3 segundos
                    import time
                    time.sleep(3)
                    status_placeholder.empty()
                else:
                    print(f"⚠️ Respuesta inesperada del webhook: {response_text}")
                    status_placeholder.markdown(
                        '<div class="tracking-status tracking-error">⚠️ Respuesta inesperada</div>',
                        unsafe_allow_html=True
                    )
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else f"HTTP {e.code}"
            print(f"❌ Error HTTP {e.code}: {error_body}")
            status_placeholder.markdown(
                '<div class="tracking-status tracking-error">❌ Error HTTP</div>',
                unsafe_allow_html=True
            )
            
        except urllib.error.URLError as e:
            print(f"❌ Error de conexión: {e.reason}")
            status_placeholder.markdown(
                '<div class="tracking-status tracking-error">❌ Sin conexión</div>',
                unsafe_allow_html=True
            )
            
        except Exception as e:
            print(f"❌ Error de request: {str(e)}")
            status_placeholder.markdown(
                '<div class="tracking-status tracking-error">❌ Error envío</div>',
                unsafe_allow_html=True
            )
            
    except Exception as e:
        print(f"❌ Error inesperado en tracking: {str(e)}")
        # Fallo silencioso para no interrumpir la app
        pass

def _test_webhook():
    """Función de prueba para verificar conectividad con Google Sheets"""
    webhook_url = safe_secret("GOOGLE_WEBHOOK_URL", "")
    
    if not webhook_url:
        st.error("❌ GOOGLE_WEBHOOK_URL no configurada en secrets")
        return False
    
    try:
        # Datos de prueba
        test_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'session_id': f'TEST-{uuid.uuid4().hex[:6]}',
            'student_name': 'Test Student',
            'n_problems': '1',
            'seed': '2025',
            'topics_used': 'Test Topic',
            'model_used': 'test-model',
            'success': 'YES',
            'app_version': 'SIGMA-AI-TEST'
        }
        
        post_data = urllib.parse.urlencode(test_data).encode('utf-8')
        
        req = urllib.request.Request(
            webhook_url,
            data=post_data,
            method='POST',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'SIGMA-AI-Test/1.0'
            }
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            response_text = response.read().decode('utf-8')
            if 'SUCCESS' in response_text:
                st.success(f"✅ Webhook funcionando correctamente: {response_text}")
                return True
            else:
                st.warning(f"⚠️ Respuesta inesperada: {response_text}")
                return False
                
    except Exception as e:
        st.error(f"❌ Error en test webhook: {str(e)}")
        return False

# =========================
# Lectura segura de secretos/env
# =========================
def safe_secret(key: str, default: str = "") -> str:
    possible_paths = ["/root/.streamlit/secrets.toml", "/content/.streamlit/secrets.toml", ".streamlit/secrets.toml"]
    has_secrets = any(os.path.exists(p) for p in possible_paths)
    if has_secrets:
        try:
            return st.secrets.get(key, default)
        except Exception:
            pass
    return os.environ.get(key, default)

OPENAI_API_KEY = safe_secret("OPENAI_API_KEY", "")
UNLOCK_PASSWORD = safe_secret("UNLOCK_PASSWORD", "")
OPENAI_MODEL = safe_secret("OPENAI_MODEL", "gpt-4o-mini")
GOOGLE_WEBHOOK_URL = safe_secret("GOOGLE_WEBHOOK_URL", "")

# =========================
# Cabecera mejorada
# =========================
st.markdown(
    """<div class='header'>
    <h1><span class='brain-animated'>🧠</span> SIGMA AI — Integrales y Area bajo la Curva</h1>
    <p>Generador IB Math AA SL con rigor formal, valores exactos y conexion logica entre incisos.</p>
    </div>""",
    unsafe_allow_html=True
)

# =========================
# Utilidades de render / LLM
# =========================
def mathjax_shell(body_html: str) -> str:
    return f"""
    <div class='card'>
        <div id="content">{body_html}</div>
    </div>
    <script>
    window.MathJax = {{
        tex: {{
            inlineMath: [['$', '$'], ['\\\\(', '\\\\)']]
        }},
        svg: {{
            fontCache: 'global'
        }}
    }};
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
    """

def _latex_list_to_html_items(inner: str) -> List[str]:
    parts = re.split(r"\\item(?:\s*\[[^\]]*\])?\s*", inner)
    return [p.strip() for p in parts if p.strip()]

def html_from_latex_body(body: str) -> str:
    """
    Convierte fragmentos LaTeX comunes a HTML simple:
    - Secciones, \\textbf, \\emph
    - enumerate/itemize (con tolerancia a opciones [..])
    - Enumerate #1 => lista de problemas; enumerate anidados => incisos (a)(b)(c) con espacio
    - itemize => pasos tipo viñetas
    """
    s = body.replace("\r\n", "\n")
    s = re.sub(r"\\section\*?\{([^}]*)\}", r"<h3>\1</h3>", s)
    s = re.sub(r"\\textbf\{([^}]*)\}", r"<strong>\1</strong>", s)
    s = re.sub(r"\\emph\{([^}]*)\}", r"<em>\1</em>", s)

    # itemize con opciones -> ul.steps
    def _item(m: re.Match) -> str:
        inner = m.group(1)
        items = _latex_list_to_html_items(inner)
        return "<ul class='step-list'>" + "".join(f"<li class='step'>{it}</li>" for it in items) + "</ul>"

    s = re.sub(r"\\begin\{itemize\*?\}(?:\[[^\]]*\])?(.*?)\\end\{itemize\*?\}", _item, s, flags=re.S)

    # enumerate con control de profundidad: 1º -> problemas; resto -> incisos (a)(b)...
    enum_seen = {"count": 0}

    def _enum(m: re.Match) -> str:
        enum_seen["count"] += 1
        inner = m.group(1)
        items = _latex_list_to_html_items(inner)
        lis = "".join(f"<li>{it}</li>" for it in items)
        if enum_seen["count"] == 1:
            return f"<ol class='prob-list'>{lis}</ol>"
        return f"<ol class='inciso-list' type='a'>{lis}</ol>"

    s = re.sub(r"\\begin\{enumerate\*?\}(?:\[[^\]]*\])?(.*?)\\end\{enumerate\*?\}", _enum, s, flags=re.S)

    # Limpieza de restos (fallback)
    s = re.sub(r"\\begin\{enumerate\*?\}(?:\[[^\]]*\])?", "", s)
    s = re.sub(r"\\end\{enumerate\*?\}", "", s)
    s = re.sub(r"\\item(?:\s*\[[^\]]*\])?\s*", "<br>• ", s)

    return s

def isolate_display_math(body: str) -> str:
    body = re.sub(r"([^\n$])\s*\$\$", r"\1\n$$", body)
    body = re.sub(r"\$\$\s*([^\n$])", r"$$\n\1", body)
    return re.sub(r"\$\$(.*?)\$\$", lambda m: "\n$$ " + m.group(1).strip() + " $$\n", body, flags=re.S)

def ensure_dx(latex: str) -> str:
    pat = r"(\\int(?:_\\{[^}]*\\}\\s*\\^\\{[^}]*\\})?\\s*[^$\n]*?)(?=(\$\$|\$|\n))"

    def has_dx(s: str) -> bool:
        return re.search(r"(\\,\\s*)?d\\s*x\\b", s) is not None

    def repl(m):
        core, end = m.group(1), m.group(2)
        return core + end if has_dx(core) else core.rstrip() + r" \,dx" + end

    try:
        return re.sub(pat, repl, latex)
    except Exception:
        return latex

def http_post_chat(payload: dict) -> str:
    if not OPENAI_API_KEY:
        return ""
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return (data["choices"][0]["message"]["content"] or "").strip()

def build_full_html(student: str, inner_html: str) -> str:
    ts = datetime.now().strftime("%d/%m/%Y %H:%M")
    return f"""<!doctype html>
<html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Alumno: {student}</title>
{STYLES}
<script>
window.MathJax={{
    tex:{{
        inlineMath:[['$','$'],['\\\\(','\\\\)']]
    }},
    svg:{{
        fontCache:'global'
    }}
}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>
<div class="card"><div id="content">{inner_html}</div></div>
<div class="small">Generado: {ts} · Sesion: {SESSION_ID}</div>
</body></html>"""

# =========================
# Mega-prompt IB Integrales
# =========================
IB_VERBS = (
    "A partir de lo anterior; Calcule; Comente; Compare; Compare y contraste; Contraste; Deduzca; Demuestre; Derive; "
    "Describa; Determine; Dibuje aproximadamente; Dibuje con precision; Distinga; Elabore; Enumere; Escriba; Estime; "
    "Explique; Halle; Identifique; Indique; Integre; Interprete; Investigue; Justifique; Muestre; Muestre que; Prediga; "
    "Pruebe; Resuelva; Rotule; Situe; Sugiera; Verifique."
)

CUADERNILLO = r"""
% ===== Cuadernillo IB — Integrales y Area bajo la curva =====
\textbf{Potencia: } \int x^n\,dx=\dfrac{x^{n+1}}{n+1}+C\ (n\neq -1),\quad 
\textbf{Log: } \int \frac{1}{x}\,dx=\ln|x|+C,\quad 
\textbf{Exp: } \int e^{kx}\,dx=\frac{1}{k}e^{kx}+C.

\textbf{Trig: } \int \sin x\,dx=-\cos x+C,\ \int \cos x\,dx=\sin x+C.

\textbf{Racionales: } division exacta de polinomios y fracciones simples cuando proceda.

\textbf{Sustitucion: } u=g(x)\Rightarrow \int f(g)g'\,dx=\int f(u)\,du.

\textbf{TFC: } \int_a^b f(x)\,dx=F(b)-F(a),\ F'=f.

\textbf{Areas: } \int_a^b f(x)\,dx\ (f\ge 0),\ \int_a^b |f(x)|\,dx,\ \int_a^b |f-g|\,dx.

\textbf{Valores exactos: } \sin\frac{\pi}{6}=\frac{1}{2},\ \sin\frac{\pi}{4}=\frac{\sqrt{2}}{2},\ \sin\frac{\pi}{3}=\frac{\sqrt{3}}{2};\ \cos\frac{\pi}{6}=\frac{\sqrt{3}}{2},\ \cos\frac{\pi}{4}=\frac{\sqrt{2}}{2},\ \cos\frac{\pi}{3}=\frac{1}{2}.
"""

PROMPT_SISTEMA = f"""
Eres un generador academico experto en IB Mathematics: Analysis & Approaches SL, especializado EXCLUSIVAMENTE en INTEGRALES y AREA BAJO LA CURVA. Produce problemas con rigor extremo, notacion impecable y conexion logica.

REQUISITOS GLOBALES
1) Solo matematica pura (sin fisica).
2) Valores exactos (fracciones, raices, pi, ln(2), etc.).
3) Sin integracion por partes.
4) 6–7 incisos por problema (a–g), de basico a avanzado.
5) Cada inciso reutiliza resultados previos.
6) Cada inciso inicia con un termino IB. Lista: {IB_VERBS}
7) Selecciona al azar 2–3 conceptos permitidos por problema.
8) Toda integral debe escribir el diferencial dx.
9) En integrales definidas, evalua F(b)−F(a) con limites exactos y ordenados.

Conceptos: racionales (con division exacta y asintotas), inversas de inyectivas (lineales, racionales, cuadraticas restringidas), a trozos (polinomios/raices), sustitucion u y completar cuadrados, compuestas (regla de la cadena), area absoluta |f| con cambios de signo, area entre curvas y con tangente/normal, TFC y cambios de limites, optimizacion de areas, conexion con limites de Riemann cuando aplique.

Cuadernillo de referencia:
{CUADERNILLO}

FORMATO CRITICO - SOLUCIONES:
• En "Soluciones": por problema, 8–14 vinetas MUY DETALLADAS
• CADA vineta tiene formato OBLIGATORIO:
  - Parrafo explicativo EXTENSO (4-8 frases completas con pasos detallados)
  - NUEVA LINEA vacia 
  - UNA sola ecuacion centrada en $$...$$
  - OTRA linea vacia antes de siguiente vineta
  
Ejemplo formato vineta correcta:
Para el inciso (a): Comenzamos identificando que se trata de una funcion racional donde debemos encontrar las asintotas. Una asintota vertical ocurre cuando el denominador se hace cero pero el numerador no. Evaluamos el denominador x-1=0, lo que nos da x=1. Verificamos que el numerador en x=1 es 1+1=2≠0, confirmando la asintota vertical. Para la asintota horizontal, calculamos el limite cuando x tiende a infinito dividiendo numerador y denominador por la mayor potencia de x.

$$ECUACION_ASINTOTAS_AQUI$$

Para el inciso (b): Para encontrar los ceros de una funcion racional, establecemos que el numerador debe ser igual a cero mientras el denominador sea diferente de cero. Resolvemos la ecuacion x+1=0, obteniendo x=-1. Verificamos que cuando x=-1, el denominador es -1-1=-2≠0, por lo que este punto esta en el dominio. Por tanto, x=-1 es el unico cero de la funcion.

$$ECUACION_CEROS_AQUI$$

• CADA inciso debe explicarse paso a paso con maximo detalle
• Sin mezclar texto y $$ en una misma linea. Sin align/cases/tabular.
• Prohibido decimales de aproximacion.  
• Verificacion conceptual breve al final de cada problema.
"""

def build_user_prompt(student: str, n_problemas: int) -> str:
    catalogo = [
        "Funciones racionales con asintotas y division exacta",
        "Funciones inversas de inyectivas (lineales, racionales, cuadraticas restringidas)",
        "Funciones a trozos con polinomios y raices",
        "Sustitucion u; completar cuadrados; raices cuadradas",
        "Compuestas con regla de la cadena (sin partes)",
        "Area absoluta |f(x)| con cambios de signo",
        "Area entre curvas; funcion y tangente/normal",
        "Teorema Fundamental del Calculo; cambio de limites",
        "Optimizacion de areas con integrales",
        "Conexion con limites (Riemann) cuando aplique"
    ]
    
    sel = ", ".join(random.sample(catalogo, k=3))
    
    items = []
    for k in range(1, n_problemas+1):
        items.append(f"\\item [Problema {k} con 6–7 incisos a–g, encadenados, exactos, dx obligatorio]")
    
    enumeracion = "\n".join(items)
    
    plantilla = f"""
ENTREGA SOLO el cuerpo LaTeX (sin preambulo). 
Numero de problemas: {n_problemas}.
Alumno: {student}.
Temas elegidos al azar: {sel}.

Estructura exacta:

\\section*{{Problemas para {student}}}

\\begin{{enumerate}}
{enumeracion}
\\end{{enumerate}}

\\section*{{Soluciones}}

\\begin{{enumerate}}
\\item Problema 1:
\\begin{{itemize}}
[8–14 vinetas: PARRAFO explicativo (4-8 frases) + LINEA VACIA + ecuacion centrada en $...$ + LINEA VACIA; sin partes; exacto; TFC; areas con signo]
\\end{{itemize}}
\\end{{enumerate}}
"""
    
    return plantilla.strip()

# =========================
# Sidebar · Modos / Contrasena
# =========================
st.sidebar.title("🧠 Configuracion")

# Parametros de generacion - ARRIBA
student = st.sidebar.text_input("Alumno", placeholder="Nombre del estudiante")
n_problemas = st.sidebar.slider("Numero de problemas", 1, 3, 1)  
seed = st.sidebar.number_input("Semilla aleatoria", value=2025, step=1)

st.sidebar.markdown("<hr/>", unsafe_allow_html=True)

# Stats tracking simple
if 'generation_count' not in st.session_state:
    st.session_state.generation_count = 0
if 'unique_students' not in st.session_state:
    st.session_state.unique_students = set()

# Mostrar stats y webhook status
webhook_status = "✅ Configurado" if GOOGLE_WEBHOOK_URL else "⚠️ No configurado"
st.sidebar.markdown(
    f"""<div class='stats-panel'>
    <div class='stats-item'>
        <span class='stats-label'>Sesion ID:</span>
        <span class='stats-value'>{SESSION_ID}</span>
    </div>
    <div class='stats-item'>
        <span class='stats-label'>Generaciones:</span>
        <span class='stats-value'>{st.session_state.generation_count}</span>
    </div>
    <div class='stats-item'>
        <span class='stats-label'>Estudiantes unicos:</span>
        <span class='stats-value'>{len(st.session_state.unique_students)}</span>
    </div>
    <div class='stats-item'>
        <span class='stats-label'>Webhook:</span>
        <span class='stats-value'>{webhook_status}</span>
    </div>
    </div>""",
    unsafe_allow_html=True
)

# Botón de prueba del webhook
if st.sidebar.button("🔧 Probar Webhook", help="Envía datos de prueba al Google Sheet"):
    _test_webhook()

TOPICS_ALL = [
    "1.1 Notacion Cientifica", "1.2 Series y secuencias Aritmeticas", "1.3 Series y secuencias Geometricas", 
    "1.4 Interes Compuesto", "1.5 Exponentes y logaritmos", "1.6 Demostracion sencilla por deduccion",
    "1.7 Propiedades de las potencias y los logaritmos", "1.8 Suma de progresiones geometricas infinitas",
    "1.9 Teorema del Binomio", "2.1 Recta, pendiente, paralelas y perpendiculares",
    "2.2 Funciones, notacion, modelos e inversas", "2.3 Grafico de una funcion",
    "2.4 Caracteristicas mas importantes de un grafico", "2.5 Funciones compuestas e inversas",
    "2.6 Funcion cuadratica", "2.7 Discriminante", "2.8 Funciones racionales",
    "2.9 Funciones exponenciales y logaritmicas", "2.10 Resolucion de ecuaciones tanto grafica como analiticamente",
    "2.11 Transformaciones de funciones", "3.1 Distancia, volumen y area, angulos en 2D y 3D",
    "3.2 Triangulos rectangulos y oblicuangulos", "3.3 Aplicaciones de los triangulos, angulos de elevacion y depresion",
    "3.4 Sector Circular", "3.5 Circulo unitario, valores exactos, caso ambiguo", "3.6 Identidades",
    "3.7 Funciones trigonometricas y sus graficas", "4.1 Introduccion a Estadistica", "4.2 Datos, curva de frecuencia acumulada, caja y bigotes",
    "4.3 Medidas de tendencia central y medidas de dispersion", "4.4 Correlacion lineal, Pearson",
    "4.5 Introduccion a Probabilidad", "4.6 Representacion y el uso de formulas en probabilidad",
    "4.7 Variables y esperanza matematica", "4.8 Distribucion Binomial, media y varianza",
    "4.9 Distribucion Normal", "4.10 Ecuacion de la recta de regresion",
    "4.11 Probabilidad condicionada, sucesos independientes", "4.12 Tipificacion de la variable en una DN (z), Normal inversa",
    "5.1 Introduccion al limite y la derivada como razon de cambio", "5.2 Funciones crecientes y decrecientes",
    "5.3 Calculo diferencial y sus reglas", "5.4 Recta tangente y recta normal",
    "5.5 Calculo integral, definidas e indefinidas", "5.6 Derivadas trascendentales y regla de la cadena",
    "5.7 Segunda derivada, criterios de la 1a, 2a y 3a derivada", "5.8 Maximos y minimos, optimizacion, puntos de inflexion",
    "5.9 Cinematica", "5.10 Integral indefinida", "5.11 Area bajo la curva y area entre curvas"
]

INTEGRAL_THEMES = [
    "5.5 Calculo integral, definidas e indefinidas",
    "5.10 Integral indefinida", 
    "5.11 Area bajo la curva y area entre curvas"
]

if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

st.sidebar.markdown("<div class='mode-status free'>Modo Integrales y Area bajo la Curva — Libre</div>", unsafe_allow_html=True)

if not st.session_state.unlocked:
    st.sidebar.markdown("<div class='mode-status lock'>Temas de MAE — Bloqueados</div>", unsafe_allow_html=True)
else:
    st.sidebar.markdown("<div class='mode-status pwd'>Temas de MAE — Desbloqueados</div>", unsafe_allow_html=True)

# Seleccion de temas - ABAJO DE STATS
if not st.session_state.unlocked:
    st.sidebar.caption("Temas activos (libres):")
    topics_selected = st.sidebar.multiselect(
        "Selecciona temas de integrales",
        INTEGRAL_THEMES,
        default=["5.11 Area bajo la curva y area entre curvas"]
    )
    # Mostrar lista bloqueada (solo informativa)
    locked = [t for t in TOPICS_ALL if t not in INTEGRAL_THEMES]
    if locked:
        st.sidebar.markdown("<strong>Temas de MAE bloqueados (requiere contrasena):</strong>", unsafe_allow_html=True)
        st.sidebar.markdown("<ul class='locked-list'>" + "".join(f"<li>🔒 {t}</li>" for t in locked) + "</ul>", unsafe_allow_html=True)
else:
    topics_selected = st.sidebar.multiselect(
        "Selecciona temas (integrales libres, resto desbloqueado)",
        TOPICS_ALL,
        default=INTEGRAL_THEMES
    )

st.sidebar.markdown("<hr/>", unsafe_allow_html=True)

# Validar contrasena - AL FINAL
pwd_try = st.sidebar.text_input("Contrasena para temas de MAE", type="password")
if st.sidebar.button("Validar contrasena"):
    if UNLOCK_PASSWORD and pwd_try == UNLOCK_PASSWORD:
        st.session_state.unlocked = True
        st.sidebar.success("Temas de MAE desbloqueados en esta sesion.")
    else:
        st.sidebar.error("Contrasena incorrecta o no establecida.")

st.sidebar.caption("Las claves se leen desde Secrets/entorno. Webhook configurado via GOOGLE_WEBHOOK_URL.")

# =========================
# Generador
# =========================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Generar problemas y soluciones (IB · Integrales)")

badge_row = "<span class='badge'>Exactitud simbolica</span><span class='badge'>TFC</span><span class='badge'>Valores exactos</span><span class='badge'>|f(x)|</span>"
st.markdown(badge_row, unsafe_allow_html=True)

run_btn = st.button("Generar ahora", use_container_width=True)

if run_btn:
    # Validar entrada
    if not student.strip():
        st.warning("Por favor, ingresa el nombre del alumno.")
        st.stop()
    
    random.seed(int(seed))
    user_prompt = build_user_prompt(student=student.strip(), n_problemas=int(n_problemas))
    
    messages = [
        {"role": "system", "content": PROMPT_SISTEMA},
        {"role": "user", "content": user_prompt}
    ]
    
    payload = {
        "model": OPENAI_MODEL,
        "messages": messages,
        "temperature": 0.6,
        "max_tokens": 9000
    }

    with st.spinner("Generando…"):
        # Donde guardamos
        run_code = _new_run_code()
        stu_slug = _slugify(student)
        out_dir = os.path.join(DEFAULT_LOCAL_ROOT, SESS_DATE, SESSION_ID, stu_slug, run_code)
        os.makedirs(out_dir, exist_ok=True)

        success = False
        
        if not OPENAI_API_KEY:
            st.warning("No se encontro OPENAI_API_KEY en Secrets ni en el entorno. Se muestra una plantilla offline.")
            
            ejemplo = """\\section*{Problemas para Estudiante IB}

\\begin{enumerate}
\\item Sea f(x) = (x+1)/(x-1) para x diferente de 1.

\\begin{enumerate}
\\item Determine las asintotas de f(x).
\\item Halle los ceros de la funcion.
\\item Distinga los intervalos donde f(x) > 0 y f(x) < 0.
\\item Calcule la integral indefinida de f(x).
\\item Evalúe la integral definida en el intervalo [0, 1/2].
\\item A partir de lo anterior, determine el area entre la curva y el eje x en [-1/2, 1/2].
\\end{enumerate}
\\end{enumerate}

\\section*{Soluciones}

\\begin{enumerate}
\\item Problema 1:
\\begin{itemize}
\\item Para determinar las asintotas verticales, buscamos los valores donde el denominador se anula pero el numerador no. Cuando x = 1, el denominador es cero pero el numerador es 2, por lo que hay una asintota vertical. Para la asintota horizontal, calculamos el limite cuando x tiende a infinito dividiendo numerador y denominador por la mayor potencia de x.

$ x = 1 \\text{ asintota vertical}, \\quad y = 1 \\text{ asintota horizontal} $

\\item Para encontrar los ceros de una funcion racional, establecemos que el numerador debe ser igual a cero mientras el denominador sea diferente de cero. Resolvemos la ecuacion x+1=0, obteniendo x=-1. Verificamos que cuando x=-1, el denominador es -1-1=-2 diferente de cero, por lo que este punto esta en el dominio.

$ x + 1 = 0 \\Rightarrow x = -1 $

\\item Analizamos el signo de la funcion en cada intervalo determinado por las discontinuidades y ceros. Evaluamos el signo en puntos test de cada intervalo usando la regla de signos para funciones racionales.

$ f(x) > 0 \\text{ en intervalos } (-\\infty, -1) \\cup (1, \\infty) $

\\item Aplicamos la tecnica de division de polinomios para reescribir la funcion racional como suma de un polinomio y una fraccion simple. Realizamos la division larga de (x+1) entre (x-1).

$ \\int \\frac{x+1}{x-1} \\,dx = x + 2\\ln|x-1| + C $

\\item Aplicamos el Teorema Fundamental del Calculo usando la antiderivada encontrada y evaluamos en los limites dados. Sustituimos los limites superior e inferior en la antiderivada.

$ \\int_0^{1/2} \\frac{x+1}{x-1} \\,dx = \\frac{1}{2} - 2\\ln 2 $

\\item Como la funcion cambia de signo en el intervalo, debemos calcular el area como la suma de las areas absolutas en cada subintervalo. Identificamos los puntos donde la funcion es positiva y negativa.

$ \\text{Area total} = \\int_{-1/2}^{-1} |f(x)| \\,dx + \\int_{-1}^{1/2} |f(x)| \\,dx $
\\end{itemize}
\\end{enumerate}"""
            
            # Render
            raw = ensure_dx(isolate_display_math(ejemplo))
            inner = html_from_latex_body(raw)
            html = mathjax_shell(inner)
            st.components.v1.html(html, height=840, scrolling=True)

            # Guardar archivos
            html_doc = build_full_html(student, inner)
            html_path = os.path.join(out_dir, f"examen_{stu_slug}.html")
            tex_path = os.path.join(out_dir, f"examen_{stu_slug}.tex")
            _save_text(html_path, html_doc)
            _save_text(tex_path, ejemplo)
            
            success = False
        else:
            # LLM en vivo
            try:
                raw = http_post_chat(payload) or ""
                if raw:
                    raw = ensure_dx(isolate_display_math(raw))
                    inner = html_from_latex_body(raw)
                    html = mathjax_shell(inner)
                    st.components.v1.html(html, height=840, scrolling=True)

                    # Guardar archivos
                    html_doc = build_full_html(student, inner)
                    html_path = os.path.join(out_dir, f"examen_{stu_slug}.html")
                    tex_path = os.path.join(out_dir, f"examen_{stu_slug}.tex")
                    _save_text(html_path, html_doc)
                    _save_text(tex_path, raw)
                    
                    success = True
                else:
                    st.error("Error: Respuesta vacia del modelo de IA.")
                    success = False
            except Exception as e:
                st.error(f"Error al generar contenido: {str(e)}")
                success = False

        # Tracking de uso
        st.session_state.generation_count += 1
        st.session_state.unique_students.add(student.strip())
        
        # Enviar tracking al Google Sheet
        _track_usage(
            student=student.strip(),
            n_problems=n_problemas,
            seed=seed,
            topics=topics_selected,
            model=OPENAI_MODEL,
            success=success
        )

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Notas de uso
# =========================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Notas de uso y configuración")
st.markdown("""
- El modo **Integrales y Area bajo la Curva** está siempre disponible.
- Los demás temas están numerados y **bloqueados** salvo que ingreses la contraseña.
- Los incisos ya salen como **(a), (b), (c)** con espacio entre renglones.
- El formato matemático muestra explicaciones claras seguidas de ecuaciones centradas.
- **Tracking automático**: Los datos de uso se envían automáticamente al Google Sheet si está configurado.

### Variables de entorno necesarias:
- `OPENAI_API_KEY`: Tu clave de OpenAI
- `UNLOCK_PASSWORD`: Contraseña para desbloquear temas de MAE  
- `GOOGLE_WEBHOOK_URL`: URL del webhook de Google Apps Script
- `OPENAI_MODEL`: Modelo a usar (por defecto: gpt-4o-mini)
""")
st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Footer
# =========================
st.markdown(
    f"""<div class='small'>
    <span class='footer-brain'>🧠</span>Developed by <strong>MarioUabgo</strong> · GitHub: 
    <a href='https://github.com/MarioIbago' target='_blank'>MarioIbago</a> · 
    Sesión: {datetime.now().strftime('%Y-%m-%d %H:%M')} · ID: {SESSION_ID}
    </div>""",
    unsafe_allow_html=True
)
