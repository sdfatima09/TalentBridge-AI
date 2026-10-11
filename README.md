# TalentBridge AI

Prototipo educativo de IA aplicada a Recursos Humanos: selección por competencias, desarrollo del talento y People Analytics.

## Módulos
- **TalentMatch:** compara competencias requeridas en una oferta con competencias declaradas en perfiles ficticios.
- **SkillPath:** propone cursos de un catálogo de demostración para desarrollar competencias seleccionadas.
- **People Analytics:** muestra la frecuencia de competencias en los perfiles de ejemplo.

## Requisitos
- Python 3.10 o superior recomendado.

## Ejecutar en local
1. Descomprime el proyecto.
2. Abre una terminal dentro de la carpeta `TalentBridge_AI`.
3. Crea un entorno virtual (recomendado):
   - Windows: `python -m venv .venv`
   - Windows PowerShell: `.venv\\Scripts\\Activate.ps1`
   - macOS/Linux: `source .venv/bin/activate`
4. Instala dependencias: `pip install -r requirements.txt`
5. Ejecuta: `streamlit run app.py`
6. Abre la URL local que indique Streamlit en el terminal.

## CSV de perfiles
El CSV debe tener las columnas:
- `profile_id`: identificador ficticio.
- `title`: nombre del perfil.
- `skills`: competencias separadas por punto y coma.
- `evidence`: breve descripción de evidencias disponibles.

## CSV de cursos
El catálogo de ejemplo se encuentra en `data/courses_demo.csv` y contiene identificador, nombre, competencias asociadas, duración y objetivo.

## Publicación
Sube `app.py`, `requirements.txt`, la carpeta `data/` y este README a un repositorio de GitHub. En Streamlit Community Cloud selecciona el repositorio, la rama `main` y el archivo `app.py`.

## Uso responsable
Los datos incluidos son sintéticos. El porcentaje de cobertura solo refleja coincidencias con competencias seleccionadas y declaradas; no es una probabilidad de rendimiento. La ausencia de una competencia en el archivo no demuestra que la persona no la posea. No se deben tomar decisiones automáticas de contratación a partir de esta demo. Revisar los resultados con criterio humano y no cargar datos personales reales.
