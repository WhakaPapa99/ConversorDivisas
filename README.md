# 💶 Conversor de Divisas (BCE) - Integración de Datos XML y GUI

Aplicación interactiva desarrollada en **Python** con **Streamlit** que consume en tiempo real los tipos de cambio oficiales de referencia publicados diariamente por el **Banco Central Europeo (BCE)** en formato XML.

Proyecto perteneciente al **Módulo Profesional 486: Acceso a Datos**, orientado a la integración de APIs/servicios web, procesamiento de estructuras XML y construcción de interfaces gráficas.

---

## 📋 Características Principales

- **Conexión en Tiempo Real**: Descarga automática del feed XML público del BCE con gestión de tiempos de espera (*timeout*) y control de errores HTTP.
- **Parsing XML Robusto**: Procesamiento del árbol XML mediante `xml.etree.ElementTree` de la librería estándar, resolviendo el espacio de nombres (*namespace*) oficial.
- **Inyección de Moneda Base**: Incorporación de `EUR = 1.0` para permitir cálculos bidireccionales con el Euro.
- **Conversión Cruzada**: Soporte para convertir entre cualquier par de divisas (por ejemplo, USD a JPY) utilizando el Euro como moneda puente.
- **Validación de Entradas**: Detección de entradas no numéricas, vacías o valores negativos, con soporte para coma decimal europea (`100,50`) y punto decimal (`100.50`).
- **Caché Eficiente**: Uso de `@st.cache_data(ttl=3600)` para optimizar el rendimiento y evitar peticiones excesivas al servidor del BCE.
- **Inspección de Datos**: Desplegable interactivo para examinar el XML en crudo recibido del servidor (*Raw Data*).
- **Tabla de Referencia**: Visualización interactiva de todas las divisas y sus tasas respecto al Euro.

---

## 📂 Arquitectura del Proyecto

El proyecto sigue una arquitectura modular en dos capas bien diferenciadas:

```text
ConversorDivisas/
│
├── .venv/                   # Entorno virtual de Python
├── conversor_bce.py         # Capa de Acceso a Datos y Lógica de Negocio
├── main.py                  # Capa de Presentación (Interfaz Gráfica con Streamlit)
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Documentación del proyecto
```

### Descripción de Módulos

1. **`conversor_bce.py`**:
   - `descargar_xml(url)`: Descarga el archivo XML mediante una petición HTTP `GET` con `requests`.
   - `parsear_xml(xml_bytes)`: Procesa el XML con `ElementTree`, extrae la fecha de publicación (`time`), lee los atributos `currency` y `rate` de cada nodo `<Cube>`, y añade la clave base `"EUR": 1.0`.
   - `convertir_divisa(importe_texto, origen, destino, tasas)`: Normaliza el texto de entrada, valida que sea un número válido no negativo y aplica la fórmula de conversión cruzada.

2. **`main.py`**:
   - Construye la interfaz web con Streamlit.
   - Gestiona la carga con caché de 1 hora.
   - Despliega el visor de XML crudo, la fecha oficial, el formulario de conversión en 3 columnas y la tabla de tipos de cambio.

---

## ⚙️ Instalación y Requisitos

### Requisitos Previos
- Python 3.10 o superior (el proyecto utiliza el entorno virtual `.venv`).

### 1. Activar el Entorno Virtual (Windows)

En PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

O en el símbolo del sistema (CMD):
```cmd
.\.venv\Scripts\activate.bat
```

### 2. Instalar Dependencias

Si necesitas reinstalar o desplegar en otro equipo:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## 🚀 Ejecución de la Aplicación

Para iniciar el servidor local de Streamlit, ejecuta el siguiente comando desde la raíz del proyecto:

```powershell
.\.venv\Scripts\streamlit.exe run main.py
```

Streamlit iniciará el servidor y abrirá automáticamente tu navegador predeterminado en:
```text
http://localhost:8501
```

---

## 🧠 Lógica Técnica para la Defensa Oral (10 Minutos)

Esta sección resume los conceptos clave evaluados en la rúbrica del proyecto:

### 1. Manejo de APIs y Conexión HTTP (2 Puntos)
- Se utiliza la librería `requests` ejecutando `requests.get(url, timeout=10)`.
- Se establece un `timeout` para evitar que la aplicación quede bloqueada indefinidamente si el servidor o la red no responden.
- Se verifica que el código de respuesta HTTP sea `200` y se capturan excepciones de tipo `RequestException` para informar de posibles fallos de conexión de forma amigable.

### 2. Procesamiento de XML y Namespaces (2 Puntos)
- El XML del BCE define un espacio de nombres por defecto (*XML Namespace*):
  ```xml
  xmlns="http://www.ecb.int/vocabulary/2002-08-01/eurofxref"
  ```
- En `xml.etree.ElementTree`, buscar una etiqueta sin prefijo falla si hay namespace. Por ello, se define:
  ```python
  ns = {"ecb": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"}
  nodo_tiempo = raiz.find(".//ecb:Cube[@time]", ns)
  ```
- De este modo se localiza de forma precisa la fecha oficial (`time`) y cada elemento `<Cube currency="..." rate="..."/>`.

### 3. Comprensión Matemática y Euro Base (2 Puntos)
- **Moneda Base**: El XML del BCE no incluye una línea para el Euro porque todas las cotizaciones son relativas a él ($1\text{ EUR} = X\text{ Divisa}$). Por tanto, se añade manualmente `tasas["EUR"] = 1.0`.
- **Conversión Cruzada**: Para convertir entre dos monedas cualesquiera (p. ej., de Dólares `USD` a Yenes `JPY`), se usa el Euro como intermediario:
  $$\text{CantidadFinal} = \left(\frac{\text{Importe}}{\text{TasaOrigen}}\right) \times \text{TasaDestino}$$
  1. $\frac{\text{Importe}}{\text{TasaOrigen}}$ convierte el importe de origen a Euros.
  2. Multiplicar por $\text{TasaDestino}$ convierte los Euros resultantes a la moneda de destino.

### 4. Interfaz Gráfica y Validación de Entradas (2 Puntos)
- Se utiliza un `st.text_input` en lugar de un `number_input` con el fin deliberado de evaluar la validación de errores en vivo frente a entradas vacías o alfanuméricas (ej. `"cien"` o `"100abc"`).
- Se gestiona la excepción con `try ... except ValueError` mostrando un componente visual `st.error(...)` sin romper el flujo de la aplicación.
- `@st.cache_data(ttl=3600)` guarda en memoria el resultado de la descarga y el parseo durante una hora, logrando recargas instantáneas de la interfaz.

---

## 🛠️ Tecnologías Empleadas

- **Lenguaje**: Python 3.13
- **Librerías Estándar**: `xml.etree.ElementTree`
- **Peticiones HTTP**: `requests`
- **Framework Web**: `streamlit`
