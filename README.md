# eva_poo
## Gabriel Urra
# EcoTech Solutions - Sistema de Gestión Operativa y Financiera (ES3)
**Asignatura:** Programación Orientada a Objeto Seguro  
**Carrera:** Analista Programador  
**Estudiante:** Urra Gabriel  

---

## 1. Descripción del Proyecto
Esta extensión del sistema para **EcoTech Solutions** integra el consumo seguro de servicios externos (APIs) para optimizar dos áreas críticas:
1. **Planificación Operativa:** Obtención de datos meteorológicos en tiempo real (temperatura, viento) mediante la API pública de *Open-Meteo* para prevenir retrasos en proyectos de tecnologías sostenibles.
2. **Gestión de Pagos Internacionales:** Consulta de tasas de cambio e indicadores económicos internacionales para calcular pagos justos de trabajadores según la moneda base.

El script incorpora estrictos mecanismos de autenticación cifrada, validación y sanitización de entradas, manejo robusto de excepciones HTTP/red y persistencia local de datos en formato JSON.

---

## 2. Estructura del Proyecto
El proyecto se encuentra modularizado para garantizar mantenibilidad, separación de responsabilidades y seguridad:
- `main.py`: Script principal encargado de la orquestación del menú interactivo y el flujo de control de acceso.
- `auth.py`: Módulo de autenticación que gestiona credenciales mediante funciones de cifrado y hash seguro (SHA-256 + Salt).
- `api_service.py`: Módulo de integración HTTP con librerías oficiales (`requests`), validación de entradas mediante expresiones regulares y control de errores por códigos de estado y tiempos de espera.
- `database.py`: Módulo de persistencia encargado de registrar las operaciones y resultados en un archivo local `ecotech_operaciones_cache.json`.

---

## 3. Uso de Herramientas de IA y Análisis Crítico (Criterios 3.1.4)

### 3.1. Código Inicial Sugerido por la IA
En las etapas preliminares de desarrollo, las herramientas de inteligencia artificial proporcionaron un prototipo funcional básico que realizaba peticiones directas:
* Uso de bloques de conexión genéricos sin manejo de excepciones (`try-except` vacíos).
* Almacenamiento de credenciales en texto plano dentro del código fuente.
* Ausencia de validación y sanitización en los parámetros de entrada para las coordenadas y códigos de moneda.
* Exposición directa de trazas de error completas y técnicas ante fallos del servidor.

### 3.2. Identificación de Vulnerabilidades y Riesgos
Mediante un análisis técnico riguroso se detectaron las siguientes deficiencias críticas:
1. **Vulnerabilidad de autenticación:** Las credenciales en texto plano exponían al sistema a accesos no autorizados mediante lectura directa del código fuente.
2. **Falta de resiliencia operativa:** Una caída de la red o un tiempo de respuesta excedido (*Timeout*) provocaba la detención abrupta (*Crash*) del script.
3. **Falta de saneamiento de inputs:** Permitía la inyección de caracteres inválidos o cadenas vacías que corrompían las peticiones URL hacia las APIs externas.
4. **Fuga de información sensible:** Los mensajes de error originales mostraban detalles internos de infraestructura y excepciones puras de Python al usuario final.

### 3.3. Refactorización y Decisiones Técnicas Adoptadas
Para cumplir con los estándares de **Programación Segura**, se realizaron las siguientes refactorizaciones:
* **Cifrado de Credenciales:** Se implementó `hashlib` combinando contraseñas con un valor aleatorio único (*Salt*) en `auth.py`, mitigando ataques de diccionario e impidiendo el almacenamiento de contraseñas reales.
* **Manejo Jerárquico de Excepciones:** Se separaron las excepciones de `requests` (`Timeout`, `ConnectionError`) de los errores generales, vinculándolas a validaciones estrictas de códigos HTTP (`200`, `404`, `500`).
* **Sanitización de Entradas:** Se integraron funciones de validación utilizando expresiones regulares (`re`) para asegurar que las divisas cumplan con el formato ISO de 3 letras, y validación estricta de tipos flotantes para las coordenadas geográficas.
* **Continuidad y Mensajes Seguros:** Se diseñaron mensajes de salida controlados que informan la incidencia de forma amigable sin comprometer la seguridad ni revelar arquitectura interna del sistema.