import re
from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"

st.set_page_config(
    page_title="TalentBridge AI",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main .block-container {padding-top: 1.8rem; max-width: 1200px;}
    .hero {padding: 1.4rem 1.6rem; border-radius: 18px; background: linear-gradient(120deg, #102a43, #176b73); color: white; margin-bottom: 1rem;}
    .hero h1 {color: white; margin-bottom: .25rem;}
    .hero p {color: #e8f4f4; margin-bottom: 0;}
    .small-note {font-size: .88rem; color: #64748b;}
</style>
""", unsafe_allow_html=True)

SKILL_ALIASES = {
    "excel avanzado": "Excel",
    "microsoft excel": "Excel",
    "hojas de cálculo": "Excel",
    "power bi": "Power BI",
    "business intelligence": "Power BI",
    "análisis de datos": "Análisis de datos",
    "analisis de datos": "Análisis de datos",
    "people analytics": "People Analytics",
    "analítica de personas": "People Analytics",
    "analitica de personas": "People Analytics",
    "selección": "Selección",
    "seleccion": "Selección",
    "reclutamiento": "Selección",
    "talent acquisition": "Selección",
    "comunicación": "Comunicación",
    "comunicacion": "Comunicación",
    "gestión de proyectos": "Gestión de proyectos",
    "gestion de proyectos": "Gestión de proyectos",
    "python": "Python",
    "sql": "SQL",
    "formación": "Formación y desarrollo",
    "formacion": "Formación y desarrollo",
    "desarrollo del talento": "Formación y desarrollo",
    "entrevistas": "Entrevistas",
    "entrevista por competencias": "Entrevistas",
}

CANONICAL_SKILLS = [
    "Excel", "Power BI", "Análisis de datos", "People Analytics",
    "Selección", "Comunicación", "Gestión de proyectos", "Python",
    "SQL", "Formación y desarrollo", "Entrevistas"
]

def normalize_text(value):
    return str(value).strip().lower()

def parse_skills(value):
    """Parse a semicolon-, comma- or pipe-separated skills cell."""
    if pd.isna(value):
        return []
    parts = re.split(r"[;,|]", str(value))
    found = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        low = part.lower()
        canonical = SKILL_ALIASES.get(low)
        if canonical is None:
            # Preserve unknown skills so the app does not silently discard them.
            canonical = part.strip().title()
        if canonical not in found:
            found.append(canonical)
    return found

def parse_job_requirements(job_text, manual_skills):
    """Use explicit manual selection first; otherwise match known skills in the job text."""
    selected = list(manual_skills or [])
    if selected:
        return selected
    low = normalize_text(job_text)
    detected = []
    # Longer aliases first to avoid short terms matching inside longer phrases.
    for alias, canonical in sorted(SKILL_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        if re.search(r"(?<!\w)" + re.escape(alias) + r"(?!\w)", low) and canonical not in detected:
            detected.append(canonical)
    return detected

def load_csv_or_demo(upload, demo_path):
    if upload is not None:
        try:
            return pd.read_csv(upload)
        except Exception as exc:
            st.error(f"No se ha podido leer el CSV: {exc}")
            return None
    if demo_path.exists():
        return pd.read_csv(demo_path)
    return None

def ensure_columns(df, required, label):
    if df is None:
        return False
    missing = [col for col in required if col not in df.columns]
    if missing:
        st.error(f"El archivo de {label} debe incluir estas columnas: {', '.join(required)}. Faltan: {', '.join(missing)}.")
        return False
    return True

def compare_profiles(profiles, required_skills):
    rows = []
    for _, row in profiles.iterrows():
        profile_skills = parse_skills(row.get("skills", ""))
        matched = [skill for skill in required_skills if skill in profile_skills]
        gaps = [skill for skill in required_skills if skill not in profile_skills]
        coverage = round(100 * len(matched) / len(required_skills), 1) if required_skills else 0
        rows.append({
            "ID de perfil": row.get("profile_id", "Sin ID"),
            "Perfil": row.get("title", "Sin título"),
            "Cobertura de competencias (%)": coverage,
            "Coincidencias": ", ".join(matched) if matched else "Ninguna identificada",
            "Brechas / no acreditadas": ", ".join(gaps) if gaps else "Ninguna en los criterios seleccionados",
            "Competencias declaradas": ", ".join(profile_skills),
            "Evidencias": row.get("evidence", "No facilitadas"),
        })
    return pd.DataFrame(rows).sort_values("Cobertura de competencias (%)", ascending=False)

def build_training_recommendations(gaps, courses):
    recs = []
    for skill in gaps:
        matched = courses[courses["skills"].apply(lambda value: skill in parse_skills(value))]
        if matched.empty:
            recs.append({
                "Competencia por desarrollar": skill,
                "Curso sugerido": "Pendiente de incorporar al catálogo",
                "Duración (horas)": "—",
                "Objetivo de aprendizaje": f"Definir un objetivo verificable para desarrollar {skill}.",
            })
        else:
            for _, course in matched.iterrows():
                recs.append({
                    "Competencia por desarrollar": skill,
                    "Curso sugerido": course["course_name"],
                    "Duración (horas)": course.get("hours", "—"),
                    "Objetivo de aprendizaje": course.get("objective", f"Desarrollar {skill}."),
                })
    return pd.DataFrame(recs)

with st.sidebar:
    st.title("🌉 TalentBridge AI")
    st.caption("Selección por competencias y desarrollo del talento")
    page = st.radio(
        "Navegación",
        ["Inicio", "TalentMatch", "SkillPath", "People Analytics"],
        index=0,
    )
    st.divider()
    st.caption("Versión inicial · Demo con datos sintéticos")
    st.caption("No utiliza datos personales reales ni toma decisiones automáticas de contratación.")

if page == "Inicio":
    st.markdown("""
    <div class="hero">
      <h1>TalentBridge AI</h1>
      <p>Conecta las necesidades de talento con las competencias y las oportunidades de desarrollo.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("Esta aplicación es un prototipo de apoyo a Recursos Humanos que combina análisis verificable en Python con recomendaciones basadas en reglas.")
    col1, col2, col3 = st.columns(3)
    col1.metric("Módulos", "3")
    col2.metric("Datos", "Sintéticos")
    col3.metric("Decisiones automáticas", "Ninguna")
    st.subheader("Qué puedes hacer")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**🎯 TalentMatch**")
        st.write("Compara competencias requeridas en una oferta con las competencias declaradas en perfiles ficticios.")
        st.markdown("**🎓 SkillPath**")
        st.write("Relaciona las brechas detectadas con cursos de ejemplo.")
    with c2:
        st.markdown("**📊 People Analytics**")
        st.write("Explora las competencias más frecuentes en los perfiles de demostración.")
        st.info("Empieza por TalentMatch y prueba la oferta de ejemplo o introduce una propia.")
    st.caption("Importante: la cobertura mide únicamente la presencia de competencias seleccionadas en los datos facilitados; no es una probabilidad de éxito ni una valoración global de una persona.")

elif page == "TalentMatch":
    st.title("🎯 TalentMatch")
    st.write("Compara los requisitos de un puesto con las competencias declaradas en perfiles de demostración.")
    job_text = st.text_area(
        "Descripción de la oferta",
        value="Buscamos un perfil de Recursos Humanos con experiencia en selección, Excel, Power BI y análisis de datos.",
        height=120,
    )
    st.markdown("**Paso 1. Revisa las competencias de la oferta**")
    st.caption("La aplicación intenta detectar competencias conocidas en el texto. Puedes corregir el resultado manualmente.")
    manual_mode = st.checkbox("Elegir las competencias manualmente", value=False)
    if manual_mode:
        manual_skills = st.multiselect(
            "Competencias que se utilizarán en la comparación",
            options=CANONICAL_SKILLS,
            default=[],
            help="Selecciona solo las competencias que quieres evaluar para este puesto.",
        )
        detected = manual_skills
    else:
        detected = parse_job_requirements(job_text, [])
        st.write("**Competencias detectadas automáticamente:**")
        if detected:
            st.write(", ".join(detected))
        else:
            st.warning("No se han detectado competencias del catálogo en el texto. Activa la selección manual o añade términos como Excel, Power BI, selección o análisis de datos.")
    st.caption("Los criterios detectados son una primera propuesta: revísalos antes de interpretar los resultados.")

    profiles_upload = st.file_uploader("Cargar perfiles en CSV (opcional)", type=["csv"], key="profiles_upload")
    profiles = load_csv_or_demo(profiles_upload, DATA_DIR / "profiles_demo.csv")
    if profiles is not None and ensure_columns(profiles, ["profile_id", "title", "skills", "evidence"], "perfiles"):
        if not detected:
            st.warning("Selecciona al menos una competencia para realizar la comparación.")
        else:
            results = compare_profiles(profiles.fillna(""), detected)
            st.subheader("Resultados de la comparación")
            m1, m2, m3 = st.columns(3)
            m1.metric("Perfiles analizados", len(results))
            m2.metric("Competencias requeridas", len(detected))
            m3.metric("Cobertura media", f"{results['Cobertura de competencias (%)'].mean():.1f}%")
            st.dataframe(
                results[["ID de perfil", "Perfil", "Cobertura de competencias (%)", "Coincidencias", "Brechas / no acreditadas"]],
                use_container_width=True,
                hide_index=True,
            )
            with st.expander("Consultar evidencias y competencias declaradas"):
                st.dataframe(results[["ID de perfil", "Competencias declaradas", "Evidencias"]], use_container_width=True, hide_index=True)
            st.download_button(
                "Descargar resultados CSV",
                data=results.to_csv(index=False).encode("utf-8-sig"),
                file_name="talentmatch_resultados.csv",
                mime="text/csv",
            )
            st.info("Interpretación responsable: una competencia no mencionada en los datos se muestra como 'no acreditada en la información disponible'; no significa que la persona no la posea. La cobertura no debe usarse como decisión automática de contratación.")
    else:
        st.caption("Formato esperado del CSV: profile_id, title, skills, evidence. Separa las competencias con punto y coma.")

elif page == "SkillPath":
    st.title("🎓 SkillPath")
    st.write("Relaciona competencias por desarrollar con acciones formativas del catálogo de ejemplo.")
    profiles = load_csv_or_demo(None, DATA_DIR / "profiles_demo.csv")
    courses = load_csv_or_demo(None, DATA_DIR / "courses_demo.csv")
    if profiles is not None and courses is not None:
        profile_labels = {
            f"{row['profile_id']} — {row['title']}": row["profile_id"]
            for _, row in profiles.iterrows()
        }
        selected_label = st.selectbox("Selecciona un perfil ficticio", list(profile_labels.keys()))
        selected_id = profile_labels[selected_label]
        selected_profile = profiles[profiles["profile_id"].astype(str) == str(selected_id)].iloc[0]
        current_skills = parse_skills(selected_profile["skills"])
        all_skills = sorted(set(CANONICAL_SKILLS + [s for s in current_skills]))
        gaps = st.multiselect(
            "Selecciona competencias que quieres desarrollar",
            options=all_skills,
            default=[s for s in ["Power BI", "Python"] if s not in current_skills],
        )
        if gaps:
            recs = build_training_recommendations(gaps, courses)
            st.subheader("Propuesta de desarrollo")
            st.dataframe(recs, use_container_width=True, hide_index=True)
            st.download_button(
                "Descargar itinerario CSV",
                data=recs.to_csv(index=False).encode("utf-8-sig"),
                file_name="skillpath_itinerario.csv",
                mime="text/csv",
            )
            st.caption("Las recomendaciones se basan en coincidencias con un catálogo de ejemplo; todavía no se utiliza un modelo generativo.")
        else:
            st.info("Selecciona al menos una competencia por desarrollar.")
    else:
        st.error("No se han encontrado los archivos de demostración en la carpeta data.")

elif page == "People Analytics":
    st.title("📊 People Analytics")
    st.write("Vista agregada de los perfiles ficticios incluidos en la demo.")
    profiles = load_csv_or_demo(None, DATA_DIR / "profiles_demo.csv")
    if profiles is not None and ensure_columns(profiles, ["profile_id", "title", "skills", "evidence"], "perfiles"):
        skill_counts = {}
        for _, row in profiles.iterrows():
            for skill in parse_skills(row["skills"]):
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
        counts = pd.DataFrame(
            [{"Competencia": skill, "Perfiles que la declaran": count} for skill, count in skill_counts.items()]
        ).sort_values("Perfiles que la declaran", ascending=False)
        c1, c2 = st.columns(2)
        c1.metric("Perfiles de demostración", len(profiles))
        c2.metric("Competencias distintas", len(counts))
        st.subheader("Frecuencia de competencias declaradas")
        st.bar_chart(counts.set_index("Competencia"))
        st.dataframe(counts, use_container_width=True, hide_index=True)
        st.caption("Los resultados describen exclusivamente los datos ficticios incluidos; no representan una plantilla real ni el mercado laboral.")
    else:
        st.error("No se han encontrado los datos de demostración.")

st.divider()
st.caption("TalentBridge AI · Prototipo educativo. Requiere revisión humana. No utilizar para tomar decisiones laborales reales.")
