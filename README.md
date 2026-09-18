# Altamira Bot

Automatización para la carga de pedidos en el catálogo web de Altamira Group.

Altamira Bot permite tomar pedidos almacenados en archivos Excel (`.xls` y `.xlsx`), extraer automáticamente los códigos de artículos y sus cantidades, revisarlos antes de comenzar y cargarlos en el carrito mediante automatización del navegador.

> Proyecto desarrollado para automatizar una tarea repetitiva de carga manual de pedidos.

---

## Características

- Lectura de archivos `.xls` y `.xlsx`.
- Detección automática de las columnas `Código` y `Cantidad`.
- Soporte para archivos con diferentes estructuras y columnas adicionales.
- Normalización de códigos con prefijo `ALT-`.
- Validación y normalización de cantidades.
- Vista previa del pedido antes de comenzar la carga.
- Confirmación manual antes de modificar el carrito.
- Login realizado manualmente por el usuario.
- Automatización del catálogo mediante Playwright.
- Búsqueda de artículos por código.
- Agregado de artículos al carrito.
- Actualización automática de cantidades.
- Detección de artículos que ya se encuentran en el carrito.
- Continuación del procesamiento ante errores individuales.
- Resumen final de artículos procesados y errores.
- Interfaz gráfica de escritorio desarrollada con PySide6.
- Ejecutable independiente para Windows.

---

## Tecnologías

Python
PySide6
Playwright
openpyxl
xlrd
Git / GitHub
PyInstaller

---

## Formatos Excel

La herramienta soporta archivos:

.xls
.xlsx

No requiere que todos los pedidos tengan exactamente la misma estructura.

El lector busca automáticamente las columnas: Código - Cantidad
y utiliza esas columnas para construir el pedido.
Las demás columnas son ignoradas.
También se normalizan códigos que utilizan el prefijo: ALT-
Por ejemplo: ALT-2511/02
se procesa como: 2511/02

---

## Instalación

1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd altamira-bot
2. Crear el entorno virtual
python -m venv .venv
.venv\Scripts\Activate.ps1
3. Instalar las dependencias
pip install -r requirements.txt
4. Instalar Firefox para Playwright
playwright install firefox

---

## Ejecutable para Windows

El proyecto puede empaquetarse como un ejecutable independiente mediante PyInstaller.
Para generar el ejecutable incluyendo el navegador de Playwright:
env:PLAYWRIGHT_BROWSERS_PATH="0"
python -m playwright install firefox
Luego:
pyinstaller --clean --noconfirm --windowed --onefile --name AltamiraBot src/main.py
El ejecutable se genera en: dist/ AltamiraBot.exe
El ejecutable incluye los componentes necesarios de Playwright y su navegador Firefox, por lo que no requiere una instalación independiente de Python para ejecutarse.

---

## Estado del proyecto

MVP funcional / v1.0

La aplicación fue probada con múltiples pedidos reales utilizando diferentes estructuras y formatos de archivos Excel.

El flujo completo fue validado tanto durante el desarrollo como mediante el ejecutable empaquetado para Windows.

La versión actual prioriza:

- Automatización confiable.
- Manejo de errores individuales.
- Interacción manual en puntos sensibles.
- Separación de responsabilidades.
- Facilidad de uso.
- Distribución mediante un ejecutable independiente.
- Posibles mejoras futuras

---

## Consideraciones

Esta herramienta está diseñada para utilizarse con una cuenta autorizada y mediante las funcionalidades normales disponibles en el catálogo.

No intenta:

- Evadir CAPTCHA o mecanismos de seguridad.
- Obtener acceso a áreas no autorizadas.
- Acceder directamente a bases de datos internas.
- Almacenar credenciales.
- Modificar información fuera del flujo normal del catálogo.
- El usuario debe revisar manualmente el carrito antes de finalizar la compra.
- Los archivos de pedidos y resultados se mantienen fuera del control de versiones para evitar almacenar información comercial en el repositorio.

---

## Funcionalidades que podrían incorporarse en futuras versiones:

- Generación automática de reportes.
- Clasificación más detallada de errores.
- Detección y consolidación de códigos duplicados.
- Reutilización de sesiones.
- Opciones de configuración desde la interfaz.
- Sistema de logs.
- Tests automatizados.
- Procesamiento de pedidos a partir de fotografías mediante OCR.

Estas funcionalidades quedan fuera del alcance de la versión actual.

## Autor

Lautaro Ezequiel Rodriguez

Proyecto personal de automatización y desarrollo de software.