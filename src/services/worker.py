from PySide6.QtCore import QObject, Signal, Slot
from playwright.sync_api import sync_playwright

from services.processor import procesar_articulo


URL_CATALOGO = (
    "https://webapp.altamiragroup.com.ar/catalogo"
)


class OrderProcessorWorker(QObject):

    progreso = Signal(int, int)
    articulo_iniciado = Signal(str, int)
    articulo_finalizado = Signal(dict)

    login_requerido = Signal()
    terminado = Signal(list)
    error = Signal(str)

    def __init__(self, pedido):
        super().__init__()

        self.pedido = pedido
        self.playwright = None
        self.browser = None
        self.page = None

    @Slot()
    def ejecutar(self):
        resultados = []

        try:
            # Iniciamos Playwright sin context manager para
            # mantener el navegador abierto al finalizar.
            self.playwright = sync_playwright().start()

            self.browser = self.playwright.firefox.launch(
                headless=False
            )

            self.page = self.browser.new_page()

            self.page.goto(URL_CATALOGO)

            # Avisamos a la UI que Firefox está listo
            # y que el usuario debe iniciar sesión.
            self.login_requerido.emit()

            # Por ahora usamos una espera bloqueante
            # temporal para mantener el login manual.
            input(
                "Hacé el login manualmente "
                "y presioná ENTER cuando termines..."
            )

            total = len(self.pedido)

            for numero, articulo in enumerate(
                self.pedido,
                start=1
            ):
                codigo = articulo["codigo"]
                cantidad = articulo["cantidad"]

                self.articulo_iniciado.emit(
                    codigo,
                    numero
                )

                resultado = procesar_articulo(
                    self.page,
                    codigo,
                    cantidad
                )

                resultados.append(resultado)

                self.articulo_finalizado.emit(
                    resultado
                )

                self.progreso.emit(
                    numero,
                    total
                )

            self.terminado.emit(
                resultados
            )

            # IMPORTANTE:
            # No cerramos browser ni Playwright.
            # El usuario debe poder revisar y enviar
            # manualmente el pedido en Firefox.

        except Exception as exc:
            self.error.emit(
                str(exc)
            )