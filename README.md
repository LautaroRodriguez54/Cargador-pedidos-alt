# Altamira Bot

Automatización para la carga de pedidos en el catálogo web de Altamira Group.

La herramienta permite tomar pedidos almacenados en archivos Excel (`.xls` y `.xlsx`), extraer automáticamente los códigos de artículos y sus cantidades, y cargarlos en el carrito mediante automatización del navegador.

> Proyecto desarrollado para automatizar una tarea repetitiva de carga manual de pedidos.

---

## Características actuales

- Lectura de archivos `.xls` y `.xlsx`.
- Detección automática de las columnas `Código` y `Cantidad`.
- Ignora columnas adicionales del pedido.
- Normalización de códigos con prefijo `ALT-`.
- Validación básica de códigos y cantidades.
- Preview del pedido antes de comenzar la carga.
- Confirmación manual antes de modificar el carrito.
- Login realizado manualmente por el usuario.
- Automatización del catálogo mediante Playwright.
- Búsqueda de artículos por código.
- Agregado de artículos al carrito.
- Actualización automática de cantidades.
- Detección de artículos que ya se encuentran en el carrito.
- Continuación del procesamiento ante errores individuales.
- Resumen final de artículos procesados y errores.

---

## Tecnologías

- **Python**
- **Playwright**
- **openpyxl**
- **xlrd**
- **Git / GitHub**


---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd altamira-bot
```

### 2. Crear el entorno virtual

```bash
python -m venv .venv
```

Activar el entorno en Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Instalar Firefox para Playwright

```bash
playwright install firefox
```

---

## Uso

Con el entorno virtual activado:

```bash
python src/main.py
```

La aplicación solicita la ruta del archivo Excel:

```text
Ruta del archivo Excel:
```

Por ejemplo:

```text
pedidos\PEDIDO ALTAMIRA PARA TEKOHA CHACO SRL 04092026.xls
```

Luego muestra un preview del pedido:

```text
============================================================
PEDIDO DETECTADO
============================================================
Archivo: pedidos\PEDIDO ALTAMIRA PARA TEKOHA CHACO SRL 04092026.xls
Artículos: 228

Primeros artículos:
2511/02        x 4
5051/02        x 1
5050/56        x 1
2288/98        x 1
10350/02       x 15

... y 223 artículos más.

============================================================

¿Cargar este pedido? [S/N]:
```

El procesamiento solamente comienza cuando el usuario confirma con `S`.

---

## Autenticación

El usuario realiza el login manualmente en el navegador.

Las credenciales no se almacenan en el código ni en archivos del proyecto.

La herramienta utiliza la sesión autenticada del navegador para realizar las operaciones necesarias en el catálogo.

---

## Manejo de errores

Cada artículo se procesa individualmente.

Si un artículo no puede ser encontrado o se produce un error durante su procesamiento, el programa registra el fallo y continúa con el siguiente artículo.

Al finalizar se muestra un resumen:

```text
============================================================
RESUMEN DEL PROCESAMIENTO
============================================================
Total:       84
Procesados:  82
Errores:      2

ERRORES:
------------------------------------------------------------
- XXXXX/XX x 1 → artículo no encontrado
- YYYYY/YY x 2 → error durante la actualización
============================================================
```

La validación final del carrito queda a cargo del usuario.

---

## Consideraciones

Esta herramienta está diseñada para utilizarse con una cuenta autorizada y mediante las funcionalidades normales disponibles en el catálogo.

No intenta:

- Evadir CAPTCHA o mecanismos de seguridad.
- Obtener acceso a áreas no autorizadas.
- Acceder directamente a bases de datos internas.
- Almacenar credenciales.
- Modificar información fuera del flujo normal del catálogo.

El usuario debe revisar manualmente el carrito antes de finalizar la compra.

---

## Estado del proyecto

**MVP funcional.**

La herramienta ha sido probada con múltiples pedidos reales utilizando diferentes formatos de archivos Excel.

La arquitectura actual separa:

- Lectura y normalización de pedidos.
- Lógica de procesamiento.
- Automatización del navegador.

El proyecto continuará evolucionando hacia una aplicación de escritorio más completa y fácil de utilizar.

---

## Autor

**Lautaro Rodriguez**

Proyecto personal de automatización y desarrollo de software.
