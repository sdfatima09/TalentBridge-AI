# 🌉 TalentBridge AI

**Prototipo educativo de tecnología aplicada a Recursos Humanos, gestión del talento y People Analytics.**

TalentBridge AI explora cómo las herramientas digitales pueden ayudar a organizar la información sobre competencias profesionales, identificar necesidades de desarrollo y analizar competencias declaradas en perfiles de demostración.

El proyecto se ha desarrollado en el marco del Máster en People Analytics y Gestión del Talento Digital.

## 🎯 Objetivo del proyecto

Diseñar una herramienta de apoyo a profesionales de Recursos Humanos que conecte tres procesos:

- Comparación de competencias asociadas a un puesto.
- Identificación de oportunidades de formación y desarrollo.
- Análisis agregado de competencias.

## 🚀 Funcionalidades

### 1. TalentMatch — Comparación de competencias

- Introducción de una descripción de puesto.
- Detección inicial de competencias conocidas.
- Revisión y selección manual de los criterios.
- Comparación con perfiles ficticios.
- Visualización de coincidencias, brechas y evidencias declaradas.
- Descarga de resultados en CSV.

### 2. SkillPath — Desarrollo del talento

- Selección de un perfil ficticio.
- Identificación de competencias que se desean desarrollar.
- Relación de competencias con cursos de demostración.
- Consulta de duración y objetivos de aprendizaje.
- Descarga del itinerario formativo.

### 3. People Analytics — Análisis de competencias

- Cálculo de frecuencias de competencias declaradas.
- Visualización gráfica de resultados.
- Consulta de una tabla agregada de competencias.

## 🛠️ Tecnologías

- Python
- Streamlit
- pandas
- CSV para la gestión de los datos de demostración
- GitHub para el almacenamiento del código y la documentación

## 📂 Estructura del proyecto

- `app.py`: aplicación principal.
- `requirements.txt`: dependencias necesarias.
- `data/`: archivos CSV de demostración.
- `Analisis_funcional_y_prompt_TalentBridge_AI.docx`: documentación del análisis funcional y del diseño del prototipo.
- `README.md`: documentación e instrucciones de uso.

## 💻 Instalación y ejecución local

Se recomienda Python 3.10 o superior.

1. Clona el repositorio:

   `git clone https://github.com/sdfatima09/TalentBridge-AI.git`

2. Accede a la carpeta del proyecto:

   `cd TalentBridge-AI`

3. Crea un entorno virtual:

   `python -m venv .venv`

4. Activa el entorno virtual.

   En Windows PowerShell:

   `.venv\Scripts\Activate.ps1`

   En macOS/Linux:

   `source .venv/bin/activate`

5. Instala las dependencias:

   `pip install -r requirements.txt`

6. Ejecuta la aplicación:

   `streamlit run app.py`

7. Abre en el navegador la dirección local indicada por Streamlit.

## 📸 Capturas de pantalla

Se incorporarán capturas de los módulos Inicio, TalentMatch, SkillPath y People Analytics para mostrar el funcionamiento y la interfaz de la aplicación.

## ⚖️ Limitaciones y uso responsable

TalentBridge AI es un prototipo educativo y no un sistema validado para su uso en procesos reales de selección.

- Los datos incluidos son sintéticos.
- La comparación se basa en reglas explícitas y competencias declaradas.
- El porcentaje de cobertura refleja coincidencias con los criterios seleccionados; no mide el rendimiento potencial ni la idoneidad global de una persona.
- La ausencia de una competencia en los datos no implica que la persona carezca de ella.
- Los resultados deben interpretarse con criterio humano.
- No deben cargarse datos personales reales ni utilizarse los resultados para automatizar decisiones de contratación.

## 📌 Estado del proyecto

Proyecto académico en evolución. La disponibilidad de una demo online y las pruebas de funcionamiento deberán indicarse una vez verificadas.

## 👩‍💻 Autora

Fátima Sánchez Dorado

Máster en People Analytics y Gestión del Talento Digital

Áreas de interés: People Analytics, HR Tech, Talent Management y desarrollo del talento.
